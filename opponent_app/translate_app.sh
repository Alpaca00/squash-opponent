#pybabel extract -F babel.cfg -o messages.pot .

#pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

#pybabel init -i messages.pot -d translations -l uk

pybabel compile -d translations

#pybabel update -i messages.pot -d translations
