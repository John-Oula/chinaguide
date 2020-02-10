from flask import Flask

#from flask.ext.uploads import  UploadSet,configure_uploads,IMAGES
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config
import os
bcrypt= Bcrypt()
mail= Mail()
db= SQLAlchemy()

login_manager = LoginManager()


#mysql://root:@qwerty1234!@localhost/CHINAGUIDE

from flask_blog import db


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app








