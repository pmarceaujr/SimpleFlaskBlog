import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import *

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_type):
    blog_fapp = Flask(__name__)

    # Set config settings from the config file
    configuration = os.path.join(os.getcwd(), 'config', f'{config_type}.py')
    blog_fapp.config.from_pyfile(configuration)

    # initialize dependancies
    db.init_app(blog_fapp)
    bootstrap.init_app(blog_fapp)

    # register each blueprint
    from src.blog import blog_app
    blog_fapp.register_blueprint(blog_app)

    return blog_fapp
