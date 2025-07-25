import argparse
import csv
from datetime import datetime
import logging
import os
from datetime import datetime

import numpy as np
import pydub
import scipy.signal as signal
import webrtcvad
import librosa
import matplotlib.pyplot as plt
import librosa.display

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pydub
import scipy.signal as signal
import webrtcvad

# Set up logging
logging.basicConfig(level=logging.INFO, filename="audio_enhancement.log", format='%(asctime)s - %(levelname)s - %(message)s')

# Define the frequency filters for different fields
def apply_low_pass_filter(audio_data, fs, cutoff):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(5, normal_cutoff, btype='low', analog=False)
    return signal.lfilter(b, a, audio_data)

def apply_band_pass_filter(audio_data, fs, low_cutoff, high_cutoff):
    nyquist = 0.5 * fs
    low_normal_cutoff = low_cutoff / nyquist
    high_normal_cutoff = high_cutoff / nyquist
    b, a = signal.butter(5, [low_normal_cutoff, high_normal_cutoff], btype='band', analog=False)
    return signal.lfilter(b, a, audio_data)

def apply_high_pass_filter(audio_data, fs, cutoff):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(5, normal_cutoff, btype='high', analog=False)
    return signal.lfilter(b, a, audio_data)


def detect_voice_segments(audio_segment, frame_duration_ms=30, aggressiveness=3):
    """Detect voice segments using WebRTC VAD.

    Parameters
    ----------
    audio_segment : pydub.AudioSegment
        Loaded audio segment.
    frame_duration_ms : int, optional
        Duration of each frame in milliseconds. Default is 30ms.
    aggressiveness : int, optional
        VAD aggressiveness (0-3). Higher values are more aggressive.

    Returns
    -------
    list of tuple
        List of ``(start, end)`` times in seconds where voice is detected.
    """

    vad = webrtcvad.Vad(aggressiveness)
    mono = audio_segment.set_channels(1).set_frame_rate(16000)
    bytes_per_frame = int(16000 * frame_duration_ms / 1000) * mono.sample_width
    raw_audio = mono.raw_data
    segments = []
    start = None
    for i in range(0, len(raw_audio), bytes_per_frame):
        frame = raw_audio[i:i + bytes_per_frame]
        if len(frame) < bytes_per_frame:
            break
        is_speech = vad.is_speech(frame, 16000)
        t = i / (16000 * mono.sample_width)
        if is_speech and start is None:
            start = t
        elif not is_speech and start is not None:
            segments.append((start, t))
            start = None
    if start is not None:
        segments.append((start, len(raw_audio) / (16000 * mono.sample_width)))
    return segments


def analyze_voice_features(audio_segment, voice_segments, input_file):
    """Analyze voice characteristics and log results.

    Parameters
    ----------
    audio_segment : pydub.AudioSegment
        The full audio.
    voice_segments : list of tuple
        ``(start, end)`` pairs in seconds from :func:`detect_voice_segments`.
    input_file : str
        Path to the audio file being analyzed.
    """

    os.makedirs("spectrograms", exist_ok=True)
    header = [
        "file",
        "start",
        "end",
        "gender",
        "age_range",
        "voice_color",
        "format",
        "possible_height",
        "timestamp",
        "spectrogram",
    ]
    file_exists = os.path.isfile("voice_analysis.csv")
    with open("voice_analysis.csv", mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)

        for idx, (start, end) in enumerate(voice_segments):
            seg = audio_segment[start * 1000 : end * 1000]
            samples = np.array(seg.get_array_of_samples()).astype(np.float32)
            if seg.channels > 1:
                samples = samples.reshape(-1, seg.channels).mean(axis=1)
            samples /= np.max(np.abs(samples)) or 1
            sr = seg.frame_rate
            if len(samples) == 0:
                continue

            f0 = librosa.yin(samples, fmin=50, fmax=500, sr=sr)
            f0 = f0[np.isfinite(f0)]
            f0_median = float(np.median(f0)) if f0.size else 0.0
            gender = "male" if f0_median < 165 else "female"
            age_range = "child/young" if f0_median > 220 else "adult"

            centroid = librosa.feature.spectral_centroid(y=samples, sr=sr)
            centroid_mean = float(np.mean(centroid)) if centroid.size else 0.0
            voice_color = "dark" if centroid_mean < 2000 else "bright"

            fmt = os.path.splitext(input_file)[1].lstrip(".").lower()
            possible_height = "tall" if f0_median < 120 else "average"
            timestamp = datetime.now().isoformat(timespec="seconds")

            S = librosa.amplitude_to_db(np.abs(librosa.stft(samples)), ref=np.max)
            spec_path = os.path.join(
                "spectrograms", f"{os.path.basename(input_file)}_{idx}.png"
            )
            plt.figure(figsize=(6, 3))
            librosa.display.specshow(S, sr=sr, x_axis="time", y_axis="hz")
            plt.colorbar(format="%+2.0f dB")
            plt.title("Spectrogram")
            plt.tight_layout()
            plt.savefig(spec_path)
            plt.close()

            writer.writerow(
                [
                    input_file,
                    start,
                    end,
                    gender,
                    age_range,
                    voice_color,
                    fmt,
                    possible_height,
                    timestamp,
                    spec_path,
                ]
            )

 n7paiv-codex/analyze-script-for-ai-voice-analysis-integration

 bguhir-codex/analyze-script-for-ai-voice-analysis-integration
 main
