import datetime
import os
from dataclasses import dataclass
from typing import Optional, final
import telebot
from telebot import types
import logging
from client_api import ApiRequest, JPath

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

token: final = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(token)


@dataclass
class UserCreatePublication:
    name: str
    email: str
    password: str
    phone: str
    city: str
    district: str
    category: str
    date: str
    time_: str


@bot.message_handler(commands=['start'])
def welcome(message):
    picture = open('eng_banner.jpg', 'rb')
    bot.send_photo(message.chat.id, picture)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    opponent = types.KeyboardButton("🕴️ Search opponent")
    tournament = types.KeyboardButton("🏆 Search tournament")
    today = types.KeyboardButton("⌚ Today")
    next_seven_day = types.KeyboardButton("📅 Next 7 days")
    create_publication = types.KeyboardButton("🎫 Create publication")
    markup.add(
        opponent,
        tournament,
        today,
        next_seven_day,
        create_publication
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
        "https://alpaca00.website/api/v1", api_method
    ).get()
    return request


def make_request_create_publication(
    name: str,
    email: str,
    phone: str,
    city: str,
    district: str,
    category: str,
    date: str,
    time: str,
    password: str,
):
    request = ApiRequest(
        "https://alpaca00.website/api/v1",
        f"/create-publication?name={name.title()}&email={email}&phone={phone}&city={city}&district={district.title()}&category={category}&date={date}&time={time}&password={password}"
    ).post()
    return request


def search_opponent(func):
    request = func
    try:
        jpath: callable = lambda glob: JPath(request).values(glob)[0]
        size = len(JPath(request).values('data/*/id'))
        html = ""
        for position in range(0, size):
            html += f"""
        <code style='color: white;'>---------------------------------------</code>
        <code> Day:      {jpath(f'data/{position}/opponent_date')[8:10]}</code>
        <code> Month:    {jpath(f'data/{position}/opponent_date')[5:7]}</code>
        <code> Time:     {jpath(f'data/{position}/opponent_date')[11:16]} - (Kiev)</code>
        <code> Name:     {jpath(f'data/{position}/opponent_name').title()}</code>
        <code> City:     {jpath(f'data/{position}/opponent_city')}</code>
        <code> District: {jpath(f'data/{position}/opponent_district')} - (Sportlife)</code>
        <code> Category: {jpath(f'data/{position}/opponent_category')}</code>
        <code> Phone:    {jpath(f'data/{position}/opponent_phone')}</code>
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
        def render_members(position):
            size_m = len(jpath(f'data/{position}/tournament/tour_members'))
            html_m = ""
            for idx in range(0, size_m):
                html_m += f"""
        <code> Name:   {jpath(f'data/{position}/tournament/tour_members/{idx}/name')}</code>
        <code> Phone:  {jpath(f'data/{position}/tournament/tour_members/{idx}/phone')}</code>
        <code> Email:  {jpath(f'data/{position}/tournament/tour_members/{idx}/email')}</code>
        <code> Accept: {jpath(f'data/{position}/tournament/tour_members/{idx}/accept')}</code>
            """
            return html_m
        html = ""
        for position in range(0, size):
            html += f"""
        <code style='color: black;'>---------------------------------------</code>
        <code> Title:    {jpath(f'data/{position}/tournament/tour_title')}</code>
        <code> Day:      {jpath(f'data/{position}/tournament/tour_date')[8:10]}</code>
        <code> Month:    {jpath(f'data/{position}/tournament/tour_date')[5:7]}</code>
        <code> Time:     {jpath(f'data/{position}/tournament/tour_date')[11:16]} - (Kiev)</code>
        <code> City:     {jpath(f'data/{position}/tournament/tour_city')}</code>
        <code> District: {jpath(f'data/{position}/tournament/tour_district')} - (Sportlife)</code>
        <code> Category: {jpath(f'data/{position}/tournament/tour_category')}</code>
        <code> Phone:    {jpath(f'data/{position}/tournament/tour_phone')}</code>
        <code> Quantity: {jpath(f'data/{position}/tournament/tour_quantity')}</code>
        <code> Members:  {render_members(position)}</code>
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
        elif message.text == '📅 Next 7 days':
            today = datetime.datetime.now().strftime('%d-%m-%Y')
            delta_time = datetime.datetime.now() + datetime.timedelta(days=7)
            to_ = delta_time.strftime('%d-%m-%Y')
            html = search_opponent(make_request(from_=today, to_=to_))
            bot.send_message(message.chat.id, html, parse_mode='html')
        elif message.text == '🏆 Search tournament':
            html = search_tournament(make_request(api_method='/get-all-tournaments'))
            bot.send_message(message.chat.id, html, parse_mode='html')
        elif message.text == '🎫 Create publication':

            markup = types.InlineKeyboardMarkup(row_width=2)
            opponent = types.InlineKeyboardButton(
                'Opponent', callback_data='opponent_resp'
            )
            tournament = types.InlineKeyboardButton(
                'Tournament', callback_data='tournament_resp'
            )
            markup.add(opponent, tournament)
            bot.send_message(
                message.chat.id,
                'Select opponent or tournament',
                reply_markup=markup
            )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        send_msg: bot.send_message = lambda text, parse=None: bot.send_message(
            call.message.chat.id, text, parse
        )
        perform_request: callable = lambda: make_request_create_publication(
                    name=UserCreatePublication.name,
                    email=UserCreatePublication.email,
                    phone=UserCreatePublication.phone,
                    city=UserCreatePublication.city,
                    district=UserCreatePublication.district,
                    category=UserCreatePublication.category,
                    date=UserCreatePublication.date,
                    time=UserCreatePublication.time_,
                    password=UserCreatePublication.password
                )
        if call.message:
            if call.data == 'opponent_resp':
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Quick publication",
                    reply_markup=None
                )
                bot.register_next_step_handler(
                    send_msg('Enter your name: '), get_name_answer
                )
            elif call.data == 'tournament_resp':
                send_msg(
                    text='<code> Coming soon will be possible this publication. </code>',
                    parse='html'
                )
            elif call.data == 'sychivskyi_resp':
                UserCreatePublication.district = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                bot.register_next_step_handler(
                    send_msg('Enter your city: '),
                    get_city_answer
                )
            elif call.data == 'zaliznychnyi_resp':
                UserCreatePublication.district = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                bot.register_next_step_handler(
                    send_msg('Enter your city: '),
                    get_city_answer
                )
            elif call.data == 'shevchenkivskyi_resp':
                UserCreatePublication.district = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                bot.register_next_step_handler(
                    send_msg('Enter your city: '),
                    get_city_answer
                )
            elif call.data == 'PRO_RESP':
                UserCreatePublication.category = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                perform_request()
                send_msg(
                    text="""<code> Successful publication.</code>\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web-app </a>""",
                    parse='html'
                )
            elif call.data == 'M1_RESP':
                UserCreatePublication.category = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                perform_request()
                send_msg(
                    text="""<code> Successful publication.</code>\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web-app </a>""",
                    parse='html'
                )
            elif call.data == 'M2_RESP':
                UserCreatePublication.category = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                perform_request()
                send_msg(
                    text="""<code> Successful publication.</code>\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web-app </a>""",
                    parse='html'
                )
            elif call.data == 'M3_RESP':
                UserCreatePublication.category = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                perform_request()
                send_msg(
                    text="""<code> Successful publication.</code>\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web-app </a>""",
                    parse='html'
                )
            elif call.data == 'AMATEUR_RESP':
                UserCreatePublication.category = call.data.split('_')[0]
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Success",
                    reply_markup=None
                )
                perform_request()
                send_msg(
                    text="""<code> Successful publication.</code>\n<a href="https://alpaca00.website/en/finder/" style='color: #73C6B6 ;text-decoration: none;'> Visit to web-app </a>""",
                    parse='html'
                )
    except Exception as err:
        print(repr(err))


