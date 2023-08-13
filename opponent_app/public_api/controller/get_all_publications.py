from flask import request, jsonify, Blueprint

from opponent_app.public_api.helpers.error_codes import ErrorCode
from opponent_app.public_api.helpers.validator import Validator
from opponent_app.public_api.repr.entities_response import EntityResponse
from opponent_app.public_api.service.provider_pg import ProviderPG

get_all_publications_api = Blueprint("get_all_publications_api", __name__)


@get_all_publications_api.route("/", methods=["GET"])
def get_all_publications():
    """Method for getting all publications."""
    if request.method == "GET":
        from_date = request.args.get("from_date", type=str)
        to_date = request.args.get("to_date", type=str)
        check_date: Validator.validate_date_value = (
            lambda date: Validator.validate_date_value(date)
        )
        if not check_date(from_date) or not check_date(to_date):
            return (
                jsonify(
                    ErrorCode.parameter_wrong_format(f"{from_date}, {to_date}")
                ),
                404,
            )
        if publication_from_db := ProviderPG.get_all_publications(
            check_date(from_date), check_date(to_date)
        ):
            return jsonify(EntityResponse.user_publications(publication_from_db))
        else:
            return jsonify(ErrorCode.internal_unhandled_error()), 502
