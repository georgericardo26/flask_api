from marshmallow import Schema, fields, post_load, validates, ValidationError

from Backend.app.auth.models import User
from Backend.app.database import db


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    email = fields.String(required=False)
    name = fields.String(required=False)
    created_at = fields.DateTime(dump_only=True)

    def create_user(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user, data):
        user.username = data.get('username', user.name)
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        db.session.commit()
        return user