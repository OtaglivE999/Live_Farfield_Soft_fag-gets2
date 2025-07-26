
"""Voice activity detection utilities for incoming audio."""

import numpy as np
import webrtcvad
import librosa

SAMPLE_RATE = 48000
FRAME_DURATION = 30  # ms
VAD_MODE = 2  # 0-3: higher = more aggressive

vad = webrtcvad.Vad(VAD_MODE)

def frame_generator(audio, sample_rate, frame_duration_ms):
    frame_len = int(sample_rate * frame_duration_ms / 1000)
    for i in range(0, len(audio) - frame_len + 1, frame_len):
        yield audio[i:i + frame_len]

def detect_voiced(audio, sample_rate=SAMPLE_RATE):
    if sample_rate not in (8000, 16000, 32000, 48000):
        audio = librosa.resample(audio.astype(np.float32), orig_sr=sample_rate, target_sr=48000)
        sample_rate = 48000
    if audio.dtype != np.int16:
        audio = (audio * 32767).astype(np.int16)
    frames = frame_generator(audio, sample_rate, FRAME_DURATION)
    voiced = []
    for frame in frames:
        if vad.is_speech(frame.tobytes(), sample_rate):
            voiced.extend(frame)
    return np.array(voiced, dtype=np.int16)

def enhance_audio(voiced_audio):
    if len(voiced_audio) == 0:
        return np.zeros(1, dtype=np.float32)
    if voiced_audio.dtype != np.float32:
        voiced_audio = voiced_audio.astype(np.float32) / 32767
    from scipy.signal import butter, lfilter

    def bandpass(data, low, high, fs, order=4):
        nyq = 0.5 * fs
        b, a = butter(order, [low / nyq, high / nyq], btype="band")
        return lfilter(b, a, data)

    filtered = bandpass(voiced_audio, 300, 6000, SAMPLE_RATE)
    normalized = filtered / (np.max(np.abs(filtered)) or 1)
    amplified = normalized * 0.9
    return (amplified * 2147483647).astype(np.int32)
