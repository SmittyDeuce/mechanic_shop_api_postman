from flask import request, jsonify
from marshmallow import ValidationError
from . service_tickets_schemas import ticket_schema, tickets_schema
from . import service_tickets_bp
from application.models import db, ServiceTickets
from sqlalchemy import select
from application.models import Customer, Mechanic, ServiceMechanics
from sqlalchemy.orm import relationship

@service_tickets_bp.route("/<int:customer_id>/<int:mechanic_id>", methods=["POST"])
def create_ticket(customer_id, mechanic_id):
    # Check if the customer exists in the database
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Check if the mechanic exists in the database
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    # Validate incoming JSON payload using the schema
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Create a new service ticket with validated data and customer ID
    ticket = ServiceTickets(**ticket_data, customer_id=customer_id)
    db.session.add(ticket)
    db.session.flush()  # Flush to get ticket.id before commit

    # Create a link between the ticket and the mechanic in the association table
    db.session.add(ServiceMechanics(ticket_id=ticket.id, mechanic_id=mechanic_id))

    # Save both the ticket and the association to the database
    db.session.commit()

    # Return the created ticket as a JSON response
    return jsonify(ticket_schema.dump(ticket)), 201


@service_tickets_bp.route("/<int:ticket_id>/assign_mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    # Get the service ticket and mechanic from DB
    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    # If either doesn't exist, return error
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    # Check if already assigned
    if mechanic in [sm.mechanic for sm in ticket.service_mechanics]:
        return jsonify({"message": "Mechanic already assigned"}), 200

    # Append mechanic via relationship
    ticket.service_mechanics.append(ServiceMechanics(ticket=ticket, mechanic=mechanic))
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}"}), 200


@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    # Fetch the ticket
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Find the matching ServiceMechanics record
    sm_link = next((sm for sm in ticket.service_mechanics if sm.mechanic_id == mechanic_id), None)
    if not sm_link:
        return jsonify({"error": "Mechanic not assigned to this ticket"}), 404

    # Remove the relationship
    db.session.delete(sm_link)
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}"}), 200


@service_tickets_bp.route("/", methods=["GET"])
def get_all_tickets():
    # 1. Query all service tickets from the database
    tickets = db.session.query(ServiceTickets).all()

    # 2. Serialize the list of tickets using the schema
    return jsonify(ticket_schema.dump(tickets, many=True)), 200