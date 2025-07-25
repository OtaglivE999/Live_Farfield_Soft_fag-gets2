@echo off
REM Ensure to install moviepy in the right Python environment
echo Installing required Python packages...
C:\ProgramData\Anaconda3\Scripts\conda.exe install numpy scipy moviepy -y

REM Run the enhancement script using the correct Anaconda Python executable
C:\ProgramData\Anaconda3\python.exe enhance_audio.py

echo Enhancement complete. Output: enhanced_audio_final.wav
pause
