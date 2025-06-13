from flask import Blueprint

service_mechanics_bp = Blueprint("service_mechanics_bp", __name__)

from . import routes
