==================
Zonza API Examples
==================

This repository contains scripts that utilise the ZONZA public API and can be
used to automate common tasks or interact with third-party systems.

Usage
=====
Set your API credentials into environment variables `BORK_USERNAME` and
`BORK_TOKEN` then run any of the included scripts. It is recommended that you
create a file called `env_vars` settings these variables and as such, this file
is excluded from being committed into Git. You can then simply `source
env_vars` before running any of the scripts.

    #!/bin/bash
    export BORK_TOKEN='<YOUR_TOKEN>'
    export BORK_USERNAME='<YOUR_USERNAME>'

WARNING:
========
Do not run these scripts without looking at them first. They are primarily for
learning purposes and should be modified for particular use cases.
