from flask import Flask
from flask_rest_paginate import Pagination

from Backend.app.utils import get_config


Config = get_config()
db_instance = None
app_instance = None


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

    app.register_blueprint(parents_api, url_prefix='/api/')
    app.register_blueprint(child_api, url_prefix='/api/')

    init_db(app)

    # Pagination
    app_instance = app
    app_instance.config['PAGINATE_PAGE_SIZE'] = 10
    app_instance.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = True

    return app


Pagination = Pagination(app_instance)
