from app import app
from models import db, Product, Character


def mens_products():
    with app.app_context():
        desc = """
Show your support for The Lviv squash team with this "SQUASH" 
T Shirt which features the teams iconic inscription 
on the chest and the short sleeves and crewneck completes the look.
"""
        c = Character(character_description=desc, sex="Mens", size="L")
        p = Product(name='Show', name_product='Man T-shirt',)

        p.characters.append(c)

        db.session.add(p)
        db.session.add(c)

        db.session.commit()


mens_products()
