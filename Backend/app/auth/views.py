from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from Backend.app import Pagination
from Backend.app.core.models import Parent, Child
from Backend.app.core.schemas import ParentSchema
from Backend.app.database import db


parents_api = Blueprint('parents_api', __name__)


@parents_api.route('parents/', methods=["GET"])
def list_parents():
    query_string_ids = request.args.get("children")

    if query_string_ids:
        try:
            splited_ids = [int(id) for id in query_string_ids.split(",")]
            parents = Parent.query.filter(Parent.children.any(Child.id.in_(splited_ids))).all()
        except Exception:
            return "Querystring contains a invalid format.", HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        parents = Parent.query.all()

    result = Pagination.paginate(parents, ParentSchema(many=True), marshmallow=True)
    result["data"] = result["data"][0]
    return result, HTTPStatus.OK


@parents_api.route('parent/', methods=["POST"])
def create_parent():
    data = request.get_json()
    schema = ParentSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    try:
        created_instance = schema.create_parent(validated_data)
        return jsonify(schema.dump(created_instance).data), HTTPStatus.CREATED
    except Exception:
        return jsonify({"Error": "Something wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR


@parents_api.route('parent/<int:id_parent>/', methods=["GET", "PUT", "PATCH"])
def retrieve_update_parent(id_parent):
    parent = Parent.query.filter_by(id=id_parent).first_or_404()
    schema = ParentSchema()

    if request.method == "GET":
        return jsonify(ParentSchema().dump(parent).data), HTTPStatus.OK

    data = request.get_json()

    if request.method == 'PATCH':
        errors = schema.validate(data, partial=True)
    else:
        errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    updated_parent = schema.update_parent(parent, data)
    return jsonify(ParentSchema().dump(updated_parent).data), HTTPStatus.OK


@parents_api.route('parent/<int:id_parent>/', methods=["DELETE"])
def delete_parent(id_parent):
    parent = Parent.query.filter_by(id=id_parent).first_or_404()
    db.session.delete(parent)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT