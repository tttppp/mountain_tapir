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
test_preview
----------------------------------

Tests for `preview` module.
"""

import unittest
import mock

from mountain_tapir import preview
from mountain_tapir import constants

class TestPreview(unittest.TestCase):
    @mock.patch('mountain_tapir.preview.TK')
    def testInitialize(self, mockTK):
        """Test creating a new Preview object.
        
        This test also covers the createPreviewFrame method."""
        mockParent = mock.Mock(name = 'Parent')
        mockController = mock.Mock(name = 'Controller')
        
        mockPreviewContainer = mock.Mock(name = 'PreviewContainer')
        mockPreviewFrame = mock.Mock(name = 'PreviewFrame')
        mockTK.Frame.side_effect = [mockPreviewContainer, mockPreviewFrame]
        
        # Call the method under test.
        preview.Preview(mockParent, mockController)
        
        mockTK.Frame.assert_any_call(mockParent)
        mockPreviewContainer.pack.assert_any_call(side=mockTK.TOP, fill=mockTK.BOTH, expand=mockTK.YES)
        mockPreviewContainer.bind.assert_any_call('<Configure>', mockController.adjustPreviewSize)
        mockTK.Frame.assert_any_call(mockPreviewContainer,
                                     width=constants.Constants.INITIAL_WIDTH,
                                     height=constants.Constants.INITIAL_HEIGHT)
        mockPreviewFrame.pack.assert_any_call()

    @mock.patch('mountain_tapir.preview.TK')
    @mock.patch('mountain_tapir.preview.Preview.createPreviewFrame')
    def testClearAndCreateFrame(self, mockCreatePreviewFrame, mockTK):
        """Test creating a new Preview object."""
        mockParent = mock.Mock(name = 'Parent')
        mockController = mock.Mock(name = 'Controller')
        
        p = preview.Preview(mockParent, mockController)
        mockPreviewFrame = mock.Mock(name = 'PreviewFrame')
        p.previewFrame = mockPreviewFrame
        
        # Call the method under test.
        p.clearAndCreateFrame(10, 20)
        
        mockPreviewFrame.destroy.assert_any_call()
        mockCreatePreviewFrame.assert_any_call(10, 20)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
