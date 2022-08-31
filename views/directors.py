from flask import request, jsonify
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from helpers import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.get_json()
        directors_id = data['id']
        director_service.create(data)
        response = jsonify()
        response.status_code = 201
        response.headers['location'] = f'movies/{directors_id}'
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, did):
        data = request.get_json()
        director_service.update(data, did)

        return '', 204

    @admin_required
    def delete(self, did):
        director_service.delete(did)

        return '', 204