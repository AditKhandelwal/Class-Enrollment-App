# Configuration settings 
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///enrollment.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'placeholder-secret-key'
