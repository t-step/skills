def handle_webhook(source: str, payload: dict) -> dict:
    return {"source": source, "received": True, "keys": list(payload.keys())}
