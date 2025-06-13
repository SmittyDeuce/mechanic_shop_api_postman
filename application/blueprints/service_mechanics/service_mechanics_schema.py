from application.extensions import ma
from application.models import ServiceMechanics

class ServiceMechanics(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceMechanics
        
service_mechanic_schema = ServiceMechanics()
service_mechanics_schema = ServiceMechanics(many=True)