def enhance_audio(input_file, output_path, low_freq_enhance, distance_field, analyze=False):
    """Enhance ``input_file`` and write the result to ``output_path``.

    ``output_path`` can be either a filename or a directory. If a directory is
    provided, the enhanced file will be saved using the input filename with an
    ``_enhanced.wav`` suffix.
    """

    input_file = input_file.strip('"')
    output_path = output_path.strip('"')

n7paiv-codex/analyze-script-for-ai-voice-analysis-integration


def enhance_audio(input_file, output_file, low_freq_enhance, distance_field, analyze=False):
 main
    logging.info(f"Processing {input_file} for {distance_field} field enhancement")

    # Determine final output file name
    output_file = output_path
    if os.path.isdir(output_path):
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_path, f"{base}_enhanced.wav")
    elif not os.path.splitext(output_path)[1]:
        output_file = output_path + "_enhanced.wav"

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    # Load the audio file
    audio = pydub.AudioSegment.from_file(input_file)
    voice_segments = detect_voice_segments(audio)
    if analyze:
        logging.info("Voice segments detected: %s", voice_segments)
        with open("voice_segments.csv", mode="a", newline="") as seg_file:
            seg_writer = csv.writer(seg_file)
            if not os.path.exists("voice_segments.csv") or os.stat("voice_segments.csv").st_size == 0:
                seg_writer.writerow(["file", "start", "end"])
            for start, end in voice_segments:
                seg_writer.writerow([input_file, start, end])
        analyze_voice_features(audio, voice_segments, input_file)

    audio_data = np.array(audio.get_array_of_samples())

    # Apply the filter based on the field type
    if distance_field == 'far':
        # Apply low-pass filter (far-field voices are typically in lower frequencies)
        logging.info("Applying low-pass filter for far-field voices.")
        enhanced_audio = apply_low_pass_filter(audio_data, audio.frame_rate, 500)  # Low-pass cutoff at 500 Hz
    elif distance_field == 'mid':
        # Apply band-pass filter (mid-field voices have a range of frequencies)
        logging.info("Applying band-pass filter for mid-field voices.")
        enhanced_audio = apply_band_pass_filter(audio_data, audio.frame_rate, 500, 5000)  # Band-pass filter between 500Hz and 5000Hz
    elif distance_field == 'close':
        # Apply high-pass filter (close-field voices are typically high-frequency)
        logging.info("Applying high-pass filter for close-field voices.")
        enhanced_audio = apply_high_pass_filter(audio_data, audio.frame_rate, 5000)  # High-pass cutoff at 5000 Hz
    else:
        raise ValueError("Invalid distance field specified: must be 'far', 'mid', or 'close'.")

    # Enhance low-frequency transmission
    logging.info("Enhancing low-frequency transmission.")
    enhanced_audio = apply_low_pass_filter(enhanced_audio, audio.frame_rate, low_freq_enhance)

    # Save the enhanced audio to the output file
    enhanced_audio_segment = pydub.AudioSegment(
        enhanced_audio.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )
    enhanced_audio_segment.export(output_file, format="wav")
    logging.info(f"Enhanced audio saved to {output_file}")

    # Log the changes in CSV
    log_header = ["file", "distance_field", "low_freq_enhance", "output", "timestamp"]
    file_exists = os.path.isfile('audio_enhancement_log.csv')
    with open('audio_enhancement_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(log_header)
        writer.writerow([
            input_file,
            distance_field,
            low_freq_enhance,
            output_file,
            datetime.now().isoformat(timespec="seconds"),
        ])
        logging.info(f"Changes logged to audio_enhancement_log.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance audio for far, mid, or close-field voices.")
    parser.add_argument("input", type=str, help="Input audio file path.")
    parser.add_argument("output", type=str, help="Output audio file path.")
    parser.add_argument("low_freq_enhance", type=int, help="Low-frequency enhancement (Hz).")
    parser.add_argument("distance_field", type=str, choices=['far', 'mid', 'close'], help="Distance field to enhance: 'far', 'mid', or 'close'.")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze voice segments with simple AI heuristics and log results.",
    )

    args = parser.parse_args()

    enhance_audio(args.input, args.output, args.low_freq_enhance, args.distance_field, analyze=args.analyze)
