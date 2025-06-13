from .mechanicSchemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import db, Mechanic
from . import mechanic_bp


@mechanic_bp.route("/", methods=["POST"])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
        
        existing= db.session.query(Mechanic).filter_by(email=mechanic_data["email"]).first()
        if existing:
            return jsonify({"error": "Mechanic with this email already exists"}), 409
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    
    return mechanic_schema.jsonify(new_mechanic), 201
    

@mechanic_bp.route("/", methods=["GET"])
def get_all_mechanics():
    try:
        all_mechanics = db.session.scalars(select(Mechanic)).all()
        
        if not all_mechanics:
            return jsonify({"Error": "No users found"}), 404
        
        return mechanics_schema.jsonify(all_mechanics)
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    

@mechanic_bp.route("/<int:id>", methods=["GET"])
def get_mechanic_by_id(id):
    
    single_mechanic = db.session.get(Mechanic, id)
    
    if not single_mechanic:
        return jsonify({"Error": "Mechanic not found"}), 404
    
    return mechanic_schema.jsonify(single_mechanic)





@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    
    single_mechanic = db.session.get(Mechanic, id)
    
    if not single_mechanic:
        return jsonify({"Error": "User not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
        
        
    except ValidationError as e:
        return jsonify(e.messages), 404
        
    
    single_mechanic.name = mechanic_data['name']
    single_mechanic.email = mechanic_data['email']
    single_mechanic.phone =  mechanic_data['phone']
    single_mechanic.salary =  mechanic_data['salary']
    
    db.session.commit()
    return mechanic_schema.jsonify(single_mechanic), 200
    
    
    
@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    single_mechanic  = db.session.get(Mechanic, id)
    
    if not single_mechanic:
        return jsonify({"Error": "Mechanic not  found"}), 404
    
    db.session.delete(single_mechanic)
    db.session.commit()
    
    return jsonify({"message": f"Mechanic with ID {id} has been deleted"}), 200