import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from enhance_audio_files.enhance_audio import (
    apply_low_pass_filter,
    apply_high_pass_filter,
    apply_band_pass_filter,
)


def test_low_pass_constant():
    data = np.ones(10000)
    out = apply_low_pass_filter(data, 16000, 1000)
    assert out.shape == data.shape
    # final samples should remain near the original value
    assert np.allclose(out[-100:], 1, atol=1e-3)


def test_high_pass_constant():
    data = np.ones(10000)
    out = apply_high_pass_filter(data, 16000, 1000)
    assert out.shape == data.shape
    # constant component should be largely removed
    assert np.allclose(out[-100:], 0, atol=1e-3)


def test_band_pass_constant():
    data = np.ones(10000)
    out = apply_band_pass_filter(data, 16000, 500, 5000)
    assert out.shape == data.shape
    # band-pass should also remove the DC component
    assert np.allclose(out[-100:], 0, atol=1e-3)
