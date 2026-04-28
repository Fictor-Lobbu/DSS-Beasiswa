import numpy as np

def proses_dss(data, bobot):
    """
    Fungsi MOORA Dinamis (Sesuai dengan logika Mapping Juara 1 = 3 Poin).
    Kriteria: 
    - C1 (Peringkat): Benefit (setelah mapping 3, 2, 1)
    - C2 (IPK): Benefit
    - C3 (Surat): Benefit
    - Kriteria Tambahan: Otomatis dianggap Benefit
    """
    # 1. Konversi ke Numpy Array untuk komputasi
    data = np.array(data, dtype=float)
    bobot = np.array(bobot, dtype=float)

    # 2. Normalisasi Matriks (Standard MOORA Ratio System)
    # Rumus: x / sqrt(sum(x^2))
    pembagi = np.sqrt((data**2).sum(axis=0))
    
    # Keamanan: Hindari pembagian dengan nol (jika kolom kosong, ganti 0 jadi 1)
    pembagi = np.where(pembagi == 0, 1, pembagi)
    
    norm = data / pembagi
    print("=== NORMALISASI ===")
    print(norm)

    # 3. Matriks Ternormalisasi Terbobot (Weighting)
    # Rumus: v = norm * weight
    skor_terbobot = norm * bobot
    print("=== SKOR TERBOBOT (norm × bobot) ===")
    print(skor_terbobot)

    # 4. Nilai Optimasi (Yi)
    # Karena Peringkat (C1) sudah dipetakan menjadi Juara 1 = 3 (Benefit),
    # maka semua kriteria sekarang adalah BENEFIT.
    # Kita cukup menjumlahkan seluruh kolom secara dinamis (axis=1).
    hasil = skor_terbobot.sum(axis=1)

    print("=== HASIL AKHIR (Yi) ===")
    print(hasil)

    return hasil