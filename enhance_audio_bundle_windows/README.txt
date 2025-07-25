Enhance Audio Bundle for Windows and Linux

This bundle contains:
- enhance_audio.py: Python script to extract and enhance far-field soft voice from a video.
- run_enhance.bat: Windows batch file to install dependencies and run the script.
- README.txt: This file.

Prerequisites:
- Python 3.x installed.
- MoviePy and SciPy dependencies.

Usage on Windows:
1. Place '1750865130332.MP4' and this bundle in the same directory.
2. Unzip the bundle.
3. Double-click 'run_enhance.bat' or run it in Command Prompt.
4. The script will output 'enhanced_audio_final.wav'.

Usage on Linux/Mac:
1. Install dependencies:
   pip install numpy scipy moviepy
2. Run:
   python3 enhance_audio.py
