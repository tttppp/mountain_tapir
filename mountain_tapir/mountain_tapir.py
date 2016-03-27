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

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfile
from PIL import Image, ImageTk
from random import randrange, sample
from collections import defaultdict
import os.path
import ConfigParser

INITIAL_WIDTH = 600
INITIAL_HEIGHT = 400
INITIAL_REGIONS = 6
INITIAL_WINDOW_WIDTH = 1060
INITIAL_WINDOW_HEIGHT = 500

TARGET_RATIO = 2/3
UNACCEPTABLE_WIDTH=50
UNACCEPTABLE_HEIGHT=50

THUMBNAIL_WIDTH = 60
THUMBNAIL_HEIGHT = 60

def randColor():
    return '#'+('%06x'%randrange(0,16777215))

class Config:
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('mountain_tapir.properties')
    def get(self, section, key, default = None):
        value = self.config.get(section, key)
        if value == None:
            value = default
        return value

class UIVars:
    def __init__(self, parent):
        self.widthVar = IntVar(parent, INITIAL_WIDTH)
        self.heightVar = IntVar(parent, INITIAL_HEIGHT)
        self.regionsVar = IntVar(parent, INITIAL_REGIONS)

class Tool:
    LOAD, SWAP, EMPTY, PLACE = range(4)
class Algorithm:
    COLLAGE, GRID, FRAME = range(3)

class ImageFile:
    def __init__(self, fileName):
        self.fileName = fileName
        # We need to store all the images otherwise they're garbage collected.
        self.images = defaultdict(list)
    def makeImage(self, purpose, dimensions, canvas):
        image = self.getImageObject(dimensions)
        if image != None:
            photoImage = ImageTk.PhotoImage(image)
            self.images[purpose].append(photoImage)
            canvas.create_image(0, 0, image=photoImage, anchor="nw")
            canvas.config(scrollregion=canvas.bbox(ALL))
    def getImageObject(self, dimensions):
        try:
            image = Image.open(self.fileName)
        except IOError:
            print 'Error opening image for %s'%purpose
            return None
        originalDimensions = image.size
        if originalDimensions[0] * dimensions[1] > originalDimensions[1] * dimensions[0]:
            resizeWidth = (originalDimensions[0] * dimensions[1]) / originalDimensions[1]
            resizeHeight = dimensions[1]
            resizeDimensions = (resizeWidth, resizeHeight)
        else:
            resizeWidth = dimensions[0]
            resizeHeight = (originalDimensions[1] * dimensions[0]) / originalDimensions[0]
            resizeDimensions = (resizeWidth, resizeHeight)
        image = image.resize(resizeDimensions, Image.ANTIALIAS)
        middle = (image.size[0] / 2, image.size[1] / 2)
        left = middle[0] - dimensions[0] / 2
        top = middle[1] - dimensions[1] / 2
        box = (left, top, left + dimensions[0], top + dimensions[1])
        return image.crop(box)
        
class Model:
    def __init__(self, config):
        self.selectedTool = Tool.LOAD
        self.regionCount = INITIAL_REGIONS
        self.width = INITIAL_WIDTH
        self.height = INITIAL_HEIGHT
        self.algorithm = Algorithm.COLLAGE
        self.regions = None
        self.imageFiles = []
        self.regionToImageFile = defaultdict(lambda : None)
        self.regionToCanvas = defaultdict(lambda : None)
        self.currentDirectory = config.get('FILE', 'initialdirectory', '/')

