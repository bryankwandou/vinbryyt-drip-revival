import os

def ensure_dir(directory):
    """Ensures that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def get_env_variable(name, default=None):
    """Safely retrieves an environment variable."""
    value = os.getenv(name, default)
    if value is None and default is None:
        print(f"Warning: Environment variable {name} is not set.")
    return value
