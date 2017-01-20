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

from collections import defaultdict
from PIL import Image, ImageTk

class ImageFile:
    """A class to provide image-based methods for a given file."""
    def __init__(self, fileName):
        self.fileName = fileName
        # We need to store all the images otherwise they're garbage collected.
        self.images = defaultdict(list)

    def makeImage(self, purpose, dimensions, rotation, canvas):
        """Make a :class:`PIL.Image` and put it in the supplied canvas.
        
        :param purpose: A string describing the purpose of the image. This is
            used for both logging and also when persisting the image so that TK
            doesn't garbage collect it.
        :param dimensions: An iterable pair - (width, height).
        :param rotation: An integer between 0 and 3 for how many times the
            image should be rotated by 90 degrees.
        :param canvas: The :class:`tkinter.Canvas` where the image will be
            displayed.
        """
        image = self.getImageObject(dimensions, purpose, rotation)
        if image != None:
            photoImage = ImageTk.PhotoImage(image)
            self.images[purpose].append(photoImage)
            canvas.create_image(0, 0, image=photoImage, anchor="nw")
            canvas.config(scrollregion=canvas.bbox(TK.ALL))

    def getImageObject(self, dimensions, purpose, rotation):
        """Return a :class:`PIL.Image` with the specified dimensions.
        
        :param dimensions: An iterable pair - (width, height).
        :param purpose: A string describing the purpose of the image. This is
            used for logging.
        :param rotation: An integer between 0 and 3 for how many times the
            image should be rotated by 90 degrees.
        """
        try:
            image = Image.open(self.fileName)
        except IOError:
            print('Error opening image for {0}'.format(purpose))
            return None
        if rotation == 1:
            image = image.transpose(Image.ROTATE_90)
        elif rotation == 2:
            image = image.transpose(Image.ROTATE_180)
        elif rotation == 3:
            image = image.transpose(Image.ROTATE_270)
        originalDimensions = image.size
        if originalDimensions[0] * dimensions[1] > originalDimensions[1] * dimensions[0]:
            resizeWidth = int((originalDimensions[0] * dimensions[1]) / originalDimensions[1])
            resizeHeight = dimensions[1]
            resizeDimensions = (resizeWidth, resizeHeight)
        else:
            resizeWidth = dimensions[0]
            resizeHeight = int((originalDimensions[1] * dimensions[0]) / originalDimensions[0])
            resizeDimensions = (resizeWidth, resizeHeight)
        image = image.resize(resizeDimensions, Image.ANTIALIAS)
        middle = (image.size[0] / 2, image.size[1] / 2)
        left = middle[0] - int(dimensions[0] / 2)
        top = middle[1] - int(dimensions[1] / 2)
        box = (left, top, left + dimensions[0], top + dimensions[1])
        return image.crop(box)
