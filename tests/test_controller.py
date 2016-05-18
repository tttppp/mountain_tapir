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
test_controller
----------------------------------

Tests for `controller` module.
"""

import unittest
import mock

from mountain_tapir import controller

class TestController(unittest.TestCase):
    @mock.patch('mountain_tapir.controller.Controller.putImageInPreviewRegion')
    @mock.patch('mountain_tapir.controller.RegionMaker')
    @mock.patch('mountain_tapir.controller.TK')
    def testInitialize(self, mockTK, mockRegionMaker, mockPutImageInPreviewRegion):
        """Test initialising a Controller object.
        
        Initialise a single region with a preview pane a tenth the size."""
        mockModel = mock.Mock(name = 'Model')
        mockModel.width = 1000
        mockModel.height = 2000
        mockModel.regionToCanvas = {}
        mockImageFile = mock.Mock(name = 'ImageFile')
        mockModel.regionToImageFile = {(100, 300, 1000, 200): mockImageFile}
        mockUIVars = mock.Mock(name = 'UIVars')
        c = controller.Controller(mockModel, mockUIVars)
        mockPreview = mock.Mock(name = 'Preview')
        mockPreview.previewContainer.winfo_width.return_value = 100
        mockPreview.previewContainer.winfo_height.return_value = 200
        mockRecentImages = mock.Mock(name = 'RecentImages')
        # Pretend there's just one region (and it doesn't cover the whole canvas)
        mockRegionMaker.makeRegions.return_value = [(100, 300, 1000, 200)]
        mockImageCell = mock.Mock(name = 'ImageCell')
        mockTK.Frame.return_value = mockImageCell
        mockCanvas = mock.Mock(name = 'Canvas')
        mockTK.Canvas.return_value = mockCanvas

        # Call the method under test.
        c.initialise(mockPreview, mockRecentImages)
        
        mockRegionMaker.makeRegions.assert_any_call(mockModel)
        mockTK.Frame.assert_any_call(mockPreview.previewFrame, width=100, height=20)
        mockImageCell.place.assert_any_call(x=10, y=30)
        self.assertEqual(mockModel.regionToCanvas, {(10, 30, 100, 20): mockCanvas})
        assert not mockPutImageInPreviewRegion.called, 'The method putImageInPreviewRegion '\
            + 'should not have been called, because regionToImageFile should have been cleared.'
        self.assertEquals(mockModel.regionToImageFile, {})

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
