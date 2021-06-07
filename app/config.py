import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Tallie1234'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@localhost/TallieImage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']