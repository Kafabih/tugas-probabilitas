# =============================================
# IMPORT LIBRARIES
# =============================================
import pandas as pd
import numpy as np
from scipy.stats import norm, shapiro, ttest_1samp, binom
import matplotlib.pyplot as plt

# =============================================
# BACA DATASET CSV
# =============================================
# File harus bernama sleep_data.csv
df = pd.read_csv("dataset_health_sleep_relation.csv")

df.columns = df.columns.str.strip().str.replace(" ", "")
print("\n=== SOAL 1: UJI DISTRIBUSI NORMAL ===")

# ------------------------------------------------------
# 1. Ambil data Sleep Duration untuk Male
# ------------------------------------------------------
# Pilih baris Gender == "Male", ambil kolom SleepDuration
male_data = df[df["Gender"] == "Male"]["SleepDuration"].dropna()

# Hitung jumlah data
n = len(male_data)
print(f"Jumlah Data: {n}")

# ------------------------------------------------------
# 2. Hitung mean dan standar deviasi
# ------------------------------------------------------
# Rata-rata (mean):
#    μ = (ΣX) / n
mean = male_data.mean()


# Standar deviasi sampel:
#    s = sqrt [ Σ(Xi - μ)^2 / (n-1) ]
std = male_data.std(ddof=1)

print(f"Mean Sleep Duration: {mean:.4f}")
print(f"Std Dev Sleep Duration: {std:.4f}")

# ------------------------------------------------------
# 3. Buat interval kelas dan hitung frekuensi observasi
# ------------------------------------------------------
# Contoh interval kelas:
#    [5.8–6.0), [6.0–6.2), [6.2–6.4)
# Menghitung banyak data yang jatuh di setiap kelas.
bins = [5.8, 6.0, 6.2, 6.4, 6.6, 8.0]
hist, edges = np.histogram(male_data, bins=bins)

# Buat DataFrame hasil histogram
freq_table = pd.DataFrame({
    "Interval": [f"{edges[i]:.1f}-{edges[i+1]:.1f}" for i in range(len(edges)-1)],
    "Frekuensi Observasi": hist
})

print("\nFrekuensi Observasi per Interval:")
print(freq_table)

# ------------------------------------------------------
# 4. Hitung Z-score batas bawah dan atas setiap kelas
# ------------------------------------------------------
# Rumus Z-score:
#    Z = (X - μ) / s
z_lower = (edges[:-1] - mean) / std
z_upper = (edges[1:] - mean) / std

print("Z Lower:", z_lower)
print("Z Upper:", z_upper)

# ------------------------------------------------------
# 5. Hitung probabilitas teoretis per kelas (CDF)
# ------------------------------------------------------
# Rumus probabilitas kelas:
#    P(kelas) = Φ(Z_upper) - Φ(Z_lower)
# Di mana Φ(z) = cumulative distribution function (CDF) normal
cdf_lower = norm.cdf(z_lower)
cdf_upper = norm.cdf(z_upper)
prob = cdf_upper - cdf_lower

# Frekuensi harapan:
#    f_e = n * P(kelas)
expected = prob * n

freq_table["Z Lower"] = z_lower.round(3)
freq_table["Z Upper"] = z_upper.round(3)
freq_table["Prob Teoretis"] = prob.round(4)
freq_table["Frekuensi Harapan"] = expected.round(2)

print("\nTabel Distribusi Kelas:")
print("Probabilitas per kelas:", prob)
print("Frekuensi Harapan:", expected)
print(freq_table)


# ------------------------------------------------------
# 6. Hitung Chi-Squared
# ------------------------------------------------------
# Rumus Chi-Squared:
#    χ² = Σ [ (f_o - f_e)² / f_e ]
# f_o = frekuensi observasi
# f_e = frekuensi harapan
chi_sq = np.sum((hist - expected)**2 / expected)
print(f"\nChi-squared: {chi_sq:.4f}")

