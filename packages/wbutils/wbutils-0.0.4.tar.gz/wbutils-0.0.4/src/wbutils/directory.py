from __future__ import annotations
import os


def set_wb_directory(path_to_dir: str = './.wb'):
    """ Use this function if you don't want to use the default './wandb' directory
    https://docs.wandb.ai/guides/track/environment-variables
    """
    os.makedirs(path_to_dir, exist_ok=True)
    os.environ['WANDB_DIR'] = path_to_dir


def set_artifacts_directory(path_to_dir: str = './.artifacts'):
    """ Use this function if you don't want to use the default './artifacts' directory
    https://docs.wandb.ai/guides/track/environment-variables
    """
    os.makedirs(path_to_dir, exist_ok=True)
    os.environ['WANDB_ARTIFACT_DIR'] = path_to_dir


def set_temp_directory(path_to_dir: str = './.tmp'):
    """ Use this function if you don't want to use the default './artifacts' directory
    https://docs.wandb.ai/guides/track/environment-variables
    """
    os.makedirs(path_to_dir, exist_ok=True)
    os.environ['WBUTILS_TEMP_DIR'] = path_to_dir


def get_wb_directory():
    # https://docs.wandb.ai/guides/track/environment-variables
    if 'WANDB_DIR' in os.environ:
        return os.environ['WANDB_DIR']
    else:
        return './wandb'


def get_artifacts_directory():
    # https://docs.wandb.ai/guides/track/environment-variables
    if 'WANDB_ARTIFACT_DIR' in os.environ:
        return os.environ['WANDB_ARTIFACT_DIR']
    else:
        return './.artifacts'


def get_temp_directory():
    if 'WBUTILS_TEMP_DIR' in os.environ:
        return os.environ['WBUTILS_TEMP_DIR']
    else:
        return './.tmp'
