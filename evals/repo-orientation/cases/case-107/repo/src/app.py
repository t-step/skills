from flask import Flask

from src.middleware import rate_limit

app = Flask(__name__)


@app.post("/checkout")
@rate_limit
def checkout(request):
    return {"ok": True}
