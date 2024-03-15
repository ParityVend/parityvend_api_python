import os


def env_get(var_name, default):
    """Retrieves an environment variable with a default value.

    Args:
     var_name (str): The name of the environment variable to retrieve.
     default (str): The default value to return if the environment variable
         is not set.

    Returns:
     str: The value of the environment variable if it exists, otherwise
         the default value.
    """
    return os.environ.get(var_name, default)
