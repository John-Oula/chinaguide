import os


UPLOAD_FOLDER = "/videos"
class Config:
    SECRET_KEY = os.environ.get('SECRET')
    POSTS_PER_PAGE= 3
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('db_uri')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USERNAME = 'cjohn222.jc@gmail.com'
    MAIL_PASSWORD = 'johncurtis222'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    UPLOAD_FOLDER = UPLOAD_FOLDER
