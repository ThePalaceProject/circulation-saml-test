import os


class Config:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask-sp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SAML_PATH = os.getenv('SAML_PATH')
