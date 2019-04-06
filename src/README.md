## Overview

Juju Lint - a Juju model linter with configurable policy.

This charm deploys Juju Lint, along with a script to automate its execution,
auto_lint.py.  In addition, a crontab is deployed to run auto_lint.py, as well
as a Nagios check which analyses Juju Lint output and alerts on errors.


### TODO

This charm is currently pre-release; the following items remain to be completed:

* Nagios check.
* Juju controller user credentials must be entered into this Charm's config in
  order to use libjuju.  Currently, it's possible to enter the credentials for a
  user with superuser privileges, which is a security risk.  Should this charm
  enforce the entry of credentials for a read only user, or should that be left
  up to the admin's discretion?  If the answer is the former, implement this.
* Tests.


## Usage

Deploy this charm with:
```sh
juju deploy charm-juju-lint juju-lint
```

The following model connection config values **must** be set to allow libjuju to
retrieve Juju status output:

* controller-endpoint - A controller API endpoint (syntax:
  "\<hostname\>:\<port\>")
* controller-username - A controller user's username
* controller-password - The respective controller user's password
* controller-cacert - The controller CA certificate
* model-uuid - The model UUID

When setting controller-cacert, the following command sytax is recommended:
```sh
juju config juju-lint controller-cacert='
-----BEGIN CERTIFICATE-----
<certificate body>
-----END CERTIFICATE-----
'
```

The following Juju Lint options are available:

* lint-config - Juju Lint rules file path
* lint-override - Hash separated subordinate rule overrides (syntax:
  "\<name\>:\<location\>#\<name\>:\<location\>")
* lint-loglevel - Logging level, either "CRITICAL", "ERROR", "WARNING", "INFO",
  "DEBUG", or "NOTSET"
* lint-logfile - Log file path
* lint-frequency - Specifies how often Juju Lint is run, in minutes


## Juju Lint (upstream)

* Website: https://launchpad.net/juju-lint
* Bug tracker: https://bugs.launchpad.net/juju-lint
* Maintainers: https://launchpad.net/~juju-linters
