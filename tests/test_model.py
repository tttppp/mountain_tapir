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
from mock import Mock, patch

from mountain_tapir import model
from mountain_tapir.algorithm import Algorithm

class TestModel(unittest.TestCase):
    @patch('mountain_tapir.model.os')
    def testInitModel(self, mockOs):
        """Test that the config object is used to set certain values."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.side_effect = [8, 100, 200, Algorithm.GRID, 'currentDirectory']
        
        m = model.Model(mockConfig)
        
        mockConfig.get.assert_any_call('COLLAGE', 'regionCount', 6, 'int')
        mockConfig.get.assert_any_call('COLLAGE', 'width', 600, 'int')
        mockConfig.get.assert_any_call('COLLAGE', 'height', 400, 'int')
        mockConfig.get.assert_any_call('COLLAGE', 'algorithm', Algorithm.COLLAGE, 'int')
        mockConfig.get.assert_any_call('FILE', 'initialdirectory', mockOs.path.expanduser('~'))
        self.assertEqual(m.getRegionCount(), 8, 'Unexpected region count')
        self.assertEqual(m.getWidth(), 100, 'Unexpected width')
        self.assertEqual(m.getHeight(), 200, 'Unexpected height')
        self.assertEqual(m.getAlgorithm(), Algorithm.GRID, 'Unexpected algorithm')
        self.assertEqual(m.getCurrentDirectory(), 'currentDirectory', msg = 'Unexpected current directory')
        self.assertEqual(m.getRegions(), None, 'Expected region list to be initialise to None')

    def testSetCurrentDirectory(self):
        """Test that setting the current directory also updates the config file."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.return_value = 'currentDirectory'
        m = model.Model(mockConfig)
        
        m.setCurrentDirectory('newDirectory')
        
        mockConfig.update.assert_any_call('FILE', 'initialdirectory', 'newDirectory')

    def testSetRegions(self):
        """Test that setting the regions also updates the config file with the number of regions."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.side_effect = [8, 100, 200, Algorithm.GRID, 'currentDirectory']
        m = model.Model(mockConfig)
        
        m.setRegions([(1, 2, 3, 4)])
        
        mockConfig.update.assert_any_call('COLLAGE', 'regionCount', 1)

    def testSetWidth(self):
        """Test that the width is persisted in the config file."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.side_effect = [8, 100, 200, Algorithm.GRID, 'currentDirectory']
        m = model.Model(mockConfig)
        
        m.setWidth(300)
        
        mockConfig.update.assert_any_call('COLLAGE', 'width', 300)

    def testSetHeight(self):
        """Test that the height is persisted in the config file."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.side_effect = [8, 100, 200, Algorithm.GRID, 'currentDirectory']
        m = model.Model(mockConfig)
        
        m.setHeight(300)
        
        mockConfig.update.assert_any_call('COLLAGE', 'height', 300)

    def testSetAlgorithm(self):
        """Test that the algorithm is persisted in the config file."""
        mockConfig = Mock(name = "Config")
        mockConfig.get.side_effect = [8, 100, 200, Algorithm.GRID, 'currentDirectory']
        m = model.Model(mockConfig)
        
        m.setAlgorithm(Algorithm.FRAME)
        
        mockConfig.update.assert_any_call('COLLAGE', 'algorithm', Algorithm.FRAME)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
