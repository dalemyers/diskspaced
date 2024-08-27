"""Test base types."""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import diskspaced

# pylint: enable=wrong-import-position


def get_test_data(test_name: str) -> tuple[str, str]:
    """Get the test data and expected result for the given test name."""

    data_folder = os.path.join(os.path.dirname(__file__), "data")

    test_data = os.path.join(data_folder, test_name)
    expected_result = os.path.join(data_folder, f"expected_{test_name}")

    return test_data, expected_result


def test_scan_downloads_json():
    """Test scanning the downloads folder and writing the results to a JSON file."""

    with tempfile.TemporaryDirectory() as tempdir:
        output_file = os.path.join(tempdir, "output.json")
        test_input, expected_data_path = get_test_data("test_scan_downloads_json")

        diskspaced.scan(
            test_input,
            output_file,
            diskspaced.OutputFormat.JSON,
            1,
            True,
        )

        with open(
            output_file,
            "rb",
        ) as f:
            result = json.load(f)

        with open(expected_data_path, "rb") as f:
            expected_result = json.load(f)

        # These will change test to test
        del result["free_space"]
        del result["used_space"]
        del expected_result["free_space"]
        del expected_result["used_space"]

        assert result == expected_result


def test_scan_downloads_grand_perspective():
    """Test scanning the downloads folder and writing the results to a GP file."""

    # with tempfile.TemporaryDirectory() as tempdir:
    tempdir = "/Users/dalemyers/Projects/diskspaced/tests"
    output_file = os.path.join(tempdir, "output.xml")
    test_input, expected_data_path = get_test_data("test_scan_downloads_gp")

    diskspaced.scan(
        test_input, output_file, diskspaced.OutputFormat.GRAND_PERSPECTIVE, 1, True, True
    )

    with open(
        output_file,
        "rb",
    ) as f:
        result = json.load(f)

    with open(expected_data_path, "rb") as f:
        expected_result = json.load(f)

    # These will change test to test
    del result["free_space"]
    del result["used_space"]
    del expected_result["free_space"]
    del expected_result["used_space"]

    assert result == expected_result
