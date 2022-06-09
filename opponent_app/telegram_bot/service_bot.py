import datetime
import os
from typing import Optional, final
import telebot
from telebot import types
import logging
from client_api import ApiRequest, JPath

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

token: final = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    picture = open('eng_banner.jpg', 'rb')
    bot.send_photo(message.chat.id, picture)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    opponent = types.KeyboardButton("🕴️ Search opponent")
    tournament = types.KeyboardButton("🏆 Search tournament")
    today = types.KeyboardButton("⌚ Today")
    next_seven_day = types.KeyboardButton("📅 Next 7 day")
    markup.add(
        opponent,
        tournament,
        today,
        next_seven_day
    )
    bot.send_message(
        message.chat.id,
        f"""<code>Hello, {message.from_user.first_name.title()}!</code>\n<code>I'm - <b>{bot.get_me().first_name.upper()}</b>, a bot helps to find an opponent for you.</code>""",
        parse_mode='html', reply_markup=markup
    )


def make_request(
    from_: str = '30-12-2020',
    to_: str = '31-12-2025',
    api_method: Optional[str] = None
):
    if not api_method:
        api_method = f"/get-all-publications?from_date={from_}&to_date={to_}"
    request = ApiRequest(
        "http://127.0.0.1:5000/api/v1", api_method
    ).get()
    return request


def search_opponent(func):
    request = func
    try:
        jpath: callable = lambda glob: JPath(request).values(glob)[0]
        size = len(JPath(request).values('data/*/id'))
        html = ""
        for num in range(0, size):
            html += f"""
        <code style='color: white;'>---------------------------------------</code>
        <code> Day:      {jpath(f'data/{num}/opponent_date')[8:10]}</code>
        <code> Month:    {jpath(f'data/{num}/opponent_date')[5:7]}</code>
        <code> Time:     {jpath(f'data/{num}/opponent_date')[11:16]} - (Kiev)</code>
        <code> Name:     {jpath(f'data/{num}/opponent_name').title()}</code>
        <code> City:     {jpath(f'data/{num}/opponent_city')}</code>
        <code> District: {jpath(f'data/{num}/opponent_district')} - (Sportlife)</code>
        <code> Category: {jpath(f'data/{num}/opponent_category')}</code>
        <code> Phone:    {jpath(f'data/{num}/opponent_phone')}</code>
        <code style='color: white;'>---------------------------------------</code>
        """
        return html + """\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web app </a>"""
    except TypeError:
        return "<code> Nothing to found :: ¯\_(ツ)_/¯ </code>"


def search_tournament(func):
    request = func
    try:
        jpath: callable = lambda glob: JPath(request).values(glob)[0]
        size = len(JPath(request).values('data/*/tournament/tour_date'))
        def render_members(search):
            size_m = len(jpath(f'data/{search}/tournament/tour_members'))
            html_m = ""
            for n in range(0, size_m):
                html_m += f"""
        <code> Name:   {jpath(f'data/{search}/tournament/tour_members/{n}/name')}</code>
        <code> Phone:  {jpath(f'data/{search}/tournament/tour_members/{n}/phone')}</code>
        <code> Email:  {jpath(f'data/{search}/tournament/tour_members/{n}/email')}</code>
        <code> Accept: {jpath(f'data/{search}/tournament/tour_members/{n}/accept')}</code>
            """
            return html_m
        html = ""
        for num in range(0, size):
            html += f"""
        <code style='color: black;'>---------------------------------------</code>
        <code> Title:    {jpath(f'data/{num}/tournament/tour_title')}</code>
        <code> Day:      {jpath(f'data/{num}/tournament/tour_date')[8:10]}</code>
        <code> Month:    {jpath(f'data/{num}/tournament/tour_date')[5:7]}</code>
        <code> Time:     {jpath(f'data/{num}/tournament/tour_date')[11:16]} - (Kiev)</code>
        <code> City:     {jpath(f'data/{num}/tournament/tour_city')}</code>
        <code> District: {jpath(f'data/{num}/tournament/tour_district')} - (Sportlife)</code>
        <code> Category: {jpath(f'data/{num}/tournament/tour_category')}</code>
        <code> Phone:    {jpath(f'data/{num}/tournament/tour_phone')}</code>
        <code> Quantity: {jpath(f'data/{num}/tournament/tour_quantity')}</code>
        <code> Members:  {render_members(num)}</code>
        <code style='color: black;'>---------------------------------------</code>
            """
        return html + """\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web app </a>"""
    except TypeError:
        return "<code> Nothing to found :: ¯\_(ツ)_/¯ </code>"


@bot.message_handler(content_types=['text'])
def imp(message):
    if message.chat.type == 'private':
        if message.text == '🕴️ Search opponent':
            html = search_opponent(make_request())
            bot.send_message(message.chat.id, html, parse_mode='html')
        elif message.text == '⌚ Today':
            today = datetime.datetime.now().strftime('%d-%m-%Y')
            html = search_opponent(make_request(from_=today, to_=today))
            bot.send_message(message.chat.id, html, parse_mode='html')
        elif message.text == '📅 Next 7 day':
            today = datetime.datetime.now().strftime('%d-%m-%Y')
            delta_time = datetime.datetime.now() + datetime.timedelta(days=7)
            to_ = delta_time.strftime('%d-%m-%Y')
            html = search_opponent(make_request(from_=today, to_=to_))
            bot.send_message(message.chat.id, html, parse_mode='html')
        elif message.text == '🏆 Search tournament':
            html = search_tournament(make_request(api_method='/get-all-tournaments'))
            bot.send_message(message.chat.id, html, parse_mode='html')


bot.polling(none_stop=True)
