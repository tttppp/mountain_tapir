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
        image = self.__getImageObject(imagePath, (64, 50), 'openDialog')
        if image is not None:
            button.image = ImageTk.PhotoImage(image)
            button.config(text=imageName, image=button.image, compound='top', width=64, height=64)
            button.grid(row=index//8, column=index%8)
        else:
            self.__createNonImageButton('file.png', None, imageName, index)
        return button

    def __getImageObject(self, fileName, dimensions, purpose):
        """Return a :class:`PIL.Image` with the specified dimensions.

        :param dimensions: An iterable pair - (width, height).
        :param purpose: A string describing the purpose of the image. This is
            used for logging.
        """
        try:
            image = Image.open(fileName)
        except IOError:
            print('Error opening image for {0}'.format(purpose))
            return None
        originalDimensions = image.size
        if originalDimensions[0] * dimensions[1] > originalDimensions[1] * dimensions[0]:
            resizeWidth = int((originalDimensions[0] * dimensions[1]) // originalDimensions[1])
            resizeHeight = dimensions[1]
            resizeDimensions = (resizeWidth, resizeHeight)
        else:
            resizeWidth = dimensions[0]
            resizeHeight = int((originalDimensions[1] * dimensions[0]) // originalDimensions[0])
            resizeDimensions = (resizeWidth, resizeHeight)
        image = image.resize(resizeDimensions, Image.ANTIALIAS)
        middle = (image.size[0] // 2, image.size[1] // 2)
        left = middle[0] - int(dimensions[0] // 2)
        top = middle[1] - int(dimensions[1] // 2)
        box = (left, top, left + dimensions[0], top + dimensions[1])
        return image.crop(box)

    def ok(self, filePath):
        print('value is', filePath)
        self.filePath = filePath
        self.parent.focus_set()
        self.destroy()

    def cancel(self, event):
        self.parent.focus_set()
        self.destroy()