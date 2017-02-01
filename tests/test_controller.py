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
from mountain_tapir.tool import Tool

class TestController(unittest.TestCase):
    @mock.patch('mountain_tapir.controller.Controller.putImageInPreviewRegion')
    @mock.patch('mountain_tapir.controller.RegionMaker')
    @mock.patch('mountain_tapir.controller.TK')
    def testInitialize(self, mockTK, mockRegionMaker, mockPutImageInPreviewRegion):
        """Test initialising a Controller object.
        
        Initialise a single region with a preview pane a tenth the size."""
        mockModel = mock.Mock(name = 'Model')
        mockModel.getWidth.return_value = 1000
        mockModel.getHeight.return_value = 2000
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
        mockModel.getRegions.return_value = [(100, 300, 1000, 200)]
        mockImageCell = mock.Mock(name = 'ImageCell')
        mockTK.Frame.return_value = mockImageCell
        mockCanvas = mock.Mock(name = 'Canvas')
        mockTK.Canvas.return_value = mockCanvas

        # Call the method under test.
        c.initialise(mockPreview, mockRecentImages)
        
        mockModel.setRegions.assert_any_call([(100, 300, 1000, 200)])
        mockTK.Frame.assert_any_call(mockPreview.previewFrame, width=100, height=20)
        mockImageCell.place.assert_any_call(x=10, y=30)
        self.assertEqual(mockModel.regionToCanvas, {(10, 30, 100, 20): mockCanvas})
        assert not mockPutImageInPreviewRegion.called, 'The method putImageInPreviewRegion '\
            + 'should not have been called, because regionToImageFile should have been cleared.'
        self.assertEqual(mockModel.regionToImageFile, {})

    @mock.patch('mountain_tapir.controller.Controller.putImageInPreviewRegion')
    @mock.patch('mountain_tapir.controller.sample')
    def testShuffle(self, mockSample, mockPutImageInPreviewRegion):
        mockModel = mock.Mock(name = 'Model')
        mockModel.getWidth.return_value = 1000
        mockModel.getHeight.return_value = 2000
        mockModel.getRegions.return_value = [(0,0,10,10), (10,0,10,10), (20,0,10,10), (30,0,10,10)]
        # Fix the order of the returned image files.
        mockModel.regionToImageFile.values.side_effect = [['imageFile2','imageFile0','imageFile1','imageFile3']]
        mockModel.regionToCanvas = {(0,0,10,10): 'canvas0', (10,0,10,10): 'canvas1', (20,0,10,10): 'canvas2', (30,0,10,10): 'canvas3'}
        mockUIVars = mock.Mock(name = 'UIVars')
        c = controller.Controller(mockModel, mockUIVars)
        # Ensure the sample function returns the regions in a known order.
        mockSample.side_effect = [[(0,0,10,10)], [(10,0,10,10)], [(20,0,10,10)], [(30,0,10,10)]]

        # Call the method under test.
        c.shuffle()

        mockModel.regionToImageFile.clear.assert_any_call()
        # Ensure the images have been 'shuffled correctly'.
        mockPutImageInPreviewRegion.assert_any_call('imageFile2', 'canvas0', (0,0,10,10))
        mockPutImageInPreviewRegion.assert_any_call('imageFile0', 'canvas1', (10,0,10,10))
        mockPutImageInPreviewRegion.assert_any_call('imageFile1', 'canvas2', (20,0,10,10))
        mockPutImageInPreviewRegion.assert_any_call('imageFile3', 'canvas3', (30,0,10,10))

    @mock.patch('mountain_tapir.controller.asksaveasfile')
    @mock.patch('mountain_tapir.controller.Image')
    @mock.patch('mountain_tapir.controller.TK')
    def testSave(self, mockTK, mockImage, mockAsksaveasfile):
        """Test saving a collage."""
        mockOutputImage = mock.Mock(name = 'mockOutputImage')
        mockImage.new.side_effect = [mockOutputImage]
        mockAsksaveasfile.side_effect = ['outputFile.png']
        mockModel = mock.Mock(name = 'Model')        
        mockModel.getWidth.return_value = 1000
        mockModel.getHeight.return_value = 2000
        mockModel.getRegions.return_value = [(0,0,10,10), (10,0,10,10), (20,0,10,10), (30,0,10,10)]
        # Fix the order of the returned image files.
        mockImages = [mock.Mock(name = 'ImageFile0'), mock.Mock(name = 'ImageFile1'),
                      mock.Mock(name = 'ImageFile2'), mock.Mock(name = 'ImageFile3')]
        mockModel.regionToImageFile = {(0,0,10,10):mockImages[0],
                                       (10,0,10,10):mockImages[1],
                                       (20,0,10,10):mockImages[2],
                                       (30,0,10,10):mockImages[3]}
        mockUIVars = mock.Mock(name = 'UIVars')
        c = controller.Controller(mockModel, mockUIVars)
        
        # Call the method under test.
        c.save()
        
        mockAsksaveasfile.assert_any_call(defaultextension = '.jpg')
        mockImage.new.assert_any_call('RGB', (1000, 2000))
        # Check the images were pasted in the right places.
        mockOutputImage.paste.assert_any_call(mockImages[0].getImageObject(), (0, 0))
        mockOutputImage.paste.assert_any_call(mockImages[1].getImageObject(), (10, 0))
        mockOutputImage.paste.assert_any_call(mockImages[2].getImageObject(), (20, 0))
        mockOutputImage.paste.assert_any_call(mockImages[3].getImageObject(), (30, 0))
        # Check the output image was saved correctly.
        mockOutputImage.save.assert_any_call('outputFile.png')

    def testMakePreviewRegion(self):
        """Test the calculation of a region forming part of the preview."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.getWidth.return_value = 40
        mockModel.getHeight.return_value = 10
        c = controller.Controller(mockModel, None)
        mockPreview = mock.Mock(name = 'mockPreview')
        mockPreview.previewContainer.winfo_width.side_effect = [30]
        mockPreview.previewContainer.winfo_height.side_effect = [6]
        c.preview = mockPreview
        
        # Call the method under test.
        previewRegion = c._Controller__makePreviewRegion((2,4,5,5))
        
        self.assertEqual(previewRegion, (1,2,3,3))

    def testGetPreviewDimensions_thinCanvas(self):
        """Check that if the preview canvas is too thin the region is scaled down."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.getWidth.return_value = 100
        mockModel.getHeight.return_value = 100
        c = controller.Controller(mockModel, None)
        mockPreview = mock.Mock(name = 'mockPreview')
        mockPreview.previewContainer.winfo_width.side_effect = [50]
        mockPreview.previewContainer.winfo_height.side_effect = [100]
        c.preview = mockPreview
        
        # Call the method under test.
        dimensions = c._Controller__getPreviewDimensions()
        
        self.assertEqual(dimensions, (50,50))

    def testGetPreviewDimensions_shortCanvas(self):
        """Check that if the preview canvas is too short the region is scaled down."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.getWidth.return_value = 100
        mockModel.getHeight.return_value = 100
        c = controller.Controller(mockModel, None)
        mockPreview = mock.Mock(name = 'mockPreview')
        mockPreview.previewContainer.winfo_width.side_effect = [100]
        mockPreview.previewContainer.winfo_height.side_effect = [50]
        c.preview = mockPreview
        
        # Call the method under test.
        dimensions = c._Controller__getPreviewDimensions()
        
        self.assertEqual(dimensions, (50,50))

    def testGetPreviewDimensions_tooLargeCanvas(self):
        """Check that if the preview canvas is larger than the output size the region is not scaled."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.getWidth.return_value = 100
        mockModel.getHeight.return_value = 100
        c = controller.Controller(mockModel, None)
        mockPreview = mock.Mock(name = 'mockPreview')
        mockPreview.previewContainer.winfo_width.side_effect = [200]
        mockPreview.previewContainer.winfo_height.side_effect = [200]
        c.preview = mockPreview
        
        # Call the method under test.
        dimensions = c._Controller__getPreviewDimensions()
        
        self.assertEqual(dimensions, (100,100))

    @mock.patch('mountain_tapir.controller.path')
    @mock.patch('mountain_tapir.controller.askopenfilename')
    @mock.patch('mountain_tapir.controller.ImageFile')
    def testLoad(self, mockImageFile, mockAskopenfilename, mockPath):
        """Check that clicking a region using the load tool causes file dialog to be launched."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.LOAD
        mockModel.getCurrentDirectory.return_value = 'oldDir'
        mockCanvas = mock.Mock(name = 'mockCanvas')
        region = (10, 20, 30, 40)
        c = controller.Controller(mockModel, None)
        mockRecentImages = c.recentImages = mock.Mock(name = 'mockRecentImages')
        mockAskopenfilename.return_value = 'newDir/Picture1.jpg'
        mockPath.dirname.return_value = 'newDir'
        mockImageFile.return_value = 'imageFile'
        mockSelectPlaceTool = c.selectPlaceTool = mock.Mock(name = 'mockSelectPlaceTool')
        mockPutImageInPreviewRegion = c.putImageInPreviewRegion = mock.Mock(name = 'mockPutImageInPreviewRegion')
        
        # Call the method under test.
        c.clicked(mockCanvas, region)
        
        mockAskopenfilename.assert_any_call(parent=mockCanvas, initialdir='oldDir', title='Choose an image.')
        mockModel.setCurrentDirectory.assert_called_with('newDir')
        mockRecentImages.addImage.assert_any_call('imageFile', mockSelectPlaceTool)
        mockPutImageInPreviewRegion.assert_any_call('imageFile', mockCanvas, region)

    def testSwapFirstClick(self):
        """Check that clicking a region using the swap tool (when no region is stored) causes it to be stored."""
        region = (10, 20, 30, 40)
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.SWAP
        mockModel.regionToImageFile = {region: 'imageFile'}
        c = controller.Controller(mockModel, None)
        c.selectedImage = c.selectedCanvas = c.selectedRegion = None
        
        # Call the method under test.
        c.clicked('canvas', region)
        
        self.assertEqual(c.selectedImage, 'imageFile')
        self.assertEqual(c.selectedCanvas, 'canvas')
        self.assertEqual(c.selectedRegion, region)

    def testSwapSecondClick(self):
        """Check that clicking a region using the swap tool when another region is stored, causes them to be swapped."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.SWAP
        mockModel.regionToImageFile = {'clickedRegion': 'clickedImage'}
        c = controller.Controller(mockModel, None)
        c.selectedImage = 'firstImage'
        c.selectedCanvas = 'firstCanvas'
        c.selectedRegion = 'firstRegion'
        mockPutImageInPreviewRegion = c.putImageInPreviewRegion = mock.Mock('mockPutImageInPreviewRegion')
        
        # Call the method under test.
        c.clicked('clickedCanvas', 'clickedRegion')
        
        mockPutImageInPreviewRegion.assert_any_call('clickedImage', 'firstCanvas', 'firstRegion')
        mockPutImageInPreviewRegion('firstImage', 'clickedCanvas', 'clickedRegion')
        self.assertEqual(c.selectedImage, None)
        self.assertEqual(c.selectedCanvas, None)
        self.assertEqual(c.selectedRegion, None)

    def testPlace(self):
        """Check that clicking a region using the place tool puts the image in that region."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.PLACE
        c = controller.Controller(mockModel, None)
        c.selectedImage = 'imageFile'
        mockPutImageInPreviewRegion = c.putImageInPreviewRegion = mock.Mock('mockPutImageInPreviewRegion')
        
        # Call the method under test.
        c.clicked('clickedCanvas', 'clickedRegion')
        
        mockPutImageInPreviewRegion.assert_any_call('imageFile', 'clickedCanvas', 'clickedRegion')

    def testEmpty(self):
        """Check that clicking a region using the empty tool removes any image in that region."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.EMPTY
        c = controller.Controller(mockModel, None)
        mockPutImageInPreviewRegion = c.putImageInPreviewRegion = mock.Mock('mockPutImageInPreviewRegion')
        
        # Call the method under test.
        c.clicked('clickedCanvas', 'clickedRegion')
        
        mockPutImageInPreviewRegion.assert_any_call(None, 'clickedCanvas', 'clickedRegion')


    def testRotate(self):
        """Check that clicking a region using the rotate tool rotates all instances of that image.
        
        Simulate three regions, two of which contain the clicked image."""
        mockModel = mock.Mock(name = 'mockModel')
        mockModel.selectedTool = Tool.ROTATE
        mockImageFile = mock.Mock(name = 'mockImageFile')
        mockModel.regionToImageFile = {'clickedRegion': mockImageFile, 'region2': mockImageFile, 'region3': 'decoyImg'}
        mockModel.regionToCanvas = {'clickedRegion': 'clickedCanvas', 'region2': 'canvas2', 'region3': 'canvas3'}
        c = controller.Controller(mockModel, None)
        mockPutImageInPreviewRegion = c.putImageInPreviewRegion = mock.Mock(name = 'mockPutImageInPreviewRegion')
        mockRecentImages = c.recentImages = mock.Mock(name = 'mockRecentImages')
        
        # Call the method under test.
        c.clicked('clickedCanvas', 'clickedRegion')
        
        mockImageFile.rotate.assert_any_call()
        mockPutImageInPreviewRegion.assert_any_call(mockImageFile, 'clickedCanvas', 'clickedRegion')
        mockPutImageInPreviewRegion.assert_any_call(mockImageFile, 'canvas2', 'region2')
        self.assertEqual(len(mockPutImageInPreviewRegion.mock_calls), 2, 'Extra call to mockPutImageInPreviewRegion.')
        # Also check that the recent images thumbnail is rotated.
        mockRecentImages.updateImage.assert_any_call(mockImageFile)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
