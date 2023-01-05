import time
from config import log

ONE_SECOND_MILLISECONDS = 1000


class SpotifyAudioAnalysis:
    def __init__(
        self,
        bars,
        beats,
        sections,
        segments,
        tatums,
        track,
        track_progress,
        lag_time_ms,
        **kwargs,
    ):
        self.bars = bars
        self.beats = beats
        self.sections = sections
        self.segments = segments
        self.tatums = tatums
        self.track_duration = track["duration"]
        self.track_progress_ms = track_progress + lag_time_ms
        self.created_time = time.time()

        log.debug(f"The lag time was {lag_time_ms}")

    def get_track_progress_seconds(self) -> float:
        """Gets the current track progress in seconds

        Returns:
            float: The current track progress in seconds
        """
        current_time_seconds = time.time() - self.created_time
        new_track_time = (self.track_progress_ms / 1000) + current_time_seconds

        return new_track_time

    def active_thingies(self):
        track_time_seconds = self.get_track_progress_seconds()

        active = {
            "bar": self.__get_active(self.bars, track_time_seconds),
            "beat": self.__get_active(self.beats, track_time_seconds),
            "section": self.__get_active(self.sections, track_time_seconds),
            "segment": self.__get_active(self.segments, track_time_seconds),
            "tatum": self.__get_active(self.tatums, track_time_seconds),
        }

        return active

    def __get_active(self, category, track_time_seconds):
        for item in category:
            start = item["start"]
            stop = start + item["duration"]

            if start <= track_time_seconds <= stop:
                return item
