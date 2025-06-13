from .service_mechanics_schema import service_mechanics_schema, service_mechanic_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import db, ServiceMechanics
from . import service_mechanics_bp


@service_mechanics_bp.route("/<int:ticket_id>/<int:mechanic_id>", methods=["POST"])
def create_service_mechaic(ticket_id, mechanic_id):
    try:
        new_entry = ServiceMechanics(ticket_id=ticket_id, mechanic_id=mechanic_id)
        db.session.add(new_entry)
        db.session.commit()
        
        return service_mechanic_schema.jsonify(new_entry), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 
