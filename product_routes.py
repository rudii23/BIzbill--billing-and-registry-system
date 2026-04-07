from flask import Blueprint, jsonify, request

from models import InvoiceItem, Product, db


product_bp = Blueprint("products", __name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_json_body():
    data = request.get_json(silent=True)
    if data is None:
        return None, error_response("Request body must be valid JSON.", 400)
    return data, None


@product_bp.route("/products", methods=["POST"])
def create_product():
    data, error = parse_json_body()
    if error:
        return error

    name = str(data.get("name", "")).strip()
    price = data.get("price")

    if not name:
        return error_response("Product name is required.", 400)
    if price is None:
        return error_response("Product price is required.", 400)

    try:
        price = float(price)
    except (TypeError, ValueError):
        return error_response("Product price must be a number.", 400)

    if price < 0:
        return error_response("Product price cannot be negative.", 400)

    product = Product(name=name, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify(
        {
            "message": "Product created successfully.",
            "product": product.to_dict(),
        }
    ), 201


@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.order_by(Product.id.asc()).all()
    return jsonify([product.to_dict() for product in products])


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return error_response("Product not found.", 404)

    if InvoiceItem.query.filter_by(product_id=product_id).first():
        return error_response(
            "Product cannot be deleted because it is used in an invoice.",
            400,
        )

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully."})
