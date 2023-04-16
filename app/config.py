import os
from typing import Dict, Any
import yaml


def read_config(env: str = "CFG_PATH") -> Dict[str, Any]:
    filename = os.environ.get(env)
    if not filename:
        raise FileNotFoundError("Config file not found")

    with open(filename) as file:
        raw = yaml.full_load(file)

    return raw
