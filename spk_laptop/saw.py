class SAW:
    @staticmethod
    def normalize(alternatives, criteria):
        """
        Normalisasi Matriks Keputusan
        alternatives: list of dict (data laptop)
        criteria: list of dict (nama, atribut)
        """
        if not alternatives:
            return []

        # Cari Max/Min untuk setiap kriteria
        bounds = {}
        for c in criteria:
            values = [alt[c['key']] for alt in alternatives]
            bounds[c['key']] = {
                'max': max(values),
                'min': min(values)
            }

        normalized = []
        for alt in alternatives:
            row = {'id': alt['id'], 'nama_laptop': alt['nama_laptop'], 'scores': {}}
            for c in criteria:
                val = alt[c['key']]
                if c['atribut'] == 'benefit':
                    row['scores'][c['key']] = val / bounds[c['key']]['max'] if bounds[c['key']]['max'] != 0 else 0
                else: # cost
                    row['scores'][c['key']] = bounds[c['key']]['min'] / val if val != 0 else 0
            normalized.append(row)
        
        return normalized

    @staticmethod
    def calculate_preference(normalized_matrix, weights):
        """
        Hitung Nilai Preferensi (Vi)
        normalized_matrix: output dari normalize()
        weights: dict {key: weight_value}
        """
        results = []
        for row in normalized_matrix:
            preference_value = 0
            detail_perhitungan = {}
            for key, weight in weights.items():
                score = row['scores'][key]
                weighted_score = score * weight
                preference_value += weighted_score
                detail_perhitungan[key] = {
                    'normalized': score,
                    'weighted': weighted_score
                }
            
            results.append({
                'id': row['id'],
                'nama_laptop': row['nama_laptop'],
                'nilai_saw': round(preference_value, 4),
                'detail': detail_perhitungan
            })
        
        # Urutkan berdasarkan nilai SAW tertinggi (Ranking)
        return sorted(results, key=lambda x: x['nilai_saw'], reverse=True)

def get_weights_by_needs(tujuan, mobilitas, multitasking):
    """
    Konversi Kebutuhan Menjadi Bobot
    """
    # Bobot Dasar berdasarkan Tujuan
    base_weights = {
        'Programming': {'harga': 0.20, 'ram': 0.30, 'ssd': 0.20, 'processor_score': 0.20, 'berat': 0.10},
        'Gaming': {'harga': 0.15, 'ram': 0.25, 'ssd': 0.15, 'processor_score': 0.35, 'berat': 0.10},
        'Editing Video': {'harga': 0.15, 'ram': 0.25, 'ssd': 0.20, 'processor_score': 0.30, 'berat': 0.10},
        'Desain Grafis': {'harga': 0.20, 'ram': 0.25, 'ssd': 0.20, 'processor_score': 0.25, 'berat': 0.10},
        'Kuliah': {'harga': 0.35, 'ram': 0.20, 'ssd': 0.15, 'processor_score': 0.10, 'berat': 0.20},
        'Kantoran': {'harga': 0.35, 'ram': 0.20, 'ssd': 0.15, 'processor_score': 0.10, 'berat': 0.20},
    }

    weights = base_weights.get(tujuan, {
        'harga': 0.30, 'ram': 0.25, 'ssd': 0.20, 'processor_score': 0.15, 'berat': 0.10
    }).copy()

    # Penyesuaian Mobilitas
    if mobilitas == 'Tinggi':
        weights['berat'] += 0.05
        weights['harga'] -= 0.05
    elif mobilitas == 'Rendah':
        weights['berat'] -= 0.05
        weights['processor_score'] += 0.05

    # Penyesuaian Multitasking
    if multitasking == 'Berat':
        weights['ram'] += 0.05
        weights['ssd'] -= 0.05
    elif multitasking == 'Ringan':
        weights['ram'] -= 0.05
        weights['harga'] += 0.05

    # Pastikan total bobot = 1 (Normalisasi bobot jika perlu)
    total = sum(weights.values())
    for key in weights:
        weights[key] = round(weights[key] / total, 2)
    
    # Fix rounding issue to ensure exactly 1.0
    diff = round(1.0 - sum(weights.values()), 2)
    if diff != 0:
        weights['harga'] = round(weights['harga'] + diff, 2)

    return weights
