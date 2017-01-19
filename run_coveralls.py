#!/bin/env/python

# Taken from:
# http://stackoverflow.com/questions/32757765/conditional-commands-in-tox-tox-travis-ci-and-coveralls

import os, sys

from subprocess import call

if __name__ == '__main__':
    if 'TRAVIS' in os.environ and sys.version_info[:2] != (2, 6):
        rc = call('coveralls')
        raise SystemExit(rc)
