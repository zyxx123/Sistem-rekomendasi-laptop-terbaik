from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Laptop(db.Model):
    __tablename__ = 'laptop'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    nama_laptop = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    ssd = db.Column(db.Integer, nullable=False)
    processor_score = db.Column(db.Integer, nullable=False)
    berat = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode': self.kode,
            'nama_laptop': self.nama_laptop,
            'harga': self.harga,
            'ram': self.ram,
            'ssd': self.ssd,
            'processor_score': self.processor_score,
            'berat': self.berat
        }

class Criteria(db.Model):
    __tablename__ = 'criteria'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(5), unique=True, nullable=False)
    nama = db.Column(db.String(50), nullable=False)
    atribut = db.Column(db.String(10), nullable=False) # 'cost' or 'benefit'
    bobot_dasar = db.Column(db.Float, nullable=False)

class RecommendationHistory(db.Model):
    __tablename__ = 'recommendation_history'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    tujuan = db.Column(db.String(50))
    budget = db.Column(db.String(50))
    mobilitas = db.Column(db.String(50))
    multitasking = db.Column(db.String(50))
    laptop_terpilih = db.Column(db.String(100))
    nilai_saw = db.Column(db.Float)
