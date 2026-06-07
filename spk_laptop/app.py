import os
from flask import Flask, render_template, redirect, url_for
from models import db, Laptop, Criteria, RecommendationHistory, User
from routes.main import main_bp
from routes.admin import admin_bp
from routes.auth import auth_bp
from werkzeug.security import generate_password_hash

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
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    if User.query.first() is None:
        admin = User(username='admin', password=generate_password_hash('admin'), role='admin')
        user = User(username='user', password=generate_password_hash('user'), role='user')
        db.session.add_all([admin, user])
        db.session.commit()

    if Laptop.query.first() is None:
        import csv
        laptops = []
        csv_path = os.path.join(basedir, 'laptop.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader, 1):
                    try:
                        price = float(row.get('price', 0) or 0) * 190
                        ram = int(row.get('ram(GB)', 0) or 0)
                        ssd = int(row.get('ssd(GB)', 0) or 0) + int(row.get('Hard Disk(GB)', 0) or 0)
                        score = int(row.get('spec_score', 0) or 0)
                        
                        screen = row.get('screen_size(inches)', '')
                        try:
                            screen_size = float(screen)
                            berat = round(1.0 + (screen_size - 13.0) * 0.15, 2)
                        except:
                            berat = 1.5
                            
                        berat = max(1.0, min(3.0, berat))
                        
                        if price <= 0 or ram <= 0 or score <= 0:
                            continue
                            
                        laptops.append(Laptop(
                            kode=f'L{idx}',
                            nama_laptop=row.get('model_name', f'Laptop {idx}'),
                            harga=price,
                            ram=ram,
                            ssd=ssd,
                            processor_score=score,
                            berat=berat
                        ))
                    except Exception:
                        continue
        
        if not laptops:
            # Fallback
            laptops = [
                Laptop(kode='A1', nama_laptop='ASUS Vivobook 14', harga=7500000, ram=8, ssd=512, processor_score=80, berat=1.4)
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
