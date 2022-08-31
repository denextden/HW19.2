from flask import request, jsonify
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.get_json()
        genres_id = data['id']
        genre_service.create(data)
        response = jsonify()
        response.status_code = 201
        response.headers['location'] = f'movies/{genres_id}'
        return "", 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        data = request.get_json()
        genre_service.update(data, gid)

        return '', 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)

        return '', 204
