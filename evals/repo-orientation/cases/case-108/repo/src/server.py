from flask import Flask, jsonify

from src.config import load_config

app = Flask(__name__)
_config = load_config("config.json")


@app.get("/config")
def get_config():
    return jsonify(_config)
