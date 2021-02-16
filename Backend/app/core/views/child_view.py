from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from Backend.app import Pagination
from Backend.app.core.models import Parent, Child
from Backend.app.core.schemas import ChildSchema
from Backend.app.database import db


child_api = Blueprint('child_api', __name__)


@child_api.route('children/', methods=["GET"])
def list_children():
    query_string_ids = request.args.get("parents")

    if query_string_ids:
        try:
            splited_ids = [int(id) for id in query_string_ids.split(",")]
            children = Child.query.filter(Child.parents.any(Parent.id.in_(splited_ids))).all()
        except Exception:
            return "Querystring contains a invalid format.", HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        children = Child.query.all()

    result = Pagination.paginate(children, ChildSchema(many=True), marshmallow=True)
    result["data"] = result["data"][0]
    return result, HTTPStatus.OK


# Todo: Endpoint requested in code challenge, but isn't good practice to Rest API
@child_api.route('child/', methods=["POST"])
def create_parent():
    data = request.get_json()
    schema = ChildSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    try:
        created_instance = schema.create_child(validated_data)
        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR


# Todo: Endpoint requested in code challenge, but isn't good practice to Rest API
@child_api.route('child/<int:id_child>/', methods=["GET", "PUT", "PATCH"])
def retrieve_update_parent(id_child):
    child = Child.query.filter_by(id=id_child).first_or_404()
    schema = ChildSchema()

    if request.method == "GET":
        return jsonify(schema.dump(child).data), HTTPStatus.OK

    data = request.get_json()

    if request.method == 'PATCH':
        errors = schema.validate(data, partial=True)
    else:
        errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    updated_parent = schema.update_child(child, data)
    return jsonify(ChildSchema().dump(updated_parent).data), HTTPStatus.OK


# Todo: Endpoint requested in code challenge, but isn't good practice to Rest API
@child_api.route('child/<int:id_child>/', methods=["DELETE"])
def delete_parent(id_child):
    child = Child.query.filter_by(id=id_child).first_or_404()
    db.session.delete(child)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT