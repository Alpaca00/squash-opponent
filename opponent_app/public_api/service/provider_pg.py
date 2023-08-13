from datetime import datetime
from typing import Union, List, Dict, Any, Optional
from flask_security.utils import hash_password
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from opponent_app.public_api.helpers.error_codes import ErrorCode
from opponent_app.models.user import (
    UserOpponent,
    UserAccount,
    OfferOpponent,
    UserMember,
    Member,
    db,
    user_datastore,
)
from opponent_app.public_api.helpers.exceptions import InternalError


Response = Union[List[Dict[str, Any]], dict]


class ProviderPG:
    """Class for working with the database."""

    @classmethod
    def put_publications(
        cls,
        opponent_item,
        opponent_name: Optional[str] = None,
        offer_item: Optional[OfferOpponent] = None,
    ) -> Dict[str, Any]:
        """Method for creating a dictionary with publications."""
        offers = None
        if offer_item:
            offers = {
                "id": offer_item.id,
                "offer_name": offer_item.offer_name,
                "offer_email": offer_item.offer_email,
                "offer_phone": offer_item.offer_phone,
                "offer_category": offer_item.offer_category,
                "offer_district": offer_item.offer_district,
                "offer_date": offer_item.offer_date,
                "offer_accept": offer_item.offer_accept,
                "offer_message": offer_item.offer_message,
            }
        field = {
            "id": opponent_item.id,
            "opponent_name": opponent_name,
            "opponent_city": opponent_item.opponent_city,
            "opponent_date": opponent_item.opponent_date,
            "opponent_district": opponent_item.opponent_district,
            "opponent_category": opponent_item.opponent_category,
            "opponent_phone": opponent_item.opponent_phone,
            "opponent_offers": offers,
        }
        return field

    @classmethod
    def put_tournaments(
        cls,
        tournament: Optional[UserMember] = None,
        members: Optional[list] = None,
    ):
        """Method for creating a dictionary with tournaments."""
        if tournament:
            tournaments = {
                "tournament": {
                    "tour_title": tournament.member_title,
                    "tour_date": tournament.member_date,
                    "tour_category": tournament.member_category,
                    "tour_city": tournament.member_city,
                    "tour_district": tournament.member_district,
                    "tour_phone": tournament.member_phone,
                    "tour_quantity": tournament.member_quantity,
                    "tour_members": members,
                }
            }
            return tournaments
        else:
            return

    @classmethod
    def get_all_tournaments(cls) -> Response:
        """Method for getting all tournaments."""
        publications: list = []
        try:
            tournaments = UserMember.query.join(Member).all()
            members = Member.query.join(UserMember).all()
            if tournaments:
                for tournament in tournaments:

                    def add(tour, members_list):
                        arr = []
                        for member in members_list:
                            if member.user_member_id == tour.id:
                                arr.append(
                                    {
                                        "name": member.tour_member_name.title(),
                                        "phone": member.tour_member_phone,
                                        "email": member.tour_member_email,
                                        "accept": member.tour_member_accept,
                                    }
                                )
                        return arr

                    publications.append(
                        cls.put_tournaments(
                            tournament=tournament,
                            members=add(tournament, members),
                        )
                    )
                return publications
            else:
                raise InternalError()
        except SQLAlchemyError as e:
            error = str(e.__dict__)
            print(error)
            return ErrorCode.db_connection_error()
        except InternalError:
            return ErrorCode.opponent_not_found()

    @classmethod
    def get_publications(cls, phone: str) -> Response:
        """Method for getting all publications."""
        publications: list = []
        try:
            opponents = (
                UserAccount.query.join(UserOpponent)
                .filter(UserOpponent.opponent_phone == phone)
                .all()
            )
            if opponents:
                for all_opponents in opponents:
                    for item in all_opponents.users_opponent:
                        if item.opponent_phone == phone:
                            publications.append(cls.put_publications(item))
                return publications
            else:
                raise InternalError()
        except SQLAlchemyError as e:
            error = str(e.__dict__)
            print(error)
            return ErrorCode.db_connection_error()
        except InternalError:
            return ErrorCode.opponent_not_found()

    @classmethod
    def get_all_publications(cls, from_date: str, to_date: str) -> Response:
        """Method for getting all publications."""
        publications: list = []
        try:
            if from_date and to_date:
                from_publication = (
                    UserAccount.query.join(UserOpponent)
                    .filter(
                        and_(
                            UserOpponent.opponent_date <= to_date + "T23:59",
                            UserOpponent.opponent_date >= from_date + "T00:00",
                        )
                    )
                    .all()
                )
                if from_publication:
                    for all_opponents in from_publication:
                        for item in all_opponents.users_opponent:
                            if (
                                from_date + "T00:00"
                                <= item.opponent_date
                                <= to_date + "T23:59"
                            ):
                                offers = (
                                    OfferOpponent.query.join(UserOpponent)
                                    .filter_by(id=int(item.id))
                                    .all()
                                )
                                for offer_item in offers:
                                    if offer_item.id is not None:
                                        publications.append(
                                            cls.put_publications(
                                                item,
                                                all_opponents.name,
                                                offer_item,
                                            )
                                        )
                                        break
                                else:
                                    publications.append(
                                        cls.put_publications(
                                            item, all_opponents.name
                                        )
                                    )
                    return publications
                else:
                    raise InternalError()
            else:
                raise InternalError()
        except SQLAlchemyError as e:
            error = str(e.__dict__)
            print(error)
            return ErrorCode.db_connection_error()
        except InternalError:
            return ErrorCode.opponent_not_found()

    @classmethod
    def create_publication(cls, data):
        """Method for creating a publication."""
        try:
            user = UserAccount.query.filter_by(email=data.email).one_or_none()
            if user is None:
                user_datastore.create_user(
                    email=data.email,
                    name=data.name,
                    password=hash_password(data.password),
                    registered_on=datetime.now(),
                    confirmed=False,
                )
                db.session.commit()
            user_ = UserAccount.query.filter_by(email=data.email).first_or_404()
            opponent = UserOpponent(
                opponent_category=data.category,
                opponent_city="Lviv",  # data.city
                opponent_district=data.district,
                opponent_phone=data.phone,
                opponent_date=data.date + "T" + data.time_,
                user_account_id=user_.id,
            )
            db.session.add(opponent)
            db.session.commit()
            return {"Successful": True}
        except SQLAlchemyError as e:
            error = str(e.__dict__)
            print(error)
            return ErrorCode.db_connection_error()
