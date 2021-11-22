import json

from flask import jsonify, request
from flask_restx import Namespace, Resource
from sqlalchemy import desc

from service.user import auth_required, admin_required
from setup_db import db
from implemented import genre_service
from dao.model.movie import usefull_many, usefull_one

# from models import Movies, usefull_many, usefull_one
# from models import Movies, Genres, Directors

genres_ns = Namespace('genres')


@genres_ns.route('/')
class Genres_view(Resource):
    @auth_required
    def get(self):
        all_genres = genre_service.get_all_genres()
        return jsonify(usefull_many.dump(all_genres))

    @admin_required
    def post(self):
        genre_details = request.json
        item = genre_service.create_genre(genre_details)
        return jsonify(usefull_one.dump(item))


@genres_ns.route('/<int:sid>')
class Genre_view(Resource):
    @auth_required
    def get(self, sid):
        one_genre = genre_service.get_one_genre(sid)
        return jsonify(usefull_one.dump(one_genre))

    @admin_required
    def put(self, sid):
        genre_details = request.json
        item = genre_service.update_genre(sid, genre_details)
        return "updated", 201

    @admin_required
    def delete(self, sid):
        item = genre_service.delete_genre(sid)
        return "deleted", 204
