from app import app


def test_get_order_returns_id():
    client = app.test_client()
    resp = client.get("/orders/42")
    assert resp.get_json()["id"] == "42"
