#!/usr/lib/juju-lint/bin/python3

"""
# auto_lint.py

Automatically grab `juju status` output and analyse it with Juju Lint.

Copyright (C) 2019 Canonical Ltd.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License version 3, as published by the Free
Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
from os import path
from subprocess import (
    CalledProcessError,
    check_output,
)

from juju import loop
from juju.model import Model

VAR_LIB = "/var/lib/juju-lint"


async def get_juju_status(auto_lint_config):
    model = Model()
    await model.connect(
        endpoint=auto_lint_config["controller-endpoint"],
        username=auto_lint_config["controller-username"],
        password=auto_lint_config["controller-password"],
        cacert=auto_lint_config["controller-cacert"],
        uuid=auto_lint_config["model-uuid"],
    )
    juju_status = await model.get_status()
    await model.disconnect()
    return juju_status


def lint_juju(auto_lint_config):
    command = [
        "juju-lint",
        "--config", auto_lint_config["lint-config"],
        "--override-subordinate", auto_lint_config["lint-override"],
        "--loglevel", auto_lint_config["lint-loglevel"],
        "--logfile", auto_lint_config["lint-logfile"],
        path.join(VAR_LIB, "juju-status.json")
    ]
    try:
        lint_results = check_output(command)
    except CalledProcessError as error:
        print("juju-lint failed with the following error:", error)
    else:
        with open(path.join(VAR_LIB, "lint-results.txt"), "w") as fp:
            fp.write(lint_results)


def main():
    with open(path.join(VAR_LIB, "auto-lint-config.json")) as fp:
        auto_lint_config = json.load(fp)
    juju_status = loop.run(get_juju_status(auto_lint_config))
    with open(path.join(VAR_LIB, "juju-status.json"), "w") as fp:
        fp.write(juju_status.to_json())
    lint_juju(auto_lint_config)


if __name__ == "__main__":
    main()
