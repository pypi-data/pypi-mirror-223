import os
import json
from typing import TypeVar, Dict, List, AnyStr
import logging

CONFIG_FILE_NAME = ".tidy-dir-config.json"

ERROR_MESSAGE = (
    'No {0} found in "{1}". Please provide a valid configuration file.'
)

TypeFileExtension = TypeVar("TypeFileExtension", str, bytes)
TypeSourceDir = TypeVar("TypeSourceDir", str, bytes)


def get_config(
    directory: AnyStr,
) -> Dict[TypeSourceDir, List[TypeFileExtension]]:
    source_dir = get_source_dir(directory)
    config_file = os.path.join(source_dir, CONFIG_FILE_NAME)

    if not os.path.isfile(config_file):
        logging.error(ERROR_MESSAGE.format(CONFIG_FILE_NAME, source_dir))
        return None

    with open(config_file) as f:
        config = json.load(f)
    return config


def get_source_dir(directory):
    absolute_path = os.path.abspath(directory)
    return absolute_path
