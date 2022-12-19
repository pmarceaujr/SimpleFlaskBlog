from flask import Blueprint
blog_app = Blueprint('blog_app', __name__, template_folder='templates', static_folder='static')
from src.blog import routes  # to avoid circular imports