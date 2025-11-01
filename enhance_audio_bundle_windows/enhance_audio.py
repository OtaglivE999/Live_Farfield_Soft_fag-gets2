import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
import moviepy.editor as mp
from tqdm import tqdm

# Load video and extract audio
video = mp.VideoFileClip("1750865130332.MP4")
video.audio.write_audiofile("extracted_audio.wav")

# Load audio
rate, data = wavfile.read("extracted_audio.wav")
data = data.astype(np.float32)
# Normalize once, not per chunk
max_val = np.max(np.abs(data))
if max_val > 0:
    data /= max_val

# Bandpass filter: 300–3400 Hz (use SOS format for numerical stability)
sos = butter(10, [300, 3400], btype='bandpass', fs=rate, output='sos')

# Process in larger chunks (5s instead of 1s for better efficiency)
chunk_size = rate * 5
chunks = []

for i in tqdm(
    range(0, len(data), chunk_size),
    desc="Processing",
    unit="chunk",
):
    chunk = data[i:i + chunk_size]
    # Apply filter using sosfilt (more stable than lfilter)
    filtered = sosfilt(sos, chunk)
    # Pre-emphasis filter
    emphasized = np.append(filtered[0], filtered[1:] - 0.97 * filtered[:-1])
    # Normalize chunk
    chunk_max = np.max(np.abs(emphasized))
    if chunk_max > 0:
        emphasized /= chunk_max
    chunks.append((emphasized * 32767).astype(np.int16))

# Concatenate and save
final_audio = np.concatenate(chunks)
wavfile.write("enhanced_audio_final.wav", rate, final_audio)
print("Enhanced audio saved as 'enhanced_audio_final.wav'")
