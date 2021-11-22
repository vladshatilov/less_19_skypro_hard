from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from setup_db import db

from dao.model.director import Directors
from dao.model.genre import Genres


class Movies(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    genre = db.relationship('Genres')
    director = db.relationship('Directors')


class Usefull_scheme(Schema):
    id = fields.Int()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()
    genre_name = fields.String()
    director_name = fields.String()
    name = fields.String()
    username = fields.String()
    password = fields.String()
    role = fields.String()
    access_token = fields.String()
    refresh_token = fields.String()

usefull_one = Usefull_scheme()
usefull_many = Usefull_scheme(many=True)