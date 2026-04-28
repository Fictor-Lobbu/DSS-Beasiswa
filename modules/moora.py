import numpy as np

def proses_dss(data, bobot):
    """
    Fungsi MOORA Dinamis.
    Menghitung skor optimasi berdasarkan matriks keputusan dan bobot BWM.
    Semua kriteria (C1, C2, C3, dst.) dianggap sebagai BENEFIT karena 
    Peringkat sudah dipetakan (Juara 1 = 3, Juara 2 = 2, Juara 3 = 1).
    """
    # 1. Konversi input ke Numpy Array untuk komputasi cepat
    data = np.array(data, dtype=float)
    bobot = np.array(bobot, dtype=float)

    # 2. Normalisasi Matriks (Standard MOORA Ratio System)
    # Rumus: x / sqrt(sum(x^2))
    pembagi = np.sqrt((data**2).sum(axis=0))
    
    # Keamanan: Hindari pembagian dengan nol (ganti 0 menjadi 1 agar hasil tetap 0)
    pembagi = np.where(pembagi == 0, 1, pembagi)
    
    norm = data / pembagi

    # 3. Matriks Ternormalisasi Terbobot (Weighting)
    # Rumus: v = norm * w
    nilai_terbobot = norm * bobot

    # 4. Nilai Optimasi (Yi)
    # Karena semua kriteria (Peringkat terpetakan, IPK, Surat, dll.) adalah BENEFIT,
    # kita cukup menjumlahkan seluruh kolom untuk setiap baris mahasiswa.
    skor = nilai_terbobot.sum(axis=1)

    return skor