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

class TestMountainTapir(unittest.TestCase):
    @mock.patch('mountain_tapir.mountain_tapir.TK')
    @mock.patch('mountain_tapir.mountain_tapir.Controller')
    @mock.patch('mountain_tapir.mountain_tapir.Preview')
    @mock.patch('mountain_tapir.mountain_tapir.RecentImages')
    @mock.patch('mountain_tapir.mountain_tapir.Menu')
    @mock.patch('mountain_tapir.mountain_tapir.UIVars')
    def testInitialize(self, mockUIVars, mockMenu, mockRecentImages, mockPreview, mockController, mockTK):
        """Test creating a new MountainTapir object."""
        mockParent = mock.Mock(name = 'Parent')
        mockParent.winfo_screenwidth.return_value = 1000
        mockParent.winfo_screenheight.return_value = 2000
        mockAppContainer = mock.Mock(name = 'AppContainer')
        mockTK.Frame.return_value = mockAppContainer

        # Call the method under test.
        mountain_tapir.MountainTapir(mockParent)
        
        mockParent.geometry.assert_any_call('1060x500+-30+750')
        mockAppContainer.pack.assert_any_call(fill=mockTK.BOTH, expand=mockTK.YES)
        mockController().initialise.assert_any_call(mockPreview(), mockRecentImages())

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
