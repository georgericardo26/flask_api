import os

from werkzeug.utils import import_string
from flask_rest_paginate import Pagination

CONFIG_NAME_MAPPER = {
    'development': 'Backend.config.DevelopmentConfig',
    'testing': 'Backend.config.TestingConfig',
}


def get_config(config_name=None):
    flask_config_name = os.getenv('FLASK_CONFIG', 'development')
    if config_name is not None:
        flask_config_name = config_name
    return import_string(CONFIG_NAME_MAPPER[flask_config_name])
