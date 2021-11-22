from marshmallow import Schema, fields
from setup_db import db

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String)