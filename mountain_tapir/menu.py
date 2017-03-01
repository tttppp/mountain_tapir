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

from __future__ import absolute_import

try:
    import tkinter as TK
except ImportError:
    import Tkinter as TK

import os
from PIL import ImageTk

from mountain_tapir.algorithm import Algorithm
from mountain_tapir.tool import Tool


class Menu:
    def __init__(self, parent, controller):
        self.myParent = parent

        # The first row of controls.
        self.menuFrameA = TK.Frame(self.myParent)

        self.loadToolButton = TK.Button(self.menuFrameA, text='Load', command=lambda: controller.selectTool(Tool.LOAD))
        self.loadToolButton.pack(side=TK.LEFT)

        self.swapToolButton = TK.Button(self.menuFrameA, text='Swap', command=lambda: controller.selectTool(Tool.SWAP))
        self.swapToolButton.pack(side=TK.LEFT)

        self.emptyToolButton = TK.Button(self.menuFrameA, text='Empty',
                                         command=lambda: controller.selectTool(Tool.EMPTY))
        self.emptyToolButton.pack(side=TK.LEFT)

        self.rotateToolButton = TK.Button(self.menuFrameA, text='Rotate',
                                          command=lambda: controller.selectTool(Tool.ROTATE))
        self.rotateToolButton.pack(side=TK.LEFT)

        self.shuffleButton = TK.Button(self.menuFrameA, text='Shuffle', command=controller.shuffle)
        self.shuffleButton.pack(side=TK.LEFT)

        self.collageAlgorithmButton = self.__createAlgorithmButton(Algorithm.COLLAGE, 'Collage',
                                                                   'algorithm_collage.png', controller)
        self.gridAlgorithmButton = self.__createAlgorithmButton(Algorithm.GRID, 'Grid',
                                                                'algorithm_grid.png', controller)
        self.frameAlgorithmButton = self.__createAlgorithmButton(Algorithm.FRAME, 'Frame',
                                                                 'algorithm_frame.png', controller)

        # The second row of controls.
        self.menuFrameB = TK.Frame(self.myParent)

        self.widthLabel = TK.Label(self.menuFrameB, text='Width:')
        self.widthLabel.pack(side=TK.LEFT)
        self.widthEntry = TK.Entry(self.menuFrameB, textvariable=controller.uiVars.widthVar)
        self.widthEntry.bind('<FocusOut>', controller.updateWidth)
        self.widthEntry.bind('<Return>', controller.updateWidth)
        self.widthEntry.bind('<KP_Enter>', controller.updateWidth)
        self.widthEntry.pack(side=TK.LEFT)
        self.heightLabel = TK.Label(self.menuFrameB, text='Height:')
        self.heightLabel.pack(side=TK.LEFT)
        self.heightEntry = TK.Entry(self.menuFrameB, textvariable=controller.uiVars.heightVar)
        self.heightEntry.bind('<FocusOut>', controller.updateHeight)
        self.heightEntry.bind('<Return>', controller.updateHeight)
        self.heightEntry.bind('<KP_Enter>', controller.updateHeight)
        self.heightEntry.pack(side=TK.LEFT)

        self.minusRegionButton = TK.Button(self.menuFrameB, text='-', command=lambda: controller.addRegions(-1))
        self.minusRegionButton.pack(side=TK.LEFT)
        self.regionsDisplay = TK.Label(self.menuFrameB, textvariable=controller.uiVars.regionsVar)
        self.regionsDisplay.pack(side=TK.LEFT)
        self.regionsLabel = TK.Label(self.menuFrameB, text='regions')
        self.regionsLabel.pack(side=TK.LEFT)
        self.plusRegionButton = TK.Button(self.menuFrameB, text='+', command=lambda: controller.addRegions(1))
        self.plusRegionButton.pack(side=TK.LEFT)

        self.saveButton = TK.Button(self.menuFrameB, text='Save', command=controller.save)
        self.saveButton.pack(side=TK.RIGHT)

        # Pack the two rows of controls.
        self.menuFrameB.pack(side=TK.BOTTOM)
        self.menuFrameA.pack(side=TK.BOTTOM)

    def __createAlgorithmButton(self, algorithm, label, resource, controller):
        """Create a button for changing algorithm.

        :param algorithm: The algorithm to change to when clicking the button.
        :param label: TODO Display this in a tooltip.
        :param resource: The file name of the image resource.
        :param controller: The main controller for the application."""
        algorithmButton = TK.Button(self.menuFrameA, text=label,
                                    command=lambda: controller.setAlgorithm(algorithm))
        path = 'mountain_tapir' + os.sep + 'resources' + os.sep + resource
        algorithmButton.image = ImageTk.PhotoImage(file=path)
        algorithmButton.config(image=algorithmButton.image, width=26, height=26)
        algorithmButton.pack(side=TK.LEFT)
        return algorithmButton
