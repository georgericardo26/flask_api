from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy

# from Backend.app.auth.models import Token, Grant, User, Client

db = SQLAlchemy()
current_app = None


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # client1 = Client(
    #     name='dev', client_id='dev', client_secret='dev',
    #     _redirect_uris=(
    #         'http://localhost:8000/authorized '
    #         'http://localhost/authorized'
    #     ),
    # )
    #
    # client2 = Client(
    #     name='confidential', client_id='confidential',
    #     client_secret='confidential', client_type='confidential',
    #     _redirect_uris=(
    #         'http://localhost:8000/authorized '
    #         'http://localhost/authorized'
    #     ),
    # )
    #
    # user = User(username='admin')
    #
    # temp_grant = Grant(
    #     user_id=1, client_id='confidential',
    #     code='12345', scope='email',
    #     expires=datetime.utcnow() + timedelta(seconds=100)
    # )
    #
    # access_token = Token(
    #     user_id=1, client_id='dev', access_token='expired', expires_in=0
    # )
    #
    # access_token2 = Token(
    #     user_id=1, client_id='dev', access_token='never_expire'
    # )
    #
    # try:
    #     db.session.add(client1)
    #     db.session.add(client2)
    #     db.session.add(user)
    #     db.session.add(temp_grant)
    #     db.session.add(access_token)
    #     db.session.add(access_token2)
    #     db.session.commit()
    # except:
    #     db.session.rollback()

    return db
