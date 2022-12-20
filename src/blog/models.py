from src import db, bcrypt
from flask_login import UserMixin
from datetime import datetime as dt
from src import login_manager


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
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_password = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default=dt.utcnow())

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    # class methods belong to a class but are not associated with any class instance
    @classmethod
    def create_user(cls, fname, lname, user_name, email, password):
        user = cls(first_name=fname,
                   last_name=lname,
                   user_name=user_name,
                   email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'))

        db.session.add(user)
        db.session.commit()
        return user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
