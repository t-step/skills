from legacy.handler import handle_webhook


def test_handle_webhook_echoes_keys():
    result = handle_webhook("stripe", {"id": "evt_1"})
    assert result["keys"] == ["id"]
