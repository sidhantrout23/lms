from datetime import timedelta

class Config:
    SECRET_KEY = 'key123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///onlinelearining.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
