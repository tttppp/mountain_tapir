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
test_recent_images
----------------------------------

Tests for `recent_images` module.
"""

import unittest
import mock

from mountain_tapir import recent_images

class TestRecentImages(unittest.TestCase):
    @mock.patch('mountain_tapir.recent_images.TK')
    def testInitialize(self, mockTK):
        """Test creating a new RecentImages object.
        
        This test also covers the createScrollFrame method."""
        mockParent = mock.Mock(name = 'Parent')
        mockController = mock.Mock(name = 'Controller')
        
        mockRecentImagesFrame = mock.Mock(name = 'RecentImagesFrame')
        mockScrollFrame = mock.Mock(name = 'ScrollFrame')
        mockTK.Frame.side_effect = [mockRecentImagesFrame, mockScrollFrame]
        mockClearAllButton = mock.Mock(name = 'ClearAllButton')
        mockTK.Button.return_value = mockClearAllButton
        
        # Call the method under test.
        r = recent_images.RecentImages(mockParent, mockController)
        
        mockTK.Frame.assert_any_call(mockParent)
        mockRecentImagesFrame.pack.assert_any_call(side=mockTK.TOP)
        mockTK.Frame.assert_any_call(mockRecentImagesFrame, height=(recent_images.THUMBNAIL_HEIGHT+2))
        mockScrollFrame.pack.assert_any_call(side=mockTK.LEFT)
        mockTK.Button.assert_any_call(mockRecentImagesFrame, text='Clear', command=r.clearAll)
        mockClearAllButton.pack.assert_any_call(side=mockTK.RIGHT)

    @mock.patch('mountain_tapir.recent_images.TK')
    @mock.patch('mountain_tapir.recent_images.RecentImages.createScrollFrame')
    def testClearAll(self, mockCreateScrollFrame, mockTK):
        """Test calling the clearAll method, as would happen when clicking the button."""
        mockParent = mock.Mock(name = 'Parent')
        mockController = mock.Mock(name = 'Controller')
        r = recent_images.RecentImages(mockParent, mockController)
        # Clear the call to createScrollFrame, as we want to test it later.
        mockCreateScrollFrame.reset_mock()
        
        mockScrollFrame = mock.Mock(name = 'ScrollFrame')
        r.scrollFrame = mockScrollFrame
        mockChildA = mock.Mock(name = 'Child A')
        mockChildB = mock.Mock(name = 'Child B')
        mockScrollFrame.winfo_children.return_value = [mockChildA, mockChildB]
        
        # Call the method under test.
        r.clearAll()
        
        mockChildA.destroy.assert_any_call()
        mockChildB.destroy.assert_any_call()
        mockCreateScrollFrame.assert_any_call()

    @mock.patch('mountain_tapir.recent_images.TK')
    def testAddImage(self, mockTK):
        """Test the behaviour when adding an image to the recent images pane."""
        mockParent = mock.Mock(name = 'Parent')
        mockController = mock.Mock(name = 'Controller')
        r = recent_images.RecentImages(mockParent, mockController)
        mockScrollFrame = mock.Mock(name = 'ScrollFrame')
        r.scrollFrame = mockScrollFrame
        mockImageFile = mock.Mock(name = 'ImageFile')
        mockSelectPlaceToolFunction = mock.Mock(name = 'SelectPlaceToolFunction')
        mockImageCell = mock.Mock(name = 'ImageCell')
        mockTK.Frame.return_value = mockImageCell
        mockImageCellCanvas = mock.Mock(name = 'ImageCellCanvas')
        mockTK.Canvas.return_value = mockImageCellCanvas

        # Call the method under test.
        r.addImage(mockImageFile, mockSelectPlaceToolFunction)

        mockTK.Frame.assert_any_call(mockScrollFrame, width=recent_images.THUMBNAIL_WIDTH, height=recent_images.THUMBNAIL_HEIGHT)
        mockTK.Canvas.assert_any_call(mockImageCell, width=recent_images.THUMBNAIL_WIDTH, height=recent_images.THUMBNAIL_HEIGHT)
        mockImageCellCanvas.pack.assert_any_call()
        mockImageFile.makeImage.assert_any_call('thumbnail', (recent_images.THUMBNAIL_WIDTH, recent_images.THUMBNAIL_HEIGHT), mockImageCellCanvas)
        assert mockImageCellCanvas.bind.called, 'Expected bind to have been called.'
        mockImageCell.pack.assert_any_call(side=mockTK.LEFT)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
