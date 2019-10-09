# -*- coding: utf-8 -*-
"""
  :synopsis: unit tests suite for the Terminal class.

.. module:: common.tests.utils.test_terminal
.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from unittest.mock import patch

from django.test import TestCase

from common.utils.terminal import Terminal


class TestTerminal(TestCase):
    """Unit test class for Terminal."""

    @classmethod
    def setUpClass(cls):
        super(TestTerminal, cls).setUpClass()
        cls.terminal = Terminal()
        cls.string = 'hello, world'
        cls.colour = Terminal.Colour.GREEN
        cls.style = Terminal.Style.BOLD

    def test_format(self):
        """Test format method using argument defaults."""
        formatted_string = Terminal.format(
            self.string,
            self.colour,
            self.style
        )

        self.assertEqual(
            formatted_string,
            f'\033[{self.style};{self.colour}; m'
            f'{self.string}\33[{Terminal.RESET}m\n'
        )

    @patch('common.utils.terminal.stdout.write')
    def test_standard(self, mock_stdout):
        """Test standard method using argument defaults."""
        with patch.object(Terminal, 'format') as mock_format:
            mock_format.return_value = 'formatted_string'
            Terminal.standard(self.string)

        mock_format.assert_called_once_with(
            string=self.string,
            colour=Terminal.Colour.DEFAULT,
            style=Terminal.Style.NONE
        )
        mock_stdout.assert_called_once_with(mock_format.return_value)

    @patch('common.utils.terminal.stdout.write')
    def test_warning(self, mock_stdout):
        """Test warning method using argument defaults."""
        with patch.object(Terminal, 'format') as mock_format:
            mock_format.return_value = 'formatted_string'
            Terminal.warning(self.string)

        mock_format.assert_called_once_with(
            string=self.string,
            colour=Terminal.Colour.YELLOW,
            style=Terminal.Style.NONE
        )
        mock_stdout.assert_called_once_with(mock_format.return_value)

    @patch('common.utils.terminal.stdout.write')
    def test_error(self, mock_stdout):
        """Test error method using argument defaults."""
        with patch.object(Terminal, 'format') as mock_format:
            mock_format.return_value = 'formatted_string'
            Terminal.error(self.string)

        mock_format.assert_called_once_with(
            string=self.string,
            colour=Terminal.Colour.RED,
            style=Terminal.Style.NONE
        )
        mock_stdout.assert_called_once_with(mock_format.return_value)

    @patch('common.utils.terminal.stdout.write')
    def test_sucess(self, mock_stdout):
        """Test success method using argument defaults."""
        with patch.object(Terminal, 'format') as mock_format:
            mock_format.return_value = 'formatted_string'
            Terminal.success(self.string)

        mock_format.assert_called_once_with(
            string=self.string,
            colour=Terminal.Colour.GREEN,
            style=Terminal.Style.NONE
        )
        mock_stdout.assert_called_once_with(mock_format.return_value)

    @patch('common.utils.terminal.stdout.write')
    def test_info(self, mock_stdout):
        """Test info method using argument defaults."""
        with patch.object(Terminal, 'format') as mock_format:
            mock_format.return_value = 'formatted_string'
            Terminal.info(self.string)

        mock_format.assert_called_once_with(
            string=self.string,
            colour=Terminal.Colour.PURPLE,
            style=Terminal.Style.NONE
        )
        mock_stdout.assert_called_once_with(mock_format.return_value)
