from app import create_app


def test_app_factory_builds():
    app = create_app()
    assert app is not None
