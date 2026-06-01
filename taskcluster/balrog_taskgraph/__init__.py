# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import tomllib
from importlib import import_module
from typing import Annotated, Optional

from msgspec import Meta
from taskgraph.parameters import extend_parameters_schema
from taskgraph.util.schema import Schema

GreaterThanZero = Annotated[int, Meta(gt=1)]

balrog_schema = Schema.from_dict({"pull_request_number": Optional[GreaterThanZero]}, kw_only=True)


extend_parameters_schema(balrog_schema)


def register(graph_config):
    """
    Import all modules that are siblings of this one, triggering decorators in
    the process.
    """
    _import_modules(
        [
            "transforms",
            "target_tasks",
        ]
    )


def _import_modules(modules):
    for module in modules:
        import_module(f".{module}", package=__name__)


def get_decision_parameters(graph_config, parameters):
    # Read version from pyproject.toml
    version_file = os.path.join(graph_config.vcs_root, "pyproject.toml")
    with open(version_file, "rb") as fd:
        data = tomllib.load(fd)
        version = data["project"]["version"]
    parameters["version"] = version

    # Environment is defined in .taskcluster.yml
    pr_number = os.environ.get("BALROG_PULL_REQUEST_NUMBER", None)
    if not pr_number:
        return
    parameters["pull_request_number"] = int(pr_number)
