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

"""
test_config
----------------------------------

Tests for `config` module.
"""

import unittest
import mock

from mountain_tapir import config

class TestConfig(unittest.TestCase):
    @mock.patch('mountain_tapir.config.configparser')
    def testPropertiesFileLoaded(self, mockConfigparser):
        """Test that the properties file is loaded when the Config is initialised."""
        mockRawConfigParser = mock.Mock(name = "RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        
        config.Config()
        
        mockRawConfigParser.read.assert_called_with('mountain_tapir.properties')

    @mock.patch('mountain_tapir.config.configparser')
    def testGetLoadsValue(self, mockConfigparser):
        """Test that loading a property returns the value from the config object."""
        mockRawConfigParser = mock.Mock(name = "RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockRawConfigParser.get.return_value = 'value'
        
        value = config.Config().get('section', 'key', 'default')
        
        mockRawConfigParser.get.assert_called_with('section', 'key')
        assert value == 'value'

    @mock.patch('mountain_tapir.config.configparser')
    def testGetCanReturnDefault(self, mockConfigparser):
        """Test that the default value is returned if the key is not found."""
        mockRawConfigParser = mock.Mock(name = "RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        class GetException(Exception):
            pass
        mockConfigparser.NoSectionError = GetException
        mockRawConfigParser.get.side_effect = GetException
        
        value = config.Config().get('section', 'key', 'default')
        
        mockRawConfigParser.get.assert_called_with('section', 'key')
        assert value == 'default'

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
