from .customerSchemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import db, Customer
from . import customers_bp
from application.extensions import limiter


@customers_bp.route("/", methods=["POST"])
@limiter.limit("3 per hour") # A client can only attempt to mkae 3 users per hour
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    
    return customer_schema.jsonify(new_customer), 201


@customers_bp.route("/", methods=["GET"])
def get_all_customers():
    all_customers = db.session.scalars(select(Customer)).all()
    
    if not all_customers:
        return jsonify({"Error": "No users found"}), 404
    
    return customers_schema.jsonify(all_customers)




@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    
    single_customer = db.session.get(Customer, id)
    if not single_customer:
        return jsonify({"Error": "User not found"}), 404
    
    return customer_schema.jsonify(single_customer), 200





@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    
    customer= db.session.get(Customer, id)
    
    if not customer:
        return jsonify({"Error": "User not found"}), 404
    try:
        customer_data = customer_schema.load(request.json)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer.name = customer_data["name"]
    customer.email = customer_data["email"]
    customer.phone = customer_data["phone"]
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200
    




@customers_bp.route("/<int:id>", methods=["DELETE"])  
def delete_customer(id):
    
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"Error": "User not found"}), 400
    

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted customer {id}"}), 200