"""This module handles the lighting loop thread. """

from multiprocessing import Process
from typing import Callable
from colors import LedColor


class LightLoop:
    def __init__(self, light_string):
        self.starting_color = LedColor.brightViolet
        self.process = Process(
            target=light_string.set_solid, args=[self.starting_color]
        )
        self.process.start()

    def set_looping_pattern(self, callback: Callable, kwargs={}):
        """Starts a light function in a secondary process to avoid blocking flask. The
            function will run endlessly in a loop until the process is terminated by
            another function call

        Args:
            callback (Callable): Function to run endlessly
            kwargs (dict, optional): Keyword arguments for function. Defaults to {}.
        """

        def loop_wrapper():
            while True:
                callback(**kwargs)

        self.process.terminate()
        self.process = Process(target=loop_wrapper)
        self.process.start()

    def set_static_lights(self, target: Callable, kwargs={}):
        """Starts a light function in a secondary process to avoid blocking flask

        Args:
            target (Callable): Lighting function to run. Function can be endless loop.
            kwargs (dict, optional): Keyword arguments for function. Defaults to {}.
        """
        self.process.terminate()
        self.process = Process(target=target, kwargs=kwargs)
        self.process.start()

    def terminate_running_process(self):
        """Terminates anything currently running so other lighting processes can be run"""
        if self.process:
            self.process.terminate()
