import json

from src.config import load_config


def test_load_config_missing_file_raises(tmp_path):
    missing = tmp_path / "nope.json"
    try:
        load_config(str(missing))
        assert False, "should have raised"
    except FileNotFoundError:
        pass
