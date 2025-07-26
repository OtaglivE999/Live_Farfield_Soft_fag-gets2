This project provides a Python script to enhance audio files and optionally analyze any detected voices.

Usage on Windows:
1. Install Python 3 and ensure `python` is on your PATH.
2. Run `pip install -r requirements.txt` to install required libraries.
3. Double-click `enhance_audio.bat` or run it from the command prompt. When prompted:
   - Provide the full path to the input audio file **without quotes**.
   - Provide either a full output file path **or a directory** where the enhanced file will be saved. Quotes are optional.
   - Choose the low-frequency enhancement value (e.g. 875).
   - Choose the distance field (`far`, `mid`, or `close`).
   - Optionally answer `y` to analyze voice segments.

The script works with any format supported by ffmpeg, such as WAV, MP3, MP4,
AAC or M4A. The enhanced file will be stored as `<input name>_enhanced.wav` in
the chosen location. Each run appends a row to `audio_enhancement_log.csv`
describing the parameters used along with a timestamp. When voice analysis is
enabled the detected segments are summarised in `voice_analysis.csv` and a
spectrogram image is saved for each one under the `spectrograms` folder.
Each row in `voice_analysis.csv` records the file name, start and end times,
as well as estimated gender, age range, voice color, the original format,
possible speaker height, a timestamp and the path to the saved spectrogram.
