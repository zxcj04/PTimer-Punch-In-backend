from vdr_route.lib import config

# (<url-prefix>, <api-blueprint>)
WSGI_APIS = [
]


def register_wsgi_api(app):
    service = config.CONF.get("app", {}).get("prefix")
    for url_prefix, api_blueprint in WSGI_APIS:
        if service:
            url_prefix = f"{service}{url_prefix}"
        app.register_blueprint(api_blueprint, url_prefix=url_prefix)
