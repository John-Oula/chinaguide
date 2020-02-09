from flask import Flask

#from flask.ext.uploads import  UploadSet,configure_uploads,IMAGES
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import os
app = Flask(__name__)
UPLOAD_FOLDER = "/videos"
from flask_blog.config import Config

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#mysql://root:@qwerty1234!@localhost/CHINAGUIDE
from flask_blog.users.routes import users
from flask_blog.posts.routes import posts
from flask_blog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

from flask_blog.models import *







