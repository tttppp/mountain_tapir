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
test_open_image_dialog
----------------------------------

Tests for `open_image_dialog` module.
"""

import unittest
import mock

from mountain_tapir import open_image_dialog


class TestOpenImageDialog(unittest.TestCase):
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog.grab_set')
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog.wait_visibility')
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog.protocol')
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog.bind')
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog._OpenImageDialog__loadThumbnails')
    @mock.patch('mountain_tapir.open_image_dialog.OpenImageDialog.transient')
    @mock.patch('mountain_tapir.open_image_dialog.resource_string')
    @mock.patch('mountain_tapir.open_image_dialog.os')
    @mock.patch('mountain_tapir.open_image_dialog.ImageTk')
    @mock.patch('mountain_tapir.open_image_dialog.TK')
    def testInitialize(self, mockTK, mockImageTk, mockOs, mockResourceString, mockTransient, mockLoadThumbnails,
                       mockBind, mockProtocol, mockWaitVisibility, mockGrabSet):
        """Test creating a new OpenImageDialog object."""

        # Call the method under test.
        o = open_image_dialog.OpenImageDialog('parent', 'initialDir')

        mockTransient.assert_any_call('parent')
        mockLoadThumbnails.assert_any_call('initialDir')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
