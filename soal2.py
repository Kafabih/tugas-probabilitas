# =============================================
# IMPORT LIBRARIES
# =============================================
import pandas as pd
import numpy as np
from scipy.stats import norm, shapiro, ttest_1samp, t
import matplotlib.pyplot as plt

# =============================================
# BACA DATASET CSV
# =============================================
df = pd.read_csv("dataset_health_sleep_relation.csv")
df.columns = df.columns.str.strip().str.replace(" ", "")

print("\n=== SOAL 2: UJI RATA-RATA TIDUR VS 8 JAM ===")

# =============================================
# LOOP PER GENDER
# =============================================
for gender in ["Male", "Female"]:
    print(f"\n--- Gender: {gender.upper()} ---")

    # ====================================
    # 1. Ambil data Sleep Duration
    # ====================================
    data = df[df["Gender"] == gender]["SleepDuration"].dropna()
    n = len(data)
    print(f"Jumlah Data: {n}")

    if n < 5:
        print("❌ Data terlalu sedikit. Lewati.")
        continue

    # ====================================
    # 2. Hitung Mean dan Standar Deviasi
    # ====================================
    # Rumus Mean:
    # μ = ΣX / n
    mean = data.mean()

    # Rumus Std Dev:
    # s = sqrt [ Σ(X - μ)² / (n-1) ]
    std = data.std(ddof=1)

    print(f"Mean Sleep Duration: {mean:.4f}")
    print(f"Std Dev Sleep Duration: {std:.4f}")

    # Buat tabel ringkasan
    summary_df = pd.DataFrame({
        "Statistik": ["Mean", "Std Dev", "Jumlah Data"],
        "Nilai": [mean, std, n]
    })

    print("\nTabel Ringkasan Statistik:")
    print(summary_df)

    # ====================================
    # 3. Uji t (H0: mean = 8 jam, H1: mean < 8 jam)
    # ====================================
    # Rumus t-statistik:
    # t = (X̄ - μ0) / (s / sqrt(n))
    # X̄ = sample mean
    # μ0 = 8
    # s = sample std dev
    mu0 = 8
    se = std / np.sqrt(n)
    t_stat = (mean - mu0) / se

    # Hitung p-value satu sisi (H1: mean < 8)
    p_value = t.cdf(t_stat, df=n-1)

    print(f"\nt-statistic: {t_stat:.4f}")
    print(f"p-value (one-tailed): {p_value:.4f}")

    # ====================================
    # 4. Interpretasi Hasil
    # ====================================
    if p_value < 0.05:
        print("Kesimpulan: Rata-rata tidur signifikan lebih pendek dari 8 jam (tolak H0).")
    else:
        print("Kesimpulan: Tidak cukup bukti untuk menyatakan rata-rata lebih pendek dari 8 jam.")

    # ====================================
    # 5. Visualisasi Distribusi Sampel dengan 8 jam
    # ====================================
    plt.figure(figsize=(10,6))

    # Histogram
    plt.hist(
        data,
        bins=6,
        color='lightblue' if gender=="Male" else 'lightpink',
        edgecolor='black',
        alpha=0.7,
        label='Distribusi Data'
    )

    # Garis rata-rata sampel
    plt.axvline(mean, color='green', linestyle='-', linewidth=2, label=f"Mean = {mean:.2f}")

    # Garis benchmark 8 jam
    plt.axvline(8, color='red', linestyle='--', linewidth=2, label="Benchmark = 8 jam")

    plt.xlabel('Sleep Duration')
    plt.ylabel('Frekuensi')
    plt.title(f'Uji Rata-rata Tidur Terhadap 8 Jam ({gender})')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
