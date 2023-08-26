import os
from pathlib import Path

root = Path(__file__).resolve().parent
config_path = os.environ.get("CONFIG_PATH", os.path.join(root, "config.yml"))
