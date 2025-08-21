# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from taskgraph.target_tasks import get_method, register_target_task
from taskgraph.util.attributes import match_run_on_git_branches as match_run_on_git_tags

_GIT_REFS_TAGS_PREFIX = "refs/tags/"


def sanity_check_release(parameters):
    if parameters["tasks_for"] != "github-release":
        return
    tag = parameters["head_tag"]
    if tag.startswith(_GIT_REFS_TAGS_PREFIX):
        tag = tag[len(_GIT_REFS_TAGS_PREFIX) :]
    if not tag.startswith("v"):
        return
    in_tree_version = parameters["version"]
    tag_version = tag[1:]
    if in_tree_version != tag_version:
        raise Exception(f"Version numbers in pyproject.toml ({in_tree_version}) and release tag ({tag_version}) don't match")


def filter_for_github_release_name(task, parameters):
    if parameters["tasks_for"] != "github-release":
        return True
    run_on_releases = set(task.attributes.get("run_on_releases", ["all"]))
    head_tag = parameters["head_tag"]
    if head_tag.startswith(_GIT_REFS_TAGS_PREFIX):
        head_tag = head_tag[len(_GIT_REFS_TAGS_PREFIX) :]
    return match_run_on_git_tags(head_tag, run_on_releases)


@register_target_task("balrog")
def target_tasks_balrog(full_task_graph, parameters, graph_config):
    sanity_check_release(parameters)

    default_tasks = frozenset(get_method("default")(full_task_graph, parameters, graph_config))

    return [label for label, t in full_task_graph.tasks.items() if label in default_tasks and filter_for_github_release_name(t, parameters)]
