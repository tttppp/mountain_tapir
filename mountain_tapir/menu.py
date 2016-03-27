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

from algorithm import Algorithm
from tool import Tool

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
