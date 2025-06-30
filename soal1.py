import pandas as pd
import numpy as np
from scipy.stats import norm, shapiro
import matplotlib.pyplot as plt

# =============================================
# BACA DATASET CSV
# =============================================
df = pd.read_csv("dataset_health_sleep_relation.csv")
df.columns = df.columns.str.strip().str.replace(" ", "")

# =============================================
# LOOP PER GENDER
# =============================================
for gender in ["Male", "Female"]:
    print(f"\n=== SOAL 1: UJI DISTRIBUSI NORMAL ({gender.upper()}) ===")
    
    # ------------------------------------------------------
    # 1. Ambil data Sleep Duration untuk gender ini
    # ------------------------------------------------------
    data = df[df["Gender"] == gender]["SleepDuration"].dropna()
    n = len(data)
    print(f"Jumlah Data: {n}")
    
    if n < 5:
        print("❌ Data terlalu sedikit atau kosong. Lewati analisis.")
        continue  # langsung ke gender berikutnya
    
    # ------------------------------------------------------
    # 2. Hitung Mean dan Standar Deviasi
    # ------------------------------------------------------
    # Rumus Mean:
    # μ = (ΣX) / n
    mean = data.mean()

    # Rumus Standar Deviasi Sampel:
    # s = sqrt [ Σ(Xi - μ)^2 / (n-1) ]
    std = data.std(ddof=1)

    print(f"Mean Sleep Duration: {mean:.4f}")
    print(f"Std Dev Sleep Duration: {std:.4f}")
    
    # ------------------------------------------------------
    # 3. Buat interval kelas dan hitung frekuensi observasi
    # ------------------------------------------------------
    # Tujuan: Menyederhanakan sebaran data menjadi kelas
    bins = [5.8, 6.0, 6.2, 6.4, 6.6, 8.0]
    hist, edges = np.histogram(data, bins=bins)

    freq_table = pd.DataFrame({
        "Interval": [f"{edges[i]:.1f}-{edges[i+1]:.1f}" for i in range(len(edges)-1)],
        "Frekuensi Observasi": hist
    })

    print("\nFrekuensi Observasi per Interval:")
    print(freq_table)

    # ------------------------------------------------------
    # 4. Hitung Z-Score untuk Batas Kelas
    # ------------------------------------------------------
    # Rumus: Z = (X - μ) / s
    z_lower = (edges[:-1] - mean) / std
    z_upper = (edges[1:] - mean) / std

    print("Z Lower:", z_lower)
    print("Z Upper:", z_upper)

    # ------------------------------------------------------
    # 5. Hitung Probabilitas Teoretis (dari distribusi normal)
    # ------------------------------------------------------
    cdf_lower = norm.cdf(z_lower)
    cdf_upper = norm.cdf(z_upper)
    prob = cdf_upper - cdf_lower
    expected = prob * n  # frekuensi harapan

    freq_table["Z Lower"] = z_lower.round(3)
    freq_table["Z Upper"] = z_upper.round(3)
    freq_table["Prob Teoretis"] = prob.round(4)
    freq_table["Frekuensi Harapan"] = expected.round(2)

    print("\nTabel Distribusi Kelas:")
    print(freq_table)

    # ------------------------------------------------------
    # 6. Hitung Chi-Squared
    # ------------------------------------------------------
    # Rumus: χ² = Σ [ (f_o - f_e)² / f_e ]
    chi_sq = np.sum((hist - expected) ** 2 / expected)
    print(f"\nChi-squared: {chi_sq:.4f}")
    
    # ------------------------------------------------------
    # 7. Uji Normalitas Shapiro-Wilk
    # ------------------------------------------------------
    # H0: Data normal
    # H1: Tidak normal
    stat, p_value = shapiro(data)
    print(f"Shapiro-Wilk p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("Interpretasi: Data TIDAK terdistribusi normal (tolak H0).")
    else:
        print("Interpretasi: Data tidak berbeda signifikan dari distribusi normal (gagal tolak H0).")
    
    # ------------------------------------------------------
    # 8. Visualisasi Histogram + Kurva Normal
    # ------------------------------------------------------
    plt.figure(figsize=(10,6))
    count, bins_plot, ignored = plt.hist(
        data,
        bins=6,
        density=True,
        alpha=0.6,
        color='skyblue' if gender=="Male" else 'pink',
        edgecolor='black',
        label='Histogram Data'
    )

    x = np.linspace(data.min()-0.2, data.max()+0.5, 200)
    pdf = norm.pdf(x, mean, std)
    plt.plot(x, pdf, 'r--', linewidth=2, label='Kurva Normal')
    plt.axvline(mean, color='green', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')
    plt.xlabel('Sleep Duration')
    plt.ylabel('Density')
    plt.title(f'Distribusi Sleep Duration ({gender})')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()