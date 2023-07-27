from __future__ import annotations

from pathlib import Path

import pytest

from file_tree_check.identifierEngine import IdentifierEngine


@pytest.fixture
def test_path():
    return Path(__file__).parent / "test_data"


@pytest.mark.parametrize(
    "prefix_file_with_parent_directory, expected",
    ([False, "_T1w.nii.gz"], [True, "_T1w.nii.gz"]),
)
def test_identifierEngine(test_path, prefix_file_with_parent_directory, expected):
    identifier = IdentifierEngine(
        file_expression="_.*$", directory_expression="^.*-", check_file=True
    )

    assert (
        identifier.get_identifier(
            test_path / "dataset1" / "sub-01" / "anat" / "sub-01_T1w.nii.gz",
            parent=prefix_file_with_parent_directory,
            file_tree=None,
        )
        == expected
    )


@pytest.mark.parametrize(
    "prefix_file_with_parent_directory, expected",
    ([False, "sub-01_T1w.nii.gz"], [True, "sub-01_T1w.nii.gz"]),
)
def test_identifierEngine_unmatchable_regex(test_path, prefix_file_with_parent_directory, expected):
    """When the regex is not matched the entire filename is used as identifier."""
    identifier = IdentifierEngine(
        file_expression="impossible_expression",
        directory_expression="^impossible_expression",
        check_file=True,
    )

    assert (
        identifier.get_identifier(
            test_path / "dataset1" / "sub-01" / "anat" / "sub-01_T1w.nii.gz",
            parent=prefix_file_with_parent_directory,
            file_tree=None,
        )
        == expected
    )


def test_identifierEngine_error(test_path):
    identifier = IdentifierEngine(
        file_expression="_.*$", directory_expression="^.*-", check_file=True
    )
    with pytest.raises(TypeError, match="Path is not a file nor a directory"):
        identifier.get_identifier(
            path=test_path / "sept_6_weekly_report.txt",
            parent=None,
            file_tree=None,
        )