# ------------------------------------------------------
# 7. Uji Shapiro-Wilk (lebih cocok n kecil)
# ------------------------------------------------------
# Uji hipotesis:
#   H0: Data terdistribusi normal
#   H1: Data tidak terdistribusi normal
# p-value < 0.05 → Tolak H0
stat, p_value = shapiro(male_data)
print(f"Shapiro-Wilk p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Interpretasi: Data TIDAK terdistribusi normal (tolak H0).")
else:
    print("Interpretasi: Data tidak berbeda signifikan dari distribusi normal (gagal tolak H0).")

# ------------------------------------------------------
# 8. Visualisasi Histogram + Kurva Normal
# ------------------------------------------------------
plt.figure(figsize=(10,6))


# Histogram empiris (density=True → sumbu Y dalam proporsi)
count, bins_plot, ignored = plt.hist(
    male_data,
    bins=6,
    density=True,
    alpha=0.6,
    color='skyblue',
    edgecolor='black',
    label='Histogram Data'
)

# Kurva normal teoretis:
# Rumus PDF Normal:
#    f(x) = 1/(s*sqrt(2π)) * exp(-(x - μ)²/(2s²))
x = np.linspace(male_data.min()-0.2, male_data.max()+0.5, 200)
pdf = norm.pdf(x, mean, std)

plt.plot(x, pdf, 'r--', linewidth=2, label='Kurva Normal')

plt.axvline(mean, color='green', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')

plt.xlabel('Sleep Duration')
plt.ylabel('Density')
plt.title('Distribusi Sleep Duration (Male)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

print("\n=== SOAL 2: UJI RATA-RATA TIDUR VS 8 JAM ===")

# ====================================
# 1. Ambil data Sleep Duration untuk Male
# ====================================
male_data = df[df["Gender"]=="Male"]["SleepDuration"].dropna()
n = len(male_data)

print(f"Jumlah Data: {n}")

# ====================================
# 2. Hitung Mean dan Standar Deviasi
# ====================================
# Rumus Mean:
# μ = ΣX / n

# Rumus Std Dev:
# s = sqrt [ Σ(X - μ)² / (n-1) ]
mean = male_data.mean()
std = male_data.std(ddof=1)

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

t_stat, p_t = ttest_1samp(
    male_data,
    popmean=8,
    alternative='less'
)

print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_t:.4f}")

# ====================================
# 4. Interpretasi Hasil
# ====================================
if p_t <0.05:
    print("Kesimpulan: Rata-rata tidur signifikan lebih pendek dari 8 jam (tolak H0).")
else:
    print("Kesimpulan: Tidak cukup bukti untuk menyatakan rata-rata lebih pendek dari 8 jam.")

# ====================================
# 5. Visualisasi Distribusi Sampel dengan 8 jam
# ====================================
plt.figure(figsize=(10,6))

# Histogram
plt.hist(
    male_data,
    bins=6,
    color='lightblue',
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
plt.title('Uji Rata-rata Tidur Terhadap 8 Jam')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


print("\n=== SOAL 3: PELUANG BINOMIAL ===")

# ====================================
# 1. Hitung proporsi Male dengan QualityOfSleep >=8
# ====================================
# Rumus proporsi:
# p = (jumlah sukses) / (total observasi)
quality = df[df["Gender"]=="Male"]["QualityofSleep"]
n_data = len(quality)
p_success = (quality >=8).mean()

print(f"Jumlah Data: {n_data}")
print(f"Proporsi kualitas tidur >=8: {p_success:.4f}")

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
plt.bar(k_values, prob_values, color='skyblue', edgecolor='black')
plt.axvline(k_success, color='red', linestyle='--', label=f"k = {k_success}")
plt.xlabel('Jumlah Orang dengan Kualitas Tidur >=8')
plt.ylabel('Probabilitas')
plt.title('Distribusi Binomial (n=20, p={:.2f})'.format(p_success))
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# ====================================
# 6. Interpretasi
# ====================================
print("Interpretasi: Ini adalah probabilitas tepat 5 orang dari 20 memiliki kualitas tidur baik (>=8).")
print("Jika probabilitasnya sangat kecil (<0.05), kejadian ini jarang terjadi.")
