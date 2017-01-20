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

THUMBNAIL_WIDTH = 60
THUMBNAIL_HEIGHT = 60

class RecentImages:
    def __init__(self, parent, controller):
        self.myParent = parent

        self.recentImagesFrame = TK.Frame(self.myParent)
        self.recentImagesFrame.pack(side=TK.TOP)

        self.createScrollFrame()
        
        self.clearAllButton = TK.Button(self.recentImagesFrame, text='Clear', command=self.clearAll)
        self.clearAllButton.pack(side=TK.RIGHT)
        
    def clearAll(self):
        for child in self.scrollFrame.winfo_children():
            child.destroy()
        self.createScrollFrame()
        
    def createScrollFrame(self):
        # THUMBNAIL_HEIGHT+2 allows for a border around the thumbnail.
        self.scrollFrame = TK.Frame(self.recentImagesFrame, height=(THUMBNAIL_HEIGHT+2))
        self.scrollFrame.pack(side=TK.LEFT)
    
    def addImage(self, imageFile, selectPlaceToolFunction):
        imageCell = TK.Frame(self.scrollFrame, width=THUMBNAIL_WIDTH, height=THUMBNAIL_HEIGHT)
        imageCellCanvas = TK.Canvas(imageCell, width=THUMBNAIL_WIDTH, height=THUMBNAIL_HEIGHT)
        imageCellCanvas.pack()
        imageFile.makeImage('thumbnail', (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), imageCellCanvas)
        imageCellCanvas.bind('<Button-1>',lambda e, c=imageCellCanvas, r=imageFile: selectPlaceToolFunction(imageFile))
        imageCell.pack(side=TK.LEFT)
