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
test_model
----------------------------------

Tests for `model` module.
"""

import unittest
from mock import Mock

from mountain_tapir import model

class TestModel(unittest.TestCase):
    def testCurrentDirectorySet(self):
        """Test that the config object is used to set the current directory."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.return_value='currentDirectory'
        
        m = model.Model(mockConfig)
        
        mockConfig.get.assert_called_with('FILE', 'initialdirectory', '/')
        assert m.currentDirectory == 'currentDirectory'

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
