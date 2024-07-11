from blackshakara.core.utils.collections import deep_update
from blackshakara.core.utils.settings import get_settings_from_environment

deep_update(globals(), get_settings_from_environment(ENV_PREFIX))  # type: ignore # noqa: F821
