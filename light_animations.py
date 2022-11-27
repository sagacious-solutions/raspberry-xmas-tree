from typing import List, Optional
import time

from rpi_ws281x import Color, PixelStrip
from colors import LedColor

from simple_logging import get_basic_logger

logger = get_basic_logger()


class LightString:
    def __init__(self) -> None:
        # LED strip configuration:
        LED_COUNT = 200  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = (
            False  # True to invert the signal (when using NPN transistor
        )
        #  level shift)
        LED_CHANNEL = 0

        self.ONE_SECOND_IN_MILLISECONDS = 1000
        self.MAX_COLOR_VALUE = 256
        self.LEFT_SIDE_PIXELS = [i for i in range(32)]
        self.TOP_PIXELS = [i for i in range(33, 66)]
        self.RIGHT_SIDE_PIXELS = [i for i in range(67, 100)]

        # Create PixelStrip object with appropriate configuration.
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        self.strip.begin()

    def set_color_for_pixels(self, pixel_list: List[int], color: Color):
        """Sets every pixel in the provided list to the given color

        Args:
            pixel_list (List[int]): A list of pixels (lights) to change
            color (Color): The color to change to
        """
        for pixel_n in pixel_list:
            self.strip.setPixelColor(pixel_n, color)
        self.strip.show()

    def color_wipe_inside_out_reversed(
        self, color: Color, wait_ms: Optional[int] = 50, *args, **kwargs
    ):
        """Does rolling color change from the outside of the string to the center

        Args:
            color (Color): The color to change to
            wait_ms (int, optional): how many milliseconds between changing each pixel.
                Defaults to 50.
        """
        logger.info("color_wipe_inside_out_reversed")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(0 + i, color)
            self.strip.setPixelColor(self.strip.numPixels() - i, color)
            self.strip.show()
            time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)

    def random_colors(self, time_ms: Optional[int] = 50, *args, **kwargs):
        """Move from outside in one pixel at a time changing to random colors

        Args:
            time_ms (Optional[int]): Time in ms between pixel changes. Defaults to 50.
        """
        logger.info("Setting string to random colors.")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(0 + i, LedColor.get_random())
            self.strip.setPixelColor(
                self.strip.numPixels() - i, LedColor.get_random()
            )
            self.strip.show()
            time.sleep(time_ms / self.ONE_SECOND_IN_MILLISECONDS)

    def color_wipe_inside_out(
        self, color: Color, wait_ms: Optional[int] = 50, *args, **kwargs
    ):
        """Changes from current color to the new color from center of the string to the
            outside of the string

        Args:
            color (Color): _description_
            wait_ms (int, optional): _description_. Defaults to 50.
        """
        logger.info("color_wipe_inside_out")
        half = int(self.strip.numPixels() / 2)
        for i in range(half):
            self.strip.setPixelColor(half - i, color)
            self.strip.setPixelColor(half + i, color)
            self.strip.show()
            time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)

    # Define functions which animate LEDs in various ways.
    def color_wipe(
        self, color: Color, wait_ms: Optional[int] = 50, reverse=False, **kwargs
    ):
        """Change the color from the current color to the provided one, one pixel at a
        time from one side of the string to the other

        Args:
            color (Color): _description_
            wait_ms (int, optional): How long in milliseconds between pixel changes.
                Defaults to 50.
            reverse (bool, optional): When True, goes from the right side to the left
                instead of vice versa. Defaults to False.
        """
        logger.info(f"Colorwipe - Reversed:{reverse}")
        wipe_direction = (
            (self.strip.numPixels(), 0, -1)
            if reverse
            else (0, self.strip.numPixels())
        )
        for i in range(*wipe_direction):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)

    def set_solid(self, color: Color):
        """Sets the whole light string to the new color all at once.

        Args:
            color (Color): New color to change too
        """
        logger.info("Setting to solid color")

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def theater_chase(
        self,
        color: Color,
        wait_ms: Optional[int] = 50,
        iterations: Optional[int] = 10,
        **kwargs,
    ):
        """Movie theater light style chaser animation.

        Args:
            color (Color): Color to do the animation in
            wait_ms (Optional[int]): Time between pixel changes. Defaults to 50.
            iterations (Optional[int]): How many time to run the animation.
                Defaults to 10.
        """
        logger.info("Running theater chase")
        for _ in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    @staticmethod
    def wheel(pos: int):
        """Generate rainbow colors across 0-255 positions. This is a helper
            for the rainbow functions

        Args:
            pos (int): See value to choose color

        Returns:
            Color: The new color
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(
        self,
        wait_ms: Optional[int] = 20,
        iterations: Optional[int] = 1,
        **kwargs,
    ):
        """Draw rainbow that fades across all pixels at once.

        Args:
            wait_ms (Optional[int]): Wait between color loops. Defaults to 20.
            iterations (Optional[int]): How many times to run through a color
                loop. Defaults to 1.
        """
        logger.info(f"Rainbow\nwait_ms: {wait_ms}\niterations: {iterations}")
        for j in range(self.MAX_COLOR_VALUE * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i, self.wheel((i + j) & self.MAX_COLOR_VALUE - 1)
                )
            self.strip.show()
            time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)

    def rainbow_cycle(
        self, wait_ms: Optional[int] = 20, iterations: Optional[int] = 5
    ):
        """Draw rainbow that uniformly distributes itself across all pixels.

        Args:
            wait_ms (Optional[int]): Time between refreshing the string. Defaults to 20.
            iterations (Optional[int]): Amount of times to run the loop. Defaults to 5.
        """
        logger.info(
            f"Rainbow Cycle\nwait_ms: {wait_ms}\niterations: {iterations}"
        )
        for j in range(self.MAX_COLOR_VALUE * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i,
                    self.wheel(
                        (
                            int(
                                i
                                * self.MAX_COLOR_VALUE
                                / self.strip.numPixels()
                            )
                            + j
                        )
                        & self.MAX_COLOR_VALUE - 1
                    ),
                )
            self.strip.show()
            time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)

    def theater_chase_rainbow(self, wait_ms: Optional[int] = 50):
        """Creates a rainbow theater chase pattern

        Args:
            wait_ms (Optional[int]): Time between refreshes. Defaults to 50.
        """
        for j in range(self.MAX_COLOR_VALUE):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(
                        i + q, self.wheel((i + j) % self.MAX_COLOR_VALUE - 1)
                    )
                self.strip.show()
                time.sleep(wait_ms / self.ONE_SECOND_IN_MILLISECONDS)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def transition_colors(
        self,
        c1: Color,
        c2: Color,
        time_ms: int = 1000,
    ) -> None:
        """Transition the whole light string from one color to another in a slow fade

        Args:
            c1 (Color): Color to transition from
            c2 (Color): Color to transition to
            time_ms (int, optional): AMount of time for the fade to take.
                Defaults to 1000.
        """
        c1 = self.get_rgb_value(c1)
        c2 = self.get_rgb_value(c2)
        # difference between colors
        dif = [c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2]]
        for j in range(time_ms):
            new_color = [
                round(c1[0] + dif[0] * (j / time_ms)),
                round(c1[1] + dif[1] * (j / time_ms)),
                round(c1[2] + dif[2] * (j / time_ms)),
            ]
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(*new_color))
            self.strip.show()

            time.sleep(0.001)

    def transition_to_color(
        self, new_color: Color, time_ms: Optional[int] = 1000
    ):
        """Transition the whole light string from current color to another in
            a slow fade. This acts on whatever the current color of pixel 0 is
            rather than fading each color to the new color. So if its currently
            multiple colors, it will turn every pixel to the first color before starting
            the transition.

        Args:
            new_color (Color): Time to transition to new color.
            time_ms (Optional[int], optional): _description_. Defaults to 1000.
        """
        current_color = self.strip.getPixelColor(0)
        self.transition_colors(current_color, new_color, time_ms)

    def transition_to_random_color(
        self,
        transition_time_ms: Optional[int] = 1000,
        wait_after_transition_sec: Optional[int] = 0,
        **kwargs,
    ):
        """Transition the whole light string from current color to another in
            a slow fade. This acts on whatever the current color of pixel 0 is
            rather than fading each color to the new color. So if its currently
            multiple colors, it will turn every pixel to the first color before starting
            the transition.

        Args:
            transition_time_ms (Optional[int]): Time to fade to the new color in
                milliseconds. Defaults to 1000.
            wait_after_transition_sec (Optional[int]): Time to wait after changing to
                the new color. Defaults to 0.
        """
        current_color = self.strip.getPixelColor(0)
        self.transition_colors(
            current_color, LedColor.get_random(), transition_time_ms
        )
        time.sleep(wait_after_transition_sec)

    @staticmethod
    def get_rgb_value(color_int: Color) -> List[int]:
        """The colors are held as integer values. This gets takes a Color and converts
            it into a list of 3 integers representing RGB in the range 0-255

        Args:
            color_int (Color): Color to get the integer list for.

        Returns:
            List[int]: 3 Integer values in a list from 0-255 for RGB
        """
        r = color_int >> 16 & 0xFF
        g = color_int >> 8 & 0xFF
        b = color_int & 0xFF

        return [r, g, b]


light_string = LightString()
