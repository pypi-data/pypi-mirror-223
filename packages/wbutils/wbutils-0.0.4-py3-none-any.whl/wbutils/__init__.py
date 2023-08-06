import os
import logging

from wbutils.version import __version__
from wbutils.framework import set_framework, get_framework, PYTORCH_FRAMEWORK, TENSORFLOW_FRAMEWORK, DEFAULT_FRAMEWORK
from wbutils.include import include_files, INCLUDE_STUBS, EXCLUDE_STUBS
from wbutils.directory import (set_wb_directory, get_wb_directory,
                               set_artifacts_directory, get_artifacts_directory,
                               set_temp_directory, get_temp_directory)
from wbutils.io import get_temp_path_to_file, read_json, write_json, read_txt, write_txt, EXTENSION_TO_IO
from wbutils.artifact import create_artifact, load_data_from_artifact
import wbutils.parsing as parsing
import wbutils.parsing.pytorch
import wbutils.keys


_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_path(partial_path=''):
    return os.path.join(_ROOT, partial_path)
