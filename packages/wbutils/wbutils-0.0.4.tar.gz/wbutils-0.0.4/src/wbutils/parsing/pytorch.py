from __future__ import annotations

import inspect
import torch
from copy import deepcopy

CONFIG_ITEMS_FROM_STR = {
    'torch.float': torch.float,
    'torch.float32': torch.float32,
    'torch.float64': torch.float64,
    'torch.int': torch.int,
    'torch.int32': torch.int32,
    'torch.int64': torch.int64
}


def parse_wb_config(metadata: dict, cls: type | None = None, extra_remove_keys: tuple[str] = ()) -> dict:
    """ Convert metadata downloaded from W&B to a format that torch.nn.Module can use """
    # Copy because we don't want to modify the input
    config = deepcopy(metadata)

    # Replace 'torch.float32' -> `torch.float32`
    for key, value in config.items():
        if isinstance(value, str) and (value in CONFIG_ITEMS_FROM_STR):
            config[key] = CONFIG_ITEMS_FROM_STR[value]

    # Convert tuple to list
    for key, value in config.items():
        if isinstance(value, list):
            config[key] = tuple(value)

    # Remove keys that are not needed for the `cls`
    if cls is None:
        cls_remove_keys = []
    else:
        cls_argument_names = set(inspect.signature(cls).parameters.keys())
        cls_remove_keys = [key for key in config if key not in cls_argument_names]

    # Remove the keys
    remove_keys = set(list(extra_remove_keys) + cls_remove_keys)
    for key in remove_keys:
        del config[key]
    return config


def get_optimizer_cls(config: dict, key: str = 'optimizer') -> type:
    """ Return the optimizer class from the str-valued optimizer name
    Example
    --------
        get_optimizer_cls({'optimizer': 'Adam'}) -> torch.optim.Adam
    """
    return getattr(torch.optim, config[key])


def get_loss_cls(config: dict, key: str = 'loss_fn') -> type:
    """ Return the loss function class from the str-valued loss function name
    Example
    -------
        get_optimizer_cls({'loss_fn': 'CrossEntropyLoss'}) -> torch.nn.CrossEntropyLoss
    """
    return getattr(torch.nn, config[key])
