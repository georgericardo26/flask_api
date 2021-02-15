import os


class BaseConfig:
    DEBUG = False
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "db.sqlite3"))
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:demo@mysql:3306/storage'
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@db_postgres:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    DOMAIN = 'http://localhost:5000'


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    DOMAIN = 'http://testserver'

    # Use memory for DB files
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
