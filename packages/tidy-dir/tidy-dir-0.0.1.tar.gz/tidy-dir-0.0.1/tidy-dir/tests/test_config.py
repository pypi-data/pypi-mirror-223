import os
import json
from tidy_dir.config import (
    get_source_dir,
    get_config,
    CONFIG_FILE_NAME,
    ERROR_MESSAGE,
)


def test_get_source_dir_relative():
    # Arrange
    relative_path = "path/to/directory"
    expected_path = os.path.abspath(relative_path)

    # Act
    result = get_source_dir(relative_path)

    # Assert
    assert result == expected_path


def test_get_source_dir_absolute():
    # Arrange
    absolute_path = "/path/to/directory"

    # Act
    result = get_source_dir(absolute_path)

    # Assert
    assert result == absolute_path


def test_get_source_dir_current_directory():
    # Arrange
    current_directory = os.getcwd()

    # Act
    result = get_source_dir(".")

    # Assert
    assert result == current_directory


def test_get_source_dir_nonexistent_directory():
    # Arrange
    nonexistent_directory = "/path/to/nonexistent/directory"

    # Act
    result = get_source_dir(nonexistent_directory)

    # Assert
    assert result == nonexistent_directory


def test_get_source_dir_empty_string():
    # Arrange
    empty_string = ""
    current_directory = os.getcwd()

    # Act
    result = get_source_dir(empty_string)

    # Assert
    assert result == current_directory


def test_get_config(tmp_path):
    # Arrange
    config = {"src": [".py"]}
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(json.dumps(config))

    # Act
    response = get_config(tmp_path)

    # Assert
    assert response == {"src": [".py"]}


def test_get_config_file_not_found(caplog):
    # Arrange
    expected_print = ERROR_MESSAGE.format(
        CONFIG_FILE_NAME, os.path.abspath("src")
    )

    # Act
    get_config("src")

    # Assert
    assert expected_print in caplog.text
