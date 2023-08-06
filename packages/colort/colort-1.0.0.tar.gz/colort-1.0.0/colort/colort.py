#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


class Style(IntEnum):
    NORMAL = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    INVERT = 7
    HIDE = 8


class ForegroundColor(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    LIGHT_GRAY = 37
    DARK_GRAY = 90
    LIGHT_RED = 91
    LIGHT_GREEN = 92
    LIGHT_YELLOW = 93
    LIGHT_BLUE = 94
    LIGHT_PURPLE = 95
    LIGHT_CYAN = 96
    WHITE = 97


class BackgroundColor(IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    LIGHT_GRAY = 47
    DARK_GRAY = 100
    LIGHT_RED = 101
    LIGHT_GREEN = 102
    LIGHT_YELLOW = 103
    LIGHT_BLUE = 104
    LIGHT_PURPLE = 105
    LIGHT_CYAN = 106
    WHITE = 107


fc = ForegroundColor
bc = BackgroundColor


StyleType = Style | ForegroundColor | BackgroundColor


class Formatter:
    END = 0

    @staticmethod
    def format_with_styles(src: str, *styles: StyleType) -> str:
        styles_str = ";".join(map(str, [i.value for i in styles]))
        return f"\033[{styles_str}m{src}\033[{Formatter.END}m"


def colorize(src: str, *styles: StyleType) -> str:
    return Formatter.format_with_styles(src, *styles)
