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

from config import Config
from controller import Controller
from menu import Menu
from model import Model
from preview import Preview
from recent_images import RecentImages
from ui_vars import UIVars

INITIAL_WINDOW_WIDTH = 1060
INITIAL_WINDOW_HEIGHT = 500

class MountainTapir:
    def __init__(self, parent):
        self.config = Config()        
        
        self.myParent = parent
        screenWidth = parent.winfo_screenwidth()
        screenHeight = parent.winfo_screenheight()
        parent.geometry('{0:d}x{1:d}+{2:d}+{3:d}'.format(INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT, int(screenWidth/2 - INITIAL_WINDOW_WIDTH/2), int(screenHeight/2 - INITIAL_WINDOW_HEIGHT/2)))
        
        self.uiVars = UIVars(self.myParent)
        self.model = Model(self.config)
        self.controller = Controller(self.model, self.uiVars)
        
        self.appContainer = TK.Frame(self.myParent)
        self.appContainer.pack(fill=TK.BOTH, expand=TK.YES)

        self.recentImages = RecentImages(self.appContainer, self.controller)
        self.preview = Preview(self.appContainer, self.controller)
        self.menu = Menu(self.appContainer, self.controller)
        
        self.controller.initialise(self.preview, self.recentImages)

if __name__ == '__main__':
    root = TK.Tk()
    MountainTapir(root)
    root.mainloop()
