from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

from dao.model.movie import Usefull_scheme
from implemented import user_service

user_ns = Namespace('')

@user_ns.route('/users/')
class User_Login(Resource):
    def get(self):
        all_users = user_service.get_all()
        return jsonify(Usefull_scheme(many=True).dump(all_users))


@user_ns.route('/auth/')
class User_Auth(Resource):
    def post(self):
        request_json = request.json
        if request_json is None:
            abort(401)
        tokens = user_service.get_access_token(request_json)
        return jsonify(tokens)

    def put(self):
        request_json = request.json
        if request_json is None:
            abort(401)
        tokens = user_service.update_access_token(request_json)
        return jsonify(tokens)