class RegionMaker:
    """A region is a tuple (left, top, width, height)."""
    @staticmethod
    def makeRegions(model):
        """Split the preview pane into disjoint regions."""
        if model.algorithm == Algorithm.COLLAGE:
            return RegionMaker.makeCollageRegions(model)
        elif model.algorithm == Algorithm.GRID:
            return RegionMaker.makeGridRegions(model)
        elif model.algorithm == Algorithm.FRAME:
            return RegionMaker.makeFrameRegions(model)
        else:
            print 'Unsupported algorithm: ' + model.algorithm
    @staticmethod
    def makeCollageRegions(model):
        """Start with the whole area as a region. Each iteration pick the 'worst' region and split it either horizontally
        or vertically at a random point. Remove the old region and add the two new regions.
        
        The worst region is defined to be the region furthest from the TARGET_RATIO.
        """
        def ratioDiff(width, height):
            if width == 0 or height == 0:
                return 0
            return min(abs((width*1.0/height) - TARGET_RATIO), abs((height*1.0/width) - TARGET_RATIO))
        def randNearMid(maximum):
            return (randrange(maximum) + randrange(maximum)) // 2
        regions = [(0, 0, model.width, model.height)]
        while len(regions) < model.regionCount:
            worstRegion = None
            worstRegionDiff = -1
            for region in regions:
                regionDiff = ratioDiff(region[2], region[3])
                if regionDiff > worstRegionDiff:
                    worstRegion = region
                    worstRegionDiff = regionDiff
            relativeSplitPoint = (randNearMid(worstRegion[2]), randNearMid(worstRegion[3]))
            worstHorizontalSplitDiff = max(ratioDiff(relativeSplitPoint[0], worstRegion[3]),
                                           ratioDiff(worstRegion[2]-relativeSplitPoint[0], worstRegion[3]))
            worstVerticalSplitDiff = max(ratioDiff(worstRegion[2], relativeSplitPoint[1]),
                                         ratioDiff(worstRegion[2], worstRegion[3]-relativeSplitPoint[1]))
            regions.remove(worstRegion)
            if worstHorizontalSplitDiff > worstVerticalSplitDiff:
                # Split vertically
                regions.append((worstRegion[0], worstRegion[1], relativeSplitPoint[0], worstRegion[3]))
                regions.append((worstRegion[0]+relativeSplitPoint[0], worstRegion[1], worstRegion[2]-relativeSplitPoint[0], worstRegion[3]))
            else:
                # Split horizontally
                regions.append((worstRegion[0], worstRegion[1], worstRegion[2], relativeSplitPoint[1]))
                regions.append((worstRegion[0], worstRegion[1]+relativeSplitPoint[1], worstRegion[2], worstRegion[3]-relativeSplitPoint[1]))
            # Restart if any width or height is unacceptable
            if regions[-2][2] <= UNACCEPTABLE_WIDTH or regions[-2][3] <= UNACCEPTABLE_HEIGHT or regions[-1][2] <= UNACCEPTABLE_WIDTH or regions[-1][3] <= UNACCEPTABLE_HEIGHT:
                regions = [(0, 0, model.width, model.height)]
        return regions
    @staticmethod
    def makeGridRegions(model):
        shortSide = int(sqrt(model.regionCount))
        while model.regionCount % shortSide != 0:
            shortSide -= 1
        longSide = model.regionCount // shortSide
        if model.width > model.height:
            columns = longSide
            rows = shortSide
        else:
            columns = shortSide
            rows = longSide
        # Need to set width and height of each cell programmatically to avoid rounding errors in calculation of cellWidth and cellHeight
        return [(x*model.width//columns,
                 y*model.height//rows,
                 (x+1)*model.width//columns - x*model.width//columns,
                 (y+1)*model.height//rows - y*model.height//rows)
                for x in range(columns) for y in range(rows)]
    @staticmethod
    def makeFrameRegions(model):
        return []

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
        print tool
    def selectPlaceTool(self, image):
        self.selectTool(Tool.PLACE)
        self.selectedImage = image
    def setAlgorithm(self, algorithm):
        self.model.algorithm = algorithm
        self.redraw()
    def shuffle(self):
        print 'Shuffle selected'
        images = self.model.regionToImageFile.values()
        self.model.regionToImageFile.clear()
        regions = set(self.model.regions)
        for region in regions:
            canvas = self.model.regionToCanvas[region]
            self.putImageInPreviewRegion(None, self.model.regionToCanvas[region], region)
        usedRegions = set()
        for imageFile in images:
            region = sample(regions.difference(usedRegions), 1)[0]
            canvas = self.model.regionToCanvas[region]
            self.putImageInPreviewRegion(imageFile, canvas, region)
            usedRegions.add(region)
    def save(self):
        print 'Save selected'
        fileName = asksaveasfile()
        if fileName != None:
            outputImage = Image.new("RGB", (self.model.width, self.model.height))
            for region in self.model.regions:
                imageFile = self.model.regionToImageFile[region]
                if imageFile == None:
                    print 'Warning: Region without image %s'%(region,)
                    continue
                image = imageFile.getImageObject((region[2], region[3]))
                outputImage.paste(image, (region[0], region[1]))
            outputImage.save(fileName)
    def addRegions(self, delta):
        print 'Change if not going below one'
        if self.model.regionCount + delta > 0:
            self.model.regionCount += delta
            self.uiVars.regionsVar.set(self.model.regionCount)
            self.redraw()
    def redraw(self):
        self.model.regions = RegionMaker.makeRegions(self.model)
        self.model.regionToImageFile.clear()
        self.refresh()
    def refresh(self):
        self.model.regionToCanvas.clear()
        containerWidth = self.preview.previewContainer.winfo_width()
        containerHeight = self.preview.previewContainer.winfo_height()
        width = min(self.model.width, containerWidth, (self.model.width * containerHeight) / self.model.height)
        height = min(self.model.height, containerHeight, (self.model.height * containerWidth) / self.model.width)
        self.preview.clearAndCreateFrame(width, height)
        for region in self.model.regions:
            previewRegion = (region[0]*width/self.model.width, region[1]*height/self.model.height, region[2]*width/self.model.width, region[3]*height/self.model.height)
            imageCell = Frame(self.preview.previewFrame, width=previewRegion[2], height=previewRegion[3])
            canvas = Canvas(imageCell, width=previewRegion[2], height=previewRegion[3], background=randColor())
            canvas.pack()
            canvas.bind('<Button-1>',lambda e, c=canvas, r=region: self.clicked(c, r))
            imageCell.place(x=previewRegion[0], y=previewRegion[1])
            self.model.regionToCanvas[previewRegion] = canvas
            if region in self.model.regionToImageFile.keys():
                imageFile = self.model.regionToImageFile[region]
                self.putImageInPreviewRegion(imageFile, canvas, previewRegion)
    def putImageInPreviewRegion(self, imageFile, canvas, region):
        """Put an image in a preview region (or remove the existing image if None is supplied)"""
        if imageFile != None:
            imageFile.makeImage('preview', (region[2], region[3]), canvas)
        else:
            # 'all' is the special reference to everything on the canvas.
            canvas.delete('all')
        self.model.regionToImageFile[region] = imageFile
    def clicked(self, canvas, region):
        if self.model.selectedTool == Tool.LOAD:
            fileName = askopenfilename(parent=canvas, initialdir=self.model.currentDirectory, title='Choose an image.')
            if fileName == '':
                print 'Cancelled opening image'
                return
            self.model.currentDirectory = os.path.dirname(fileName)
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
        else:
            print 'Currently selected tool is not supported yet: %d'%self.model.selectedTool
    def updateWidth(self, event):
        newWidth = int(self.uiVars.widthVar.get())
        if newWidth != self.model.width:
            self.scaleRegions((self.model.width, self.model.height), (newWidth, self.model.height))
            self.model.width = newWidth
            self.refresh()
    def updateHeight(self, event):
        newHeight = int(self.uiVars.heightVar.get())
        if newHeight != self.model.height:
            self.scaleRegions((self.model.width, self.model.height), (self.model.width, newHeight))
            self.model.height = newHeight
            self.refresh()
    def scaleRegions(self, oldDimensions, newDimensions):
        oldRegions, self.model.regions = self.model.regions, []
        oldRegionToImageFile, self.model.regionToImageFile = self.model.regionToImageFile, defaultdict(lambda : None)
        oldRegionToCanvas, self.model.regionToCanvas = self.model.regionToCanvas, defaultdict(lambda : None)
        for oldRegion in oldRegions:
            newRegion = ((oldRegion[0]*newDimensions[0])//oldDimensions[0], (oldRegion[1]*newDimensions[1])//oldDimensions[1],
                         (oldRegion[2]*newDimensions[0])//oldDimensions[0], (oldRegion[3]*newDimensions[1])//oldDimensions[1])
            self.model.regions.append(newRegion)
            self.model.regionToImageFile[newRegion] = oldRegionToImageFile[oldRegion]
            self.model.regionToCanvas[newRegion] = oldRegionToCanvas[oldRegion]
    def adjustPreviewSize(self, event=None):
        print 'Ok%d %d'%(self.preview.previewContainer.winfo_width(), self.preview.previewContainer.winfo_height())
        self.refresh()

class RecentImages:
    def __init__(self, parent, controller):
        self.myParent = parent

        self.recentImagesFrame = Frame(self.myParent)
        self.recentImagesFrame.pack(side=TOP)

        self.createScrollFrame()
        
        self.clearAll = Button(self.recentImagesFrame, text='Clear', command=self.clearAll)
        self.clearAll.pack(side=RIGHT)
        
    def clearAll(self):
        for child in self.scrollFrame.winfo_children():
            child.destroy()
        self.createScrollFrame()
        
    def createScrollFrame(self):
        # THUMBNAIL_HEIGHT+2 allows for a border around the thumbnail.
        self.scrollFrame = Frame(self.recentImagesFrame, height=(THUMBNAIL_HEIGHT+2))
        self.scrollFrame.pack(side=LEFT)
    
    def addImage(self, imageFile, selectPlaceToolFunction):
        imageCell = Frame(self.scrollFrame, width=THUMBNAIL_WIDTH, height=THUMBNAIL_HEIGHT)
        imageCellCanvas = Canvas(imageCell, width=THUMBNAIL_WIDTH, height=THUMBNAIL_HEIGHT)
        imageCellCanvas.pack()
        imageFile.makeImage('thumbnail', (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), imageCellCanvas)
        imageCellCanvas.bind('<Button-1>',lambda e, c=imageCellCanvas, r=imageFile: selectPlaceToolFunction(imageFile))
        imageCell.pack(side=LEFT)

class Preview:
    def __init__(self, parent, controller):
        self.myParent = parent
        
        self.previewContainer = Frame(self.myParent)
        self.previewContainer.pack(side=TOP, fill=BOTH, expand=YES)
        self.previewContainer.bind('<Configure>', controller.adjustPreviewSize)
        
        self.createPreviewFrame(INITIAL_WIDTH, INITIAL_HEIGHT)
    def clearAndCreateFrame(self, width, height):
        self.previewFrame.destroy()
        self.createPreviewFrame(width, height)
    def createPreviewFrame(self, width, height):
        self.previewFrame = Frame(self.previewContainer, width=width, height=height)
        self.previewFrame.pack()

class Menu:
    def __init__(self, parent, controller):
        self.myParent = parent
        
        self.menuFrame = Frame(self.myParent)
        self.menuFrame.pack(side=BOTTOM)
        
        self.loadToolButton = Button(self.menuFrame, text='Load', command=lambda : controller.selectTool(Tool.LOAD))
        self.loadToolButton.pack(side=LEFT)
        
        self.swapToolButton = Button(self.menuFrame, text='Swap', command=lambda : controller.selectTool(Tool.SWAP))
        self.swapToolButton.pack(side=LEFT)
        
        self.emptyToolButton = Button(self.menuFrame, text='Empty', command=lambda : controller.selectTool(Tool.EMPTY))
        self.emptyToolButton.pack(side=LEFT)
        
        self.shuffleButton = Button(self.menuFrame, text='Shuffle', command=controller.shuffle)
        self.shuffleButton.pack(side=LEFT)
        
        self.collageAlgorithmButton = Button(self.menuFrame, text='Collage', command=lambda : controller.setAlgorithm(Algorithm.COLLAGE))
        self.collageAlgorithmButton.pack(side=LEFT)
        self.gridAlgorithmButton = Button(self.menuFrame, text='Grid', command=lambda : controller.setAlgorithm(Algorithm.GRID))
        self.gridAlgorithmButton.pack(side=LEFT)
        self.frameAlgorithmButton = Button(self.menuFrame, text='Frame', command=lambda : controller.setAlgorithm(Algorithm.FRAME))
        self.frameAlgorithmButton.pack(side=LEFT)
        
        self.widthLabel = Label(self.menuFrame, text='Width:')
        self.widthLabel.pack(side=LEFT)
        self.widthEntry = Entry(self.menuFrame, textvariable=controller.uiVars.widthVar)
        self.widthEntry.bind('<FocusOut>', controller.updateWidth)
        self.widthEntry.bind('<Return>', controller.updateWidth)
        self.widthEntry.bind('<KP_Enter>', controller.updateWidth)
        self.widthEntry.pack(side=LEFT)
        self.heightLabel = Label(self.menuFrame, text='Height:')
        self.heightLabel.pack(side=LEFT)
        self.heightEntry = Entry(self.menuFrame, textvariable=controller.uiVars.heightVar)
        self.heightEntry.bind('<FocusOut>', controller.updateHeight)
        self.heightEntry.bind('<Return>', controller.updateHeight)
        self.heightEntry.bind('<KP_Enter>', controller.updateHeight)
        self.heightEntry.pack(side=LEFT)
        
        self.minusRegionButton = Button(self.menuFrame, text='-', command=lambda : controller.addRegions(-1))
        self.minusRegionButton.pack(side=LEFT)
        self.regionsDisplay = Label(self.menuFrame, textvariable=controller.uiVars.regionsVar)
        self.regionsDisplay.pack(side=LEFT)
        self.regionsLabel = Label(self.menuFrame, text='regions')
        self.regionsLabel.pack(side=LEFT)
        self.plusRegionButton = Button(self.menuFrame, text='+', command=lambda : controller.addRegions(1))
        self.plusRegionButton.pack(side=LEFT)
        
        self.saveButton = Button(self.menuFrame, text='Save', command=controller.save)
        self.saveButton.pack(side=RIGHT)

class MyApp:
    def __init__(self, parent):
        self.config = Config()        
        
        self.myParent = parent
        screenWidth = parent.winfo_screenwidth()
        screenHeight = parent.winfo_screenheight()
        parent.geometry('%dx%d+%d+%d'%(INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT, screenWidth/2 - INITIAL_WINDOW_WIDTH/2, screenHeight/2 - INITIAL_WINDOW_HEIGHT/2))
        
        self.uiVars = UIVars(self.myParent)
        self.model = Model(self.config)
        self.controller = Controller(self.model, self.uiVars)
        
        self.appContainer = Frame(self.myParent)
        self.appContainer.pack(fill=BOTH, expand=YES)

        self.recentImages = RecentImages(self.appContainer, self.controller)
        self.preview = Preview(self.appContainer, self.controller)
        self.menu = Menu(self.appContainer, self.controller)
        
        self.controller.initialise(self.preview, self.recentImages)


root = Tk()
myapp = MyApp(root)
print "Ready to start executing the event loop."
root.mainloop()
print "Finished       executing the event loop."