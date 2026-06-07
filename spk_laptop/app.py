import os
from flask import Flask, render_template, redirect, url_for
from models import db, Laptop, Criteria, RecommendationHistory
from routes.main import main_bp
from routes.admin import admin_bp

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    if Laptop.query.first() is None:
        # Dummy Laptop Data
        laptops = [
            Laptop(kode='A1', nama_laptop='ASUS Vivobook 14', harga=7500000, ram=8, ssd=512, processor_score=80, berat=1.4),
            Laptop(kode='A2', nama_laptop='Lenovo IdeaPad Slim 3', harga=6200000, ram=8, ssd=256, processor_score=75, berat=1.5),
            Laptop(kode='A3', nama_laptop='Acer Aspire 5', harga=8500000, ram=16, ssd=512, processor_score=85, berat=1.6),
            Laptop(kode='A4', nama_laptop='HP 14s', harga=5800000, ram=4, ssd=256, processor_score=70, berat=1.45),
            Laptop(kode='A5', nama_laptop='Dell Inspiron 14', harga=11000000, ram=16, ssd=512, processor_score=90, berat=1.4),
        ]
        db.session.bulk_save_objects(laptops)
        
        # Criteria Data
        criteria = [
            Criteria(kode='C1', nama='Harga', atribut='cost', bobot_dasar=0.30),
            Criteria(kode='C2', nama='RAM', atribut='benefit', bobot_dasar=0.25),
            Criteria(kode='C3', nama='SSD', atribut='benefit', bobot_dasar=0.20),
            Criteria(kode='C4', nama='Processor Score', atribut='benefit', bobot_dasar=0.15),
            Criteria(kode='C5', nama='Berat', atribut='cost', bobot_dasar=0.10),
        ]
        db.session.bulk_save_objects(criteria)
        
        db.session.commit()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
