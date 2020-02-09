class Config:
    SECRET_KEY = "yibaizhonguoguide"
    POSTS_PER_PAGE= 3
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@qwerty1234!@localhost/postgres'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USERNAME = 'cjohn222.jc@gmail.com'
    MAIL_PASSWORD = 'johncurtis222'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
