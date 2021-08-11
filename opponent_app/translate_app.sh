#pybabel extract -F babel.cfg -o messages.pot . # to extract strings  1!

# pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . #  use "lazy_gettext()" function

#pybabel init -i messages.pot -d translations -l uk # example to translate to German 2!

pybabel compile -d translations # to compile the translations for use 3!

#pybabel update -i messages.pot -d translations # (if create a new messages.pot) - update
