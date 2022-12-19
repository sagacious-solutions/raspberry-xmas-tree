"""Defines many preset colors for the LED Light string as well as having a couple
    functions to define new colors.
"""

from typing import List, Dict
import random

from rpi_ws281x import Color


class LedColor:
    # All colors provided in GRB format instead of RGB
    # black = Color(0, 0, 0)
    # white = Color(255, 255, 255)
    # warmWhite = Color(45, 180, 10)
    # autumnOrange = Color(35, 180, 0)
    # lightOrange = Color(45, 180, 0)
    # blue = Color(0, 0, 255)
    # green = Color(255, 0, 0)
    # red = Color(0, 255, 0)
    # teal = new = Color(92, 0, 255)
    # purple = Color(10, 30, 80)
    # brightPurple = Color(10, 180, 255)
    # darkPurple = Color(10, 92, 190)
    # yellow = Color(150, 255, 0)
    # fallYellow = Color(100, 255, 0)
    # pink = Color(50, 255, 100)
    # brightViolet = Color(10, 255, 100)
    # ------------------------

    black = {"r": 0, "g": 0, "b": 0}
    white = {"r": 255, "g": 255, "b": 255}
    warmWhite = {"g": 45, "r": 180, "b": 10}
    autumnOrange = {"g": 35, "r": 180, "b": 0}
    lightOrange = {"g": 45, "r": 180, "b": 0}
    blue = {"g": 0, "r": 0, "b": 255}
    green = {"g": 255, "r": 0, "b": 0}
    red = {"g": 0, "r": 255, "b": 0}
    teal = {"g": 92, "r": 0, "b": 255}
    purple = {"g": 10, "r": 30, "b": 80}
    brightPurple = {"g": 10, "r": 180, "b": 255}
    darkPurple = {"g": 10, "r": 92, "b": 190}
    yellow = {"g": 150, "r": 255, "b": 0}
    fallYellow = {"g": 100, "r": 255, "b": 0}
    pink = {"g": 50, "r": 255, "b": 100}
    brightViolet = {"g": 10, "r": 255, "b": 100}

    def brg(color: Dict[str, int]):
        return Color(color.get("b"), color.get("r"), color.get("g"))

    def grb(color: Dict[str, int]):
        return Color(color.get("g"), color.get("r"), color.get("b"))

    def rgb(color: Dict[str, int]):
        return Color(color.get("r"), color.get("g"), color.get("b"))

    def get_color(color: Dict[str, int], color_mode: str):
        color = []

        for letter in color_mode.lower():
            color_val = color.get(letter, "None")
            if color_val == "None":
                raise ValueError(f"No value provided for key:{letter}.")
            color.append(color_val)

        return Color(*color)

    def get_random():
        colors = [
            value
            for key, value in LedColor.__dict__.items()
            if type(value) == int
        ]
        index = round(random.random() * len(colors)) - 1

        return colors[index]
