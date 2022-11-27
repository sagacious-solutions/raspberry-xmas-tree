from typing import Callable
import logging
from multiprocessing import Process

from flask import Flask
from flask import Response as FlaskResponse
from flask_ask_sdk.skill_adapter import SkillAdapter


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from light_animations import light_string
from colors import LedColor

import config

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LightLoop:
    def __init__(self):
        self.process = Process(target=light_string.set_solid, args=[LedColor.brightViolet])
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


light_loop = LightLoop()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Choose a lighting option."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Holiday Lights", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("setRainbowChaseIntent"))
def set_rainbow_chase_handler(handler_input):
    """Handler for setRainbowChaseIntent Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Setting lights to Rainbow Chase"
    light_loop.set_looping_pattern(light_string.rainbow_cycle)
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("slowRainbowTheaterChaseIntent"))
def slow_rainbow_chase_handler(handler_input):
    """Handler for setRainbowChaseIntent Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Setting lights to slow Rainbow Theater Chase"
    light_loop.set_looping_pattern(light_string.theater_chase_rainbow, {"wait_ms": 100})
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("turnOffIntent"))
def turn_off_lights_intent(handler_input):
    """Handler to turn off the lights."""
    # type: (HandlerInput) -> Response
    speech_text = "Turning off the lights."
    light_loop.set_static_lights(light_string.set_solid, {"color": LedColor.black})
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("solidRandomIntent"))
def random_solid_intent(handler_input):
    """Handler to turn the string random colors."""
    # type: (HandlerInput) -> Response
    speech_text = "Setting to random solid colors."
    light_loop.set_static_lights(light_string.random_colors)
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("slowRandomTransitionIntent"))
def randomly_transition_between_colors_intent(handler_input):
    """Handler to turn the string random colors."""
    # type: (HandlerInput) -> Response
    speech_text = "Starting random color mood."
    light_loop.set_looping_pattern(
        light_string.transition_to_random_color, {"wait_after_transition_ms": 1}
    )
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can set the light string with me."

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "oh, okay. Bye then!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = ("Sorry, thats not a thing.")
    reprompt = "Choose a light pattern. Trying saying Start Rainbow chase."
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Something happened that I couldn't deal with."
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


app = Flask(__name__)
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id=config.secrets["ALEXA_SKILL_ID"],
    app=app)


@app.route("/", methods=['GET', 'POST'])
def invoke_skill():
    return skill_adapter.dispatch_request()


@app.route("/test/", methods=['GET', 'POST'])
def test_turn_yellow():
    light_loop.process.terminate()
    light_loop.process = Process(target=light_string.set_solid, args=[LedColor.yellow])
    light_loop.process.start()
    return FlaskResponse("Test Received!!", status=202)


if __name__ == "__main__":
    app.run(
        # Port in use by tunnel
        port=5000,
        # Run on all IPs
        host="0.0.0.0",
        # ssl_context=(config.https_cert, config.https_key)
    )