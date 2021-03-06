#!/bin/env/python

# Taken from:
# http://stackoverflow.com/questions/32757765/conditional-commands-in-tox-tox-travis-ci-and-coveralls

import os
import sys
import platform

from subprocess import call

if __name__ == '__main__':
    if 'TRAVIS' in os.environ \
       and platform.python_implementation() != 'PyPy':
        rc = call('coveralls')
        raise SystemExit(rc)
