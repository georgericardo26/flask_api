from datetime import datetime, timedelta

from marshmallow import Schema, fields, post_load, validates, ValidationError, post_dump
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.app.auth.exceptions import NotFoundError
from Backend.app.auth.models import User, Client, Grant, Token
from Backend.app.database import db
from Backend.app.helpers import get_or_create


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


class ClientSchema(Schema):
    client_id = fields.String(dump_only=True)
    client_secret = fields.String(dump_only=True)
    user_id = fields.Integer(required=True, load_only=True)
    scope_in = fields.String(default="read", load_only=True)

    def create_client(self, data):
        user_id = data.get("user_id")
        scope = data.get("scope")

        user = User.query.filter_by(id=user_id).first_or_404()

        try:
            client = get_or_create(db=db, model=Client, user_id=user.id)

            Grant(
                        user_id=user.id, client_id=client.client_id,
                        code='12345', scope=scope,
                        expires=datetime.utcnow() + timedelta(seconds=300)
            )

        except:
            raise Exception("Error to create Client Object")

        db.session.add(client)
        db.session.commit()
        return client


class TokenSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)
    expires = fields.String(dump_only=True)
    token_type = fields.String(dump_only=True)
    scope = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    client_id = fields.String(load_only=True, required=True)
    client_secret = fields.String(load_only=True, required=True)
    username = fields.String(load_only=True, required=True)
    password = fields.String(load_only=True, required=True)

    def create_token(self, user, data):
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")

        client = Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()

        if not client:
            raise NotFoundError()

        token = Token(user_id=user.id, client_id=client.client_id)

        db.session.add(token)
        db.session.commit()

        return token
