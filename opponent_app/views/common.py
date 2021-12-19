import calendar
from datetime import datetime
import humanize
from flask import render_template
from flask_login import current_user
from opponent_app.models import db, Member, UserMember


def count_members(query: db) -> dict:
    ordinary_members = []
    for value in map(list, query):
        ordinary_members.append(value[0])
    count_members_every_tour = dict(
        (x, ordinary_members.count(x))
        for x in set(ordinary_members)
        if ordinary_members.count(x) >= 1
    )
    return count_members_every_tour


def render_content_tournaments(
    history: db.query_expression, render_html: str, query: db.query_expression
) -> render_template:
    tournaments_history_lst = []
    modals_ids = []
    tournament_members = Member.query.join(UserMember).all()
    size_tournaments = len(history)
    if size_tournaments >= 1:
        for i in history:
            convert_dt = datetime.strptime(i.member_date, "%Y-%m-%dT%H:%M")
            full_month = calendar.month_name[int(convert_dt.date().month)]
            day_ = humanize.naturaldate(convert_dt.day)
            time_ = humanize.naturaltime(convert_dt.time())
            modals_ids.append([i.id])
            tournaments_history_lst.append(
                [
                    full_month,
                    day_,
                    time_,
                    i.member_category,
                    i.member_title,
                    i.member_city,
                    i.member_district,
                    i.member_phone,
                    i.member_quantity,
                    i.user_account.name,
                    size_tournaments,
                    i.id,
                ]
            )
    return render_template(
        render_html,
        cur=current_user,
        tournaments=tournaments_history_lst,
        modals_ids=modals_ids,
        members=tournament_members,
        count_members=count_members(query=query),
    )
