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

from constants import *

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
