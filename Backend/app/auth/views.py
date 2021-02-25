from http import HTTPStatus

from flask import Blueprint, jsonify, request, session, url_for
from flask import request

from Backend.app.auth.exceptions import NotFoundError
from Backend.app.auth.models import User
from Backend.app.auth.schemas import UserSchema, ClientSchema, TokenSchema
from Backend.app.database import db
from Backend.app.helpers import check_username_and_password

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('user/', methods=['POST'])
def create_user():
    data = request.get_json()
    schema = UserSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    try:
        created_instance = schema.create_user(validated_data)
        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR


@auth_api.route('application/', methods=['POST'])
def create_application():
    data = request.get_json()
    schema = ClientSchema()
    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    try:
        created_instance = schema.create_client(validated_data)

        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR


@auth_api.route('oauth/token/', methods=['POST'])
def authentication():
    data = request.get_json()
    schema = TokenSchema()
    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    user_checked_instance, user_checked_errors = check_username_and_password(db, User, data)

    if not user_checked_instance:
        return HTTPStatus.NOT_FOUND

    if user_checked_errors:
        return jsonify({"errors": errors}), HTTPStatus.UNAUTHORIZED

    try:
        created_instance = schema.create_token(user_checked_instance, validated_data)
        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED

    # # If the client is not found
    except NotFoundError:
        return jsonify({"Error": "Application not found from client_id provided!"}), HTTPStatus.BAD_REQUEST

    # # If something is wrong
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR
