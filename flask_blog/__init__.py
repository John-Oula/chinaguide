from flask import Flask

#from flask.ext.uploads import  UploadSet,configure_uploads,IMAGES
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import os
app = Flask(__name__)
UPLOAD_FOLDER = "/videos"
#mysql://root:@qwerty1234!@localhost/CHINAGUIDE
from flask_blog import routes


app.config['SECRET_KEY'] = "yibaizhonguoguide"
app.config['POSTS_PER_PAGE'] = 3

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






