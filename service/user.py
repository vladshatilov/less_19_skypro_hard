import base64
import calendar
import datetime
import hashlib

import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT, PWD_HASH_ALGO, JWT_ALGO
from dao.user import UserDAO



class UserService:
    def __init__(self, dao: UserDAO):
        self.user_dao = dao

    def get_one(self,username):
        return self.user_dao.get_one(username)

    def get_all(self):
        return self.user_dao.get_all()

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).hex()

    def get_access_token(self,json_obj):
        username = json_obj.get('username', None)
        password = json_obj.get('password', None)
        if None in [username, password]:
            abort(401)

        user = self.get_one(username)

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = self.get_hash(password)
        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }
        secret = PWD_HASH_SALT
        algo = JWT_ALGO

        expired_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30.0)
        data['exp'] = calendar.timegm(expired_date.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def update_access_token(self,json_obj):
        refresh_token = json_obj.get("refresh_token")
        if refresh_token is None:
            abort(400)

        secret = PWD_HASH_SALT
        algo = JWT_ALGO
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")
        user = self.get_one(username)

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201


def auth_required(func):
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers:
            abort(401)
        try:
            token_to_check = request.headers['Authorization'].split('Bearer ')[-1]
            res = jwt.decode(token_to_check, PWD_HASH_SALT,algorithms=[JWT_ALGO])
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers:
            abort(401)
        try:
            token_to_check = request.headers['Authorization'].split('Bearer ')[-1]
            user = jwt.decode(token_to_check, PWD_HASH_SALT, algorithms=[JWT_ALGO])
            role = user.get('role')
            if role != 'admin':
                abort(401)
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)

        return func(*args, **kwargs)

    return wrapper