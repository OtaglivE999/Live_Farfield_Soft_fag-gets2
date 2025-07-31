Zoom H6 GPU Transcriber
=======================

This tool performs real-time transcription of Zoom H6 audio using the Faster Whisper model.

Setup
-----
1. From the repository root install the common dependencies:
   ```bash
   pip install -r ../../../requirements.txt
   ```
2. Install the Faster Whisper package which provides GPU support:
   ```bash
   pip install faster-whisper
   ```

Usage
-----
Run the script directly or use the provided batch file:
```bash
python live_transcribe_zoomh6_gpu.py
```

The configuration at the top of the script sets
`COMPUTE_TYPE="float32"` and `DEVICE_TYPE="cuda"` to leverage the GPU.
If you encounter an error such as:
```
RuntimeError: CUDA failed with error CUDA driver version is insufficient for CUDA runtime version
```
your system may not have compatible CUDA drivers. Edit the script to
use the CPU instead:
```python
COMPUTE_TYPE = "int8"   # or "float32"
DEVICE_TYPE = "cpu"
```
Rerun the command and transcription should start using the CPU.
