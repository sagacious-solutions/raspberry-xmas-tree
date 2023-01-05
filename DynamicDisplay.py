"""This module handles displaying lights on the device for complex visualizations

It runs the light_string in a second thread constantly refreshing it based on what
 exists in the DynamicDisplay class pixel_array like a primitive display driver. This
 array is shared with the main thread and is thread safe, so it can be updated while
 ignoring the display refresh cycles and will update the display device on the
 next cycle.
"""
from multiprocessing import Process, Array
from typing import Callable, List
import time
import copy
from rpi_ws281x import Color

from SpotifyAudioAnalysis import SpotifyAudioAnalysis
from colors import LedColor


class DynamicDisplay:
    def __init__(self, light_string):
        self.light_string = light_string
        self.groups = {}
        self.group_threads = {}
        self.light_refresh_loop = None
        self.pixel_array = Array("l", light_string.led_count)
        self.__start_refresh_thread()

    def clean_up(self):
        """End all processes associated with the class. Meant to be run in the finally
        block anytime the class is instantiated.
        """
        self.light_refresh_loop.terminate()

        # Terminate all open animation threads
        for key in self.group_threads.keys():
            self.group_threads[key].terminate()

    def __start_refresh_thread(self):
        self.light_refresh_loop = Process(
            target=self.__refresh_loop, args=[self.pixel_array]
        )
        self.light_refresh_loop.start()

    def __refresh_loop(self, pixel_array):
        while True:
            for pixel_n, color in enumerate(pixel_array):
                self.light_string.strip.setPixelColor(pixel_n, color)

            self.light_string.strip.show()
            time.sleep(0.005)

    def __start_thread_for_group(
        self,
        group_name: str,
        target: Callable,
        args: list = [],
        kwargs: dict = {},
    ):
        self.group_threads[group_name] = Process(
            target=target, args=args, kwargs=kwargs
        )
        self.group_threads[group_name].start()

    def update_group(self, group_name: str, color: Color):
        """Updates every pixel in the group to the provided color

        Args:
            group_name (str): Key in groups dict to get pixel numbers from
            color (Color): Color to update those pixels too
        """
        for pixel_n in self.groups[group_name]:
            self.pixel_array[pixel_n] = color

    def create_group_of_every_nth(self, n: int, offset: int, group_name: str):
        group_pixels = []

        for i in range(self.light_string.led_count):
            if i % n == offset:
                group_pixels.append(i)

        self.groups[group_name] = group_pixels

    def run_group_on_beat(
        self,
        audio_analysis,
        group_name: str,
        nth_beat: int,
        colors: List[Color] = None,
        color_change_on: str = "bar",
    ):
        last_active = {}

        while (
            audio_analysis.get_track_progress_seconds()
            < audio_analysis.track_duration * 1000
        ):
            now_active = audio_analysis.active_thingies()

            if now_active.get(color_change_on) and (
                not last_active.get(color_change_on)
                == now_active.get(color_change_on)
            ):
                color = (
                    LedColor.get_random()
                    if not colors
                    else colors[
                        now_active.get(color_change_on)["index"] % len(colors)
                    ]
                )

            if now_active.get("beat") and (
                not last_active.get("beat") == now_active.get("beat")
            ):
                if (
                    now_active.get("beat")
                    and now_active.get("beat")["index"] % nth_beat == 0
                ):
                    print(f"run_group_on_beat - {group_name} - ran")
                    self.update_group(group_name, color)

            last_active = copy.deepcopy(now_active)

    def dual_beats(self, audio_analysis: SpotifyAudioAnalysis):
        self.groups = {}
        self.create_group_of_every_nth(n=2, offset=0, group_name="all_beat")
        self.create_group_of_every_nth(
            n=2, offset=1, group_name="every_2nd_beat"
        )

        all_beat = {
            "target": self.run_group_on_beat,
            "args": [audio_analysis, "all_beat", 1],
            "kwargs": {
                "color_change_on": "beat",
                "colors": [
                    Color(
                        255,
                        0,
                        0,
                    ),
                    Color(
                        255,
                        255,
                        255,
                    ),
                ],
            },
        }
        every_2nd_beat = {
            "target": self.run_group_on_beat,
            "args": [audio_analysis, "every_2nd_beat", 2],
            "kwargs": {
                "colors": [
                    Color(
                        0,
                        255,
                        0,
                    ),
                    Color(
                        0,
                        0,
                        255,
                    ),
                ]
            },
        }

        self.__start_thread_for_group("all_beat", **all_beat)
        self.__start_thread_for_group("every_2nd_beat", **every_2nd_beat)

        # def all_beat():
        #     last_active = {}

        #     while (
        #         audio_analysis.get_track_progress_seconds()
        #         < audio_analysis.track_duration * 1000
        #     ):
        #         now_active = audio_analysis.active_thingies()

        #         if now_active.get("bar") and (
        #             not last_active.get("bar") == now_active.get("bar")
        #         ):
        #             color = LedColor.get_random()

        #         if now_active.get("beat") and (
        #             not last_active.get("beat") == now_active.get("beat")
        #         ):
        #             print("All beat run")
        #             self.update_group("all_beat", color)
        #             # self.set_solid(color)
        #             # self.transition_colors(
        #             #     color,
        #             #     Color(0, 0, 0),
        #             #     int(now_active.get("beat")["duration"] * 100),
        #             # )

        #         last_active = copy.deepcopy(now_active)

        # def every_2nd_beat():
        #     last_active = {}

        #     while (
        #         audio_analysis.get_track_progress_seconds()
        #         < audio_analysis.track_duration * 1000
        #     ):
        #         now_active = audio_analysis.active_thingies()

        #         if now_active.get("bar") and (
        #             not last_active.get("bar") == now_active.get("bar")
        #         ):
        #             color = LedColor.get_random()

        #         if now_active.get("beat") and (
        #             not last_active.get("beat") == now_active.get("beat")
        #         ):
        #             print("every_2nd_beat ran")
        #             if (
        #                 now_active.get("beat")
        #                 and now_active.get("beat")["index"] % 2 == 0
        #             ):
        #                 self.update_group("every_2nd_beat", color)
        #             # self.set_solid(color)
        #             # self.transition_colors(
        #             #     color,
        #             #     Color(0, 0, 0),
        #             #     int(now_active.get("beat")["duration"] * 100),
        #             # )

        #         last_active = copy.deepcopy(now_active)
