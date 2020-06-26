class Config(object):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///circulation-test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
