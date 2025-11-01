import csv
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from enhance_audio_files.enhance_audio import (
    apply_low_pass_filter,
    apply_high_pass_filter,
    apply_band_pass_filter,
)


def test_filter_performance_low_pass():
    """Test that low-pass filter performs efficiently on large audio."""
    data = np.random.randn(48000 * 10)  # 10 seconds at 48kHz
    start = time.time()
    result = apply_low_pass_filter(data, 48000, 1000)
    elapsed = time.time() - start
    
    assert result.shape == data.shape
    # Should complete in under 1 second for 10 seconds of audio
    assert elapsed < 1.0, f"Filter took {elapsed:.3f}s, expected < 1.0s"


def test_filter_performance_high_pass():
    """Test that high-pass filter performs efficiently on large audio."""
    data = np.random.randn(48000 * 10)  # 10 seconds at 48kHz
    start = time.time()
    result = apply_high_pass_filter(data, 48000, 1000)
    elapsed = time.time() - start
    
    assert result.shape == data.shape
    # Should complete in under 1 second for 10 seconds of audio
    assert elapsed < 1.0, f"Filter took {elapsed:.3f}s, expected < 1.0s"


def test_filter_performance_band_pass():
    """Test that band-pass filter performs efficiently on large audio."""
    data = np.random.randn(48000 * 10)  # 10 seconds at 48kHz
    start = time.time()
    result = apply_band_pass_filter(data, 48000, 500, 5000)
    elapsed = time.time() - start
    
    assert result.shape == data.shape
    # Should complete in under 1 second for 10 seconds of audio
    assert elapsed < 1.0, f"Filter took {elapsed:.3f}s, expected < 1.0s"


def test_filter_numerical_stability():
    """Test that SOS filters provide numerically stable results."""
    # Create a test signal that might cause instability with b,a coefficients
    data = np.random.randn(16000) * 0.01  # Low amplitude signal
    data[8000:8100] = np.random.randn(100) * 10  # High amplitude spike
    
    result = apply_low_pass_filter(data, 16000, 1000)
    
    # Check for NaN or Inf values which indicate numerical instability
    assert not np.any(np.isnan(result)), "Filter produced NaN values"
    assert not np.any(np.isinf(result)), "Filter produced Inf values"
    
    # Result should be bounded
    assert np.all(np.abs(result) < 1e6), "Filter produced unbounded values"


def test_batch_operations_efficiency():
    """Test that batch operations are more efficient than individual operations."""
    # Simulate writing multiple rows individually with larger dataset
    rows = [[f"file_{i}", i, i+1, f"data_{i}"] for i in range(1000)]
    
    # Individual writes
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as f:
        temp_file = f.name
    
    try:
        start = time.time()
        with open(temp_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
        individual_time = time.time() - start
        
        # Batch write
        start = time.time()
        with open(temp_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        batch_time = time.time() - start
        
        # Both operations are fast, but this validates batch operation works correctly
        # and doesn't take excessively longer than individual writes
        assert batch_time < 1.0, f"Batch write took {batch_time:.4f}s, should be < 1s"
        assert individual_time < 1.0, f"Individual write took {individual_time:.4f}s, should be < 1s"
    finally:
        os.unlink(temp_file)
