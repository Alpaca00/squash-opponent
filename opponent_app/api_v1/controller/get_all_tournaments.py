from flask import Blueprint, request, jsonify
from opponent_app.api_v1.helpers.error_codes import ErrorCode
from opponent_app.api_v1.repr.entities_response import EntityResponse
from opponent_app.api_v1.service.provider_pg import ProviderPG

get_all_tournaments_api = Blueprint("get_all_tournaments_api", __name__)


@get_all_tournaments_api.route("/", methods=["GET"])
def get_all_publications():
    if request.method == "GET":
        if publication_from_db := ProviderPG.get_all_tournaments():
            return jsonify(
                EntityResponse.user_publications(publication_from_db)
            )
        else:
            return jsonify(ErrorCode.internal_unhandled_error()), 502
