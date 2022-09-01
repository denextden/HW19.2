from flask import request, jsonify
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service, auth_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        result = UserSchema(many=True).dump(users)
        return result, 200

    def post(self):
        req_json = request.json
        user = user_service.create_user(req_json)
        if user.username not in req_json:
            return UserSchema().dump(user), 201
        return 'такой пользователь уже существует', 400


@user_ns.route('/<int:uid>')
class UsersView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        result = UserSchema().dump(user)
        return result, 200


