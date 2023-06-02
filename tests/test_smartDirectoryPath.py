from __future__ import annotations

from pathlib import Path

import pytest
from file_tree_check.smartDirectoryPath import SmartDirectoryPath


@pytest.fixture
def test_path():
    return Path(__file__).parent / "test_data"


@pytest.mark.parametrize("is_last", [False, True])
def test_SmartDirectoryPath(test_path, is_last):
    dir_path = SmartDirectoryPath(path=test_path, parent_smart_path=None, is_last=is_last)
    assert dir_path.dir_count == 2
    assert dir_path.file_count == 1
    assert dir_path.display() == "test_data                                                   \n"
    assert (
        dir_path.displayable() == "test_data                                                   \n"
    )


@pytest.mark.parametrize("is_last", [False, True])
def test_SmartDirectoryPath_one_level(test_path, is_last):
    parent_smart_path = SmartDirectoryPath(path=test_path, parent_smart_path=None, is_last=False)
    dir_path = SmartDirectoryPath(
        path=test_path / "dataset1", parent_smart_path=parent_smart_path, is_last=is_last
    )
    assert dir_path.dir_count == 4
    assert dir_path.file_count == 1

    expected = "dataset1                                                 \n"
    assert dir_path.display() == expected

    if is_last:
        expected = "└── dataset1                                                 \n"
    else:
        expected = "├── dataset1                                                 \n"
    assert dir_path.displayable() == expected
