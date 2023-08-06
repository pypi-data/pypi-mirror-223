import pytest
from wbutils import get_temp_path_to_file


def test_get_temp_path_to_file():
    filename = 'some-file-name.txt'
    path_to_file = get_temp_path_to_file(filename)
    assert path_to_file.endswith(filename)
