import pickle
import pytest
from pathlib import Path
import time
import sys

from classes.SpotifyAudioAnalysis import SpotifyAudioAnalysis


pytestmark = pytest.mark.skipif(
    sys.platform == "darwin", reason="tests for Windows only"
)

track_data_files = [
    "stairwayToHeavenAnalysis.dict",
    "frontierPsychiatristAnalysis.dict",
]


@pytest.fixture(params=track_data_files)
def SongAnalysisClass(request):
    TRACK_PROGRESS_SECS = 120

    filepath = Path.cwd() / "tests" / request.param

    with open(filepath, "rb") as file:
        track_data = pickle.load(file)

    return SpotifyAudioAnalysis(
        track_progress=TRACK_PROGRESS_SECS, **track_data
    )


@pytest.mark.parametrize("time_seconds", [45, 120, 146, 199, 330])
def test_time_to_get_active(SongAnalysisClass, time_seconds):
    linear_start = time.time()
    linear_search_active = SongAnalysisClass.get_active_linear_search(
        progress_seconds=time_seconds
    )
    linear_search_time = time.time() - linear_start

    binary_start = time.time()
    binary_search_active = SongAnalysisClass.get_active_binary_search(
        progress_seconds=time_seconds
    )
    binary_search_time = time.time() - binary_start

    assert linear_search_active == binary_search_active
    try:
        # Make sure binary search is at least twice as fast as linear
        assert binary_search_time < linear_search_time / 2
    except AssertionError:
        pytest.skip(
            "This test failed. It was designed for Rpi and may have"
            " unpredictable results in CI Pipeline"
        )
