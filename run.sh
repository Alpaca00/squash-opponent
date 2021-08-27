export SPS="Mozi2229659Ozi"
export SECRET_KEY="6Lf0rL8bAAAAAL0YqesYius-y0iQnYThoR-RWd0s"
export EMAIL_USERNAME="squashopponent@gmail.com"
export EMAIL_PASSWORD="OM2229659"

#FLASK_ENV=development FLASK_APP="opponent_app:create_app" flask run --host=0.0.0.0
echo production version
#echo run wsgi app heroku
#gunicorn -b 0.0.0.0:8000 wsgi:app
gunicorn wsgi:app

