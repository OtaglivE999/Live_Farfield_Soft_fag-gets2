import os
import sys
import subprocess
import hashlib
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as signal
import webrtcvad


def bandpass_filter(data, sr, low=300, high=3400):
    """Apply a band-pass filter to `data`."""
    sos = signal.butter(4, [low, high], btype="band", fs=sr, output="sos")
    return signal.sosfilt(sos, data)


def detect_voice_segments(y, sr, aggressiveness=3):
    """Return voice segments ``(start, end)`` detected via WebRTC VAD."""
    vad = webrtcvad.Vad(aggressiveness)
    mono = librosa.to_mono(y) if y.ndim > 1 else y
    resampled = librosa.resample(mono, orig_sr=sr, target_sr=16000)
    max_abs = np.max(np.abs(resampled)) or 1.0
    int16 = (resampled / max_abs * 32767).astype(np.int16)
    frame_length = int(16000 * 0.03)
    segments, start = [], None
    for i in range(0, len(int16), frame_length):
        frame = int16[i : i + frame_length]
        if len(frame) < frame_length:
            break
        speech = vad.is_speech(frame.tobytes(), 16000)
        t = i / 16000.0
        if speech and start is None:
            start = t
        elif not speech and start is not None:
            segments.append((start, t))
            start = None
    if start is not None:
        segments.append((start, len(int16) / 16000.0))
    return segments


def fingerprint_segment(segment, sr):
    """Return a simple fingerprint hash for a voice ``segment``."""
    mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=13)
    return hashlib.md5(mfcc.mean(axis=1).astype(np.float32).tobytes()).hexdigest()

print("🔊 Full Soft Voice Enhancer + Transcriber (VAD + Fingerprint)")

input_path = input("Enter full path to your audio/video file (.wav, .mp3, .mp4): ").strip().strip('"')
if not os.path.exists(input_path):
    print(f"❌ File not found: {input_path}")
    sys.exit(1)

base_name = os.path.splitext(os.path.basename(input_path))[0]
ext = os.path.splitext(input_path)[1].lower()

try:
    print("📥 Loading audio...")
    y, sr = sf.read(input_path, always_2d=False, dtype="float32")
except Exception as e:
    print(f"❌ Error loading file: {e}")
    sys.exit(1)

# Resample to 192kHz if needed
if sr != 192000:
    y = librosa.resample(y, orig_sr=sr, target_sr=192000)
    sr = 192000

# Detect voice segments using VAD
segments = detect_voice_segments(y, sr)
if segments:
    print(f"🗣️ Detected {len(segments)} voice segments")
else:
    print("ℹ️ No speech detected - continuing with full audio")

try:
    print("🎚️ Enhancing soft voices...")

    # Mid-range boost for detected voice segments
    y_proc = np.array(y, dtype=np.float32)
    for start, end in segments:
        s = int(start * sr)
        e = int(end * sr)
        seg = y_proc[s:e]
        if len(seg) == 0:
            continue
        fp = fingerprint_segment(seg, sr)
        print(f"   🔑 fingerprint {fp[:8]} from {start:.2f}s to {end:.2f}s")
        y_proc[s:e] = bandpass_filter(seg, sr, 500, 5000)

    frame_length = 2048
    hop_length = 512
    max_amp = np.max(np.abs(y_proc)) + 1e-9
    y_enhanced = np.copy(y_proc)
    for start in range(0, len(y_proc), hop_length):
        frame = y_proc[start : start + frame_length]
        rms = np.sqrt(np.mean(frame**2))
        rms_db = 20 * np.log10(rms / max_amp)
        gain = 10 ** ((-30 - rms_db) / 20) if rms_db < -30 else 1.0
        y_enhanced[start : start + len(frame)] = np.clip(frame * gain, -1.0, 1.0)
    wav_output = f"enhanced_{base_name}.wav"
    sf.write(wav_output, y_enhanced, sr, subtype="PCM_32")
    print(f"✅ Saved enhanced audio: {wav_output}")
except Exception as e:
    print(f"❌ Enhancement error: {e}")
    sys.exit(1)

# Convert back to MP4 if needed
if ext == ".mp4":
    try:
        mp4_output = f"enhanced_{base_name}.mp4"
        print("🎞️ Rebuilding MP4 with enhanced audio...")
        cmd = f'ffmpeg -y -i "{input_path}" -i "{wav_output}" -c:v copy -map 0:v:0 -map 1:a:0 -shortest "{mp4_output}"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Rebuilt MP4 saved as: {mp4_output}")
    except Exception as e:
        print(f"⚠️ Could not rebuild MP4: {e}")

# Whisper transcription
try:
    print("📝 Transcribing using Whisper (if installed)...")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(wav_output)
    with open(f"transcript_{base_name}.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"✅ Transcript saved: transcript_{base_name}.txt")
except Exception as e:
    print(f"ℹ️ Whisper transcription skipped or failed: {e}")
