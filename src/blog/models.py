from src import db
from datetime import datetime as dt


# PUBLICATION TABLE
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(9999), nullable=False)
    # author_id = db.Column(db.String(50), nullable=False, index=True)

    # ESTABLISH A RELATIONSHIP BETWEEN PUBLICATION AND BOOK TABLES
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f'The title is is {self.title}'


# BOOK TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), nullable=False, index=True)
    password = db.Column(db.String(50), nullable=False)
    create_date = db.Column(db.DateTime, default=dt.utcnow())

    def __init__(self, first_name, last_name, username, email, create_date):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.create_date = create_date

    def __repr__(self):
        return f'User: {self.first_name} {self.last_name} {self.username} {self.email} {self.create_date}'
