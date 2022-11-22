# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Set environment variables for the skopeo push-image command
"""


import os

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def set_push_environment(config, jobs):
    """Set the environment variables for the push to docker hub task."""
    for job in jobs:
        version_file = os.path.join(config.graph_config.vcs_root, "version.txt")
        version = open(version_file).read().strip()

        env = job["worker"].setdefault("env", {})
        env.update(
            {
                "VCS_HEAD_REPOSITORY": config.params["head_repository"],
                "VCS_HEAD_REV": config.params["head_rev"],
                # TODO: Figure out if we still need to add the version
                "APP_VERSION": version,
            }
        )
        yield job
