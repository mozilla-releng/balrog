# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Tox-specific transforms
"""

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def update_env(config, jobs):
    for job in jobs:
        pr_number = config.params.get("pull_request_number", "")
        env = job.pop("env", {})
        env["CI_PULL_REQUEST"] = str(pr_number)
        job["worker"].setdefault("env", {}).update(env)
        yield job
