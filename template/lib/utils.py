from operator import itemgetter


def list_wsgi_routes(app):
    basic_methods = ["GET", "POST", "PUT", "DELETE"]
    routes = []  # url, func_path
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        vf = app.view_functions[rule.endpoint]
        routes.append(
            {
                "url": rule.rule,
                "methods": ", ".join(
                    set(rule.methods).intersection(basic_methods)
                ),
                "function": "%s.%s" % (vf.__module__, vf.__name__),
            }
        )
    return routes


def gen_wsgi_report(wsgi_routes):
    # calc report width
    col_wsgi_url_width = max([*[len(x["url"]) for x in wsgi_routes], 16])
    col_wsgi_methods_width = max(
        [*[len(x["methods"]) for x in wsgi_routes], 6]
    )
    col_wsgi_function_width = max(
        [*[len(x["function"]) for x in wsgi_routes], 16]
    )

    body_tmpl = (
        "| %-{url_width}s | %-{method_width}s | %-{func_width}s |".format(
            url_width=col_wsgi_url_width,
            method_width=col_wsgi_methods_width,
            func_width=col_wsgi_function_width,
        )
    )
    lines = []
    br = (
        "+"
        + "-" * (col_wsgi_url_width + 2)
        + "+"
        + "-" * (col_wsgi_methods_width + 2)
        + "+"
        + "-" * (col_wsgi_function_width + 2)
        + "+"
    )
    # header
    lines.append(br)
    lines.append(body_tmpl % ("Url", "Method", "Code Path"))
    lines.append(br)
    # body
    for route in sorted(wsgi_routes, key=itemgetter("url")):
        lines.append(
            body_tmpl % (route["url"], route["methods"], route["function"])
        )
    # footer
    lines.append(br)
    return "\n".join(lines)


def get_report(app):
    routes = list_wsgi_routes(app)
    return gen_wsgi_report(routes)
