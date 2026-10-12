from pathlib import Path

import numpy as np
import pytest

from measurements.processing import load_readings
from measurements.selection import select_warm_rounds

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR.parent / "datos"


@pytest.fixture
def readings():
    return load_readings(DATA_DIR / "readings.csv")


def test_exact_threshold_is_included(readings):
    selected = select_warm_rounds(readings, 27)
    np.testing.assert_array_equal(selected, [[27, 29, 25], [28, 30, 26], [29, 31, 27]])


def test_no_match_returns_empty_rows_with_three_columns(readings):
    selected = select_warm_rounds(readings, 100)
    assert selected.shape == (0, 3)


@pytest.mark.parametrize("bad_value", [np.nan, np.inf])
def test_non_finite_readings_are_rejected(readings, bad_value):
    readings[0, 1] = bad_value
    with pytest.raises(ValueError, match="finite readings"):
        select_warm_rounds(readings, 27)


@pytest.mark.parametrize("bad_threshold", [np.nan, np.inf, -np.inf])
def test_non_finite_threshold_is_rejected(readings, bad_threshold):
    with pytest.raises(ValueError, match="Threshold"):
        select_warm_rounds(readings, bad_threshold)


def test_selection_can_change_without_changing_input(readings):
    original = readings.copy()
    selected = select_warm_rounds(readings, 27)
    selected[0, 0] = -100
    np.testing.assert_array_equal(readings, original)
