from flask import Blueprint, g, render_template

about_app = Blueprint("about_app", __name__)


@about_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@about_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@about_app.route("/", methods=["GET"])
def about() -> str:
    """Render about page."""
    if g.lang_code == "en":
        return render_template("about.html")
    else:
        return render_template("about_ua.html")
