from registry.plugins import register, initialize, _plugins


def test_registration_after_initialize_is_silently_dropped():
    _plugins.clear()
    register("first", lambda: "first-instance")

    snapshot = initialize()

    register("second", lambda: "second-instance")

    names = {name for name, _ in snapshot}
    assert names == {"first"}
    assert "second" not in names
