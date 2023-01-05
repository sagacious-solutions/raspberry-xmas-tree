"""Defines many preset colors for the LED Light string as well as having a couple
    functions to define new colors.
"""

from typing import List
import random

from rpi_ws281x import Color


class LedColor:
    white = Color(255, 255, 255)
    warmWhite = Color(180, 45, 10)
    autumnOrange = Color(180, 35, 0)
    lightOrange = Color(180, 45, 0)
    blue = Color(0, 0, 255)
    green = Color(0, 255, 0)
    red = Color(255, 0, 0)
    teal = Color(0, 92, 255)
    purple = Color(30, 10, 80)
    brightPurple = Color(180, 10, 255)
    darkPurple = Color(92, 10, 190)
    yellow = Color(255, 150, 0)
    fallYellow = Color(255, 100, 0)
    pink = Color(255, 50, 100)
    brightViolet = Color(255, 10, 100)

    def rgb(rgb: List[int]):
        return Color(rgb[0], rgb[1], rgb[2])

    def get_random():
        colors = [
            value
            for key, value in LedColor.__dict__.items()
            if type(value) == int
        ]
        index = round(random.random() * len(colors)) - 1

        return colors[index]

    def interpolate_rgb(
        c1: List[int], c2: List[int], amount: float
    ) -> List[int]:
        """Given 2 colors and a value between 0-1, it will give you back a color thats
            between the 2 values by that percentage of 1

        Args:
            c1 (List[int]): Color transitioning from
            c2 (List[int]): Color transitioning to
            amount (float): What percentage of change between the two

        Returns:
            List[int]: New interpolated color
        """
        dif_r = c2[0] - c1[0]
        dif_g = c2[1] - c1[1]
        dif_b = c2[2] - c1[2]

        new_r = c1[0] + round(dif_r * amount)
        new_g = c1[1] + round(dif_g * amount)
        new_b = c1[2] + round(dif_b * amount)

        return [new_r, new_g, new_b]
