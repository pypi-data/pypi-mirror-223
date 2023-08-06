from __future__ import annotations
import os

PYTORCH_FRAMEWORK = 'pytorch'
TENSORFLOW_FRAMEWORK = 'tensorflow'
DEFAULT_FRAMEWORK = PYTORCH_FRAMEWORK


def set_framework(framework: str = DEFAULT_FRAMEWORK):
    os.environ['WBUTILS_FRAMEWORK'] = framework


def get_framework():
    if 'WBUTILS_FRAMEWORK' in os.environ:
        return os.environ['WBUTILS_FRAMEWORK']
    else:
        return DEFAULT_FRAMEWORK
