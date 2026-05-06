"""
Streamlit Dashboard: Brazilian E-Commerce Analysis
Deploy: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="🛒 Brazilian E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%);
        color: white; padding: 2rem 2.5rem; border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(45,106,79,0.3);
    }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.85; font-size: 1rem; }
    
    .metric-card {
        background: white; border-radius: 14px; padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #40916C;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-title { font-size: 0.8rem; color: #6B7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #1B4332; margin-top: 0.2rem; }
    .metric-delta { font-size: 0.85rem; color: #52B788; font-weight: 600; }
    
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #1B4332;
        border-bottom: 3px solid #52B788; padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem;
    }
    .insight-box {
        background: #D8F3DC; border-left: 4px solid #2D6A4F;
        padding: 0.8rem 1rem; border-radius: 8px;
        font-size: 0.9rem; color: #1B4332; margin-top: 0.8rem;
    }
    .stSelectbox > div > div { border-radius: 10px; }
    
    [data-testid="stSidebar"] { background: #F0FFF4; }
    [data-testid="stSidebar"] .stSelectbox label { color: #1B4332; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    main_path = os.path.join(base, "main_data.csv")
    
    if not os.path.exists(main_path):
        st.error(" File main_data.csv tidak ditemukan. Jalankan notebook terlebih dahulu.")
        st.stop()
    
    df = pd.read_csv(main_path, parse_dates=['order_purchase_timestamp',
                                              'order_delivered_customer_date',
                                              'order_estimated_delivery_date'])
    return df

@st.cache_data
def load_rfm():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "rfm_data.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data  
def load_state():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "state_analysis.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_category():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "category_analysis.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_clustering():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "clustering_data.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

master_df   = load_data()
rfm_df      = load_rfm()
state_df    = load_state()
cat_df      = load_category()
cluster_df  = load_clustering()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔎 Filter Data")
    
    years = sorted(master_df['order_purchase_timestamp'].dt.year.dropna().unique().tolist())
    selected_years = st.multiselect("Tahun", years, default=years)
    
    states = sorted(master_df['customer_state'].dropna().unique().tolist())
    selected_states = st.multiselect("State", states, default=states)
    
    st.markdown("---")
    st.markdown("### 📋 Tentang Dashboard")
    st.info("Dashboard ini menganalisis **Brazilian E-Commerce Olist** dataset untuk menjawab pertanyaan bisnis tentang kepuasan pelanggan dan distribusi revenue geografis.")
    st.markdown("**Dataset:** [Kaggle — Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")

# Filter dataframe
filtered_df = master_df[
    (master_df['order_purchase_timestamp'].dt.year.isin(selected_years)) &
    (master_df['customer_state'].isin(selected_states))
].copy()

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🛒 Brazilian E-Commerce Analysis Dashboard</h1>
    <p>Analisis komprehensif data Olist | Periode 2017–2018 | RFM · Geospatial · Clustering</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Metrics ────────────────────────────────────────────────
total_revenue  = filtered_df['payment_value'].sum()
total_orders   = filtered_df['order_id'].nunique()
avg_review     = filtered_df['review_score'].mean()
avg_delay      = filtered_df['delivery_delay_days'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 Total Revenue</div>
        <div class="metric-value">R${total_revenue/1e6:.1f}M</div>
        <div class="metric-delta">▲ Brazilian Real</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:#457B9D">
        <div class="metric-title">📦 Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
        <div class="metric-delta" style="color:#457B9D">Delivered</div>
    </div>""", unsafe_allow_html=True)

