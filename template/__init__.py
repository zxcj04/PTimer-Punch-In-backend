import logging
from flask import Flask
from template import db
from template.lib import utils, config, log
from template.wsgiapi import register_wsgi_api
from aclaaa import session
from flask_cors import CORS


def setup():

    conf_dir = "configurations/"

    # config
    conf_file = "config.yaml"
    config.setup(config_dir=conf_dir, config_yaml=conf_file)

    # logger
    log_conf_file = "api.log.yaml"
    log.setup(config_dir=conf_dir, log_config_yaml=log_conf_file)

    # database
    db_conf = config.CONF.get("database", {})
    db_conf["schema"] = config.CONF.get("schema", {})
    db.setup(db_conf)

    # redis session
    session_conf = config.CONF.get("session", {})
    session.setup(session_conf)


# In flask run. The name is imported, automatically detecting an app (app) or factory (create_app).
# https://flask.palletsprojects.com/en/1.1.x/cli/?highlight=flask%20run
def create_app():
    # create app
    app = Flask(__name__)
    CORS(app)

    # Setup
    setup()

    # register api
    register_wsgi_api(app)
    wsgi_report = utils.get_report(app)
    log.LOGGER.info("WSGI summary:\n%s", wsgi_report)

    return app
