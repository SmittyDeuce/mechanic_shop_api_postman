from application.extensions import ma
from application.models import ServiceTickets

class ServiceTickets(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        
ticket_schema = ServiceTickets()
tickets_schema = ServiceTickets(many=True)