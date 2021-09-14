export SPS="Mozi2229659Ozi"
export SECRET_KEY="6Lf0rL8bAAAAAL0YqesYius-y0iQnYThoR-RWd0s"
export EMAIL_USERNAME="squashopponent@gmail.com"
export EMAIL_PASSWORD="changes"

#echo run development app
#FLASK_ENV=development FLASK_APP="opponent_app:create_app" flask run --host=0.0.0.0

#echo production version
#echo run wsgi app heroku
#gunicorn 0.0.0.0:8000 wsgi:app
#gunicorn wsgi:app

#echo run app digital-ocean
#gunicorn -w 1 -b 172.25.0.1:8000 wsgi:app

#echo run tests
#pytest -s -H tests/tests_ui/test_smoke/test_send_offer_to_opponent.py
