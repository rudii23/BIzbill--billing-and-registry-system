from datetime import datetime

from flask import Blueprint, jsonify, request

from models import Customer, Invoice, InvoiceItem, Product, db


invoice_bp = Blueprint("invoices", __name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_json_body():
    data = request.get_json(silent=True)
    if data is None:
        return None, error_response("Request body must be valid JSON.", 400)
    return data, None


@invoice_bp.route("/invoices", methods=["POST"])
def create_invoice():
    data, error = parse_json_body()
    if error:
        return error

    customer_id = data.get("customer_id")
    items = data.get("items")

    if customer_id is None:
        return error_response("customer_id is required.", 400)
    if not isinstance(items, list) or not items:
        return error_response("items must be a non-empty list.", 400)

    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found.", 404)

    invoice_items = []
    total_amount = 0.0

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return error_response(f"Item {index} must be an object.", 400)

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if product_id is None:
            return error_response(f"Item {index}: product_id is required.", 400)
        if quantity is None:
            return error_response(f"Item {index}: quantity is required.", 400)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return error_response(f"Item {index}: quantity must be an integer.", 400)

        if quantity <= 0:
            return error_response(f"Item {index}: quantity must be greater than 0.", 400)

        product = Product.query.get(product_id)
        if not product:
            return error_response(f"Item {index}: product not found.", 404)

        total_amount += quantity * product.price
        invoice_items.append(
            InvoiceItem(
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=product.price,
            )
        )

    invoice = Invoice(
        customer_id=customer.id,
        date=datetime.utcnow().isoformat(),
        total_amount=round(total_amount, 2),
    )
    db.session.add(invoice)
    db.session.flush()

    for invoice_item in invoice_items:
        invoice_item.invoice_id = invoice.id
        db.session.add(invoice_item)

    db.session.commit()

    return jsonify(
        {
            "message": "Invoice created successfully.",
            "invoice": invoice.to_dict(include_items=True),
        }
    ), 201


@invoice_bp.route("/invoices", methods=["GET"])
def get_invoices():
    invoices = Invoice.query.order_by(Invoice.id.desc()).all()
    return jsonify([invoice.to_dict() for invoice in invoices])


@invoice_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return error_response("Invoice not found.", 404)
    return jsonify(invoice.to_dict(include_items=True))
