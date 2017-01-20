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

from algorithm import Algorithm
from constants import Constants
from tool import Tool

class Model:
    def __init__(self, config):
        self.selectedTool = Tool.LOAD
        self.regionCount = Constants.INITIAL_REGIONS
        self.width = Constants.INITIAL_WIDTH
        self.height = Constants.INITIAL_HEIGHT
        self.algorithm = Algorithm.COLLAGE
        self.regions = None
        self.imageFiles = []
        self.regionToImageFile = defaultdict(lambda : None)
        self.regionToCanvas = defaultdict(lambda : None)
        self.currentDirectory = config.get('FILE', 'initialdirectory', '/')
