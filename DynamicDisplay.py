"""This module handles displaying lights on the device for complex visualizations

It runs the light_string in a second thread constantly refreshing it based on what
 exists in the DynamicDisplay class pixel_array like a primitive display driver. This
 array is shared with the main thread and is thread safe, so it can be updated while
 ignoring the display refresh cycles and will update the display device on the
 next cycle.
"""
from multiprocessing import Process, Array
import time
import copy

from rpi_ws281x import Color, PixelStrip, ws

from SpotifyAudioAnalysis import SpotifyAudioAnalysis
from colors import LedColor


class DynamicDisplay:
    def __init__(self, light_string):
        self.light_string = light_string
        self.groups = {}
        self.light_refresh_loop = None
        self.pixel_array = Array("l", light_string.led_count)
        self.start_refresh_thread()

        for i in range(self.light_string.led_count):
            self.pixel_array[i] = Color(255, 255, 255)
            # self.light_string.strip.setPixelColor(i, Color(255, 255, 255))

        time.sleep(4)

        for i in range(self.light_string.led_count):
            self.pixel_array[i] = Color(0, 0, 255)

    def update_group(self, group_name, color):
        for pixel_n in self.groups[group_name]:
            self.pixel_array[pixel_n] = color

    def create_group_of_every_nth(self, n: int, offset: int, group_name: str):
        group_pixels = []

        for i in range(self.light_string.led_count):
            if i % n == offset:
                group_pixels.append(i)

        self.groups[group_name] = group_pixels

    def start_refresh_thread(self):
        self.light_refresh_loop = Process(
            target=self.__refresh_loop, args=[self.pixel_array]
        )
        self.light_refresh_loop.start()

    def __refresh_loop(self, pixel_array):
        while True:
            for pixel_n, color in enumerate(pixel_array):
                self.light_string.strip.setPixelColor(pixel_n, color)

            self.light_string.strip.show()
            time.sleep(0.01)

    def dual_beats(self, audio_analysis: SpotifyAudioAnalysis):
        self.groups = {}
        self.create_group_of_every_nth(n=2, offset=0, group_name="all_beat")
        self.create_group_of_every_nth(
            n=2, offset=1, group_name="every_2nd_beat"
        )

        last_active = {}

        while (
            audio_analysis.get_track_progress_seconds()
            < audio_analysis.track_duration * 1000
        ):
            now_active = audio_analysis.active_thingies()

            if now_active.get("bar") and (
                not last_active.get("bar") == now_active.get("bar")
            ):
                color = LedColor.get_random()

            if now_active.get("beat") and (
                not last_active.get("beat") == now_active.get("beat")
            ):
                self.set_solid(color)
                self.transition_colors(
                    color,
                    Color(0, 0, 0),
                    int(now_active.get("beat")["duration"] * 100),
                )

            last_active = copy.deepcopy(now_active)
