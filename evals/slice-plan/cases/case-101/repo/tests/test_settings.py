import os
from app.config.settings import Settings


def test_debug_default_false():
    assert Settings().debug is False


def test_max_upload_mb_default():
    assert Settings().max_upload_mb == 10
