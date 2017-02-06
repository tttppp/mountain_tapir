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
    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testPropertiesFileLoaded(self, mockConfigparser, mockOs):
        """Test that the properties file is loaded when the Config is initialised."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockOs.path.expanduser.return_value = 'HOME'
        mockOs.path.join.side_effect = ['HOME/.mountain_tapir', 'HOME/.mountain_tapir/mountain_tapir.properties']
        mockRawConfigParser.read.return_value = ['HOME/.mountain_tapir/mountain_tapir.properties']

        c = config.Config()

        expectedList = ['mountain_tapir.properties', 'HOME/.mountain_tapir/mountain_tapir.properties']
        mockRawConfigParser.read.assert_called_with(expectedList)
        self.assertEqual('HOME/.mountain_tapir/mountain_tapir.properties', c.persistFile)

    @mock.patch('mountain_tapir.config.open')
    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testPropertiesFileCreated(self, mockConfigparser, mockOs, mockOpen):
        """Test that a properties file is created if one couldn't be loaded."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockOs.path.expanduser.return_value = 'HOME'
        mockOs.path.join.side_effect = ['HOME/.mountain_tapir', 'HOME/.mountain_tapir/mountain_tapir.properties']
        mockRawConfigParser.read.return_value = []
        mockFile = mockOpen.return_value = mock.Mock(name='mockFile')

        config.Config()

        mockOpen.assert_called_with('HOME/.mountain_tapir/mountain_tapir.properties', 'a')
        mockFile.close.assert_called_with()

    @mock.patch('mountain_tapir.config.open')
    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testFileCreationErrorSwallowed(self, mockConfigparser, mockOs, mockOpen):
        """Test that if a properties file can't be created the method doesn't throw an exception."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockOs.path.expanduser.return_value = 'HOME'
        mockOs.path.join.side_effect = ['HOME/.mountain_tapir', 'HOME/.mountain_tapir/mountain_tapir.properties']
        mockRawConfigParser.read.return_value = []
        mockOpen.side_effect = OSError()

        c = config.Config()

        mockOpen.assert_called_with('HOME/.mountain_tapir/mountain_tapir.properties', 'a')
        # ...and no exception is seen
        self.assertEqual(None, c.persistFile, msg='Expected the persist file to be set to None.')

    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testGetLoadsValue(self, mockConfigparser, mockOs):
        """Test that loading a property returns the value from the config object."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockRawConfigParser.get.return_value = 'value'
        mockRawConfigParser.read.return_value = ['HOME/.mountain_tapir/mountain_tapir.properties']

        value = config.Config().get('section', 'key', 'default')

        mockRawConfigParser.get.assert_called_with('section', 'key')
        assert value == 'value'

    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testGetCanReturnDefault(self, mockConfigparser, mockOs):
        """Test that the default value is returned if the key is not found."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser

        class GetException(Exception):
            pass
        mockConfigparser.NoSectionError = GetException
        mockConfigparser.NoOptionError = GetException
        mockRawConfigParser.get.side_effect = GetException
        mockRawConfigParser.read.return_value = ['HOME/.mountain_tapir/mountain_tapir.properties']

        value = config.Config().get('section', 'key', 'default')

        mockRawConfigParser.get.assert_called_with('section', 'key')
        assert value == 'default'

    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testGetInt(self, mockConfigparser, mockOs):
        """Test that loading an integer property works."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockRawConfigParser.getint.return_value = 123
        mockRawConfigParser.read.return_value = ['HOME/.mountain_tapir/mountain_tapir.properties']

        value = config.Config().get('section', 'key', 'default', 'int')

        mockRawConfigParser.getint.assert_called_with('section', 'key')
        self.assertEqual(value, 123, msg='Unexpected value returned from get.')

    @mock.patch('mountain_tapir.config.os')
    @mock.patch('mountain_tapir.config.configparser')
    def testGetBoolean(self, mockConfigparser, mockOs):
        """Test that loading a boolean property works."""
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockConfigparser.RawConfigParser.return_value = mockRawConfigParser
        mockRawConfigParser.getboolean.return_value = True
        mockRawConfigParser.read.return_value = ['HOME/.mountain_tapir/mountain_tapir.properties']

        value = config.Config().get('section', 'key', 'default', 'boolean')

        mockRawConfigParser.getboolean.assert_called_with('section', 'key')
        self.assertEqual(value, True, msg='Unexpected value returned from get.')

    @mock.patch('mountain_tapir.config.open')
    def testUpdateConfig(self, mockOpen):
        """Test updating a config value."""
        c = config.Config()
        c.persistFile = 'path/to/file'
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockRawConfigParser.has_section.return_value = False
        c.config = mockRawConfigParser
        mockOutFile = mockOpen.return_value = mock.MagicMock(name='outFile')

        c.update('section', 'key', 'newValue')

        mockRawConfigParser.add_section.assert_called_with('section')
        mockRawConfigParser.set.assert_called_with('section', 'key', 'newValue')
        # Check the config is written to the file.
        mockRawConfigParser.write.assert_called_with(mockOutFile.__enter__())
        assert mock.call('path/to/file', 'w') in mockOpen.mock_calls

    @mock.patch('mountain_tapir.config.open')
    def testUpdateCouldntWriteFile(self, mockOpen):
        """Test that the application doesn't crash if it can't write to the config file."""
        c = config.Config()
        c.persistFile = 'path/to/file'
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockRawConfigParser.has_section.return_value = True
        c.config = mockRawConfigParser
        mockRawConfigParser.write.side_effect = OSError()

        c.update('section', 'key', 'newValue')

        mockRawConfigParser.set.assert_called_with('section', 'key', 'newValue')
        # Note that there were no exceptions thrown by the method.

    @mock.patch('mountain_tapir.config.open')
    def testNoWriteIfNoPersistFile(self, mockOpen):
        """Test that we don't try to write to a file if persistFile isn't set."""
        c = config.Config()
        c.persistFile = None
        mockRawConfigParser = mock.Mock(name="RawConfigParser")
        mockRawConfigParser.has_section.return_value = True
        c.config = mockRawConfigParser

        c.update('section', 'key', 'newValue')

        mockRawConfigParser.set.assert_called_with('section', 'key', 'newValue')
        # On Travis mockOpen is called, but I'm not sure why. Here we check that it wasn't
        # called to write a file.
        for call in mockOpen.mock_calls:
            if len(call) > 1 and len(call[1]) > 1:
                self.assertFalse(call[1][1] == 'w', msg='Unexpected attempt to write to a file.')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
