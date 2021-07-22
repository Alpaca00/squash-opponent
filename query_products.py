from app import app
from models import db, Product, TShirt

# def mens_products():
#     with app.app_context():
#         desc = """
# Show your support for The Lviv squash team with this "SQUASH"
# T Shirt which features the teams iconic inscription
# on the chest and the short sleeves and crewneck completes the look.
# """
#         c = Character(character_description=desc, sex="Mens", size="L")
#         p = Product(name='Show', name_product='Man T-shirt',)
#
#         p.characters.append(c)
#
#         db.session.add(p)
#         db.session.add(c)
#
#         db.session.commit()
#
#
# # mens_products()
#
#
# def woman_products():
#     with app.app_context():
#         desc = """
# Show your support for The Lviv squash team with this "SQUASH"
# T Shirt which features the teams iconic inscription
# on the chest and the short sleeves and crewneck completes the look.
# """
#         c2 = Character(character_description=desc, sex="Woman", size="S")
#         p2 = Product(name='TEAM', name_product='Woman T-shirt',)
#
#         p2.characters.append(c2)
#
#         db.session.add(p2)
#         db.session.add(c2)
#
#         db.session.commit()
#
#
# # woman_products()
#
#
# def child_products():
#     with app.app_context():
#         desc = """
# Show your support for The Lviv squash team with this "SQUASH"
# T Shirt which features the teams iconic inscription
# on the chest and the short sleeves and crewneck completes the look.
# """
#         c3 = Character(character_description=desc, sex="Child", size="XS")
#         p3 = Product(name='SQUASH', name_product='Child T-shirt',)
#
#         p3.characters.append(c3)
#
#         db.session.add(p3)
#         db.session.add(c3)
#
#         db.session.commit()
#
#
# child_products()


def child_products():
    with app.app_context():

        c3 = TShirt(name='squash', color='red', size='L', sex='man', quantity=2)
        p3 = Product(name='man', price='800')

        p3.t_shirts.append(c3)

        db.session.add(p3)
        db.session.add(c3)

        db.session.commit()


child_products()
