# Goal

`load_config()` in `config/loader.py` currently silently falls back to a
default value for any missing key, which has caused deploys with wrong
values to go unnoticed. Make it fail loudly (raise `ConfigError`) on any
missing required key.
