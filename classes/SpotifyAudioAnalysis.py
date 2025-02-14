import time
from typing import Dict


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
        lag_time_ms=0,
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
        self.confidence_average = {
            "beats": self.__get_average_item_confidence("beats"),
            "tatums": self.__get_average_item_confidence("tatums"),
        }

    def __get_average_item_confidence(self, item_name):
        confidence = []
        for item in self.__dict__[item_name]:
            confidence.append(item["confidence"])

        return sum(confidence) / len(self.__dict__[item_name])

    def get_track_progress_seconds(self) -> float:
        """Gets the current track progress in seconds

        Returns:
            float: The current track progress in seconds
        """
        current_time_seconds = time.time() - self.created_time
        new_track_time = (self.track_progress_ms / 1000) + current_time_seconds

        return new_track_time

    def get_active_linear_search(
        self, progress_seconds: int = None
    ) -> Dict[str, dict]:
        """Gets the current active items from spotify data using a linear search

        Args:
            progress_seconds (int, optional): What point in track to check whats active.
                Only exists for consistency in testing. Defaults to None.

        Returns:
            dict: The current active items for the given progress in the song
        """
        track_time_seconds = (
            self.get_track_progress_seconds()
            if not progress_seconds
            else progress_seconds
        )

        if track_time_seconds > self.track_duration:
            return None

        active = {
            "bars": self.__linear_search_active(self.bars, track_time_seconds),
            "beats": self.__linear_search_active(
                self.beats, track_time_seconds
            ),
            "sections": self.__linear_search_active(
                self.sections, track_time_seconds
            ),
            "segments": self.__linear_search_active(
                self.segments, track_time_seconds
            ),
            "tatums": self.__linear_search_active(
                self.tatums, track_time_seconds
            ),
        }

        return active

    def __linear_search_active(self, category, track_time_seconds):
        for i, item in enumerate(category):
            start = item["start"]
            stop = start + item["duration"]

            if start <= track_time_seconds <= stop:
                return {"index": i, **item}

    def get_active_binary_search(
        self, progress_seconds: int = None
    ) -> Dict[str, dict]:
        """Gets the current active items from spotify data using a binary search

        Args:
            progress_seconds (int, optional): What point in track to check whats active.
                Only exists for consistency in testing. Defaults to None.

        Returns:
            dict: The current active items for the given progress in the song
        """
        track_time_seconds = (
            self.get_track_progress_seconds()
            if not progress_seconds
            else progress_seconds
        )

        if track_time_seconds > self.track_duration:
            return None

        active = {
            "bars": self._binary_search_active(self.bars, track_time_seconds),
            "beats": self._binary_search_active(self.beats, track_time_seconds),
            "sections": self._binary_search_active(
                self.sections, track_time_seconds
            ),
            "segments": self._binary_search_active(
                self.segments, track_time_seconds
            ),
            "tatums": self._binary_search_active(
                self.tatums, track_time_seconds
            ),
        }

        return active

    def _binary_search_active(self, data_arr, track_time_seconds):
        low = 0
        high = len(data_arr) - 1
        mid = 0

        while low <= high:
            mid = (high + low) // 2
            current = data_arr[mid]
            start = current["start"]
            end = start + current["duration"]

            if end < track_time_seconds:
                low = mid + 1

            elif start > track_time_seconds:
                high = mid - 1

            else:
                return {"index": mid, **data_arr[mid]}

        return None
