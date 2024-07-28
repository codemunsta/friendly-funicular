from blackshakara.core.utils.settings import get_settings_from_environment
from blackshakara.core.utils.settings_collections import deep_update

deep_update(globals(), get_settings_from_environment(ENV_PREFIX))  # type: ignore # noqa: F821
