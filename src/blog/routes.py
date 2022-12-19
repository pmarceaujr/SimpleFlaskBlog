from src.blog import blog_app
from flask import *
from src.blog.models import *


@blog_app.route('/index')
def index():  # put application's code here
    return render_template('index.html')


@blog_app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@blog_app.route('/css')
def css():  # put application's code here
    return render_template('css.html')
