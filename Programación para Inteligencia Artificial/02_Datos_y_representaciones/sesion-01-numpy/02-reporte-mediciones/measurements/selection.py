import math

import numpy as np

from measurements.processing import FloatArray, validate_shape


def select_warm_rounds(readings: FloatArray, threshold: float) -> FloatArray:
    """Return independent rows whose north room reaches the threshold."""
    validate_shape(readings)
    if not np.isfinite(readings).all():
        raise ValueError("Selection requires finite readings")
    if not math.isfinite(threshold):
        raise ValueError("Threshold must be finite")
    warm = readings[:, 0] >= threshold
    return readings[warm]
