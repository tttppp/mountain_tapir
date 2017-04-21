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
import threading
from PIL import Image, ImageTk
from pkg_resources import resource_string
# TODO: Refactor code to allow use of multiple processes rather than threads.
from multiprocessing.dummy import Pool
from collections import OrderedDict

from mountain_tapir.image_file import ImageFile

class OpenImageDialog(TK.Toplevel):
    """A static map from imagePath to thumbnail."""
    thumbnailCache = {}

    def __init__(self, parent, initialDir):
        TK.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.parent = parent
        TK.Label(self, text='Select a image').pack()

        self.navigateBar = TK.Frame(self)
        self.currentDirVar = TK.StringVar(self)
        directoryEntry = TK.Entry(self.navigateBar, textvariable=self.currentDirVar)
        directoryEntry.grid(row=0, column=0)
        directoryEntry.bind('<FocusOut>', self.__updateDirectory)
        directoryEntry.bind('<Return>', self.__updateDirectory)
        directoryEntry.bind('<KP_Enter>', self.__updateDirectory)
        self.navigateBar.pack()

        self.browser = TK.Frame(self)
        self.__loadThumbnails(initialDir)
        self.browser.pack(side=TK.TOP, fill=TK.X)

        #self.initial_focus = TK.Button(self, text='OK', command=self.ok).pack()
        self.bind('<Escape>', self.cancel)
        self.wait_visibility()
        self.grab_set()

    def __loadThumbnails(self, currentDir):
        parentDirectory = currentDir.rsplit(os.sep, 1)[0]
        upDirectory = self.__createButton(self.navigateBar, 'up_directory.png', lambda dirPath=parentDirectory: self.__loadThumbnails(dirPath))
        upDirectory.config(image=upDirectory.image, width=26, height=26)
        upDirectory.grid(row=0, column=1)

        for thumbnail in self.browser.winfo_children():
            thumbnail.destroy()
        self.currentDirVar.set(currentDir)
        index = 0
        for (_, dirNames, filenames) in os.walk(currentDir):
            for dirName in sorted(dirNames):
                dirPath = os.sep.join((currentDir, dirName))
                self.__createNonImageButton('directory.png', lambda dirPath=dirPath: self.__loadThumbnails(dirPath), dirName, index)
                index += 1
            imageButtonMap = OrderedDict()
            for filename in sorted(filenames):
                imagePath = os.sep.join((currentDir, filename))
                button = self.__createNonImageButton('file.png', lambda imagePath=imagePath: self.ok(imagePath), filename, index)
                imageButtonMap[imagePath] = button
                index += 1
            t = self.ThumbnailLoader(imageButtonMap)
            t.start()
            break

    def __createNonImageButton(self, resource, action, name, index):
        """Create a button with an image and a label below it.

        :param resource: The file name of the image resource.
        :param action: The action to take when clicked."""
        button = self.__createButton(self.browser, resource, action)
        button.config(text=name, image=button.image, compound='top', width=64, height=64)
        button.grid(row=index//8, column=index%8)
        return button

    def __createButton(self, parent, resource, action):
        button = TK.Button(parent, command=action)
        imageBinary = resource_string('mountain_tapir.resources', resource)
        button.image = ImageTk.PhotoImage(data = imageBinary)
        return button

    def __updateDirectory(self, event):
        self.__loadThumbnails(self.currentDirVar.get())

    class ThumbnailLoader(threading.Thread):
        """A class to load the thumbnails and display them on the buttons."""
        def __init__(self, imageButtonMap):
            """:param imageButtonMap: A map from the image path to the button to display it on."""
            threading.Thread.__init__(self)
            self.imageButtonMap = imageButtonMap

        def run(self):
            """Start the background thread."""
            pool = Pool()
            pool.map(self.setThumbnail, self.imageButtonMap.items())

        def setThumbnail(self, imageButtonPair):
            """Try to load the image from the path and display it on the button.

            :param imageButtonPair: A pair containing an image path and a button."""
            imagePath = imageButtonPair[0]
            if imagePath not in OpenImageDialog.thumbnailCache.keys():
                imageFile = ImageFile(imagePath)
                image = imageFile.getImageObject((64, 50), 'openDialog')
                OpenImageDialog.thumbnailCache[imagePath] = image
            image = OpenImageDialog.thumbnailCache[imagePath]
            if image is not None:
                button = imageButtonPair[1]
                button.image = ImageTk.PhotoImage(image)
                button.config(image=button.image)

    def ok(self, filePath):
        print('value is', filePath)
        self.filePath = filePath
        self.parent.focus_set()
        self.destroy()

    def cancel(self, event):
        self.parent.focus_set()
        self.destroy()
