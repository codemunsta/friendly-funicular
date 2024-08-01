import os.path
from pathlib import Path
from decouple import config
from split_settings.tools import include, optional

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENV_PREFIX = config("ENV_PREFIX")

LOCAL_SETTINGS_PATH = config("LOCAL_SETTINGS_PATH")

# if not LOCAL_SETTINGS_PATH:
#     # We dedicate local/settings.unittests.py to have reproducible unittest runs
#     LOCAL_SETTINGS_PATH = f'local/settings{".unittests" if is_pytest_running() else ".dev"}.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py", "logging.py", "application_settings.py", optional(LOCAL_SETTINGS_PATH), "environment_variables.py", "docker.py", "restframework.py",
    "third_party_setup.py"
)

# if not is_pytest_running():
#     assert SECRET_KEY is not NotImplemented  # type: ignore # noqa: F821
