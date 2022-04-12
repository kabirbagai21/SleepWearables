
from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    auth_token = db.Column(db.String(700))
    refresh_token = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    tokens = db.relationship('Tokens', backref = 'user', uselist = False)




