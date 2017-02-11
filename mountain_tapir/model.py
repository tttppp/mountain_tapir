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

from collections import defaultdict
import os

from .algorithm import Algorithm
from .constants import Constants
from .tool import Tool


class Model:
    def __init__(self, config):
        self.config = config
        self.selectedTool = Tool.LOAD
        self.__regionCount = config.get('COLLAGE', 'regionCount', Constants.INITIAL_REGIONS, 'int')
        self.__width = config.get('COLLAGE', 'width', Constants.INITIAL_WIDTH, 'int')
        self.__height = config.get('COLLAGE', 'height', Constants.INITIAL_HEIGHT, 'int')
        self.__algorithm = config.get('COLLAGE', 'algorithm', Algorithm.COLLAGE, 'int')
        self.__regions = None
        self.imageFiles = []
        self.regionToImageFile = defaultdict(lambda: None)
        self.regionToCanvas = defaultdict(lambda: None)
        self.__currentDirectory = config.get('FILE', 'initialdirectory', os.path.expanduser('~'))

    def setCurrentDirectory(self, currentDirectory):
        """Set the directory to start looking for images in."""
        self.__currentDirectory = currentDirectory
        self.config.update('FILE', 'initialdirectory', currentDirectory)

    def getCurrentDirectory(self):
        """Get the directory to start looking for images in."""
        return self.__currentDirectory

    def setWidth(self, width):
        """Set the width of the output collage."""
        self.__width = width
        self.config.update('COLLAGE', 'width', width)

    def getWidth(self):
        """Get the width of the output collage."""
        return self.__width

    def setHeight(self, height):
        """Set the height of the output collage."""
        self.__height = height
        self.config.update('COLLAGE', 'height', height)

    def getHeight(self):
        """Get the height of the output collage."""
        return self.__height

    def setAlgorithm(self, algorithm):
        """Set the algorithm used to generate the collage."""
        self.__algorithm = algorithm
        self.config.update('COLLAGE', 'algorithm', algorithm)

    def getAlgorithm(self):
        """Get the algorithm used to generate the collage."""
        return self.__algorithm

    def setRegionCount(self, regionCount):
        """Set the number of regions in the collage."""
        self.__regionCount = regionCount
        self.config.update('COLLAGE', 'regionCount', regionCount)

    def getRegionCount(self):
        """Get the number of regions in the collage."""
        return self.__regionCount

    def setRegions(self, regions):
        """Set the regions in the collage."""
        self.__regions = regions
        self.setRegionCount(len(regions))

    def getRegions(self):
        """Get the regions in the collage."""
        return self.__regions
