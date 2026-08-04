from flask import Flask, request

from legacy.handler import handle_webhook

app = Flask(__name__)


@app.post("/webhooks/<source>")
def receive(source):
    return handle_webhook(source, request.json)
