"""This module handles the lighting loop thread. """

from multiprocessing import Process
from typing import Callable

from light_animations import LightString
from colors import LedColor

light_string = LightString()


class LightLoop:
    def __init__(self):
        self.starting_color = LedColor.brightViolet
        self.process = Process(
            target=light_string.set_solid, args=[self.starting_color]
        )
        self.process.start()

    def set_looping_pattern(self, callback: Callable, kwargs={}):
        def loop_wrapper():
            while True:
                callback(**kwargs)

        self.process.terminate()
        self.process = Process(target=loop_wrapper)
        self.process.start()

    def set_static_lights(self, callback: Callable, kwargs={}):
        self.process.terminate()
        self.process = Process(target=callback, kwargs=kwargs)
        self.process.start()
