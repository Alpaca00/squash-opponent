from dataclasses import dataclass

from flask import Blueprint, request, jsonify

from opponent_app.public_api.helpers.error_codes import ErrorCode
from opponent_app.public_api.helpers.validator import Validator
from opponent_app.public_api.service.provider_pg import ProviderPG

create_publication_api = Blueprint("create_publication_api", __name__)


@dataclass
class DataPublication:
    """Class for data publication."""

    name: str
    password: any
    email: str
    phone: str
    city: str
    district: str
    category: str
    date: str
    time_: str


@create_publication_api.route("", methods=["POST"])
def create_publication():
    """Method for creating a publication."""
    if request.method == "POST":
        data_publication = DataPublication(
            name=request.args.get("name", type=str)
            if request.args.get("name", type=str)
            else 0,
            password=request.args.get("password", type=str),
            email=request.args.get("email", type=str),
            phone=request.args.get("phone", type=str),
            city=request.args.get("city", type=str),
            district=request.args.get("district", type=str),
            category=request.args.get("category", type=str),
            date=request.args.get("date", type=str),
            time_=request.args.get("time", type=str),
        )
        if Validator.validate_create_data_publication(data_publication):
            return jsonify(ProviderPG.create_publication(data_publication))
        else:
            return jsonify(ErrorCode.internal_unhandled_error()), 502
