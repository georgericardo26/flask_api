from marshmallow import Schema, fields, post_load, validates, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.app.auth.models import User
from Backend.app.database import db


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=False)
    name = fields.String(required=False)
    created_at = fields.DateTime(dump_only=True)

    def create_user(self, data):
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        name = data.get("name")

        user = User(username=username,
                    password=generate_password_hash(password, method='sha256'),
                    email=email,
                    name=name)

        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user, data):
        user.username = data.get('username', user.name)
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        db.session.commit()
        return user