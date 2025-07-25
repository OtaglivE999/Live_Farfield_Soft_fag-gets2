import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
import moviepy.editor as mp

# Load video and extract audio
video = mp.VideoFileClip("1750865130332.MP4")
video.audio.write_audiofile("extracted_audio.wav")

# Load audio
rate, data = wavfile.read("extracted_audio.wav")
data = data.astype(np.float32)
data /= np.max(np.abs(data))

# Bandpass filter: 300–3400 Hz
sos = butter(10, [300, 3400], btype='bandpass', fs=rate, output='sos')

# Process in small chunks (1s)
chunk_size = rate * 1
chunks = []

for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    filtered = sosfilt(sos, chunk)
    emphasized = np.append(filtered[0], filtered[1:] - 0.97 * filtered[:-1])
    emphasized /= np.max(np.abs(emphasized))
    chunks.append((emphasized * 32767).astype(np.int16))

# Concatenate and save
final_audio = np.concatenate(chunks)
wavfile.write("enhanced_audio_final.wav", rate, final_audio)
print("Enhanced audio saved as 'enhanced_audio_final.wav'")