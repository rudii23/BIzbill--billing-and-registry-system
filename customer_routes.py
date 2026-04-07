from flask import Blueprint, jsonify, request

from models import Customer, db


customer_bp = Blueprint("customers", __name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_json_body():
    data = request.get_json(silent=True)
    if data is None:
        return None, error_response("Request body must be valid JSON.", 400)
    return data, None


@customer_bp.route("/customers", methods=["POST"])
def create_customer():
    data, error = parse_json_body()
    if error:
        return error

    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    email = data.get("email")

    if not name:
        return error_response("Customer name is required.", 400)
    if not phone:
        return error_response("Customer phone is required.", 400)

    if email is not None:
        email = str(email).strip() or None

    customer = Customer(name=name, phone=phone, email=email)
    db.session.add(customer)
    db.session.commit()

    return jsonify(
        {
            "message": "Customer created successfully.",
            "customer": customer.to_dict(),
        }
    ), 201


@customer_bp.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.order_by(Customer.id.asc()).all()
    return jsonify([customer.to_dict() for customer in customers])


@customer_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found.", 404)
    return jsonify(customer.to_dict())


@customer_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found.", 404)

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully."})
