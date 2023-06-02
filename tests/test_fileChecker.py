from __future__ import annotations

from pathlib import Path

import pytest
from file_tree_check.fileChecker import get_total_file_count


@pytest.fixture
def test_path():
    return Path(__file__).parent / "test_data"


@pytest.mark.parametrize("modality, expected", (["anat", 1], ["dwi", 4], ["func", 2]))
def test_get_total_file_count(test_path, modality, expected):
    total_file_count = get_total_file_count(
        path=test_path / "dataset1" / "sub-01" / modality, print_items=True
    )

    assert total_file_count == expected
