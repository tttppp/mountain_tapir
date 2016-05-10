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
test_menu
----------------------------------

Tests for `menu` module.
"""

import unittest
import mock

from mountain_tapir import region_maker
from mountain_tapir import algorithm

class TestRegionMaker(unittest.TestCase):
    @mock.patch('mountain_tapir.region_maker.randrange')
    def testMakeRegions_collage(self, mockRandrange):
        """Test generating some regions using the collage algorithm."""
        mockModel = mock.Mock(name = 'Model')
        mockModel.algorithm = algorithm.Algorithm.COLLAGE
        mockModel.width = 1000
        mockModel.height = 2000
        mockModel.regionCount = 4
        
        # Pick an arbitrary integer sequence to be returned by the randrange
        # method. We ensure that all values are 'near' to half the supplied
        # value as this helps to avoid "unacceptable" regions.
        mockRandrange.side_effect = (lambda m: ((m**2)%int(m//4)) + int(3*m//8))

        # Call the method under test.
        regions = region_maker.RegionMaker.makeRegions(mockModel)
        
        self.assertEqual(regions, [(375, 0, 625, 2000), (149, 0, 226, 2000), (0, 0, 56, 2000), (56, 0, 93, 2000)])

    def testMakeRegions_grid(self):
        """Test generating some regions using the grid algorithm."""
        mockModel = mock.Mock(name = 'Model')
        mockModel.algorithm = algorithm.Algorithm.GRID
        mockModel.width = 1000
        mockModel.height = 2000
        mockModel.regionCount = 4

        # Call the method under test.
        regions = region_maker.RegionMaker.makeRegions(mockModel)
        
        self.assertEqual(regions, [(0, 0, 500, 1000), (0, 1000, 500, 1000), (500, 0, 500, 1000), (500, 1000, 500, 1000)])

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
