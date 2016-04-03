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
        
        # Call the method under test.
        recent_images.RecentImages(mockParent, mockController)
        
        mockTK.Frame.assert_any_call(mockParent)
        mockRecentImagesFrame.pack.assert_any_call(side=mockTK.TOP)
        mockTK.Frame.assert_any_call(mockRecentImagesFrame, height=(recent_images.THUMBNAIL_HEIGHT+2))
        mockScrollFrame.pack.assert_any_call(side=mockTK.LEFT)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
