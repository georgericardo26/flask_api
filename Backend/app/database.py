from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
current_app = None


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return db
