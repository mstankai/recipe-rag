import keyring

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
