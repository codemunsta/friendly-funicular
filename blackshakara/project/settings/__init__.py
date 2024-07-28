import os.path
from pathlib import Path
from decouple import config
from split_settings.tools import include, optional

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENV_PREFIX = config("ENV_PREFIX")

LOCAL_SETTINGS_PATH = config("LOCAL_SETTINGS_PATH")

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include("base.py", "logging.py", "application_settings.py", optional(LOCAL_SETTINGS_PATH), "environment_variables.py", "docker.py")
