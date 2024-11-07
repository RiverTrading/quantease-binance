from pathlib import Path
import os

# Default cache directory
CACHE_DIR = Path.cwd() / ".cache"


def set_cache_dir(path: str):
    """Set the cache directory."""
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    global CACHE_DIR
    CACHE_DIR = Path(path)
