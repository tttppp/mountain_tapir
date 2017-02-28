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

from mountain_tapir import menu


class TestMenu(unittest.TestCase):
    @mock.patch('mountain_tapir.menu.os')
    @mock.patch('mountain_tapir.menu.ImageTk')
    @mock.patch('mountain_tapir.menu.TK')
    def testInitialize(self, mockTK, mockImageTk, mockOs):
        """Test creating a new Menu object.

        This test mainly looks out for exceptions, but also checks that the right images are loaded for the buttons."""
        mockParent = mock.Mock(name='Parent')
        mockController = mock.Mock(name='Controller')
        mockOs.sep = '/'

        # Call the method under test.
        menu.Menu(mockParent, mockController)

        # Just check that the expected images are loaded, don't bother checking which buttons they're bound to.
        mockImageTk.PhotoImage.assert_any_call(file='mountain_tapir/resources/algorithm_collage.png')
        mockImageTk.PhotoImage.assert_any_call(file='mountain_tapir/resources/algorithm_grid.png')
        mockImageTk.PhotoImage.assert_any_call(file='mountain_tapir/resources/algorithm_frame.png')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
