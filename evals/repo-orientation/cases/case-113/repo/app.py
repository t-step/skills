from flask import Flask

from handlers.refund import refund_bp
from handlers.order import order_bp

app = Flask(__name__)
app.register_blueprint(order_bp, url_prefix="/orders")
app.register_blueprint(refund_bp, url_prefix="/refunds")

if __name__ == "__main__":
    app.run()
