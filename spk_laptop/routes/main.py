from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Laptop, Criteria, RecommendationHistory
from saw import SAW, get_weights_by_needs
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.before_request
def require_login():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

@main_bp.route('/')
def index():
    return render_template('user/index.html')

@main_bp.route('/rekomendasi', methods=['GET', 'POST'])
def rekomendasi():
    if request.method == 'POST':
        tujuan = request.form.get('tujuan')
        budget = request.form.get('budget')
        mobilitas = request.form.get('mobilitas')
        multitasking = request.form.get('multitasking')

        # 1. Ambil Bobot berdasarkan kebutuhan
        weights = get_weights_by_needs(tujuan, mobilitas, multitasking)
        
        # 2. Ambil data Laptop & Kriteria
        laptops = Laptop.query.all()
        criteria_list = Criteria.query.all()
        
        # Mapping criteria untuk SAW
        # key mapping: C1->harga, C2->ram, C3->ssd, C4->processor_score, C5->berat
        key_map = {
            'C1': 'harga',
            'C2': 'ram',
            'C3': 'ssd',
            'C4': 'processor_score',
            'C5': 'berat'
        }
        
        saw_criteria = []
        for c in criteria_list:
            saw_criteria.append({'key': key_map[c.kode], 'atribut': c.atribut})

        # Data alternatives
        alternatives = [l.to_dict() for l in laptops]

        # 3. Proses SAW
        # Normalisasi
        normalized_matrix = SAW.normalize(alternatives, saw_criteria)
        
        # Hitung Nilai Preferensi & Ranking
        # weights dict keys must match key_map values
        final_ranking = SAW.calculate_preference(normalized_matrix, weights)
        
        # Simpan Riwayat
        best_laptop = final_ranking[0]['nama_laptop']
        best_score = final_ranking[0]['nilai_saw']
        
        history = RecommendationHistory(
            tujuan=tujuan,
            budget=budget,
            mobilitas=mobilitas,
            multitasking=multitasking,
            laptop_terpilih=best_laptop,
            nilai_saw=best_score
        )
        db.session.add(history)
        db.session.commit()

        return render_template('user/hasil.html', 
                               user_profile={
                                   'tujuan': tujuan,
                                   'budget': budget,
                                   'mobilitas': mobilitas,
                                   'multitasking': multitasking
                               },
                               weights=weights,
                               normalized_matrix=normalized_matrix,
                               ranking=final_ranking,
                               best=final_ranking[0])

    return render_template('user/rekomendasi_form.html')

@main_bp.route('/riwayat')
def riwayat():
    histories = RecommendationHistory.query.order_by(RecommendationHistory.tanggal.desc()).all()
    return render_template('user/riwayat.html', histories=histories)
