# -*- coding: utf-8 -*-
#
# Mountain Tapir Collage Maker is a tool for combining images into collages.
# Copyright (c) 2017, tttppp
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

import os
from PIL import Image, ImageTk
from pkg_resources import resource_string

from mountain_tapir.image_file import ImageFile

class OpenImageDialog(TK.Toplevel):
    def __init__(self, parent, initialDir):
        TK.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.parent = parent
        TK.Label(self, text='Select a image').pack()

        self.browser = TK.Frame(self)
        self.__loadThumbnails(initialDir)
        self.browser.pack(side=TK.TOP, fill=TK.X)

        #self.initial_focus = TK.Button(self, text='OK', command=self.ok).pack()
        self.bind('<Escape>', self.cancel)
        self.wait_visibility()
        self.grab_set()

    def __loadThumbnails(self, currentDir):
        print(currentDir)
        index = 0
        for (_, dirNames, filenames) in os.walk(currentDir):
            print(dirNames)
            print(filenames)
            for dirName in dirNames:
                dirPath = os.sep.join((currentDir, dirName))
                self.__createNonImageButton('directory.png', lambda dirPath=dirPath: self.__loadThumbnails(dirPath), dirName, index)
                index += 1
            for filename in filenames:
                imagePath = os.sep.join((currentDir, filename))
                self.__createImageButton(imagePath, lambda imagePath=imagePath: self.ok(imagePath), filename, index)
                index += 1
            break

    def __createNonImageButton(self, resource, action, name, index):
        """Create a button for changing algorithm.

        :param resource: The file name of the image resource.
        :param action: The action to take when clicked."""
        button = TK.Button(self.browser, command=action)
        imageBinary = resource_string('mountain_tapir.resources', resource)
        button.image = ImageTk.PhotoImage(data = imageBinary)
        button.config(text=name, image=button.image, compound='top', width=64, height=64)
        button.grid(row=index//8, column=index%8)
        return button

    def __createImageButton(self, imagePath, action, imageName, index):
        """Create a button for changing algorithm.

        :param resource: The file name of the image resource.
        :param action: The action to take when clicked."""
        button = TK.Button(self.browser, command=action)
        imageFile = ImageFile(imagePath)
        image = imageFile.getImageObject((64, 50), 'openDialog')
        if image is not None:
            button.image = ImageTk.PhotoImage(image)
            button.config(text=imageName, image=button.image, compound='top', width=64, height=64)
            button.grid(row=index//8, column=index%8)
        else:
            self.__createNonImageButton('file.png', None, imageName, index)
        return button

    def ok(self, filePath):
        print('value is', filePath)
        self.filePath = filePath
        self.parent.focus_set()
        self.destroy()

    def cancel(self, event):
        self.parent.focus_set()
        self.destroy()