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
    import configparser
except ImportError:
    import ConfigParser as configparser

class Config:
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read('mountain_tapir.properties')
    def get(self, section, key, default = None):
        try:
            value = self.config.get(section, key)
        except configparser.NoSectionError:
            value = default
        if value == None:
            value = default
        return value