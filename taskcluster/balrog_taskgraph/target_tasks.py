# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from taskgraph.target_tasks import _target_task, get_method
from taskgraph.util.attributes import match_run_on_git_branches as match_run_on_git_tags

_GIT_REFS_TAGS_PREFIX = "refs/tags/"


def filter_for_github_release_name(task, parameters):
    if parameters["tasks_for"] != "github-release":
        return True
    run_on_release_tags = set(task.attributes.get("run_on_release_tags", ["all"]))
    head_tag = parameters["head_tag"]
    if head_tag.startswith(_GIT_REFS_TAGS_PREFIX):
        head_tag = head_tag[len(_GIT_REFS_TAGS_PREFIX) :]
    return match_run_on_git_tags(head_tag, run_on_release_tags)


@_target_task("release")
def target_tasks_release(full_task_graph, parameters, graph_config):
    default_tasks = frozenset(get_method("default")(full_task_graph, parameters, graph_config))

    return [label for label, t in full_task_graph.tasks.items() if label in default_tasks and filter_for_github_release_name(t, parameters)]
