from flask import Flask, jsonify, render_template
from flask_cors import CORS

from models import db
from routes import customer_bp, invoice_bp, product_bp


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def home():
    return jsonify(
        {
            "message": "Billing and Registry System API",
            "endpoints": {
                "customers": ["/customers", "/customers/<id>"],
                "products": ["/products", "/products/<id>"],
                "invoices": ["/invoices", "/invoices/<id>"],
            },
        }
    )


db.init_app(app)
app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
app.register_blueprint(invoice_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
