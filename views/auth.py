import calendar
import datetime

import jwt
from flask_restx import Resource, Namespace
from flask import request, abort
from models import User, UserSchema
from setup_db import db
import hashlib


auth_ns = Namespace('auth')
secret = 's3cR$eT'
algo = 'HS256'

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        if None in [username, password]:
            abort(400)

        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401


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

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 201


    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token', None)
        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get('username')

        user = db.session.query(User).filter(User.username == username).first()

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

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 201