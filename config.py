import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password/mechanic_shop'
    DEBUG = True
    
class TestingConfig:
    pass

class ProdcutionConfig:
    pass