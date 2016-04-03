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

from constants import Constants

class Preview:
    def __init__(self, parent, controller):
        self.myParent = parent
        
        self.previewContainer = TK.Frame(self.myParent)
        self.previewContainer.pack(side=TK.TOP, fill=TK.BOTH, expand=TK.YES)
        self.previewContainer.bind('<Configure>', controller.adjustPreviewSize)
        
        self.createPreviewFrame(Constants.INITIAL_WIDTH, Constants.INITIAL_HEIGHT)

    def clearAndCreateFrame(self, width, height):
        """Clear the preview frame, then create a new one using the given dimensions.
        
        :param width: The width of the new frame.
        :param height: The height of the new frame.
        """
        self.previewFrame.destroy()
        self.createPreviewFrame(width, height)

    def createPreviewFrame(self, width, height):
        """Create the preview frame using the given dimensions.
        
        :param width: The width of the new frame.
        :param height: The height of the new frame.
        """
        self.previewFrame = TK.Frame(self.previewContainer, width=width, height=height)
        self.previewFrame.pack()
