import json
from pathlib import Path
from config import log


def write_config_to_file(config: dict, filename: str = "config.ini"):
    """Writes the current device config to a file for storage incase of system restart

    Args:
        config (dict): Dictionary holding values for device configuration
        filename (str, optional): filename to hold config in. Defaults to "config.ini".
    """
    config_json = json.dumps(config, indent=4)
    with open(filename, "w") as config_file:
        config_file.write(config_json)
        log.info(f"config dumped to {filename}")


def get_config_from_file(filename: str = "config.ini") -> dict:
    """Loads the current config from the config file

    Args:
        filename (str, optional): _description_. Defaults to "config.ini".

    Returns:
        dict: A dict with the current device config
    """
    if not (Path.cwd() / filename).exists():
        return {}

    with open(filename, "r") as config_file:
        config_json = json.load(config_file)
        log.info(f"Config loaded from {filename}\n{config_json}")
        return config_json
