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

try:
    import tkinter as TK
except ImportError:
    import Tkinter as TK
try:
    from tkinter.filedialog import askopenfilename, asksaveasfile
except ImportError:
    from tkFileDialog import askopenfilename, asksaveasfile

from collections import defaultdict
from os import path
from PIL import Image
from random import randrange, sample

from image_file import ImageFile
from region_maker import RegionMaker
from tool import Tool

def randColor():
    return '#{0:06x}'.format(randrange(0,16777215))

class Controller:
    def __init__(self, model, uiVars):
        self.model = model
        self.uiVars = uiVars
    def initialise(self, preview, recentImages):
        self.preview = preview
        self.recentImages = recentImages
        self.redraw()
    def selectTool(self, tool):
        self.model.selectedTool = tool
        self.selectedImage = None
        self.selectedCanvas = None
        self.selectedRegion = None
        print(tool)
    def selectPlaceTool(self, image):
        self.selectTool(Tool.PLACE)
        self.selectedImage = image
    def setAlgorithm(self, algorithm):
        self.model.setAlgorithm(algorithm)
        self.redraw()
    def shuffle(self):
        print('Shuffle selected')
        images = self.model.regionToImageFile.values()
        self.model.regionToImageFile.clear()
        regions = set(self.model.getRegions())
        for region in regions:
            canvas = self.model.regionToCanvas[region]
            self.putImageInPreviewRegion(None, canvas, region)
        usedRegions = set()
        for imageFile in images:
            region = sample(regions.difference(usedRegions), 1)[0]
            canvas = self.model.regionToCanvas[region]
            self.putImageInPreviewRegion(imageFile, canvas, region)
            usedRegions.add(region)
    def save(self):
        print('Save selected')
        outputFile = asksaveasfile(defaultextension = '.jpg')
        if outputFile != None:
            outputImage = Image.new('RGB', (self.model.getWidth(), self.model.getHeight()))
            for region in self.model.getRegions():
                imageFile = self.model.regionToImageFile[region]
                if imageFile == None:
                    print('Warning: Region without image {0}'.format(region))
                    continue
                image = imageFile.getImageObject((region[2], region[3]), 'export')
                outputImage.paste(image, (region[0], region[1]))
            outputImage.save(outputFile)
    def addRegions(self, delta):
        print('Change if not going below one')
        if self.model.getRegionCount() + delta > 0:
            self.model.setRegionCount(self.model.getRegionCount() + delta)
            self.uiVars.regionsVar.set(self.model.getRegionCount())
            self.redraw()
    def redraw(self):
        self.model.setRegions(RegionMaker.makeRegions(self.model))
        self.model.regionToImageFile.clear()
        self.refresh()
    def refresh(self):
        self.model.regionToCanvas.clear()
        width, height = self.__getPreviewDimensions()
        self.preview.clearAndCreateFrame(width, height)
        for region in self.model.getRegions():
            previewRegion = self.__makePreviewRegion(region)
            imageCell = TK.Frame(self.preview.previewFrame, width=previewRegion[2], height=previewRegion[3])
            canvas = TK.Canvas(imageCell, width=previewRegion[2], height=previewRegion[3], background=randColor())
            canvas.pack()
            canvas.bind('<Button-1>',lambda e, c=canvas, r=region: self.clicked(c, r))
            imageCell.place(x=previewRegion[0], y=previewRegion[1])
            self.model.regionToCanvas[previewRegion] = canvas
            if region in self.model.regionToImageFile.keys():
                imageFile = self.model.regionToImageFile[region]
                self.putImageInPreviewRegion(imageFile, canvas, region)
    def putImageInPreviewRegion(self, imageFile, canvas, region):
        """Put an image in a preview region (or remove the existing image if None is supplied)"""
        if imageFile != None:
            previewRegion = self.__makePreviewRegion(region)
            imageFile.makeImage('preview', (previewRegion[2], previewRegion[3]), canvas)
        else:
            # 'all' is the special reference to everything on the canvas.
            canvas.delete('all')
        self.model.regionToImageFile[region] = imageFile
        self.model.regionToCanvas[region] = canvas
    def __makePreviewRegion(self, region):
        """Create a region based on the model region and the current size of the preview pane."""
        width, height = self.__getPreviewDimensions()
        return (region[0]*width//self.model.getWidth(), region[1]*height//self.model.getHeight(),
                region[2]*width//self.model.getWidth(), region[3]*height//self.model.getHeight())
    def __getPreviewDimensions(self):
        """Get the current dimensions of the preview panel as a tuple."""
        containerWidth = self.preview.previewContainer.winfo_width()
        containerHeight = self.preview.previewContainer.winfo_height()
        width = min(self.model.getWidth(), containerWidth,
                    (self.model.getWidth() * containerHeight) / self.model.getHeight())
        height = min(self.model.getHeight(), containerHeight,
                     (self.model.getHeight() * containerWidth) / self.model.getWidth())
        return (width, height)
    def clicked(self, canvas, region):
        if self.model.selectedTool == Tool.LOAD:
            fileName = askopenfilename(parent=canvas, initialdir=self.model.getCurrentDirectory(),
                                       title='Choose an image.')
            if fileName == ():
                print('Cancelled opening image')
                return
            self.model.setCurrentDirectory(path.dirname(fileName))
            imageFile = ImageFile(fileName)
            self.model.imageFiles.append(imageFile)
            
            self.recentImages.addImage(imageFile, self.selectPlaceTool)
            
            self.putImageInPreviewRegion(imageFile, canvas, region)
        elif self.model.selectedTool == Tool.SWAP:
            imageFile = self.selectedImage
            otherCanvas = self.selectedCanvas
            otherRegion = self.selectedRegion
            if imageFile == None or otherCanvas == None or otherRegion == None:
                self.selectedImage = self.model.regionToImageFile[region]
                self.selectedCanvas = canvas
                self.selectedRegion = region
            else:
                otherImageFile = self.model.regionToImageFile[region]
                self.putImageInPreviewRegion(imageFile, canvas, region)
                self.putImageInPreviewRegion(otherImageFile, otherCanvas, otherRegion)
                self.selectedImage = None
                self.selectedCanvas = None
                self.selectedRegion = None
        elif self.model.selectedTool == Tool.PLACE:
            imageFile = self.selectedImage
            self.putImageInPreviewRegion(imageFile, canvas, region)
        elif self.model.selectedTool == Tool.EMPTY:
            self.putImageInPreviewRegion(None, canvas, region)
        elif self.model.selectedTool == Tool.ROTATE:
            imageFile = self.model.regionToImageFile[region]
            if imageFile != None:
                imageFile.rotate()
                # Rotate all instances of the image in the collage.
                for r, i in self.model.regionToImageFile.items():
                    if i == imageFile:
                        self.putImageInPreviewRegion(imageFile, self.model.regionToCanvas[r], r)
                self.recentImages.updateImage(imageFile)
        else:
            print('Currently selected tool is not supported yet: {0}'.format(self.model.selectedTool))
    def updateWidth(self, event):
        newWidth = int(self.uiVars.widthVar.get())
        if newWidth != self.model.getWidth():
            self.__scaleRegions((self.model.getWidth(), self.model.getHeight()), (newWidth, self.model.getHeight()))
            self.model.setWidth(newWidth)
            self.refresh()
    def updateHeight(self, event):
        newHeight = int(self.uiVars.heightVar.get())
        if newHeight != self.model.getHeight():
            self.__scaleRegions((self.model.getWidth(), self.model.getHeight()), (self.model.getWidth(), newHeight))
            self.model.setHeight(newHeight)
            self.refresh()
    def __scaleRegions(self, oldDimensions, newDimensions):
        oldRegions, newRegions = self.model.getRegions(), []
        oldRegionToImageFile, self.model.regionToImageFile = self.model.regionToImageFile, defaultdict(lambda : None)
        oldRegionToCanvas, self.model.regionToCanvas = self.model.regionToCanvas, defaultdict(lambda : None)
        for oldRegion in oldRegions:
            newRegion = ((oldRegion[0]*newDimensions[0])//oldDimensions[0], (oldRegion[1]*newDimensions[1])//oldDimensions[1],
                         (oldRegion[2]*newDimensions[0])//oldDimensions[0], (oldRegion[3]*newDimensions[1])//oldDimensions[1])
            newRegions.append(newRegion)
            self.model.regionToImageFile[newRegion] = oldRegionToImageFile[oldRegion]
            self.model.regionToCanvas[newRegion] = oldRegionToCanvas[oldRegion]
        self.model.setRegions(newRegions)
    def adjustPreviewSize(self, event=None):
        self.refresh()
