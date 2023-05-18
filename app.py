import marshmallow as marshmallow
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref, relationship
import os
from flask_migrate import Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'stock.db')



db = SQLAlchemy(app) #orm
ma = Marshmallow(app) #object serialization
migrate = Migrate(app, db)

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


@app.cli.command('db_update')
def insert_def():
    description_carbon_steel = "The term carbon steel may also be used in reference to steel which is not stainless steel; " \
                               "in this use carbon steel may include alloy steels. High carbon steel has many different uses such as milling machines, " \
                               "cutting tools (such as chisels) and high strength wires. These applications require a much finer microstructure, which improves the toughness."

    product = Product.query.filter_by(product_id=1).first()
    product.product_description=description_carbon_steel
    db.session.commit()

    desc_stainless_steel = "Stainless steel is an alloy of iron that is resistant to rusting and corrosion. It contains at least 11% chromium and may contain elements such as carbon, " \
                           "other nonmetals and to obtain other desired properties. Stainless steel's resistance to corrosion results from the chromium, which forms a passive film that can " \
                           "protect the material and self-heal in the presence of oxygen"
    product = Product.query.filter_by(product_id=2).first()
    product.product_description = desc_stainless_steel
    db.session.commit()

    neo_desc = "Neoprene (also polychloroprene) is a family of synthetic rubbers that are produced by polymerization of chloroprene.[1] Neoprene exhibits good chemical stability and maintains flexibility over " \
               "a wide temperature range. Neoprene is sold either as solid rubber or in latex form and is used in a wide variety of commercial applications, such as laptop sleeves, orthopaedic " \
               "braces (wrist, knee, etc.), electrical insulation, liquid and sheet-applied elastomeric membranes or flashings, and automotive fan belts"

    product = Product.query.filter_by(product_id=3).first()
    product.product_description=neo_desc
    db.session.commit()

    poly_desc = "Polycarbonates (PC) are a group of thermoplastic polymers containing carbonate groups in their chemical structures. Polycarbonates used in engineering are strong, tough materials, " \
                "and some grades are optically transparent. "

    product = Product.query.filter_by(product_id=6).first()
    product.product_description = poly_desc
    db.session.commit()

    pp_desc = "Polypropylene (PP), also known as polypropene, is a thermoplastic polymer used in a wide variety of applications. It is produced via chain-growth polymerization from the monomer propylene. " \
              "Polypropylene belongs to the group of polyolefins and is partially crystalline and non-polar. Its properties are similar to polyethylene, but it is slightly harder and more heat-resistant. It is a white, " \
              "mechanically rugged material and has a high chemical resistance"

    product = Product.query.filter_by(product_id=5).first()
    product.product_description = pp_desc
    db.session.commit()

    alu_desc = "1100 aluminium alloy is an aluminium-based alloy in the commercially pure wrought family (1000 or 1xxx series). With a minimum of 99.0% aluminium, it is the most heavily alloyed of the 1000 series. " \
               "It is also the mechanically strongest alloy in the series,"

    product = Product.query.filter_by(product_id=7).first()
    product.product_description = alu_desc
    db.session.commit()

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



@app.route('/increase/<int:product_id>', methods=['POST'])
def increase(product_id):
    print('increase triggered')
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        product.product_stock=product.product_stock+1
        db.session.commit()
        print(product.product_stock)
        return jsonify({'success': True, 'yeni_deger': product.product_stock})
    return jsonify({'success': False})


@app.route('/decrease/<int:product_id>', methods=['POST'])
def decrease(product_id):
    print('increase triggered')
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        product.product_stock=product.product_stock-1
        db.session.commit()
        print(product.product_stock)
        return jsonify({'success': True, 'yeni_deger': product.product_stock})
    return jsonify({'success': False})




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
    product_description = Column(String)


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