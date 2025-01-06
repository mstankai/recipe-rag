import keyring
import yaml

def get_api_key(key_name: str) -> str:
    """
    Get the API key from the Keyring.

    Args:
        key_name (str): Name of the APIkey in the Keyring.

    Raises:
        ValueError: If the API key is not found in the Keyring.

    Returns:
        str: The API key.
    """
    api_key = keyring.get_password("system", key_name)
    if api_key is None:
        raise ValueError("API key not found in Keyring!")
    return api_key


def read_yaml(path: str) -> dict:
    """
    Get dict from a yaml file

    Args:
        path (str): Path to the yaml file.

    Returns:
        dict: The yaml file as a dict.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)
