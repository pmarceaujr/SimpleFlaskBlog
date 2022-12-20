import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import *
from flask_login import *
from flask_bcrypt import *

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'blog_app.login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()
ckeditor = CKEditor()


def create_app(config_type):
    blog_fapp = Flask(__name__)

    # Set config settings from the config file
    configuration = os.path.join(os.getcwd(), 'config', f'{config_type}.py')
    blog_fapp.config.from_pyfile(configuration)

    # initialize dependencies
    db.init_app(blog_fapp)
    bootstrap.init_app(blog_fapp)
    login_manager.init_app(blog_fapp)
    bcrypt.init_app(blog_fapp)
    ckeditor.init_app(blog_fapp)

    # register each blueprint
    from src.blog import blog_app
    blog_fapp.register_blueprint(blog_app)

    return blog_fapp
