from application.extensions import ma
from application.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer #using the SQLAlechmy model to create fields used in serial/deserialzation

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)