# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

# ==========================
# 1. KONFIGURASI DASHBOARD
# ==========================
st.set_page_config(
    page_title="🌦️ Dashboard Cuaca Nasional",
    page_icon="☀️",
    layout="wide"
)

st.title("🌤️ Dashboard Simulasi Cuaca Harian Indonesia")
st.markdown("""
Dashboard ini menampilkan **simulasi suhu, kelembaban, dan kecepatan angin** untuk seluruh provinsi di Indonesia.
""")

# ==========================
# 2. DAFTAR PROVINSI
# ==========================
provinsi = [
    "Aceh","Sumatera Utara","Sumatera Barat","Riau","Jambi","Sumatera Selatan","Bengkulu","Lampung",
    "Kepulauan Bangka Belitung","Kepulauan Riau","DKI Jakarta","Jawa Barat","Jawa Tengah","DI Yogyakarta",
    "Jawa Timur","Banten","Bali","Nusa Tenggara Barat","Nusa Tenggara Timur","Kalimantan Barat",
    "Kalimantan Tengah","Kalimantan Selatan","Kalimantan Timur","Kalimantan Utara",
    "Sulawesi Utara","Sulawesi Tengah","Sulawesi Selatan","Sulawesi Tenggara","Gorontalo","Sulawesi Barat",
    "Maluku","Maluku Utara","Papua Barat","Papua","Papua Selatan","Papua Tengah","Papua Pegunungan","Papua Barat Daya"
]

# ==========================
# 3. FUNGSI SIMULASI
# ==========================
def simulasi_suhu(prov):
    means = {
        "Aceh":29,"Sumatera Utara":28,"Sumatera Barat":30,"Riau":31,"Jambi":30,"Sumatera Selatan":29,
        "Bengkulu":30,"Lampung":31,"Kepulauan Bangka Belitung":30,"Kepulauan Riau":31,
        "DKI Jakarta":32,"Jawa Barat":31,"Jawa Tengah":31,"DI Yogyakarta":32,"Jawa Timur":32,"Banten":31,
        "Bali":30,"Nusa Tenggara Barat":32,"Nusa Tenggara Timur":33,
        "Kalimantan Barat":29,"Kalimantan Tengah":28,"Kalimantan Selatan":30,"Kalimantan Timur":30,"Kalimantan Utara":29,
        "Sulawesi Utara":28,"Sulawesi Tengah":29,"Sulawesi Selatan":30,"Sulawesi Tenggara":31,"Gorontalo":30,"Sulawesi Barat":29,
        "Maluku":29,"Maluku Utara":28,
        "Papua Barat":26,"Papua":25,"Papua Selatan":27,"Papua Tengah":24,"Papua Pegunungan":22,"Papua Barat Daya":26
    }
    mean = means.get(prov, 30)
    return round(np.maximum(15, np.random.normal(mean, 2)), 1)

def simulasi_kelembaban(prov):
    # Simulasi kelembaban: Papua lembab, NTT kering
    base = {
        "Nusa Tenggara Timur": 55, "Papua": 85, "DKI Jakarta": 75,
        "Sumatera Selatan": 78, "Kalimantan Tengah": 82
    }
    mean = base.get(prov, 70)
    kelembaban = np.clip(np.random.normal(mean, 10), 40, 95)
    return round(kelembaban, 1)

def simulasi_angin(prov):
    # Simulasi kecepatan angin (m/s)
    # Pantai dan timur Indonesia cenderung lebih berangin
    base = {
        "DKI Jakarta": 3.5, "Nusa Tenggara Timur": 5.2, "Papua": 2.5,
        "Sulawesi Selatan": 4.5, "Bali": 4.0
    }
    mean = base.get(prov, 3.0)
    angin = np.clip(np.random.normal(mean, 1), 0.5, 8.0)
    return round(angin, 1)

def kategori_suhu(s):
    if s < 25:
        return "❄️ Dingin"
    elif s < 30:
        return "🌤️ Hangat"
    else:
        return "🔥 Panas"

# ==========================
# 4. SIMULASI DATA
# ==========================
data = []
for prov in provinsi:
    suhu = simulasi_suhu(prov)
    lembab = simulasi_kelembaban(prov)
    angin = simulasi_angin(prov)
    data.append([prov, suhu, lembab, angin, kategori_suhu(suhu)])

