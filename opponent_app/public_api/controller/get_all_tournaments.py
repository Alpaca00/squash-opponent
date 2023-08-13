from flask import Blueprint, request, jsonify
from opponent_app.public_api.helpers.error_codes import ErrorCode
from opponent_app.public_api.repr.entities_response import EntityResponse
from opponent_app.public_api.service.provider_pg import ProviderPG

get_all_tournaments_api = Blueprint("get_all_tournaments_api", __name__)


@get_all_tournaments_api.route("/", methods=["GET"])
def get_all_publications():
    """Method for getting all publications."""
    if request.method == "GET":
        if publication_from_db := ProviderPG.get_all_tournaments():
            return jsonify(EntityResponse.user_publications(publication_from_db))
        else:
            return jsonify(ErrorCode.internal_unhandled_error()), 502
