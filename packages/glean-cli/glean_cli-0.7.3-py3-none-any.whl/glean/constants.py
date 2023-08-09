from glean.utils.cli import getenv_bool


GLEAN_DEBUG = getenv_bool("GLEAN_DEBUG")
DEFAULT_CREDENTIALS_FILEPATH = "~/.glean/glean_access_key.json"