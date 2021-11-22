import hashlib

from flask import request, abort

from dao.model.movie import Movies
from dao.model.genre import Genres
from dao.model.director import Directors
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self,username):
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        return self.session.query(User).all()

    def get_tokens(self, json_obj):
        pass