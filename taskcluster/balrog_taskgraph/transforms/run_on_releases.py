# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Support run-on-releases option
"""


from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def run_on_git_tags(config, jobs):
    """Set the run_on_releases attribute"""
    for job in jobs:
        if job.get("run-on-releases") is not None:
            job.setdefault("attributes", {})["run_on_releases"] = job.pop("run-on-releases")

        yield job
