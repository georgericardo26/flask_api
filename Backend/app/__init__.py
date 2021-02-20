from flask import Flask
from flask_oauthlib.provider import OAuth2Provider
from flask_rest_paginate import Pagination

from Backend.app.auth.views import auth_api
from Backend.app.middleware import default_provider, user_config
from Backend.app.utils import get_config


Config = get_config()
# oauth = OAuth2Provider()
db_instance = None
app_instance = None
# Oauth = None


def create_app(config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    from Backend.app.database import init_db
    from Backend.app.core.views.parent_view import parents_api
    from Backend.app.core.views.child_view import child_api

    app = Flask(__name__, **kwargs)

    try:
        app.config.from_object(get_config(config_name))
    except ImportError:
        raise Exception('Invalid Config')

    # if not Oauth:
    # Oauth = default_provider(app)

    init_db(app)
    # oauth.init_app(app)

    app.register_blueprint(parents_api, url_prefix='/api/')
    app.register_blueprint(child_api, url_prefix='/api/')
    # app.register_blueprint(auth_api, url_prefix='/api/')

    # Pagination
    app_instance = app
    app_instance.config['PAGINATE_PAGE_SIZE'] = 10
    app_instance.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = True

    # set Middleware
    # user_config(app)

    return app


Pagination = Pagination(app_instance)
# Oauth = default_provider(app_instance)
