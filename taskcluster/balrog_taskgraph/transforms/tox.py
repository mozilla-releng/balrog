# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Tox-specific transforms
"""

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


COVERALLS_SCOPE = "secrets:get:repo:github.com/mozilla-releng/balrog:coveralls"


@transforms.add
def update_env(config, tasks):
    for task in tasks:
        pr_number = config.params.get("pull_request_number", "")
        env = task["worker"].setdefault("env", {})
        env["CI_PULL_REQUEST"] = str(pr_number)
        yield task


@transforms.add
def add_coveralls(config, tasks):
    """Layer coveralls reporting onto tasks marked with `coveralls: true`, but
    only when the secret is available. Untrusted pull requests aren't granted
    the coveralls scope, so leave those tasks untouched."""
    for task in tasks:
        enabled = task.pop("coveralls", False)
        if enabled and config.params["tasks_for"] != "github-pull-request-untrusted":
            task["run"]["command"] = "taskcluster/scripts/get-coveralls-token " + task["run"]["command"]

            env = task["worker"].setdefault("env", {})
            toxenvs = env["TOXENV"].split(",") if env.get("TOXENV") else []
            if "coveralls" not in toxenvs:
                toxenvs.append("coveralls")
            env["TOXENV"] = ",".join(toxenvs)

            task.setdefault("scopes", []).append(COVERALLS_SCOPE)
        yield task
