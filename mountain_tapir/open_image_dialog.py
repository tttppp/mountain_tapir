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

from __future__ import absolute_import

try:
    import tkinter as TK
except ImportError:
    import Tkinter as TK

import os
import threading
from PIL import ImageTk
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
        self.filePath = None
        self.transient(parent)
        self.parent = parent

        self.navigateBar = TK.Frame(self)
        TK.Label(self.navigateBar, text='Select a image').grid(row=0, column=0)
        self.currentDirVar = TK.StringVar(self)
        directoryEntry = TK.Entry(self.navigateBar, textvariable=self.currentDirVar, width=50)
        self.navigateBar.grid_columnconfigure(1, weight=1)
        directoryEntry.grid(row=0, column=1)
        directoryEntry.bind('<FocusOut>', self.__updateDirectory)
        directoryEntry.bind('<Return>', self.__updateDirectory)
        directoryEntry.bind('<KP_Enter>', self.__updateDirectory)
        self.navigateBar.pack()

        self.browserCanvas = TK.Canvas(self, width=750, height=550)
        self.browser = TK.Frame(self.browserCanvas)
        browserScroll = TK.Scrollbar(self, orient=TK.VERTICAL, command=self.browserCanvas.yview)
        self.browserCanvas.configure(yscrollcommand=browserScroll.set)
        browserScroll.pack(side=TK.RIGHT, fill=TK.Y)
        self.browserCanvas.pack(side=TK.LEFT, fill=TK.BOTH, expand=True)
        self.browserCanvas.create_window(1, 0, window=self.browser, anchor=TK.NW)
        self.browser.bind('<Configure>', lambda event,
                          canvas=self.browserCanvas: canvas.configure(scrollregion=canvas.bbox(TK.ALL)))

        def mouseWheelHandler(event):
            """Scrolling callback based on answers from this question:
            http://stackoverflow.com/q/17355902/171296"""
            if event.num == 5 or event.delta < 0:
                self.browserCanvas.yview_scroll(1, 'units')
            else:
                self.browserCanvas.yview_scroll(-1, 'units')
        self.browserCanvas.bind_all('<MouseWheel>', mouseWheelHandler)
        self.browserCanvas.bind_all('<Button-4>', mouseWheelHandler)
        self.browserCanvas.bind_all('<Button-5>', mouseWheelHandler)

        self.__loadThumbnails(initialDir)

        self.bind('<Escape>', self.cancel)
        self.protocol('WM_DELETE_WINDOW', self.tearDown)
        self.wait_visibility()
        self.grab_set()

    def __loadThumbnails(self, currentDir, clearCache=False):
        """Create buttons for all the files and folders in the current directory.

        :param currentDir: The current directory.
        :param clearCache: Whether to clear everything from the thumbnail cache or not."""
        if clearCache:
            OpenImageDialog.thumbnailCache = {}
        parentDirectory = currentDir.rsplit(os.sep, 1)[0]
        upDirectory = self.__createButton(self.navigateBar, 'up_directory.png',
                                          lambda dirPath=parentDirectory: self.__loadThumbnails(dirPath))
        upDirectory.config(image=upDirectory.image, width=26, height=26)
        upDirectory.grid(row=0, column=2)
        refreshDirectory = self.__createButton(self.navigateBar, 'refresh.png',
                                               lambda dirPath=currentDir: self.__loadThumbnails(dirPath, True))
        refreshDirectory.config(image=refreshDirectory.image, width=26, height=26)
        refreshDirectory.grid(row=0, column=3)

        for thumbnail in self.browser.winfo_children():
            thumbnail.destroy()
        self.browserCanvas.yview_moveto(0)
        self.currentDirVar.set(currentDir)
        index = 0
        for (_, dirNames, filenames) in os.walk(currentDir):
            for dirName in sorted(dirNames):
                dirPath = os.sep.join((currentDir, dirName))
                self.__createImageButton('directory.png',
                                         lambda dirPath=dirPath: self.__loadThumbnails(dirPath), dirName, index)
                index += 1
            imageButtonMap = OrderedDict()
            for filename in sorted(filenames):
                imagePath = os.sep.join((currentDir, filename))
                button = self.__createImageButton('file.png',
                                                  lambda imagePath=imagePath: self.ok(imagePath), filename, index)
                imageButtonMap[imagePath] = button
                index += 1
            # Load thumbnails of the actual images in the background.
            t = self.ThumbnailLoader(imageButtonMap)
            t.start()
            break

    def __createImageButton(self, resource, action, name, index):
        """Create a button with an image and a label below it.

        :param resource: The file name of the image resource.
        :param action: The action to take when clicked."""
        button = self.__createButton(self.browser, resource, action)
        button.config(text=name, image=button.image, compound='top', width=64, height=64)
        button.grid(row=index // 8, column=index % 8)
        return button

    def __createButton(self, parent, resource, action):
        button = TK.Button(parent, command=action)
        imageBinary = resource_string('mountain_tapir.resources', resource)
        button.image = ImageTk.PhotoImage(data=imageBinary)
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
            button = imageButtonPair[1]
            if not button.winfo_exists():
                # This might happen if the refresh button has been pressed, or navigation has taken place.
                return
            imagePath = imageButtonPair[0]
            if imagePath not in OpenImageDialog.thumbnailCache.keys():
                imageFile = ImageFile(imagePath)
                image = imageFile.getImageObject((64, 50), 'openDialog')
                OpenImageDialog.thumbnailCache[imagePath] = image
            image = OpenImageDialog.thumbnailCache[imagePath]
            if image is not None:
                button.image = ImageTk.PhotoImage(image)
                try:
                    button.config(image=button.image)
                except TK.TclError:
                    # This might happen if the dialog has been closed.
                    return

    def ok(self, filePath):
        """Set the path to the selected image and close the dialog."""
        self.filePath = filePath
        self.tearDown()

    def cancel(self, event):
        """Close the dialog without selecting an image."""
        self.tearDown()

    def tearDown(self):
        """Return focus to the parent, close the dialog and unbind any global events."""
        self.unbind_all('<MouseWheel>')
        self.unbind_all('<Button-4>')
        self.unbind_all('<Button-5>')
        self.parent.focus_set()
        self.destroy()
