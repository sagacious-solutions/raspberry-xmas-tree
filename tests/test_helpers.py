import helpers
from pathlib import Path

TEST_CONFIG_PATH = Path.cwd() / "tests" / "TEXT_CONFIG_FILE.ini"

TEST_DICT = {"key1": 45, "key2": 99}


def test_can_write_and_read_config_to_file():
    # Create the file, make sure it exists
    helpers.write_config_to_file(TEST_DICT, TEST_CONFIG_PATH)
    assert TEST_CONFIG_PATH.exists()

    # Read from the file, make sure the data is correct
    read_dict = helpers.get_config_from_file(TEST_CONFIG_PATH)
    assert read_dict == TEST_DICT

    # Delete the created test file
    TEST_CONFIG_PATH.unlink()
