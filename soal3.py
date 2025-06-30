# =============================================
# IMPORT LIBRARIES
# =============================================
import pandas as pd
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

# =============================================
# BACA DATASET CSV
# =============================================
df = pd.read_csv("dataset_health_sleep_relation.csv")
df.columns = df.columns.str.strip().str.replace(" ", "")

print("\n=== SOAL 3: PELUANG BINOMIAL ===")

# =============================================
# LOOP PER GENDER
# =============================================
for gender in ["Male", "Female"]:
    print(f"\n--- Gender: {gender.upper()} ---")

    # ====================================
    # 1. Hitung proporsi dengan QualityOfSleep >=8
    # ====================================
    # Rumus proporsi:
    # p = (jumlah sukses) / (total observasi)
    quality = df[df["Gender"] == gender]["QualityofSleep"].dropna()
    n_data = len(quality)
    p_success = (quality >=8).mean()

    print(f"Jumlah Data: {n_data}")
    print(f"Proporsi kualitas tidur >=8: {p_success:.4f}")

    if n_data < 5:
        print("❌ Data terlalu sedikit. Lewati.")
        continue

    # ====================================
    # 2. Tentukan parameter binomial
    # ====================================
    n_binomial = 20   # jumlah percobaan
    k_success = 5     # jumlah keberhasilan yang ingin dihitung

    # ====================================
    # 3. Hitung probabilitas binomial
    # ====================================
    # Rumus distribusi binomial:
    # P(X = k) = C(n, k) * p^k * (1-p)^(n-k)
    prob_binom = binom.pmf(k_success, n_binomial, p_success)

    print(f"\nPeluang tepat {k_success} dari {n_binomial} orang kualitas tidur >=8: {prob_binom:.4f}")

    # ====================================
    # 4. Tabel Probabilitas Semua K (0..n)
    # ====================================
    k_values = np.arange(0, n_binomial+1)
    prob_values = binom.pmf(k_values, n_binomial, p_success)

    prob_table = pd.DataFrame({
        "Jumlah Sukses (k)": k_values,
        "Probabilitas": prob_values.round(6)
    })

    print("\nTabel Distribusi Binomial:")
    print(prob_table)

    # ====================================
    # 5. Visualisasi Distribusi Binomial
    # ====================================
    plt.figure(figsize=(12,6))
    plt.bar(k_values, prob_values,
            color='skyblue' if gender=="Male" else 'lightpink',
            edgecolor='black')
    plt.axvline(k_success, color='red', linestyle='--', label=f"k = {k_success}")
    plt.xlabel('Jumlah Orang dengan Kualitas Tidur >=8')
    plt.ylabel('Probabilitas')
    plt.title(f'Distribusi Binomial (n=20, p={p_success:.2f}) - {gender}')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # ====================================
    # 6. Interpretasi
    # ====================================
    print("Interpretasi: Ini adalah probabilitas tepat", k_success, "orang dari 20 yang memiliki kualitas tidur baik (>=8).")
    if prob_binom < 0.05:
        print("Peluangnya rendah (<0.05), kejadian jarang terjadi.")
    else:
        print("Peluangnya tidak terlalu kecil (>0.05), kejadian bisa terjadi.")