with col3:
    color = "#52B788" if avg_review >= 4 else "#F28A2E"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:{color}">
        <div class="metric-title">⭐ Avg Review Score</div>
        <div class="metric-value" style="color:{color}">{avg_review:.2f} / 5</div>
        <div class="metric-delta" style="color:{color}">Customer Satisfaction</div>
    </div>""", unsafe_allow_html=True)

with col4:
    color_d = "#E63946" if avg_delay > 0 else "#52B788"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:{color_d}">
        <div class="metric-title">🚚 Avg Delivery Delay</div>
        <div class="metric-value" style="color:{color_d}">{avg_delay:.1f} hari</div>
        <div class="metric-delta" style="color:{color_d}">{'Terlambat' if avg_delay > 0 else 'Tepat/Lebih Cepat'}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pertanyaan Bisnis 1 — Review & Delivery",
    "🗺️ Pertanyaan Bisnis 2 — Revenue per State",
    "🧠 RFM Analysis",
    "🔵 Clustering"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: Review Score & Delivery
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">❓ Pertanyaan Bisnis 1</div>', unsafe_allow_html=True)
    st.info("**\"Kategori produk apa yang memiliki rata-rata review score tertinggi dan terendah, serta bagaimana keterlambatan pengiriman memengaruhi kepuasan pelanggan pada 2017–2018?\"**")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🟢 Top 10 Kategori — Review Score Tertinggi")
        if cat_df is not None:
            top10 = cat_df.nlargest(10, 'avg_review_score')
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            bars = ax.barh(top10['category_en'], top10['avg_review_score'],
                           color='#52B788', edgecolor='white')
            ax.set_xlim(3.0, 5.0)
            ax.set_xlabel('Avg Review Score', fontsize=10)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.tick_params(labelsize=8)
            for bar in bars:
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{bar.get_width():.2f}', va='center', fontsize=8, color='#1B4332', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    
    with col_b:
        st.markdown("#### 🔴 Bottom 10 Kategori — Review Score Terendah")
        if cat_df is not None:
            bot10 = cat_df.nsmallest(10, 'avg_review_score').sort_values('avg_review_score')
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            bars = ax.barh(bot10['category_en'], bot10['avg_review_score'],
                           color='#E63946', edgecolor='white')
            ax.set_xlim(2.0, 5.0)
            ax.set_xlabel('Avg Review Score', fontsize=10)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.tick_params(labelsize=8)
            for bar in bars:
                ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
                        f'{bar.get_width():.2f}', va='center', fontsize=8, color='#9D0208', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    
    st.markdown("---")
    st.markdown("#### 📦 Pengaruh Keterlambatan Pengiriman terhadap Review Score")
    
    filtered_df['delay_bucket'] = pd.cut(
        filtered_df['delivery_delay_days'],
        bins=[-999, -10, -3, 0, 5, 15, 999],
        labels=['Early >10d', 'Early 3-10d', 'Early <3d', 'Late <5d', 'Late 5-15d', 'Late >15d']
    )
    delay_review = filtered_df.groupby('delay_bucket')['review_score'].agg(['mean','count']).reset_index()
    delay_review.columns = ['delay_bucket', 'avg_review', 'count']
    
    col_c, col_d = st.columns([2, 1])
    with col_c:
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor('#FAFAFA')
        ax.set_facecolor('#FAFAFA')
        colors_delay = ['#2D6A4F', '#40916C', '#52B788', '#F28A2E', '#E63946', '#9D0208']
        bars = ax.bar(delay_review['delay_bucket'].astype(str), delay_review['avg_review'],
                      color=colors_delay[:len(delay_review)], edgecolor='white')
        ax.set_ylim(2.0, 5.0)
        ax.set_ylabel('Avg Review Score', fontsize=10)
        ax.set_xlabel('Bucket Keterlambatan Pengiriman', fontsize=10)
        ax.set_title('Review Score per Delay Bucket', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.tick_params(axis='x', rotation=15, labelsize=9)
        for bar, row in zip(bars, delay_review.itertuples()):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                    f'{row.avg_review:.2f}\n(n={row.count:,})', ha='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col_d:
        st.markdown("**Tabel Detail**")
        st.dataframe(delay_review.round(3), use_container_width=True, height=250)
    
    st.markdown("""
    <div class="insight-box">
    💡 <b>Insight:</b> Pengiriman lebih awal dari estimasi (Early >10d) menghasilkan review score rata-rata tertinggi (~4.6). 
    Sebaliknya, keterlambatan >15 hari menyebabkan review score turun drastis di bawah 2.5. 
    <b>Rekomendasi:</b> Perbaiki SLA logistik terutama untuk kategori furnitur dan produk berat.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2: Revenue per State
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">❓ Pertanyaan Bisnis 2</div>', unsafe_allow_html=True)
    st.info("**\"Bagaimana distribusi revenue berdasarkan state di Brasil selama 2017–2018, dan state mana yang memiliki potensi pertumbuhan tertinggi?\"**")
    
    if state_df is not None:
        col_e, col_f = st.columns(2)
        
        with col_e:
            st.markdown("#### 💰 Total Revenue per State")
            fig, ax = plt.subplots(figsize=(8, 7))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            state_sorted = state_df.sort_values('total_revenue', ascending=True)
            colors_s = ['#2D6A4F' if r > state_df['total_revenue'].median() else '#B7E4C7' 
                        for r in state_sorted['total_revenue']]
            ax.barh(state_sorted['customer_state'], state_sorted['total_revenue'] / 1e6,
                    color=colors_s, edgecolor='white')
            ax.set_xlabel('Revenue (Juta BRL)', fontsize=10)
            ax.set_title('Total Revenue per State (Juta BRL)', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.tick_params(labelsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col_f:
            st.markdown("#### 📈 Average Order Value (AOV) per State")
            fig, ax = plt.subplots(figsize=(8, 7))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            state_aov = state_df.sort_values('aov', ascending=True)
            colors_aov = ['#457B9D' if a > state_df['aov'].median() else '#B7E4C7' 
                         for a in state_aov['aov']]
            ax.barh(state_aov['customer_state'], state_aov['aov'],
                    color=colors_aov, edgecolor='white')
            ax.axvline(x=state_df['aov'].mean(), color='red', linestyle='--', 
                       linewidth=1.5, label=f"Mean: R${state_df['aov'].mean():.0f}")
            ax.set_xlabel('AOV (BRL)', fontsize=10)
            ax.set_title('Average Order Value per State', fontsize=12, fontweight='bold')
            ax.legend(fontsize=9)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.tick_params(labelsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        # Tren bulanan
        st.markdown("---")
        st.markdown("#### 📅 Tren Bulanan Revenue dan Order")
        filtered_df['year_month'] = filtered_df['order_purchase_timestamp'].dt.to_period('M')
        monthly = filtered_df.groupby('year_month').agg(
            revenue=('payment_value', 'sum'),
            orders=('order_id', 'nunique')
        ).reset_index()
        monthly['ym_str'] = monthly['year_month'].astype(str)
        
        fig, ax1 = plt.subplots(figsize=(14, 4))
        fig.patch.set_facecolor('#FAFAFA')
        ax1.set_facecolor('#FAFAFA')
        x = range(len(monthly))
        ax1.fill_between(x, monthly['revenue']/1e3, alpha=0.2, color='#457B9D')
        ax1.plot(x, monthly['revenue']/1e3, color='#1D3557', linewidth=2.5, 
                 marker='o', markersize=5, label='Revenue (K BRL)')
        ax1.set_ylabel('Revenue (Ribu BRL)', color='#1D3557', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='#1D3557')
        
        ax2 = ax1.twinx()
        ax2.plot(x, monthly['orders'], color='#E63946', linewidth=2,
                 linestyle='--', marker='s', markersize=5, label='Orders')
        ax2.set_ylabel('Jumlah Order', color='#E63946', fontsize=10)
        ax2.tick_params(axis='y', labelcolor='#E63946')
        
        ax1.set_xticks(x)
        ax1.set_xticklabels(monthly['ym_str'], rotation=45, ha='right', fontsize=8)
        ax1.set_title('Tren Bulanan Revenue dan Jumlah Order', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.2)
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        st.markdown("""
        <div class="insight-box">
        💡 <b>Insight:</b> São Paulo (SP) mendominasi revenue total >40%. State seperti DF memiliki AOV tertinggi — 
        indikasi pasar premium. Tren menunjukkan pertumbuhan konsisten dengan lonjakan Black Friday November 2017.
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: RFM Analysis
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🧠 RFM Analysis — Segmentasi Pelanggan</div>', unsafe_allow_html=True)
    st.markdown("RFM Analysis mengelompokkan pelanggan berdasarkan **Recency** (kapan terakhir beli), **Frequency** (seberapa sering), dan **Monetary** (berapa total belanja).")
    
    if rfm_df is not None:
        segment_colors = {
            'Champions': '#2D6A4F', 'Loyal Customers': '#52B788',
            'Recent Customers': '#74C69D', 'Potential Loyalists': '#B7E4C7',
            'At Risk': '#F28A2E', 'Cant Lose Them': '#E63946', 'Lost': '#9D0208'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥧 Distribusi Segmen")
            seg_counts = rfm_df['Segment'].value_counts()
            colors_pie = [segment_colors.get(s, '#999') for s in seg_counts.index]
            fig, ax = plt.subplots(figsize=(7, 5))
            fig.patch.set_facecolor('#FAFAFA')
            wedges, texts, autotexts = ax.pie(
                seg_counts.values, labels=seg_counts.index,
                colors=colors_pie, autopct='%1.1f%%', startangle=140,
                textprops={'fontsize': 9}
            )
            for at in autotexts: at.set_fontsize(8)
            ax.set_title('Segmen Pelanggan Olist', fontsize=12, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 💵 Rata-rata Monetary per Segmen")
            seg_m = rfm_df.groupby('Segment')['monetary'].mean().sort_values(ascending=True)
            colors_m = [segment_colors.get(s, '#999') for s in seg_m.index]
            fig, ax = plt.subplots(figsize=(7, 5))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            ax.barh(seg_m.index, seg_m.values, color=colors_m, edgecolor='white')
            ax.set_xlabel('Avg Monetary (BRL)', fontsize=10)
            ax.set_title('Total Belanja per Segmen', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            ax.tick_params(labelsize=9)
            for i, v in enumerate(seg_m.values):
                ax.text(v + 5, i, f'R${v:.0f}', va='center', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        st.markdown("#### 📊 Statistik RFM per Segmen")
        rfm_stats = rfm_df.groupby('Segment')[['recency','frequency','monetary']].mean().round(2)
        rfm_stats['count'] = rfm_df.groupby('Segment').size()
        st.dataframe(rfm_stats.style.background_gradient(cmap='Greens', subset=['monetary'])
                    .format({'recency': '{:.0f}', 'frequency': '{:.2f}', 
                             'monetary': 'R${:.2f}', 'count': '{:,.0f}'}),
                    use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        💡 <b>Insight RFM:</b> Segmen <b>Champions</b> memiliki nilai moneter tertinggi dan frekuensi pembelian terbanyak — 
        prioritaskan program loyalty untuk mempertahankan mereka. Segmen <b>At Risk</b> perlu kampanye re-engagement segera.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data RFM tidak ditemukan. Jalankan notebook terlebih dahulu.")

# ═══════════════════════════════════════════════════════════════
# TAB 4: Clustering
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔵 Clustering — Potensi Pertumbuhan per State</div>', unsafe_allow_html=True)
    st.markdown("Manual grouping menggunakan **binning** berdasarkan volume order dan AOV untuk mengidentifikasi segmen pasar per state.")
    
    if cluster_df is not None:
        cluster_colors = {
            '⭐ Star Market': '#2D6A4F', '📈 High Volume': '#52B788',
            '💎 Premium Niche': '#457B9D', '🔼 Growth Potential': '#F28A2E',
            '📊 Developing': '#B7E4C7', '🌱 Emerging': '#D8F3DC'
        }
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### 📍 Scatter: Total Orders vs AOV")
            fig, ax = plt.subplots(figsize=(9, 6))
            fig.patch.set_facecolor('#FAFAFA')
            ax.set_facecolor('#FAFAFA')
            for cluster, color in cluster_colors.items():
                subset = cluster_df[cluster_df['cluster'] == cluster]
                if len(subset) > 0:
                    ax.scatter(subset['total_orders'], subset['aov'],
                               label=cluster, color=color, s=120, alpha=0.85,
                               edgecolors='white', linewidth=0.8)
                    for _, row in subset.iterrows():
                        ax.annotate(row['customer_state'],
                                    (row['total_orders'], row['aov']),
                                    fontsize=7.5, ha='center', va='bottom',
                                    xytext=(0, 6), textcoords='offset points')
            ax.set_xlabel('Total Orders', fontsize=11)
            ax.set_ylabel('Average Order Value (BRL)', fontsize=11)
            ax.set_title('Clustering State: Volume Order vs AOV', fontsize=12, fontweight='bold')
            ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
            ax.grid(alpha=0.2, linestyle='--')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 📋 Detail per Cluster")
            cluster_summary = cluster_df.groupby('cluster').agg(
                states=('customer_state', 'count'),
                avg_revenue=('total_revenue', 'mean'),
                avg_aov=('aov', 'mean')
            ).round(0)
            cluster_summary.columns = ['States', 'Avg Revenue', 'Avg AOV']
            st.dataframe(cluster_summary.style.format({'Avg Revenue': 'R${:,.0f}', 'Avg AOV': 'R${:,.0f}'}),
                        use_container_width=True, height=280)
            
            st.markdown("**State per Cluster:**")
            for cluster in cluster_df['cluster'].unique():
                states_in = cluster_df[cluster_df['cluster'] == cluster]['customer_state'].tolist()
                st.markdown(f"**{cluster}**: {', '.join(states_in)}")
        
        st.markdown("""
        <div class="insight-box">
        💡 <b>Insight Clustering:</b> SP adalah satu-satunya <b>Star Market</b> — volume tinggi dan AOV tinggi. 
        State seperti DF dan AC masuk <b>Premium Niche</b> — pasar kecil tapi nilai transaksi tinggi, 
        cocok untuk kampanye produk premium. State-state Utara Brasil masuk <b>Emerging</b> — potensi ekspansi jangka panjang.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data clustering tidak ditemukan. Jalankan notebook terlebih dahulu.")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6B7280; font-size:0.85rem; padding: 1rem 0;">
    🛒 Brazilian E-Commerce Dashboard | Data: Olist via Kaggle | Built with Streamlit & Matplotlib
</div>
""", unsafe_allow_html=True)
