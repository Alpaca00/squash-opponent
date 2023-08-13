from flask import request, jsonify, Blueprint

health_api = Blueprint("health_api", __name__)


@health_api.route("/", methods=["GET"])
def check_health():
    """Method for checking health."""
    if request.method == "GET":
        return jsonify({"Check health": "OK"})
