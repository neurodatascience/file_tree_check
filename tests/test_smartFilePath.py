from __future__ import annotations

from pathlib import Path

import pytest
from file_tree_check.smartDirectoryPath import SmartDirectoryPath
from file_tree_check.smartFilePath import SmartFilePath


@pytest.fixture
def test_path():
    return Path(__file__).parent / "test_data"


def test_SmartDirectoryPath(test_path):
    dir_path = SmartFilePath(
        path=test_path / "filetree.tree",
        parent_smart_path=SmartDirectoryPath(test_path, parent_smart_path=None, is_last=False),
        is_last=False,
    )
    assert dir_path.display() == "filetree.tree                                            \n"
    assert (
        dir_path.displayable() == "├── filetree.tree                                            \n"
    )
