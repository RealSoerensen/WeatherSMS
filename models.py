from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    number = db.Column(db.String, primary_key=True)
    city = db.Column(db.String)