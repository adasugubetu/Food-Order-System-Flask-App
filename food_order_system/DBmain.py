from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import pymysql
from datetime import datetime


hostname = "127.0.0.1"
username = "root"
password = ""
port = 33061
database = "food_order_system"

conex = pymysql.connect(host=hostname, user=username, password=password, port=port)
cursor = conex.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
cursor.close()
conex.close()

DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'
engine = create_engine(DATABASE_URI)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    cart = relationship('Cart', back_populates='user', uselist=False)
    orders = relationship('Order', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    menu_items = relationship('MenuItem', back_populates='category')

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='menu_items')
    cart_items = relationship('CartItem', back_populates='menu_item')

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    user = relationship('User', back_populates='cart')
    cart_items = relationship('CartItem', back_populates='cart', cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    cart = relationship('Cart', back_populates='cart_items')
    menu_item = relationship('MenuItem', back_populates='cart_items')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship('OrderItem', back_populates='order')
    user = relationship('User', back_populates='orders')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    quantity = Column(Integer)
    order = relationship('Order', back_populates='items')
    menu_item = relationship('MenuItem')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def populate_menu():
    categories = {
        "Aperitive si Garnituri": [
            {"name": "Ardei Iuti Verzi",
             "description": "Ardei iuți verzi, picanți și savuroși.",
             "image": "ardei-iuti-verzi.jpg",
             "price": 10.0
             },
            {"name": "Cartofi cu Rozmarin",
             "description": "Cartofi rumeniți cu rozmarin proaspăt.",
             "image": "cartofi-cu-rozmarin.jpg",
             "price": 12.0
             },
            {"name": "Chec Aperitiv cu Roșii Branza Busuioc",
             "description": "Chec aperitiv umplut cu roșii, brânză și busuioc.",
             "image": "chec-aperitiv-cu-rosii-branza-busuioc.jpg",
             "price": 14.0
             },
            {"name": "Crutoane",
             "description": "Crutoane crocante, perfecte pentru supe și salate.",
             "image": "crutoane.jpg",
             "price": 8.0
             },
            {"name": "Fasole Batuta",
             "description": "Fasole batută fin, delicioasă ca aperitiv.",
             "image": "fasole-batuta.jpg",
             "price": 9.0
             },
            {"name": "Hummus",
             "description": "Hummus cremos, ideal pentru dipping sau salate.",
             "image": "hummus.jpg",
             "price": 10.0
             },
            {"name": "Mamaliguta",
             "description": "Mămăliguță tradițională, perfectă ca garnitură.",
             "image": "mamaliguta.jpg",
             "price": 7.0
             },
            {"name": "Mujdei de Usturoi",
             "description": "Mujdei aromat de usturoi, ideal pentru carne și legume.",
             "image": "mujdei-de-usturoi.jpg",
             "price": 6.0
             },
            {"name": "Orez cu Curry",
             "description": "Orez basmati cu curry și condimente.",
             "image": "orez-cu-curry.jpg",
             "price": 20.0
             },
            {"name": "Orez cu Vin",
             "description": "Orez gătit cu vin, perfect ca garnitură.",
             "image": "orez-cu-vin.jpg",
             "price": 15.0
             },
            {"name": "Pachetele de Primavara Sos Sweet Chilli",
             "description": "Pachete de primăvară crocante, servite cu sos sweet chilli.",
             "image": "pachetele-de-primavara-sos-sweet-chilli.jpg",
             "price": 12.0
             },
            {"name": "Paine Alba cu Maia",
             "description": "Pâine albă cu maia, perfectă pentru orice masă.",
             "image": "paine-alba-cu-maia.jpg",
             "price": 8.0
             },
            {"name": "Paine Integrala cu Maia",
             "description": "Pâine integrală cu maia, sănătoasă și gustoasă.",
             "image": "paine-integrala-cu-maia.jpg",
             "price": 9.0
             },
            {"name": "Pilaf cu Ciuperci",
             "description": "Pilaf aromat cu ciuperci proaspete.",
             "image": "pilaf-cu-ciuperci.jpg",
             "price": 12.0
             },
            {"name": "Piure de Cartofi",
             "description": "Piure fin de cartofi, perfect ca garnitură.",
             "image": "piure-de-cartofi.jpg",
             "price": 7.0
             },
            {"name": "Platou Bunatati Asortate",
             "description": "Platou cu bunătăți asortate, ideal pentru orice ocazie.",
             "image": "platou-bunatati-asortate.jpg",
             "price": 25.0
             },
            {"name": "Platou Bunatati din Carne",
             "description": "Platou bogat cu bunătăți din carne, perfect pentru petreceri.",
             "image": "platou-bunatati-din-carne.jpg",
             "price": 30.0
             },
            {"name": "Platou Fritto Misto",
             "description": "Platou cu diverse bunătăți prăjite, ideal pentru aperitive.",
             "image": "platou-fritto-misto.jpg",
             "price": 28.0},
            {"name": "Quesadilla",
             "description": "Quesadilla cu brânză și legume, perfectă ca aperitiv.",
             "image": "quesadilla.jpg",
             "price": 14.0
             },
            {"name": "Quiche Lorraine",
             "description": "Quiche Lorraine clasic, cu bacon și brânză.",
             "image": "quiche-lorraine.jpg",
             "price": 16.0
             },
            {"name": "Saratele de Post",
             "description": "Sârățele dulci de post, perfecte pentru orice masă.",
             "image": "saratele-de-post.jpg",
             "price": 6.0
             },
            {"name": "Sos de Usturoi",
             "description": "Sos de usturoi cremos, ideal pentru carne și legume.",
             "image": "sos-de-usturoi.jpg",
             "price": 5.0
             },
            {"name": "Sos Ranchero",
             "description": "Sos ranchero aromat, perfect pentru diverse bunătăți.",
             "image": "sos-ranchero.jpg",
             "price": 7.0
             },
            {"name": "Sos Sweet Chilli",
             "description": "Sos sweet chilli dulce și picant, ideal pentru dipping.",
             "image": "sos-sweet-chilli.jpg",
             "price": 8.0
             },
            {"name": "Trigoane cu Branza și Marar",
             "description": "Trigoane umplute cu brânză și mărar proaspăt.",
             "image": "trigoane-cu-branza-si-marar.jpg",
             "price": 10.0
             }
        ],
        "Bunatati din Carne": [
            {"name": "Ardei Umpluti Porc",
             "description": "Ardei umpluți cu carne de porc și legume proaspete.",
             "image": "ardei-umpluti-porc.jpg",
             "price": 14.0
             },
            {"name": "Aripioare Crocante de Pui",
             "description": "Aripioare de pui crocante, perfecte pentru gustări.",
             "image": "aripioare-crocante-de-pui.jpg",
             "price": 12.0
             },
            {"name": "Cannelloni cu Sos Bolognese",
             "description": "Cannelloni umplute cu carne și sos Bolognese savuros.",
             "image": "cannelloni-cu-sos-bolognese.jpg",
             "price": 16.0
             },
            {"name": "Chiftele de Porc",
             "description": "Chiftele suculente din carne de porc, aromate și delicioase.",
             "image": "chiftele-de-porc.jpg",
             "price": 13.0
             },
            {"name": "Chiftele de Pui",
             "description": "Chiftele de pui fraged, gătite la perfecție.",
             "image": "chiftele-de-pui.jpg",
             "price": 12.0
             },
            {"name": "Chiftelute de Curcan",
             "description": "Chifteluțe din carne de curcan, savuroase și ușoare.",
             "image": "chiftelute-de-curcan.jpg",
             "price": 14.0
             },
            {"name": "Chiftelute Marinate de Curcan",
             "description": "Chifteluțe de curcan marinate pentru un gust intens.",
             "image": "chiftelute-marinate-de-curcan.jpg",
             "price": 15.0
             },
            {"name": "Chiftelute Marinate de Porc",
             "description": "Chifteluțe de porc marinate cu condimente speciale.",
             "image": "chiftelute-marinate-de-porc.jpg",
             "price": 15.0
             },
            {"name": "Copanele la Cuptor",
             "description": "Copanele gătite la cuptor, crocante și gustoase.",
             "image": "copanele-la-cuptor.jpg",
             "price": 16.0
             },
            {"name": "Curry de Pui cu Orez",
             "description": "Curry de pui aromat servit cu orez proaspăt.",
             "image": "curry-de-pui-cu-orez.jpg",
             "price": 17.0
             },
            {"name": "Escalop de Pui pe Pat de Piure",
             "description": "Escalop de pui servit pe un pat cremos de piure de cartofi.",
             "image": "escalop-de-pui-pe-pat-de-piure.jpg",
             "price": 18.0
             },
            {"name": "Friptura de Curcan la Cuptor",
             "description": "Friptură de curcan suculentă, gătită perfect la cuptor.",
             "image": "friptura-de-curcan-la-cuptor.jpg",
             "price": 20.0
             },
            {"name": "Friptura de Porc la Cuptor",
             "description": "Friptură de porc aromată, gătită la perfecție.",
             "image": "friptura-de-porc-la-cuptor.jpg",
             "price": 19.0
             },
            {"name": "Gujoane de Pui cu Sos de Usturoi",
             "description": "Gujoane de pui suculente servite cu sos de usturoi cremos.",
             "image": "gujoane-de-pui-cu-sos-de-usturoi.jpg",
             "price": 17.0
             },
            {"name": "Gulas de Vita",
             "description": "Gulas tradițional de vită, bogat în arome.",
             "image": "gulas-de-vita.jpg",
             "price": 19.0
             },
            {"name": "Lasagna",
             "description": "Lasagna clasică cu straturi de paste, carne și sos bechamel.",
             "image": "lasagna.jpg",
             "price": 18.0
             },
            {"name": "Mancare de Cartofi cu Afumatura",
             "description": "Mâncare delicioasă de cartofi cu afumătură.",
             "image": "mancare-de-cartofi-cu-afumatura.jpg",
             "price": 16.0
             },
            {"name": "Mancare de Spanac cu Piept de Pui",
             "description": "Mâncare sănătoasă de spanac cu piept de pui suculent.",
             "image": "mancare-de-spanac-cu-piept-de-pui.jpg",
             "price": 17.0
             },
            {"name": "Mazare cu Piept de Pui",
             "description": "Mazăre proaspătă cu bucăți de piept de pui.",
             "image": "mazare-cu-piept-de-pui.jpg",
             "price": 15.0
             },
            {"name": "Ostropel de Pui pe pat de Piure",
             "description": "Ostropel de pui servit pe un pat cremos de piure de cartofi.",
             "image": "ostropel-de-pui-pe-pat-de-piure.jpg",
             "price": 18.0
             },
            {"name": "Paprikas Ardelenesc de Pui",
             "description": "Paprikas tradițional ardeleneasc de pui, bogat în arome.",
             "image": "paprikas-ardelenesc-de-pui.jpg",
             "price": 19.0
             },
            {"name": "Pilaf cu Piept de Pui",
             "description": "Pilaf aromat cu piept de pui fraged.",
             "image": "pilaf-cu-piept-de-pui.jpg",
             "price": 16.0
             },
            {"name": "Pui Boieresc",
             "description": "Pui boieresc suculent, gătit cu legume și condimente.",
             "image": "pui-boieresc.jpg",
             "price": 20.0
             },
            {"name": "Pui Crocant cu Susan",
             "description": "Pui crocant servit cu sos de susan aromatic.",
             "image": "pui-crocant-cu-susan.jpg",
             "price": 17.0
             },
            {"name": "Pui Gratinat cu Cartofi și Ciuperci",
             "description": "Pui gratinat cu cartofi și ciuperci, cremos și gustos.",
             "image": "pui-gratinat-cu-cartofi-si-ciuperci.jpg",
             "price": 19.0
             },
            {"name": "Pui in Stil Turcesc cu Orez",
             "description": "Pui în stil turcesc servit cu orez aromatic.",
             "image": "pui-in-stil-turcesc-cu-orez.jpg",
             "price": 18.0
             },
            {"name": "Pui Shanghai",
             "description": "Pui Shanghai suculent și crocant, perfect pentru gustări.",
             "image": "pui-shanghai.jpg",
             "price": 16.0
             },
            {"name": "Sarmalute din Porc",
             "description": "Sarmalute tradiționale din carne de porc, gătite lent.",
             "image": "sarmalute-din-porc.jpg",
             "price": 17.0
             },
            {"name": "Sarmalute din Pui",
             "description": "Sarmalute delicioase din carne de pui, aromate cu condimente.",
             "image": "sarmalute-din-pui.jpg",
             "price": 16.0
             },
            {"name": "Sarmalute in Foi de Vita",
             "description": "Sarmalute fragede în foi de vită, gătite cu grijă.",
             "image": "sarmalute-in-foi-de-vita.jpg",
             "price": 18.0
             },
            {"name": "Snitel Panko",
             "description": "Șnițel crocant Panko, servit cu sosuri delicioase.",
             "image": "snitel-panko.jpg",
             "price": 17.0
             },
            {"name": "Snitele din Curcan",
             "description": "Șnițele din curcan, ușoare și sănătoase.",
             "image": "snitele-din-curcan.jpg",
             "price": 18.0
             },
            {"name": "Snitele Panko de Pui",
             "description": "Șnițel de pui crocant cu pesmet Panko.",
             "image": "snitele-panko-de-pui.jpg",
             "price": 17.0
             },
            {"name": "Snitelele de Pui ale Copilariei",
             "description": "Șnițele de pui ale copilăriei, gust autenticului casnic.",
             "image": "snitelele-de-pui-ale-copilariei.jpg",
             "price": 16.0
             },
            {"name": "Tigaie Picanta de Pui",
             "description": "Tigaie picantă de pui, perfectă pentru cei care iubesc aromele intense.",
             "image": "tigaie-picanta-de-pui.jpg",
             "price": 18.0
             },
            {"name": "Tocanita Munteneasca",
             "description": "Tocănită muntenească de vită, bogată în arome tradiționale.",
             "image": "tocanita-munteneasca.jpg",
             "price": 19.0
             }
        ],
        "Bunatati vegetariene": [
            {"name": "Cannelloni cu Spanac",
             "description": "Cannelloni umplute cu spanac proaspăt.",
             "image": "cannelloni-cu-spanac.jpg",
             "price": 14.0
             },
            {"name": "Chiftelute cu Dovlecei și Branza",
             "description": "Chifteluțe delicioase cu dovlecei și brânză.",
             "image": "chiftelute-cu-dovlecei-si-branza.jpg",
             "price": 12.0
             },
            {"name": "Chiftelute din Ciuperci și Zucchini",
             "description": "Chifteluțe savuroase din ciuperci și zucchini.",
             "image": "chiftelute-din-ciuperci-si-zucchini.jpg",
             "price": 13.0
             },
            {"name": "Ciulama de Ciuperci de Padure cu Mamaliga",
             "description": "Ciulama cremoasă de ciuperci cu mămăligă.",
             "image": "ciulama-de-ciuperci-de-padure-cu-mamaliga.jpg",
             "price": 15.0
             },
            {"name": "Curry de Naut",
             "description": "Curry aromat de naut.",
             "image": "curry-de-naut.jpg",
             "price": 11.0
             },
            {"name": "Ghiveci Calugaresc",
             "description": "Ghiveci tradițional cu legume și condimente.",
             "image": "ghiveci-calugaresc.jpg",
             "price": 14.0
             },
            {"name": "Iahnie de Fasole",
             "description": "Iahnie consistentă de fasole.",
             "image": "iahnie-de-fasole.jpg",
             "price": 10.0
             },
            {"name": "Legume Natur cu Unt",
             "description": "Legume proaspete gătite în unt.",
             "image": "legume-natur-cu-unt.jpg",
             "price": 9.0
             },
            {"name": "Mancare de Fasole Galbena",
             "description": "Mâncare delicioasă de fasole galbenă.",
             "image": "mancare-de-fasole-galbena.jpg",
             "price": 10.0
             },
            {"name": "Mancare de Mazare",
             "description": "Mâncare savuroasă de mazăre.",
             "image": "mancare-de-mazare.jpg",
             "price": 9.0
             },
            {"name": "Mancare de Varza",
             "description": "Mâncare consistentă de varză.",
             "image": "mancare-de-varza.jpg",
             "price": 8.0
             },
            {"name": "Pilaf cu Ciuperci",
             "description": "Pilaf aromat cu ciuperci.",
             "image": "pilaf-cu-ciuperci.jpg",
             "price": 12.0
             },
            {"name": "Sarmalute din Ciuperci Champignon",
             "description": "Sarmalute vegetariene din ciuperci champignon.",
             "image": "sarmalute-din-ciuperci-champignon.jpg",
             "price": 13.0
             },
            {"name": "Vinete Gratinate cu Branza și Sos de Roșii",
             "description": "Vinete gratinate cu brânză și sos de roșii.",
             "image": "vinete-gratinate-cu-branza-si-sos-de-rosii.jpg",
             "price": 14.0
             }
        ],
        "Deserturi": [
            {"name": "Brownie",
             "description": "Delicios brownie cu ciocolată.",
             "image": "brownie.jpg",
             "price": 10.0
             },
            {"name": "Budinca de paste cu branza și stafide",
             "description": "Budincă cremoasă cu brânză și stafide.",
             "image": "budinca-de-paste-cu-branza-si-stafide-.jpg",
             "price": 12.0
             },
            {"name": "Chec pufos cu nuca și cacao",
             "description": "Chec moale cu nuci și cacao.",
             "image": "chec-pufos-cu-nuca-si-cacao.jpg",
             "price": 11.0
             },
            {"name": "Cheesecake cu fructe de padure",
             "description": "Cheesecake cremos cu topping de fructe de pădure.",
             "image": "cheesecake-cu-fructe-de-padure.jpg",
             "price": 15.0
             },
            {"name": "Ciocolata de casa cu nuca",
             "description": "Ciocolată făcută acasă cu nuci crocante.",
             "image": "ciocolata-de-casa-cu-nuca.jpg",
             "price": 9.0
             },
            {"name": "Cornulete de casa cu gem și nuca",
             "description": "Cornulețe delicioase umplute cu gem și nuci.",
             "image": "cornulete-de-casa-cu-gem-si-nuca.jpg",
             "price": 8.0
             },
            {"name": "Crema de zahar ars",
             "description": "Crema de zahăr ars cu textură fină.",
             "image": "crema-de-zahar-ars.jpg",
             "price": 7.0
             },
            {"name": "Cremsnit",
             "description": "Cremsnit cu strat de cremă și foietaj crocant.",
             "image": "cremsnit.jpg",
             "price": 10.0
             },
            {"name": "Fursecuri cu ciocolata",
             "description": "Fursecuri moi cu bucăți de ciocolată.",
             "image": "fursecuri-cu-ciocolata.jpg",
             "price": 6.0
             },
            {"name": "Galuste cu prune",
             "description": "Găluște pufoase cu prune.",
             "image": "galuste-cu-prune.jpg",
             "price": 7.0
             },
            {"name": "Papanași cu dulceata",
             "description": "Papanași tradiționali cu dulceață de prune.",
             "image": "papanasi-cu-dulceata-.jpg",
             "price": 9.0
             },
            {"name": "Placinta cu branza dulce și stafide",
             "description": "Plăcintă umplută cu brânză dulce și stafide.",
             "image": "placinta-cu-branza-dulce-si-stafide.jpg",
             "price": 8.0
             },
            {"name": "Placinta cu mere",
             "description": "Plăcintă tradițională cu mere proaspete.",
             "image": "placinta-cu-mere.jpg",
             "price": 7.0
             },
            {"name": "Poale-n brau",
             "description": "Poale-n brau delicioase.",
             "image": "poale-n-brau.jpg",
             "price": 6.0
             },
            {"name": "Prajitura Alba-ca-Zapada",
             "description": "Prajitură ușoară și pufoasă.",
             "image": "prajitura-alba-ca-zapada.jpg",
             "price": 10.0
             },
            {"name": "Prajitura Crumble cu vișine",
             "description": "Crumble crocant cu vișine suculente.",
             "image": "prajitura-crumble-cu-visine.jpg",
             "price": 9.0
             },
            {"name": "Prajitura cu miere și crema de smantana",
             "description": "Prajitură dulce cu miere și cremă de smântână.",
             "image": "prajitura-cu-miere-si-crema-de-smantana.jpg",
             "price": 11.0
             },
            {"name": "Prajituri asortate",
             "description": "O selecție de prăjituri asortate.",
             "image": "prajituri-asortate.jpg",
             "price": 12.0
             },
            {"name": "Salam de biscuiti",
             "description": "Salam delicios de biscuiți.",
             "image": "salam-de-biscuiti.jpg",
             "price": 7.0
             },
            {"name": "Salam de biscuiti de post",
             "description": "Salam de biscuiți potrivit pentru post.",
             "image": "salam-de-biscuiti-de-post.jpg",
             "price": 7.0
             },
            {"name": "Saratele de post",
             "description": "Saratele dulci de post.",
             "image": "saratele-de-post.jpg",
             "price": 6.0
             },
            {"name": "Tort cu vanilie și fructe de padure",
             "description": "Tort cremos cu vanilie și fructe de pădure.",
             "image": "tort-cu-vanilie-si-fructe-de-padure.jpg",
             "price": 20.0
             },
            {"name": "Tort fructe fara zahar",
             "description": "Tort cu fructe fără zahăr adăugat.",
             "image": "tort-fructe-fara-zahar.jpg",
             "price": 18.0
             },
            {"name": "Tort Rocher",
             "description": "Tort cu gust intens de ciocolată Rocher.",
             "image": "tort-rocher.jpg",
             "price": 19.0
             }
        ],
        "Salate": [
            {"name": "Mix Salate Savuroase",
             "description": "Un amestec proaspăt de salate savuroase, perfect pentru orice masă.",
             "image": "mix-salate-savuroase.jpg",
             "price": 12.0
             },
            {"name": "Salata Boeuf",
             "description": "Salată tradițională boeuf cu legume și maioneză.",
             "image": "salata-boeuf.jpg",
             "price": 14.0
             },
            {"name": "Salata Boeuf cu piept de Pui",
             "description": "Variantă de Salata Boeuf cu adăugare de piept de pui fraged.",
             "image": "salata-boeuf-cu-piept-de-pui.jpg",
             "price": 16.0
             },
            {"name": "Salata Boeuf fara Carne",
             "description": "Salată boeuf delicioasă fără carne, ideală pentru vegetarieni.",
             "image": "salata-boeuf-fara-carne.jpg",
             "price": 13.0
             },
            {"name": "Salata cu Pui și Telina",
             "description": "Salată răcoritoare cu pui și țelină crocantă.",
             "image": "salata-cu-pui-si-telina.jpg",
             "price": 15.0
             },
            {"name": "Salata de Ardei Copti",
             "description": "Salată de ardei copți cu feta și măsline.",
             "image": "salata-de-ardei-copti.jpg",
             "price": 14.0
             },
            {"name": "Salata de ciuperci și pui",
             "description": "Salată bogată cu ciuperci și bucăți de pui.",
             "image": "salata-de-ciuperci-si-pui.jpg",
             "price": 15.0
             },
            {"name": "Salata de Vinete",
             "description": "Salată de vinete coapte, asezonată perfect.",
             "image": "salata-de-vinete.jpg",
             "price": 13.0
             },
            {"name": "Salata Orientala",
             "description": "Salată orientală vibrantă cu legume proaspete și dressing aromat.",
             "image": "salata-orientala.jpg",
             "price": 14.0
             },
            {"name": "Salata Tabouleh",
             "description": "Salată tabouleh tradițională cu bulgur și ierburi proaspete.",
             "image": "salata-tabouleh.jpg",
             "price": 12.0
             },
            {"name": "Salata Tzatziki",
             "description": "Salată tzatziki cremoasă cu castraveți și iaurt grecesc.",
             "image": "salata-tzatziki.jpg",
             "price": 13.0
             }
        ],
        "Supe si Ciorbe": [
            {"name": "Bors de Curcan",
             "description": "Bors delicios cu carne de curcan.",
             "image": "bors-de-curcan.jpg",
             "price": 15.0
             },
            {"name": "Ciorba de Burta",
             "description": "Ciorbă tradițională cu burtă de vită.",
             "image": "ciorba-de-burta.jpg",
             "price": 16.0
             },
            {"name": "Ciorba de Fasole",
             "description": "Ciorbă hrănitoare de fasole.",
             "image": "ciorba-de-fasole.jpg",
             "price": 14.0
             },
            {"name": "Ciorba de Legume",
             "description": "Ciorbă proaspătă de legume.",
             "image": "ciorba-de-legume.jpg",
             "price": 12.0
             },
            {"name": "Ciorba de Perisoare",
             "description": "Ciorbă tradițională cu perisoare de carne.",
             "image": "ciorba-de-perisoare.jpg",
             "price": 17.0
             },
            {"name": "Ciorba de Pui a-la-grec",
             "description": "Ciorbă de pui cu legume și smântână.",
             "image": "ciorba-de-pui-a-la-grec.jpg",
             "price": 18.0
             },
            {"name": "Ciorba de Pui Taraneasca",
             "description": "Ciorbă consistentă cu carne de pui și legume.",
             "image": "ciorba-de-pui-taraneasca.jpg",
             "price": 16.0
             },
            {"name": "Ciorba de Vacuta",
             "description": "Ciorbă gustoasă cu carne de vacă.",
             "image": "ciorba-de-vacuta.jpg",
             "price": 17.0
             },
            {"name": "Ciorba Radauteana",
             "description": "Ciorbă consistentă cu carne de pui și smântână.",
             "image": "ciorba-radauteana.jpg",
             "price": 18.0
             },
            {"name": "Supă Crema de Legume",
             "description": "Supă cremoasă de legume, perfectă pentru o cină ușoară.",
             "image": "supa-crema-de-legume.jpg",
             "price": 13.0
             },
            {"name": "Supă Crema de Linte",
             "description": "Supă cremoasă de linte, bogată în proteine.",
             "image": "supa-crema-de-linte.jpg",
             "price": 14.0
             },
            {"name": "Supă de Pui cu Galuste",
             "description": "Supă de pui cu găluște pufoase.",
             "image": "supa-de-pui-cu-galuste.jpg",
             "price": 15.0
             },
            {"name": "Supă de Pui cu Tăiței",
             "description": "Supă de pui cu tăiței proaspeți.",
             "image": "supa-de-pui-cu-taitei.jpg",
             "price": 14.0
             },
            {"name": "Supă de Roșii cu Tăiței",
             "description": "Supă delicioasă de roșii cu tăiței.",
             "image": "supa-de-rosii-cu-taitei.jpg",
             "price": 12.0
             }
        ]
    }

    for category_name, items in categories.items():
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.commit()

        for item in items:
            existing_item = session.query(MenuItem).filter_by(name=item['name'], category=category).first()
            if not existing_item:
                menu_item = MenuItem(
                    name=item['name'],
                    description=item['description'],
                    image=item['image'],
                    price=item['price'],
                    category=category
                )
                session.add(menu_item)

    session.commit()
    print("Meniul a fost populat cu succes!")

def add_example_user():
    user = session.query(User).filter_by(username="admin").first()
    if not user:
        new_user = User(username="admin", password="password123", email="admin@example.com")
        session.add(new_user)
        session.commit()
        print("Utilizatorul 'admin' a fost adăugat.")
    else:
        print("Utilizatorul 'admin' există deja.")
