import pytest
from wbutils import (get_wb_directory, get_artifacts_directory, get_temp_directory,
                     set_wb_directory, set_artifacts_directory, set_temp_directory)


def test_get_wb_directory():
    assert isinstance(get_wb_directory(), str)


def test_get_artifacts_directory():
    assert isinstance(get_artifacts_directory(), str)


def test_get_temp_directory():
    assert isinstance(get_temp_directory(), str)


def test_set_wb_directory():
    new_wb_directory = './.wb'
    set_wb_directory(new_wb_directory)
    assert get_wb_directory() == new_wb_directory


def test_set_artifacts_directory():
    new_artifacts_directory = './.artifacts'
    set_artifacts_directory(new_artifacts_directory)
    assert get_artifacts_directory() == new_artifacts_directory


def test_set_temp_directory():
    new_temp_directory = './.tmp'
    set_temp_directory(new_temp_directory)
    assert get_temp_directory() == new_temp_directory
