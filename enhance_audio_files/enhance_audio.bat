@echo off
:: Use Python from PATH. Modify this if you need a specific interpreter
set "PYTHON_CMD=python"

:: Path to enhance_audio.py (assumes this BAT is in the same folder)
set "SCRIPT_PATH=%~dp0enhance_audio.py"

:: Ask the user for input and output files
echo Enter the input audio file path:
set /p input_file=
echo Enter the output audio file path:
set /p output_file=
echo Enter the low-frequency enhancement (e.g., 1000 for 1000 Hz):
set /p low_freq_enhance=
echo Enter the distance field ('far', 'mid', 'close'):
set /p distance_field=
echo Analyze voice segments? (y/n):
set /p analyze=

:: Strip surrounding quotes if users added them
set "input_file=%input_file:"=%"
set "output_file=%output_file:"=%"

set analyze_flag=
if /I "%analyze%"=="y" set analyze_flag=--analyze

:: Execute the Python script
%PYTHON_CMD% "%SCRIPT_PATH%" "%input_file%" "%output_file%" %low_freq_enhance% %distance_field% %analyze_flag%

:: Pause to see the result
pause
