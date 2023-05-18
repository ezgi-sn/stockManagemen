import marshmallow as marshmallow
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref, relationship
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'stock.db')



db = SQLAlchemy(app) #orm
ma = Marshmallow(app) #object serialization

@app.route('/')
def index():
    categories_list = Category.query.all()
    return render_template('index.html', categories_list=categories_list)



@app.cli.command('db_create')
def create():
    db.create_all()

@app.cli.command('db_drop')
def drop():
    db.drop_all()

@app.cli.command('db_seed')
def seed():
    test_user = User(first_name='ezgi',
                     last_name='sune',
                     e_mail='test@test.com',
                     password='P@ssw0rd')

    steel = Category(category_name = 'steel')
    rubber = Category(category_name = 'rubber')
    plastics = Category(category_name = 'plastics')
    aluminum = Category(category_name = 'aluminum')

    carbon_steel = Product(category_id=1, product_name = 'carbon_steel', product_stock = 10)
    stainless_steel = Product(category_id=1, product_name = 'stainless_steel ',product_stock = 20)

    neoprene_rubber = Product(category_id=2, product_name = 'neoprene_rubber', product_stock = 30)
    silicone_rubber = Product(category_id = 2, product_name = 'silicone_rubber', product_stock = 40)

    polycarbonate = Product(category_id =3, product_name = 'polycarbonate', product_stock = 50)
    polypropylene = Product(category_id = 3, product_name='polypropylene', product_stock = 60)

    aluminum_1100= Product(category_id=4, product_name='aluminum_1100', product_stock =70)

    db.session.add(steel)
    db.session.add(rubber)
    db.session.add(plastics)
    db.session.add(aluminum)

    db.session.add(carbon_steel)
    db.session.add(stainless_steel)
    db.session.add(neoprene_rubber)
    db.session.add(silicone_rubber)
    db.session.add(polypropylene)
    db.session.add(polycarbonate)
    db.session.add(aluminum_1100)

    db.session.add(test_user)
    db.session.commit()
    print('database seeded')

@app.route('/products', methods = ['GET'])
def products():
    products_list = Product.query.all() #returns json
    result = products_schema.dump(products_list) #json.dump
    return jsonify(result)


@app.route('/product', methods = ['GET'])
def product():
    products_list = Category.query.all() #returns json
    return render_template('products.html', products_list=products_list)

@app.route('/product_details/<int:category_id>')

def product_details(category_id:int):
    products_in_category = Product.query.filter_by(category_id=category_id)
    return render_template('categories.html', products_in_category=products_in_category)

#def increase(product_id:int):
#    product=Product.query.filter_by(product_id=product_id)
#    product.product_stock=product.product_stock+1

@app.route('/increase/')

#database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    e_mail = Column(String, unique=True)
    password = Column(String)


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True )
    category_name = Column(String)



class Product(db.Model):
    __tablename__ = 'product'
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    product_name = Column(String)
    product_id = Column(Integer, primary_key=True)
    category = db.relationship("Category", backref=backref("categories"), uselist=False)
    product_stock = Column(Integer)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'e_mail', 'password')


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('category_id', 'category_name')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_name', 'category_id', 'product_stock')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


if __name__ == '__main__':
    app.run()