# 🛒 Brazilian E-Commerce Analysis

Proyek analisis data akhir menggunakan dataset **Olist Brazilian E-Commerce** dari Kaggle.

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Data utama hasil cleaning & join (di-generate oleh notebook)
│   └── dashboard.py        # Aplikasi Streamlit
├── data/
│   ├── rfm_data.csv        # Hasil RFM analysis
│   ├── state_analysis.csv  # Agregasi per state
│   ├── category_analysis.csv # Agregasi per kategori
│   └── clustering_data.csv # Hasil clustering
├── notebook.ipynb          # Notebook analisis utama (Colab)
├── README.md
├── requirements.txt
└── url.txt
```

## ❓ Pertanyaan Bisnis

### Pertanyaan 1 (SMART)
> **"Kategori produk apa yang memiliki rata-rata review score tertinggi dan terendah, serta bagaimana pola pengiriman (rata-rata keterlambatan dalam hari) memengaruhi kepuasan pelanggan (review score) pada periode 2017–2018?"**

### Pertanyaan 2 (SMART)
> **"Bagaimana distribusi nilai transaksi (revenue) berdasarkan negara bagian (state) di Brasil selama tahun 2017–2018, dan state mana yang memiliki potensi pertumbuhan tertinggi berdasarkan jumlah order dan rata-rata nilai pembelian per pelanggan?"**

## 🚀 Cara Menjalankan

### 1. Jalankan Notebook di Google Colab
1. Buka `notebook.ipynb` di Google Colab
2. Upload `kaggle.json` saat diminta (dari Kaggle Settings > API)
3. Jalankan semua cell secara berurutan
4. File CSV akan tersimpan otomatis ke folder `dashboard/` dan `data/`

### 2. Jalankan Dashboard Streamlit (Lokal)
```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

### 3. Deploy ke Streamlit Cloud
1. Push project ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Connect repo dan set main file: `dashboard/dashboard.py`

## 🧠 Teknik Analisis Lanjutan

| Teknik | Tujuan |
|---|---|
| **RFM Analysis** | Segmentasi pelanggan berdasarkan Recency, Frequency, Monetary |
| **Geospatial Analysis** | Distribusi order dan revenue di peta Brasil menggunakan Folium |
| **Clustering (Binning)** | Pengelompokan state berdasarkan potensi pasar (volume + AOV) |

## 📊 Dataset

- **Sumber:** [Kaggle — Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Periode:** 2016–2018
- **Tabel utama:** orders, order_items, products, customers, reviews, payments, geolocation

## ✅ Kesimpulan

1. **Review Score & Delivery:** Keterlambatan pengiriman >5 hari menyebabkan review score turun di bawah 3.0. Pengiriman lebih awal meningkatkan kepuasan secara signifikan.
2. **Revenue per State:** SP mendominasi >40% revenue. State DF dan RJ memiliki AOV tertinggi — potensi pasar premium.

## 🎯 Rekomendasi

1. Perbaiki SLA logistik untuk kategori produk dengan delay tinggi
2. Program loyalty untuk segmen Champions (RFM)
3. Ekspansi kampanye premium ke state niche (DF, AC)
4. Re-engagement campaign untuk segmen At Risk