df = pd.DataFrame(data, columns=["Provinsi", "Suhu (°C)", "Kelembaban (%)", "Angin (m/s)", "Kategori"])
df = df.sort_values(by="Suhu (°C)", ascending=False)

# ==========================
# 5. STATISTIK NASIONAL
# ==========================
rata_suhu = df["Suhu (°C)"].mean()
rata_lembab = df["Kelembaban (%)"].mean()
rata_angin = df["Angin (m/s)"].mean()
hari_ini = datetime.date.today().strftime("%d %B %Y")

st.markdown("### 📊 Ringkasan Nasional")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📅 Tanggal", hari_ini)
col2.metric("🌡️ Suhu Rata-rata", f"{rata_suhu:.1f}°C", kategori_suhu(rata_suhu))
col3.metric("💧 Kelembaban Rata-rata", f"{rata_lembab:.1f}%")
col4.metric("🌬️ Kecepatan Angin Rata-rata", f"{rata_angin:.1f} m/s")

# ==========================
# 6. TABEL INTERAKTIF
# ==========================
with st.expander("📋 Lihat Data Lengkap"):
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================
# 7. GRAFIK SUHU
# ==========================
st.subheader("🌡️ Distribusi Suhu per Provinsi")
fig1, ax1 = plt.subplots(figsize=(10, 12))
ax1.barh(df["Provinsi"], df["Suhu (°C)"], color='tomato', edgecolor='darkred', alpha=0.8)
ax1.axvline(rata_suhu, color='red', linestyle='--', label=f'Rata-rata: {rata_suhu:.1f}°C')
ax1.set_xlabel("Suhu (°C)")
ax1.legend()
ax1.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# ==========================
# 8. GRAFIK KELEMBABAN
# ==========================
st.subheader("💧 Distribusi Kelembaban per Provinsi")
fig2, ax2 = plt.subplots(figsize=(10, 12))
ax2.barh(df["Provinsi"], df["Kelembaban (%)"], color='skyblue', edgecolor='navy', alpha=0.8)
ax2.axvline(rata_lembab, color='blue', linestyle='--', label=f'Rata-rata: {rata_lembab:.1f}%')
ax2.set_xlabel("Kelembaban (%)")
ax2.legend()
ax2.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ==========================
# 9. GRAFIK KECEPATAN ANGIN
# ==========================
st.subheader("🌬️ Distribusi Kecepatan Angin per Provinsi")
fig3, ax3 = plt.subplots(figsize=(10, 12))
ax3.barh(df["Provinsi"], df["Angin (m/s)"], color='lightgreen', edgecolor='darkgreen', alpha=0.8)
ax3.axvline(rata_angin, color='green', linestyle='--', label=f'Rata-rata: {rata_angin:.1f} m/s')
ax3.set_xlabel("Kecepatan Angin (m/s)")
ax3.legend()
ax3.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

# ==========================
# 10. SIMULASI DINAMIS
# ==========================
st.subheader("🔄 Simulasi Dinamis Fluktuasi Cuaca Nasional")

progress = st.progress(0)
placeholder = st.empty()
x = np.linspace(0, 24, 100)

# loop simulasi (80 tahapan)
for i in range(80):
    suhu = rata_suhu + 4 * np.sin(2 * np.pi * x / 24) + np.random.normal(0, 0.4, len(x))
    lembab = rata_lembab + 5 * np.cos(2 * np.pi * x / 24) + np.random.normal(0, 1, len(x))
    angin = rata_angin + np.sin(2 * np.pi * x / 6) + np.random.normal(0, 0.2, len(x))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, suhu, '-', label='Suhu (°C)', linewidth=2)
    ax.plot(x, lembab, '-', label='Kelembaban (%)', linewidth=1.5)
    ax.plot(x, angin * 10, '--', label='Angin (x10 m/s)', linewidth=1.5)  # skala agar terlihat
    ax.set_title(f"Simulasi ke-{i+1}: Fluktuasi Cuaca Harian")
    ax.set_xlabel("Jam")
    ax.grid(alpha=0.3)
    ax.legend()

    placeholder.pyplot(fig)
    plt.close(fig)

    # update progress (0-100 integer)
    progress_val = int((i + 1) / 80 * 100)
    progress.progress(progress_val)
    time.sleep(0.05)

st.success("✅ Simulasi dinamis selesai!")
st.caption("Catatan: Data ini bersifat simulatif untuk demonstrasi dashboard interaktif.")
