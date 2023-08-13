from flask import request, jsonify, Blueprint
from opponent_app.public_api.helpers.error_codes import ErrorCode
from opponent_app.public_api.helpers.validator import Validator
from opponent_app.public_api.repr.entities_response import EntityResponse
from opponent_app.public_api.service.provider_pg import ProviderPG


get_user_publications_api = Blueprint("get_user_publications_api", __name__)


@get_user_publications_api.route("/", methods=["GET"])
def get_user_publications() -> jsonify:
    """Method for getting all publications."""
    if request.method == "GET":
        phone = request.args.get("phone_number", type=str)
        if phone.startswith(" "):
            phone = phone.lstrip("+").strip()
        if not Validator.validate_phone_value(phone):
            return jsonify(ErrorCode.parameter_wrong_format(phone)), 404
        else:
            if publication_from_db := ProviderPG.get_publications(phone):
                return jsonify(
                    EntityResponse.user_publications(publication_from_db)
                )
            else:
                return jsonify(ErrorCode.internal_unhandled_error()), 502
