from http import HTTPStatus

from flask import Blueprint, jsonify, request, session, url_for
from flask import request

from Backend.app.auth.models import User
from Backend.app.auth.schemas import UserSchema
from Backend.app.database import db


auth_api = Blueprint('auth_api', __name__)


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@auth_api.route('user/', methods='POST')
def create_user():
    data = request.get_json()
    schema = UserSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    try:
        created_instance = schema.create_user(validated_data)
        session['id'] = created_instance.id
        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR
