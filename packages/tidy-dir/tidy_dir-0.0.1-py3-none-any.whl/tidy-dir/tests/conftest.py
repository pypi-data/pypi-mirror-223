import os
import shutil
import json
import tempfile
import pytest
from tidy_dir.config import CONFIG_FILE_NAME


@pytest.fixture
def setup_test_directory():
    # Create a temporary test directory
    test_dir = tempfile.mkdtemp()

    # Create test files in the source directories
    file1 = os.path.join(test_dir, "source_directory_1", "file1.txt")
    file2 = os.path.join(test_dir, "source_directory_1", "file2.txt")
    os.makedirs(os.path.dirname(file1), exist_ok=True)
    os.makedirs(os.path.dirname(file2), exist_ok=True)

    with open(file1, "w") as f:
        f.write("Test file 1")
    with open(file2, "w") as f:
        f.write("Test file 2")

    # Create the configuration file
    config = {"source_directory_2": [".txt"]}
    config_file = os.path.join(test_dir, CONFIG_FILE_NAME)

    with open(config_file, "w") as f:
        json.dump(config, f)

    yield test_dir

    # Clean up the test directory
    shutil.rmtree(test_dir)
