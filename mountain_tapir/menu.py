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

from algorithm import Algorithm
from tool import Tool

class Menu:
    def __init__(self, parent, controller):
        self.myParent = parent
        
        self.menuFrame = TK.Frame(self.myParent)
        self.menuFrame.pack(side=TK.BOTTOM)
        
        self.loadToolButton = TK.Button(self.menuFrame, text='Load', command=lambda : controller.selectTool(Tool.LOAD))
        self.loadToolButton.pack(side=TK.LEFT)
        
        self.swapToolButton = TK.Button(self.menuFrame, text='Swap', command=lambda : controller.selectTool(Tool.SWAP))
        self.swapToolButton.pack(side=TK.LEFT)
        
        self.emptyToolButton = TK.Button(self.menuFrame, text='Empty', command=lambda : controller.selectTool(Tool.EMPTY))
        self.emptyToolButton.pack(side=TK.LEFT)
        
        self.shuffleButton = TK.Button(self.menuFrame, text='Shuffle', command=controller.shuffle)
        self.shuffleButton.pack(side=TK.LEFT)
        
        self.collageAlgorithmButton = TK.Button(self.menuFrame, text='Collage', command=lambda : controller.setAlgorithm(Algorithm.COLLAGE))
        self.collageAlgorithmButton.pack(side=TK.LEFT)
        self.gridAlgorithmButton = TK.Button(self.menuFrame, text='Grid', command=lambda : controller.setAlgorithm(Algorithm.GRID))
        self.gridAlgorithmButton.pack(side=TK.LEFT)
        self.frameAlgorithmButton = TK.Button(self.menuFrame, text='Frame', command=lambda : controller.setAlgorithm(Algorithm.FRAME))
        self.frameAlgorithmButton.pack(side=TK.LEFT)
        
        self.widthLabel = TK.Label(self.menuFrame, text='Width:')
        self.widthLabel.pack(side=TK.LEFT)
        self.widthEntry = TK.Entry(self.menuFrame, textvariable=controller.uiVars.widthVar)
        self.widthEntry.bind('<FocusOut>', controller.updateWidth)
        self.widthEntry.bind('<Return>', controller.updateWidth)
        self.widthEntry.bind('<KP_Enter>', controller.updateWidth)
        self.widthEntry.pack(side=TK.LEFT)
        self.heightLabel = TK.Label(self.menuFrame, text='Height:')
        self.heightLabel.pack(side=TK.LEFT)
        self.heightEntry = TK.Entry(self.menuFrame, textvariable=controller.uiVars.heightVar)
        self.heightEntry.bind('<FocusOut>', controller.updateHeight)
        self.heightEntry.bind('<Return>', controller.updateHeight)
        self.heightEntry.bind('<KP_Enter>', controller.updateHeight)
        self.heightEntry.pack(side=TK.LEFT)
        
        self.minusRegionButton = TK.Button(self.menuFrame, text='-', command=lambda : controller.addRegions(-1))
        self.minusRegionButton.pack(side=TK.LEFT)
        self.regionsDisplay = TK.Label(self.menuFrame, textvariable=controller.uiVars.regionsVar)
        self.regionsDisplay.pack(side=TK.LEFT)
        self.regionsLabel = TK.Label(self.menuFrame, text='regions')
        self.regionsLabel.pack(side=TK.LEFT)
        self.plusRegionButton = TK.Button(self.menuFrame, text='+', command=lambda : controller.addRegions(1))
        self.plusRegionButton.pack(side=TK.LEFT)
        
        self.saveButton = TK.Button(self.menuFrame, text='Save', command=controller.save)
        self.saveButton.pack(side=TK.RIGHT)
