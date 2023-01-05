from typing import List

from flask import Flask, request
from flask import Response as FlaskResponse
from flask_cors import CORS
import socketio

from SpotifyAudioAnalysis import SpotifyAudioAnalysis
from colors import LedColor
from LightLoop import LightLoop
from LightString import LightString, strip_mode
from DynamicDisplay import DynamicDisplay

import config
import helpers

log = config.log

# Create server and set allowed domain origins
sio = socketio.Server(
    logger=True, async_mode="eventlet", cors_allowed_origins="*"
)
app = Flask(__name__)
cors = CORS(app, origins=config.secrets["CORS_ALLOWED_DOMAINS"])
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

device_config = helpers.get_config_from_file()

light_string = LightString(**device_config)
light_loop = LightLoop(light_string)
dynamic_display = DynamicDisplay(light_string=light_string)


@app.route("/configDevice/", methods=["POST"])
def config_string():
    """sets all pixels on tree to black

    Returns:
        FlaskResponse: Positive HTTP Response
    """
    global light_string
    global dynamic_display
    data = request.json
    color_mode = data.get("color_mode").lower()
    led_count = data.get("led_count")

    log.info(data)

    if color_mode not in strip_mode.keys():
        return FlaskResponse(f"Data : {color_mode} is not valid", status=406)

    helpers.write_config_to_file(
        {"led_count": int(led_count), "color_mode": color_mode}
    )

    light_string = LightString(led_count=int(led_count), color_mode=color_mode)
    dynamic_display = DynamicDisplay(light_string=light_string)

    light_loop.set_static_lights(
        light_string.set_solid, {"color": LedColor.white}
    )

    return FlaskResponse("Updated string config", status=202)


@sio.event
def connect(*args):
    """Logs a message on new client connections."""
    log.info("New client connected.")


@sio.event
def set_color(_sid, color: List[int]):
    """Sets the color to the one provided in the message

    Args:
        color (List[int]): Color to set tree
    """
    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(
        light_string.set_solid, {"color": LedColor.rgb(color)}
    )


@app.route("/turnOffLights/", methods=["POST"])
def turn_off_lights():
    """sets all pixels on tree to black

    Returns:
        FlaskResponse: Positive HTTP Response
    """
    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(
        light_string.set_solid, {"color": LedColor.black}
    )
    return FlaskResponse("Turned off lights.", status=202)


# Function and arguments for setPattern endpoint
pattern_fn_map = {
    "rainbowCycle": {"fn": light_string.rainbow_cycle},
    "slowRandomTransition": {
        "fn": light_string.transition_to_random_color,
        "kwargs": {"wait_after_transition_ms": 1},
    },
    "fastRandomTransition": {
        "fn": light_string.transition_to_random_color,
        "kwargs": {"transition_time_ms": 100, "wait_after_transition_ms": 1},
    },
}


# Sets color to an existing mapped preset color
@app.route("/setSolidPreset/", methods=["POST"])
def set_solid():
    data = request.json
    color = data.get("color")
    led_color = getattr(LedColor, color)
    log.info(f"Setting color to {color}")
    if not led_color:
        return FlaskResponse(
            f"No valid preset color found for {color}", status=401
        )
    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(light_string.set_solid, {"color": led_color})
    return FlaskResponse(f"Set lights to color {color}", status=202)


@app.route("/setCustomPattern/", methods=["POST"])
def set_custom_pattern():
    """sets all pixels on tree to black

    Returns:
        FlaskResponse: Positive HTTP Response
    """
    data = request.json
    pattern = data.get("pattern")
    log.info(pattern)
    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(
        light_string.set_solid_from_rgb_list, {"rgb_list": pattern}
    )
    return FlaskResponse("Set to custom pattern", status=202)


@app.route("/setRgbColor/", methods=["POST"])
def set_rgb_color():
    data = request.json
    color = data.get("color")
    if not type(color) == list or len(color) != 3:
        return FlaskResponse(
            f"Improper data sent. Must be a 3 index list. {color}", status=401
        )

    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(
        light_string.set_solid, {"color": LedColor.rgb(color)}
    )
    return FlaskResponse(f"Set lights to color {color}", status=202)


# Starts an animated pattern
@app.route("/setPattern/", methods=["POST"])
def set_pattern():
    data = request.json
    pattern = data.get("pattern")
    if not pattern or pattern not in pattern_fn_map.keys():
        return FlaskResponse("Missing or Invalid Pattern", status=404)

    dynamic_display.terminate_all_running_process()
    pattern_fn = pattern_fn_map.get(pattern)
    light_loop.set_looping_pattern(
        pattern_fn.get("fn"),
        pattern_fn.get("kwargs", {}),
    )
    return FlaskResponse(
        f"Set to lighting pattern {request.json['pattern']}", status=200
    )


# Simple test endpoint for debugging
@app.route("/test/", methods=["GET", "POST"])
def test_turn_yellow():
    dynamic_display.terminate_all_running_process()
    light_loop.set_static_lights(light_string.random_colors)

    return FlaskResponse("Test Received!!", status=202)


# Starts lighting device running with dual beat spotify visualization
@app.route("/spotifyVisualizeDualBeat/", methods=["POST"])
def spotify_visualize_dual_beat():
    data = request.json
    track_progress = data.get("track_progress")
    track_data = data.get("track_data")
    lag_time_ms = data.get("lag_time_ms")

    audio_analysis = SpotifyAudioAnalysis(
        track_progress=track_progress, lag_time_ms=lag_time_ms, **track_data
    )

    light_loop.terminate_running_process()
    dynamic_display.reinitialize()
    dynamic_display.dual_beats(audio_analysis)

    return FlaskResponse("Setting visualizer to dual beat", status=202)


# Simple test endpoint for debugging
@app.route("/bonjour/", methods=["GET"])
def bonjour_to_web_server():
    light_loop.set_static_lights(
        light_string.set_solid_from_rgb_list,
        {"rgb_list": [[100, 255, 0], [0, 0, 255]]},
    )
    return FlaskResponse("BONJOUR!", status=202)


if __name__ == "__main__":
    # deploy with eventlet
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(
        eventlet.wrap_ssl(
            eventlet.listen(("", 5000)),
            certfile="./credentials/cert.pem",
            keyfile="./credentials/key.pem",
            server_side=True,
        ),
        app,
    )
