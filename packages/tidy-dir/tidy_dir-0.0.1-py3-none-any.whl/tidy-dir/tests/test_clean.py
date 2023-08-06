import os
from tidy_dir.clean import clean_directory


def _test_clean_directory_file_moved(setup_test_directory):
    # Arrange
    test_dir = setup_test_directory

    # Act
    clean_directory(test_dir)

    # Assert
    assert not os.path.exists(
        os.path.join(test_dir, "source_directory_1", "file1.txt")
    )
    assert not os.path.exists(
        os.path.join(test_dir, "source_directory_1", "file2.txt")
    )
    assert os.path.exists(
        os.path.join(test_dir, "source_directory_2", "file1.txt")
    )
    assert os.path.exists(
        os.path.join(test_dir, "source_directory_2", "file2.txt")
    )

    # Verify the contents of the moved files
    with open(os.path.join(test_dir, "source_directory_2", "file1.txt")) as f:
        assert f.read() == "Test file 1"
    with open(os.path.join(test_dir, "source_directory_2", "file2.txt")) as f:
        assert f.read() == "Test file 2"
