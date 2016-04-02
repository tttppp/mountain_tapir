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
test_image_file
----------------------------------

Tests for `image_file` module.
"""

import unittest
import mock

from mountain_tapir import image_file

class TestImageFile(unittest.TestCase):
    @mock.patch('mountain_tapir.image_file.TK')
    @mock.patch('mountain_tapir.image_file.Image')
    @mock.patch('mountain_tapir.image_file.ImageTk')
    @mock.patch('mountain_tapir.image_file.ImageFile.getImageObject')
    def testMakeImage(self, mockGetImageObject, mockImageTk, mockImage, mockTK):
        """Test that the properties file is loaded when the Config is initialised."""
        mockCanvas = mock.Mock(name = "Canvas")
        dimensions = (2, 3)
        
        mockImageObject = mock.Mock(name = 'ImageObject')
        mockGetImageObject.return_value = mockImageObject
        mockPhotoImage = mock.Mock(name = 'PhotoImage')
        mockImageTk.PhotoImage.return_value = mockPhotoImage
        
        imageFile = image_file.ImageFile('file/path')
        imageFile.makeImage('purpose', dimensions, mockCanvas)
        
        mockGetImageObject.assert_called_with((2,3), 'purpose')
        mockImageTk.PhotoImage.assert_called_with(mockImageObject)
        assert mockPhotoImage in imageFile.images['purpose'], \
            'The new photo image was not added to the persisted images list'
        mockCanvas.create_image.assert_called_with(0, 0, image=mockPhotoImage, anchor="nw")
        mockCanvas.config.assert_called_with(scrollregion=mockCanvas.bbox())

    @mock.patch('mountain_tapir.image_file.TK')
    @mock.patch('mountain_tapir.image_file.Image')
    @mock.patch('mountain_tapir.image_file.ImageTk')
    def testGetImageObject_tooWide(self, mockImageTk, mockImage, mockTK):
        """Test creating an image that needs to be cropped horizontally."""
        mockPhotoImage = mock.Mock(name = "PhotoImage")
        mockImageTk.PhotoImage.return_value = mockPhotoImage
        mockImg = mock.Mock(name = 'Img')
        mockImage.open.return_value = mockImg
        mockImg.size = (20, 30)
        mockResizedImg = mock.Mock(name = 'ResizedImg')
        mockImg.resize.return_value = mockResizedImg
        mockResizedImg.size = (26, 40)
        mockResizedImg.crop.return_value = 'Final image'

        imageFile = image_file.ImageFile('file/path')
        image = imageFile.getImageObject((10, 40), 'purpose')
        
        mockImg.resize.assert_called_with((26, 40), mockImage.ANTIALIAS)
        mockResizedImg.crop.assert_called_with((8, 0, 18, 40))
        assert image == 'Final image'

    @mock.patch('mountain_tapir.image_file.TK')
    @mock.patch('mountain_tapir.image_file.Image')
    @mock.patch('mountain_tapir.image_file.ImageTk')
    def testGetImageObject_tooTall(self, mockImageTk, mockImage, mockTK):
        """Test creating an image that needs to be cropped vertically."""
        mockPhotoImage = mock.Mock(name = "PhotoImage")
        mockImageTk.PhotoImage.return_value = mockPhotoImage
        mockImg = mock.Mock(name = 'Img')
        mockImage.open.return_value = mockImg
        mockImg.size = (20, 30)
        mockResizedImg = mock.Mock(name = 'ResizedImg')
        mockImg.resize.return_value = mockResizedImg
        mockResizedImg.size = (40, 60)
        mockResizedImg.crop.return_value = 'Final image'

        imageFile = image_file.ImageFile('file/path')
        image = imageFile.getImageObject((40, 10), 'purpose')
        
        mockImg.resize.assert_called_with((40, 60), mockImage.ANTIALIAS)
        mockResizedImg.crop.assert_called_with((0, 25, 40, 35))
        assert image == 'Final image'

    @mock.patch('mountain_tapir.image_file.TK')
    @mock.patch('mountain_tapir.image_file.Image')
    @mock.patch('mountain_tapir.image_file.ImageTk')
    def testGetImageObject_notFound(self, mockImageTk, mockImage, mockTK):
        """Test creating an image when the file couldn't be opened."""
        mockImage.open.side_effect = IOError

        imageFile = image_file.ImageFile('file/path')
        image = imageFile.getImageObject((40, 10), 'purpose')
        
        assert image == None

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
