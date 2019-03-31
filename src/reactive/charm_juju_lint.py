"""
# charm_juju_lint.py

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
from os import (
    getenv,
    mkdir,
    path,
)
import virtualenv

from charmhelpers.core import hookenv
from charmhelpers.core.host import rsync
from charmhelpers.fetch.python import packages
from charms.reactive import (
    when,
    when_not,
    set_flag,
)

USR_LIB = "/usr/lib/juju-lint"
VAR_LIB = "/var/lib/juju-lint"


@when_not("charm-juju-lint.installed")
def install_charm_juju_lint():
    create_install_dirs()
    virtualenv.create_environment(USR_LIB)
    packages.pip_install("juju", venv=USR_LIB)
    deploy_scripts()
    hookenv.status_set("active", "Unit is ready")
    set_flag("charm-juju-lint.installed")


def create_install_dirs():
    install_dirs = (USR_LIB, VAR_LIB)
    for install_dir in install_dirs:
        if not path.isdir(install_dir):
            try:
                mkdir(install_dir)
            except OSError as error:
                print("{} directory creation failed: {}".format(
                    install_dir, error
                ))


def deploy_scripts():
    rsync(
        path.join(getenv("CHARM_DIR"), "scripts", "auto_lint.py"),
        path.join(USR_LIB, "auto_lint.py")
    )


@when("charm-juju-lint.installed", "config.changed")
def verify_config():
    config = hookenv.config()
    required = ("controller-endpoint", "controller-username",
                "controller-password", "controller-cacert", "model-uuid")
    for option in required:
        if not config[option]:
            hookenv.status_set("active", "Set model connection config values")
            return
    hookenv.status_set("active", "Unit is ready")


@when("charm-juju-lint.installed", "config.changed")
def create_auto_lint_config():
    """Create JSON configuration file at
    "/var/lib/juju-lint/auto-lint-config.json" containing charm config options.
    """
    with open(path.join(VAR_LIB, "auto-lint-config.json"), "w") as fp:
        json.dump(hookenv.config(), fp)


def create_crontab():
    """Create a crontab at "/etc/cron.d/juju-lint" that runs auto_lint.py and
    directs output to "/var/lib/juju-lint/lint-results.txt".
    """
    pass
