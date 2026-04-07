from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)

    invoices = db.relationship(
        "Invoice",
        backref="customer",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    invoice_items = db.relationship("InvoiceItem", backref="product", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    date = db.Column(
        db.String(30),
        nullable=False,
        default=lambda: datetime.utcnow().isoformat(),
    )
    total_amount = db.Column(db.Float, nullable=False, default=0.0)

    items = db.relationship(
        "InvoiceItem",
        backref="invoice",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self, include_items=False):
        data = {
            "id": self.id,
            "customer_id": self.customer_id,
            "date": self.date,
            "total_amount": self.total_amount,
        }
        if include_items:
            data["customer"] = self.customer.to_dict()
            data["items"] = [item.to_dict() for item in self.items]
        return data


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity": self.quantity,
            "price_at_purchase": self.price_at_purchase,
            "line_total": round(self.quantity * self.price_at_purchase, 2),
        }
