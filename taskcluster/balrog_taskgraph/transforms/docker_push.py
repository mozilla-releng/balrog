# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Set environment variables for the skopeo push-image command
"""


import os
import tomllib

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def set_push_environment(config, jobs):
    """Set the environment variables for the push to docker hub task."""
    for job in jobs:
        version_file = os.path.join(config.graph_config.vcs_root, "pyproject.toml")
        with open(version_file, "rb") as fd:
            data = tomllib.load(fd)
            version = data["project"]["version"]

        env = job["worker"].setdefault("env", {})
        env.update(
            {
                "VCS_HEAD_REPOSITORY": config.params["head_repository"],
                "VCS_HEAD_REV": config.params["head_rev"],
                "APP_VERSION": version,
            }
        )
        yield job
