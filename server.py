import logging

from flask import Flask
from flask import Response as FlaskResponse

from colors import LedColor
from lightloop import LightLoop
from light_animations import LightString


import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

light_loop = LightLoop()
light_string = LightString()


@app.route("/setPattern/turnOffLights/", methods=['GET', 'POST'])
def turn_off_lights(handler_input):
    """Handler to turn off the lights."""
    # type: (HandlerInput) -> Response
    speech_text = "Turning off the lights."
    light_loop.set_static_lights(light_string.set_solid, {"color": LedColor.black})
    return FlaskResponse("Turned off lights.", status=202)
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response






# @sb.request_handler(can_handle_func=is_intent_name("slowRainbowTheaterChaseIntent"))
# def slow_rainbow_chase_handler(handler_input):
#     """Handler for setRainbowChaseIntent Intent."""
#     # type: (HandlerInput) -> Response
#     speech_text = "Setting lights to slow Rainbow Theater Chase"
#     light_loop.set_looping_pattern(light_string.theater_chase_rainbow, {"wait_ms": 100})
#     return handler_input.response_builder.speak(speech_text).set_should_end_session(
#         True).response




# @sb.request_handler(can_handle_func=is_intent_name("solidRandomIntent"))
# def random_solid_intent(handler_input):
#     """Handler to turn the string random colors."""
#     # type: (HandlerInput) -> Response
#     speech_text = "Setting to random solid colors."
#     light_loop.set_static_lights(light_string.random_colors)
#     return handler_input.response_builder.speak(speech_text).set_should_end_session(
#         True).response


@app.route("/setPattern/slowRandomTransition/", methods=['GET', 'POST'])
def randomly_transition_between_colors():
    """Handler to turn the string random colors."""
    light_loop.set_looping_pattern(
        light_string.transition_to_random_color, {"wait_after_transition_ms": 1}
    )
    return FlaskResponse("Changing to slowRandomTransition", status=202)



# Register your intent handlers to the skill_builder object
@app.route("/setPattern/rainbowCycle/", methods=['GET', 'POST'])
def rainbow_cycle():
    """Handler for setRainbowChaseIntent Intent."""
    # type: (HandlerInput) -> Response
    light_loop.set_looping_pattern(light_string.rainbow_cycle)
    return FlaskResponse("Starting Rainbow Cycle", status=202)


@app.route("/test/", methods=['GET', 'POST'])
def test_turn_yellow():
    light_loop.set_static_lights(light_string.random_colors)

    return FlaskResponse("Test Received!!", status=202)


if __name__ == "__main__":
    app.run(
        # Port in use by tunnel
        port=5000,
        # Run on all IPs
        host="0.0.0.0",
        # ssl_context=(config.https_cert, config.https_key)
    )