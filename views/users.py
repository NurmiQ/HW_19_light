from flask_restx import Resource, Namespace
from flask import request
from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200


    def post(self):
        req_json = request.json
        new_user = User(**req_json)

        db.session.add(new_user)
        db.session.commit()
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        r = db.session.query(User).get(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200


    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204


    def delete(self, uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204

