## func to produce our flask apps
from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.customer import customers_bp
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.service_mechanics import service_mechanics_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #init extensions
    ma.init_app(app)
    db.init_app(app)
    
    
    #register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_mechanics_bp, url_prefix='/service_mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    
    
    
    return app

