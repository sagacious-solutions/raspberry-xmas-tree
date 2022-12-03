"""Defines many preset colors for the LED Light string as well as having a couple
    functions to define new colors.
"""

from typing import List
import random

from rpi_ws281x import Color


class LedColor:
    # All colors provided in GRB format instead of RGB
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    warmWhite = Color(45, 180, 10)
    autumnOrange = Color(35, 180, 0)
    lightOrange = Color(45, 180, 0)
    blue = Color(0, 0, 255)
    green = Color(255, 0, 0)
    red = Color(0, 255, 0)
    teal = new = Color(92, 0, 255)
    purple = Color(10, 30, 80)
    brightPurple = Color(10, 180, 255)
    darkPurple = Color(10, 92, 190)
    yellow = Color(150, 255, 0)
    fallYellow = Color(100, 255, 0)
    pink = Color(50, 255, 100)
    brightViolet = Color(10, 255, 100)

    def rgb(rgb: List[int]):
        # The ws281x library takes color in GRB format. This corrects that.
        return Color(rgb[1], rgb[0], rgb[2])

    def get_random():
        colors = [
            value
            for key, value in LedColor.__dict__.items()
            if type(value) == int
        ]
        index = round(random.random() * len(colors)) - 1

        return colors[index]
