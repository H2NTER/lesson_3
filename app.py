from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?charset=utf8'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128))
    price = db.Column(db.Float)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "price")
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)
    def post(self):
        new_product = Product(
            title = request.json["title"],
            price = request.json["price"]
        )
        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product)

class ProductResource(Resource):
    def put(self, id):
        product = Product.query.get_or_404(id)
        if 'title' in request.json:
            product.title = request.json['title']
        if 'price' in request.json:
            product.title = request.json['product']
        db.session.commit()
        return product_schema.dump(product)
    def delete(self, id):
         product = Product.query.get_or_404(id)
         db.session.delete(product)
         db.session.commit()
         return "delete success"



api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:id>')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, host="0.0.0.0", port=5001)