@bot.message_handler(content_types=['text'])
def get_name_answer(message):
    name = message.text
    UserCreatePublication.name = name
    msg = bot.send_message(message.chat.id, 'Enter your email: ')
    bot.register_next_step_handler(msg, get_email_answer)


@bot.message_handler(content_types=['text'])
def get_email_answer(message):
    email = message.text
    UserCreatePublication.email = email
    msg = bot.send_message(
        message.chat.id,
        'Enter your password.\nPassword should be more than 7 symbols. '
    )
    bot.register_next_step_handler(msg, get_password_answer)


@bot.message_handler(content_types=['text'])
def get_password_answer(message):
    password = message.text
    UserCreatePublication.password = password

    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    msg = bot.send_message(
        message.chat.id, 'Enter your phone.\nExample: 380631112223'
    )
    bot.register_next_step_handler(msg, get_phone_answer)


@bot.message_handler(content_types=['text'])
def get_phone_answer(message):
    phone = message.text
    UserCreatePublication.phone = phone
    msg = bot.send_message(
        message.chat.id,
        'Enter date to start game.\nExample: 2022-12-31 '
    )
    bot.register_next_step_handler(msg, get_date_answer)


@bot.message_handler(content_types=['text'])
def get_date_answer(message):
    date = message.text
    UserCreatePublication.date = date
    msg = bot.send_message(
        message.chat.id, 'Enter time to start game.\nExample: 18:00 '
    )
    bot.register_next_step_handler(msg, get_time_answer)


@bot.message_handler(content_types=['text'])
def get_time_answer(message):
    time = message.text
    UserCreatePublication.time = time
    msg = bot.send_message(message.chat.id, 'Select district:')
    bot.register_next_step_handler(msg, get_time_answer)


@bot.message_handler(content_types=['text'])
def get_time_answer(message):
    time = message.text
    UserCreatePublication.time_ = time
    markup = types.InlineKeyboardMarkup(row_width=3)
    sychivskyi = types.InlineKeyboardButton(
        'Sychivskyi - (Sportlife)', callback_data='sychivskyi_resp'
    )
    zaliznychnyi = types.InlineKeyboardButton(
        'Zaliznychnyi - (Sportlife)', callback_data='zaliznychnyi_resp'
    )
    shevchenkivskyi = types.InlineKeyboardButton(
        'Shevchenkivskyi - (Sportlife)', callback_data='shevchenkivskyi_resp'
    )

    markup.add(sychivskyi, zaliznychnyi, shevchenkivskyi)
    bot.send_message(message.chat.id, 'Select district: ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_city_answer(message):
    if message.text != 'Lviv':
        bot.send_message(
            message.chat.id,
            "Sorry, default city is Lviv.",
            parse_mode='html'
        )
        city = 'Lviv'
    else:
        city = message.text
    UserCreatePublication.city = city
    markup = types.InlineKeyboardMarkup(row_width=4)
    pro = types.InlineKeyboardButton('PRO', callback_data='PRO_RESP')
    m1 = types.InlineKeyboardButton('M1', callback_data='M1_RESP')
    m2 = types.InlineKeyboardButton('M2', callback_data='M2_RESP')
    m3 = types.InlineKeyboardButton('M3', callback_data='M3_RESP')
    amateur = types.InlineKeyboardButton('AMATEUR', callback_data='AMATEUR_RESP')

    markup.add(pro, m1, m2, m3, amateur)
    bot.send_message(message.chat.id, 'Select category: ', reply_markup=markup)


bot.polling(none_stop=True)
