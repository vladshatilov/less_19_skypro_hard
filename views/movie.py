

import json

from flask import jsonify, request
from flask_restx import Namespace, Resource
from sqlalchemy import desc

from service.user import auth_required, admin_required
from setup_db import db
from implemented import movie_service
from dao.model.movie import usefull_many,usefull_one
# from models import Movies, usefull_many, usefull_one
# from models import Movies, Genres, Directors

movies_ns = Namespace('movies')


@movies_ns.route('/')
class Movies_view(Resource):
    @auth_required
    def get(self):
        all_movies = movie_service.get_all_movies()
        return jsonify(usefull_many.dump(all_movies))

    @admin_required
    def post(self):
        movie_details = request.json
        mov = movie_service.create_movie(movie_details)
        return jsonify(usefull_one.dump(mov))

@movies_ns.route('/<int:mid>')
class Movie_view(Resource):
    @auth_required
    def get(self,mid):
        one_movie = movie_service.get_one_movie(mid)
        return jsonify(usefull_many.dump(one_movie))

    @admin_required
    def put(self,mid):
        movie_details = request.json
        mov = movie_service.update_movie(mid, movie_details)
        return "updated", 201

    @admin_required
    def delete(self,mid):
        mov = movie_service.delete_movie(mid)
        return "deleted", 204