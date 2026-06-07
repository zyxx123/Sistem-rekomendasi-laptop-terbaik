from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Laptop, Criteria, RecommendationHistory
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    total_laptop = Laptop.query.count()
    total_rekomendasi = RecommendationHistory.query.count()
    
    # Laptop paling sering direkomendasikan
    best_laptop_stat = db.session.query(
        RecommendationHistory.laptop_terpilih, 
        func.count(RecommendationHistory.laptop_terpilih).label('total')
    ).group_by(RecommendationHistory.laptop_terpilih).order_by(func.count(RecommendationHistory.laptop_terpilih).desc()).first()

    return render_template('admin/dashboard.html', 
                           total_laptop=total_laptop, 
                           total_rekomendasi=total_rekomendasi,
                           best_laptop=best_laptop_stat)

# CRUD Laptop
@admin_bp.route('/laptop')
def laptop_index():
    laptops = Laptop.query.all()
    return render_template('admin/laptop_index.html', laptops=laptops)

@admin_bp.route('/laptop/add', methods=['GET', 'POST'])
def laptop_add():
    if request.method == 'POST':
        new_laptop = Laptop(
            kode=request.form.get('kode'),
            nama_laptop=request.form.get('nama_laptop'),
            harga=float(request.form.get('harga')),
            ram=int(request.form.get('ram')),
            ssd=int(request.form.get('ssd')),
            processor_score=int(request.form.get('processor_score')),
            berat=float(request.form.get('berat'))
        )
        db.session.add(new_laptop)
        db.session.commit()
        return redirect(url_for('admin.laptop_index'))
    return render_template('admin/laptop_form.html', action='Tambah')

@admin_bp.route('/laptop/edit/<int:id>', methods=['GET', 'POST'])
def laptop_edit(id):
    laptop = Laptop.query.get_or_404(id)
    if request.method == 'POST':
        laptop.kode = request.form.get('kode')
        laptop.nama_laptop = request.form.get('nama_laptop')
        laptop.harga = float(request.form.get('harga'))
        laptop.ram = int(request.form.get('ram'))
        laptop.ssd = int(request.form.get('ssd'))
        laptop.processor_score = int(request.form.get('processor_score'))
        laptop.berat = float(request.form.get('berat'))
        db.session.commit()
        return redirect(url_for('admin.laptop_index'))
    return render_template('admin/laptop_form.html', laptop=laptop, action='Edit')

@admin_bp.route('/laptop/delete/<int:id>')
def laptop_delete(id):
    laptop = Laptop.query.get_or_404(id)
    db.session.delete(laptop)
    db.session.commit()
    return redirect(url_for('admin.laptop_index'))

# CRUD Kriteria
@admin_bp.route('/kriteria')
def kriteria_index():
    criteria = Criteria.query.all()
    return render_template('admin/kriteria_index.html', criteria=criteria)

@admin_bp.route('/kriteria/edit/<int:id>', methods=['GET', 'POST'])
def kriteria_edit(id):
    c = Criteria.query.get_or_404(id)
    if request.method == 'POST':
        c.nama = request.form.get('nama')
        c.atribut = request.form.get('atribut')
        c.bobot_dasar = float(request.form.get('bobot_dasar'))
        db.session.commit()
        return redirect(url_for('admin.kriteria_index'))
    return render_template('admin/kriteria_form.html', kriteria=c)
