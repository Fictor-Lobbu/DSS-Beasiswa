import numpy as np
from scipy.optimize import minimize

def calculate_bwm_weights(bo_vector, ow_vector):
    """
    Fungsi untuk menghitung bobot kriteria menggunakan Best-Worst Method.
    Menerima input list Best-to-Others (BO) dan Others-to-Worst (OW).
    """
    bo = np.array(bo_vector)
    ow = np.array(ow_vector)
    n = len(bo)

    # Secara otomatis mencari index mana yang menjadi kriteria Best (nilai 1 di BO)
    # dan mana kriteria Worst (nilai 1 di OW)
    best_idx = np.where(bo == 1)[0][0]
    worst_idx = np.where(ow == 1)[0][0]

    # Fungsi Objektif: Meminimalkan nilai Ksi (Ksi adalah variabel terakhir di array x)
    def objective(x):
        return x[-1]

    constraints = []
    
    # Kendala 1: Total semua bobot harus = 1
    constraints.append({'type': 'eq', 'fun': lambda x: np.sum(x[:-1]) - 1})

    # Kendala 2: Optimasi absolut untuk BO dan OW
    for j in range(n):
        # | w_best - a_bj * w_j | <= Ksi
        constraints.append({'type': 'ineq', 'fun': lambda x, j=j: x[-1] - (x[best_idx] - bo[j] * x[j])})
        constraints.append({'type': 'ineq', 'fun': lambda x, j=j: x[-1] - (bo[j] * x[j] - x[best_idx])})

        # | w_j - a_jw * w_worst | <= Ksi
        constraints.append({'type': 'ineq', 'fun': lambda x, j=j: x[-1] - (x[j] - ow[j] * x[worst_idx])})
        constraints.append({'type': 'ineq', 'fun': lambda x, j=j: x[-1] - (ow[j] * x[worst_idx] - x[j])})

    # Batasan: Semua bobot >= 0, Ksi >= 0
    bounds = [(0, 1) for _ in range(n)] + [(0, None)]
    
    # Nilai tebakan awal (Initial guess)
    x0 = np.append(np.ones(n) / n, 0.1)

    # Menjalankan algoritma optimasi SLSQP
    res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

    # Mengembalikan bobot kriteria dan nilai Konsistensi (Ksi)
    weights = res.x[:-1]
    ksi = res.x[-1]

    return weights, ksi