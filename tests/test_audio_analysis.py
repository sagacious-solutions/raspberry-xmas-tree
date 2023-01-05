import pickle
import pytest
from pathlib import Path

from SpotifyAudioAnalysis import SpotifyAudioAnalysis


@pytest.fixture
def StairwayToHeavenSpotifyData():
    filepath = Path.cwd() / "tests" / "stairwayToHeavenAnalysis.dict"

    with open(filepath, "rb") as file:
        return pickle.load(file)


@pytest.fixture
def SongAnalysisClass(StairwayToHeavenSpotifyData):
    TRACK_PROGRESS_SECS = 120

    return SpotifyAudioAnalysis(
        track_progress=TRACK_PROGRESS_SECS, **StairwayToHeavenSpotifyData
    )


def test_time_to_get_active(SongAnalysisClass):
    print(SongAnalysisClass)
