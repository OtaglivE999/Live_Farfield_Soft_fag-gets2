LFN Docker Toolkit Extended
==========================

This directory contains helper scripts for analyzing audio files for low-frequency noise (LFN) and ultrasonic peaks.

Setup
-----
1. Install [Python 3](https://www.python.org/downloads/).
2. Install the required Python libraries:

```
pip install -r requirements.txt
```

3. Ensure [`ffmpeg`](https://ffmpeg.org/) is installed and available on your PATH. It is used to convert non‑WAV files to WAV.

Usage
-----
You can run the analyzer directly with Python:

```
python lfn_batch_file_analyzer.py <audio_directory> [--block-duration SECONDS]
```

or use the Windows helper script `run_lfn_batch_analysis.bat` which prompts for a folder and launches the analyzer.

The analyzer accepts **WAV**, **MP3**, **MP4**, and **M4A** files. Non‑WAV inputs are automatically converted before processing. Results are written to `lfn_analysis_results.csv` and spectrogram images are saved to the `spectrograms` folder within the chosen directory.

