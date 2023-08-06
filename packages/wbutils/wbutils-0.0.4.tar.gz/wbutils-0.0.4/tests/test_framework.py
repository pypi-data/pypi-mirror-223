import pytest
from wbutils import set_framework, get_framework


def test_get_framework():
    assert isinstance(get_framework(), str)


def test_set_framework():
    framework = 'pytorch'
    set_framework(framework)
    assert get_framework() == framework


