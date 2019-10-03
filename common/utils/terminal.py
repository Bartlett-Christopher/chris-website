# -*- coding: utf-8 -*-
"""
:synopsis: utility class for terminal print formatting.

.. module:: common.utils.terminal
.. author:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from sys import stdout


class Terminal(object):
    """Container for common terminal features."""

    RESET = 0

    class Colour(object):
        """Terminal colours."""

        DEFAULT = 0
        BLACK = 30
        RED = 31
        GREEN = 32
        YELLOW = 33
        BLUE = 34
        PURPLE = 35
        CYAN = 36
        WHITE = 37

    class Style(object):
        """Terminal styles."""

        NONE = 0
        BOLD = 1
        UNDERLINE = 2
        NEGATIVE1 = 3
        NEGATIVE2 = 5

    class Background(object):
        """Terminal background colours."""

        BLACK = 40
        RED = 41
        GREEN = 42
        YELLOW = 43
        BLUE = 44
        PURPLE = 45
        CYAN = 46
        WHITE = 47

    @classmethod
    def format(cls, string, colour, style, background=' ', terminator='\n'):
        """
        Format a string for printing to the terminal.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style
        :type style: int (common.utils.terminal.Terminal.Style)
        :param background: the desired background
        :param terminator: the string terminator
        :type terminator: str
        :type background: int (common.utils.terminal.Terminal.Background)
        :return: the formatted string
        :rtype: str
        """
        pre = f'\033[{style};{colour};{background}m'
        post = f'\033[{cls.RESET}m'
        return f'{pre}{string}{post}{terminator}'

    @classmethod
    def standard(cls, string, colour=Colour.DEFAULT, style=Style.NONE):
        """
        Format a string for standard text.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour (default: white)
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style (default: none)
        :type style: int (common.utils.terminal.Terminal.Style)
        :return: the formatted string
        :rtype: str
        """
        return stdout.write(cls.format(
            string=string,
            colour=colour,
            style=style,
        ))

    @classmethod
    def warning(cls, string, colour=Colour.YELLOW, style=Style.NONE):
        """
        Format a string for warning text.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour (default: yellow)
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style (default: none)
        :type style: int (common.utils.terminal.Terminal.Style)
        :return: the formatted string
        :rtype: str
        """
        return stdout.write(cls.format(
            string=string,
            colour=colour,
            style=style,
        ))

    @classmethod
    def error(cls, string, colour=Colour.RED, style=Style.NONE):
        """
        Format a string for error text.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour (default: red)
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style (default: none)
        :type style: int (common.utils.terminal.Terminal.Style)
        :return: the formatted string
        :rtype: str
        """
        return stdout.write(cls.format(
            string=string,
            colour=colour,
            style=style,
        ))

    @classmethod
    def success(cls, string, colour=Colour.GREEN, style=Style.NONE):
        """
        Format a string for error text.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour (default: green)
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style (default: none)
        :type style: int (common.utils.terminal.Terminal.Style)
        :return: the formatted string
        :rtype: str
        """
        return stdout.write(cls.format(
            string=string,
            colour=colour,
            style=style,
        ))

    @classmethod
    def info(cls, string, colour=Colour.PURPLE, style=Style.NONE):
        """
        Format a string for error text.

        :param string: the string to format
        :type string: str
        :param colour: the desired colour (default: purple)
        :type colour: int (common.utils.terminal.Terminal.Colour)
        :param style: the desired style (default: none)
        :type style: int (common.utils.terminal.Terminal.Style)
        :return: the formatted string
        :rtype: str
        """
        return stdout.write(cls.format(
            string=string,
            colour=colour,
            style=style,
        ))
