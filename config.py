import os
from password import password
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{password}@localhost/mechanic_shop'
    DEBUG = True
    
class TestingConfig:
    pass

class ProdcutionConfig:
    pass