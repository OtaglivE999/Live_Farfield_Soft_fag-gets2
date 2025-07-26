import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pydub.generators import Sine
from enhance_audio_files.enhance_audio import detect_voice_segments


def test_detect_voice_segments_returns_list():
    seg = Sine(440).to_audio_segment(duration=1000).set_frame_rate(16000)
    segments = detect_voice_segments(seg, frame_duration_ms=30, aggressiveness=3)
    assert isinstance(segments, list)
    for start, end in segments:
        assert 0 <= start < end <= seg.duration_seconds
