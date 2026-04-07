Project Title

Billing and Registry System for Small Business (Backend Only)

Objective

Create a backend system that allows a small business to:

Store customer details
Store product details
Generate and store invoices (bills)
Retrieve stored records

The system should expose REST API endpoints using Flask and SQL.

Tech Stack
Language: Python
Framework: Flask
Database: SQLite
ORM: Flask-SQLAlchemy
IDE: Visual Studio Code
Core Functional Requirements
1. Customer Registry

The system must allow storing customer information.

Fields:

id (integer, primary key)
name (string)
phone (string)
email (string, optional)

Functions:

add customer
view all customers
view single customer
delete customer
2. Product Registry

The system must allow storing product/service details.

Fields:

id (integer, primary key)
name (string)
price (float)

Functions:

add product
view all products
delete product
3. Invoice (Billing)

The system must allow creating a bill.

Fields:

id (integer, primary key)
customer_id (foreign key)
date (auto generated)
total_amount (float)

Invoice must store purchased products.

Invoice Item fields:

id
invoice_id (foreign key)
product_id (foreign key)
quantity (integer)
price_at_purchase (float)

Functions:

create invoice
view invoice
view all invoices
API Endpoints
Customer APIs

POST /customers
Create new customer

GET /customers
Get all customers

GET /customers/<id>
Get customer by ID

DELETE /customers/<id>
Delete customer

Product APIs

POST /products
Create product

GET /products
Get all products

DELETE /products/<id>
Delete product

Invoice APIs

POST /invoices
Create invoice

GET /invoices
Get all invoices

GET /invoices/<id>
Get invoice details including products

Database Schema

Customer table:

id INTEGER PRIMARY KEY
name TEXT
phone TEXT
email TEXT

Product table:

id INTEGER PRIMARY KEY
name TEXT
price REAL

Invoice table:

id INTEGER PRIMARY KEY
customer_id INTEGER
date TEXT
total_amount REAL

InvoiceItem table:

id INTEGER PRIMARY KEY
invoice_id INTEGER
product_id INTEGER
quantity INTEGER
price_at_purchase REAL
Functional Workflow
Create bill workflow
user selects customer
user selects products
user enters quantity
system calculates total price
system stores invoice in database
system returns invoice ID
Non-functional requirements
simple folder structure
modular code
SQLite database file stored locally
JSON request and response format
basic error handling
Folder structure

project/

app.py
models.py
routes/

customer_routes.py
product_routes.py
invoice_routes.py

database.db

Output expectations

The generated backend code should:

run using command:

python app.py

automatically create database tables if not present
expose REST API endpoints
return JSON responses