#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Mountain Tapir Collage Maker is a tool for combining images into collages.
# Copyright (c) 2016, tttppp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
test_mountain_tapir
----------------------------------

Tests for `mountain_tapir` module.
"""

import unittest
import mock

from mountain_tapir import mountain_tapir

class TestMountain_tapir(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    @mock.patch('mountain_tapir.mountain_tapir.Tk')
    @mock.patch('mountain_tapir.mountain_tapir.Frame')
    @mock.patch('mountain_tapir.mountain_tapir.BOTH')
    @mock.patch('mountain_tapir.mountain_tapir.YES')
    def test_000_something(self, mockTk, mockFrame, mockBOTH, mockYES):
        pass

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
