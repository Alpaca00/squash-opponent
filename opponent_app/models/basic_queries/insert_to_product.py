from dataclasses import dataclass
from app import app
from opponent_app.models import db, Product, TShirt


@dataclass
class ProductObj:
    name: str
    price: str



@dataclass
class TShirtObj:
    name: str
    color: str
    size: str
    sex: str
    quantity: int


product_dct = {
    'name': ['Clothes', 'Rackets'],
    'price': [800, 3500]
}

t_shirt_dct = {
    'name': ['Man T-shirt', 'Woman T-shirt', 'Child T-shirt'],
    'color': ['black', 'white', 'red', 'blue', 'yellow', 'green'],
    'size': ['XL', 'L', 'M', 'S', 'XS'],
    'quantity': [1, 2, 3, 4, 5]
}



def product_factory(product, name):
    with app.app_context():
        product_obj = product(name="Clothes", price="800")
        product_model = name(name="Child T-shirt", color="red",
                             sex="Child", size="XS", quantity=5
                             )
        p = Product(name=product_obj.name, price=product_obj.price)
        m = TShirt(name=product_model.name, color=product_model.color,
                   sex=product_model.sex, size=product_model.size,
                   quantity=product_model.quantity
                   )
        p.t_shirts.append(m)
        db.session.add(p)
        db.session.add(m)
        db.session.commit()


product_factory(ProductObj, TShirtObj)
