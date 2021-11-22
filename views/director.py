

import json

from flask import jsonify, request
from flask_restx import Namespace, Resource
from sqlalchemy import desc

from service.user import auth_required, admin_required
from setup_db import db
from implemented import director_service
from dao.model.movie import usefull_many,usefull_one
# from models import Movies, usefull_many, usefull_one
# from models import Movies, Genres, Directors

directors_ns = Namespace('directors')


@directors_ns.route('/')
class Directors_view(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all_directors()
        return jsonify(usefull_many.dump(all_directors))

    @admin_required
    def post(self):
        director_details = request.json
        dir = director_service.create_director(director_details)
        return jsonify(usefull_one.dump(dir))

@directors_ns.route('/<int:sid>')
class Director_view(Resource):
    @auth_required
    def get(self,sid):
        one_director = director_service.get_one_director(sid)
        return jsonify(usefull_one.dump(one_director))


    @admin_required
    def put(self,sid):
        director_details = request.json
        dir = director_service.update_director(sid, director_details)
        return "updated", 201

    @admin_required
    def delete(self,sid):
        mov = director_service.delete_director(sid)
        return "deleted", 204