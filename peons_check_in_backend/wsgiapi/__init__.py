from peons_check_in_backend.lib import config

from .auth import auth_api
from .project import project_api
from .punch import punch_api
from .report import report_api
from .user import user_api

# (<url-prefix>, <api-blueprint>)
WSGI_APIS = [
    ("/auth", auth_api),
    ("/punch", punch_api),
    ("/user", user_api),
    ("/project", project_api),
    ("/report", report_api),
]


def register_wsgi_api(app):
    service = config.CONF.get("app", {}).get("prefix")
    for url_prefix, api_blueprint in WSGI_APIS:
        if service:
            url_prefix = f"{service}{url_prefix}"
        app.register_blueprint(api_blueprint, url_prefix=url_prefix)
