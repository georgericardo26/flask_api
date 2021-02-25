from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import relationship

from Backend.app.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)


class Client(db.Model):
    name = db.Column(db.String(40))
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')
    client_id = db.Column(db.String(55), unique=True, default=uuid4, primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              default=uuid4().hex)
    client_type = db.Column(db.String(20), default='public')
    _redirect_uris = db.Column(db.Text)
    default_scope = db.Column(db.Text, default='__all__')

    @property
    def user(self):
        return User.query.get(1)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    client = relationship('Client')
    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    scope = db.Column(db.Text)
    expires = db.Column(db.DateTime)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return None


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')
    client = relationship('Client')
    token_type = db.Column(db.String(40), default="password")
    access_token = db.Column(db.String(55), unique=True, index=True,
                              default=uuid4().hex)
    refresh_token = db.Column(db.String(55), unique=True, index=True,
                              default=uuid4().hex)
    expires = db.Column(db.Integer, default=3600)
    scope = db.Column(db.Text, default="read write")

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
