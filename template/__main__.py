import logging
from flask import Flask
from template import db
from template.lib import utils, config, log
from template.wsgiapi import register_wsgi_api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


setup()
register_wsgi_api(app)
wsgi_report = utils.get_report(app)
log.LOGGER.info("WSGI summary:\n%s", wsgi_report)

def main():
    app.run(debug=True)
    return

if __name__ == "__main__":
    main()
