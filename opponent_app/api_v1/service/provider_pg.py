from typing import Union, List, Dict, Any
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from opponent_app.api_v1.helpers.error_codes import ErrorCode
from opponent_app.models.user import UserOpponent, UserAccount, OfferOpponent, UserMember, Member
from opponent_app.api_v1.helpers.exceptions import InternalError

Response = Union[List[Dict[str, Any]], dict]


class ProviderPG:

    @classmethod
    def put_publications(
        cls, opponent_item, opponent_name=None, offer_item=None
    ):
        offers = None
        if offer_item:
            offers = {
                'id': offer_item.id,
                'offer_name': offer_item.offer_name,
                'offer_email': offer_item.offer_email,
                'offer_phone': offer_item.offer_phone,
                'offer_category': offer_item.offer_category,
                'offer_district': offer_item.offer_district,
                'offer_date': offer_item.offer_date,
                'offer_accept': offer_item.offer_accept,
                'offer_message': offer_item.offer_message
            }
        field = {
            'id': opponent_item.id,
            'opponent_name': opponent_name,
            'opponent_city': opponent_item.opponent_city,
            'opponent_date': opponent_item.opponent_date,
            'opponent_district': opponent_item.opponent_district,
            'opponent_category': opponent_item.opponent_category,
            'opponent_phone': opponent_item.opponent_phone,
            'opponent_offers': offers
        }
        return field

    @classmethod
    def put_tournaments(cls, tournament=None, members=None):
        if tournament:
            tournaments = {
                'tournament': {
                    'tour_title': tournament.member_title,
                    'tour_date': tournament.member_date,
                    'tour_category': tournament.member_category,
                    'tour_city': tournament.member_city,
                    'tour_district': tournament.member_district,
                    'tour_phone': tournament.member_phone,
                    'tour_quantity': tournament.member_quantity,
                    'tour_members': members
                }
            }
            return tournaments
        else:
            return

    @classmethod
    def get_all_tournaments(cls) -> Response:
        publications: list = []
        try:
            tournaments = UserMember.query.join(Member).all()
            members = Member.query.join(UserMember).all()
            if tournaments:
                for tournament in tournaments:
                    def add(cup, mem):
                        arr = []
                        for member in mem:
                            if member.user_member_id == cup.id:
                                arr.append(
                                    {
                                        'name': member.tour_member_name.title(),
                                        'phone': member.tour_member_phone,
                                        'email': member.tour_member_email,
                                        'accept': member.tour_member_accept,
                                    }
                                )
                        return arr
                    publications.append(
                        cls.put_tournaments(
                            tournament=tournament,
                            members=add(tournament, members)
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
        publications: list = []
        try:
            opponents = UserAccount.query.join(UserOpponent).filter(
                UserOpponent.opponent_phone == phone
            ).all()
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
        publications: list = []
        try:
            if from_date and to_date:
                from_publication = UserAccount.query.join(UserOpponent).filter(
                    and_(
                        UserOpponent.opponent_date <= to_date+"T23:59",
                        UserOpponent.opponent_date >= from_date+"T00:00"
                    )
                ).all()
                if from_publication:
                    for all_opponents in from_publication:
                        for item in all_opponents.users_opponent:
                            if from_date + "T00:00" <= item.opponent_date <= to_date + "T23:59":
                                offers = OfferOpponent.query.join(UserOpponent)\
                                    .filter_by(id=int(item.id)).all()
                                for offer_item in offers:
                                    if offer_item.id is not None:
                                        publications.append(cls.put_publications(
                                            item, all_opponents.name, offer_item
                                        ))
                                        break
                                else:
                                    publications.append(
                                        cls.put_publications(item, all_opponents.name)
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
