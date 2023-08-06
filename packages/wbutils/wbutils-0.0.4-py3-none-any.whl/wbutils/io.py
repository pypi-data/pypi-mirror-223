from __future__ import annotations
import os
import ujson
import tempfile
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset, DataLoader

from .directory import get_temp_directory


def get_temp_path_to_file(filename: str):
    path_to_tempdir = tempfile.mktemp(dir=get_temp_directory())
    os.makedirs(path_to_tempdir, exist_ok=True)
    return os.path.join(path_to_tempdir, filename)


def read_json(path_to_file: str):
    with open(path_to_file, 'r') as f:
        data = ujson.load(f)
    return data


def write_json(payload, path_to_file: str, indent=2):
    with open(path_to_file, 'w') as f:
        ujson.dump(payload, f, indent=indent)


def read_txt(path_to_file: str) -> str:
    with open(path_to_file, 'r') as f:
        lines = f.readlines()
    text = ''.join(lines)
    return text


def write_txt(payload, path_to_file: str):
    with open(path_to_file, 'w') as f:
        f.writelines(payload)


EXTENSION_TO_IO = {
    'txt': (read_txt, write_txt),
    'json': (read_json, write_json),
    'pt': (torch.load, torch.save),
    'pth': (torch.load, torch.save)
}
