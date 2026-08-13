import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ========== Page Config ==========
st.set_page_config(
    page_title="Billing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== Custom CSS ==========
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0a0e1a 100%); }
    .main .block-container { padding-top: 0rem !important; padding-bottom: 2rem !important; }
    
    .header {
        background: linear-gradient(135deg, #0f1729 0%, #1a2744 50%, #0f1729 100%);
        padding: 18px 30px;
        margin: -10px -10px 25px -10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #fbbf24;
        box-shadow: 0 4px 40px rgba(251,191,36,0.08);
        border-radius: 0 0 20px 20px;
    }
    .header-title { font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px; }
    .header-title .highlight { color: #fbbf24; text-shadow: 0 0 30px rgba(251,191,36,0.2); }
    .header-sub { color: #94a3b8; font-size: 13px; letter-spacing: 1px; margin-top: 2px; }
    .header-right { color: #ffffff; text-align: right; font-size: 14px; }
    .header-right .date { color: #94a3b8; font-size: 12px; }
    .badge { background: rgba(251,191,36,0.12); padding: 4px 14px; border-radius: 20px; font-size: 12px; color: #fbbf24; border: 1px solid rgba(251,191,36,0.15); }
    
    .stButton button {
        background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
        color: #0a0e1a !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        font-size: 13px !important;
        letter-spacing: 0.3px !important;
    }
    .stButton button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(251,191,36,0.2) !important; }
    
    .kpi-card {
        background: linear-gradient(145deg, #1a2744, #0f1729);
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 4px 25px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: default;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
    }
    .kpi-card:hover { transform: translateY(-4px); border-color: rgba(251,191,36,0.15); box-shadow: 0 8px 35px rgba(251,191,36,0.08); }
    .kpi-card .value { font-size: 30px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px; }
    .kpi-card .value .pct { font-size: 16px; color: #94a3b8; font-weight: 400; }
    .kpi-card .label { font-size: 13px; color: #94a3b8; margin-top: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-card .icon { position: absolute; right: 18px; top: 18px; font-size: 30px; opacity: 0.10; }
    .kpi-card.gold::before { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
    .kpi-card.green::before { background: linear-gradient(90deg, #34d399, #059669); }
    .kpi-card.blue::before { background: linear-gradient(90deg, #60a5fa, #2563eb); }
    .kpi-card.red::before { background: linear-gradient(90deg, #f87171, #dc2626); }
    .kpi-card.purple::before { background: linear-gradient(90deg, #a78bfa, #7c3aed); }
    .kpi-card.cyan::before { background: linear-gradient(90deg, #22d3ee, #0891b2); }
    .kpi-card.pink::before { background: linear-gradient(90deg, #f472b6, #db2777); }
    .kpi-card.teal::before { background: linear-gradient(90deg, #2dd4bf, #0d9488); }
    .kpi-card.orange::before { background: linear-gradient(90deg, #fb923c, #f97316); }
    
    .section-title { color: #ffffff; font-size: 20px; font-weight: 600; margin: 28px 0 16px 0; padding-bottom: 10px; border-bottom: 2px solid rgba(251,191,36,0.12); display: flex; align-items: center; gap: 10px; }
    .section-title span { color: #fbbf24; }
    
    .filter-box { background: rgba(255,255,255,0.02); border-radius: 14px; padding: 16px 20px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.04); }
    .filter-label { color: #ffffff !important; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
    
    .stSelectbox > div > div { background: #0f1729 !important; border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 10px !important; color: #ffffff !important; }
    .stSelectbox label { color: #ffffff !important; font-weight: 600 !important; font-size: 14px !important; letter-spacing: 0.5px !important; }
    
    .stDataFrame { background: transparent !important; border-radius: 14px !important; border: 1px solid rgba(255,255,255,0.04) !important; overflow: hidden !important; }
    .stDataFrame thead { background: #1a2744 !important; }
    
    .footer { text-align: center; padding: 25px; margin-top: 35px; border-top: 1px solid rgba(255,255,255,0.04); color: #64748b; font-size: 13px; letter-spacing: 0.5px; }
    .footer strong { color: #94a3b8; }
    .footer .email { color: #fbbf24; text-decoration: none; font-weight: 500; }
    .footer .email:hover { color: #f59e0b; text-decoration: underline; }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #fbbf24; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ========== File Paths (Dynamic - Cloud Ready) ==========
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

BILLED_FILE_XLSX = os.path.join(BASE_PATH, "billed_data.xlsx")
BILLED_FILE_CSV = os.path.join(BASE_PATH, "billed_data.csv")
BILLABLE_FILE_XLSX = os.path.join(BASE_PATH, "billable_data.xlsx")
BILLABLE_FILE_CSV = os.path.join(BASE_PATH, "billable_data.csv")

RDF_IDF_FILE_XLSX = os.path.join(BASE_PATH, "rdf_idf.xlsx")
RDF_IDF_FILE_CSV = os.path.join(BASE_PATH, "rdf_idf.csv")

SAME_LOCATION_FILE_XLSX = os.path.join(BASE_PATH, "same_location.xlsx")
SAME_LOCATION_FILE_CSV = os.path.join(BASE_PATH, "same_location.csv")

# New: Agent Master file
AGENT_MASTER_FILE_XLSX = os.path.join(BASE_PATH, "agent_master.xlsx")
AGENT_MASTER_FILE_CSV = os.path.join(BASE_PATH, "agent_master.csv")

# ========== Utility Functions ==========
def normalize_agent_id(series):
    s = series.fillna('').astype(str).str.strip().str.upper()
    s = s.str.replace(r'\.0$', '', regex=True)
    s = s.str.strip("'\"")
    return s

# ========== Load Excel / CSV Files ==========
@st.cache_data(ttl=3600)
def load_billed_file():
    if os.path.exists(BILLED_FILE_XLSX):
        df = pd.read_excel(BILLED_FILE_XLSX)
    elif os.path.exists(BILLED_FILE_CSV):
        df = pd.read_csv(BILLED_FILE_CSV)
    else:
        return None

    df.columns = df.columns.str.upper().str.strip()
    return df


@st.cache_data(ttl=3600)
def load_billable_file():
    if os.path.exists(BILLABLE_FILE_XLSX):
        df = pd.read_excel(BILLABLE_FILE_XLSX)
    elif os.path.exists(BILLABLE_FILE_CSV):
        df = pd.read_csv(BILLABLE_FILE_CSV)
    else:
        return None

    df.columns = df.columns.str.upper().str.strip()
    return df


@st.cache_data(ttl=3600)
def load_rdf_idf_file():
    empty_cols = [
        'DIV_CODE', 'DIVISION',
        'total_rdf_idf', 'rdf_count', 'idf_count',
        'newly_rdf_count', 'newly_idf_count', 'newly_total'
    ]

    if os.path.exists(RDF_IDF_FILE_XLSX):
        df = pd.read_excel(RDF_IDF_FILE_XLSX)
    elif os.path.exists(RDF_IDF_FILE_CSV):
        df = pd.read_csv(RDF_IDF_FILE_CSV)
    else:
        return pd.DataFrame(columns=empty_cols)

    df.columns = df.columns.str.lower().str.strip()

    required = [
        'acct_id', 'agent_id', 'div_code', 'division',
        'curr_meter_read_remark', 'prev_meter_read_remark',
        'prev_bill_basis'
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ''

    for col in required:
        df[col] = df[col].fillna('').astype(str).str.strip()

    df['curr_meter_read_remark'] = df['curr_meter_read_remark'].str.upper()
    df['prev_bill_basis'] = df['prev_bill_basis'].str.upper()

    rdf_idf = df[
        df['curr_meter_read_remark'].isin(['RDF', 'IDF'])
    ].copy()

    if len(rdf_idf) == 0:
        return pd.DataFrame(columns=empty_cols)

    rdf_idf['is_rdf'] = (rdf_idf['curr_meter_read_remark'] == 'RDF').astype(int)
    rdf_idf['is_idf'] = (rdf_idf['curr_meter_read_remark'] == 'IDF').astype(int)
    rdf_idf['is_newly'] = (rdf_idf['prev_bill_basis'] == 'MU').astype(int)

    rdf_idf['newly_rdf'] = ((rdf_idf['is_rdf'] == 1) & (rdf_idf['is_newly'] == 1)).astype(int)
    rdf_idf['newly_idf'] = ((rdf_idf['is_idf'] == 1) & (rdf_idf['is_newly'] == 1)).astype(int)

    result = rdf_idf.groupby(
        ['div_code', 'division'],
        dropna=False
    ).agg(
        total_rdf_idf=('curr_meter_read_remark', 'size'),
        rdf_count=('is_rdf', 'sum'),
        idf_count=('is_idf', 'sum'),
        newly_rdf_count=('newly_rdf', 'sum'),
        newly_idf_count=('newly_idf', 'sum')
    ).reset_index()

    result['newly_total'] = result['newly_rdf_count'] + result['newly_idf_count']

    result.columns = [
        'DIV_CODE', 'DIVISION',
        'total_rdf_idf', 'rdf_count', 'idf_count',
        'newly_rdf_count', 'newly_idf_count', 'newly_total'
    ]

    return result


@st.cache_data(ttl=3600)
def load_rdf_idf_mr_file():
    required = [
        'ACCT_ID', 'AGENT_ID', 'DIV_CODE', 'DIVISION',
        'CURR_METER_READ_REMARK', 'PREV_METER_READ_REMARK',
        'PREV_BILL_BASIS'
    ]

    if os.path.exists(RDF_IDF_FILE_CSV):
        df = pd.read_csv(RDF_IDF_FILE_CSV, dtype=str, low_memory=False)
    elif os.path.exists(RDF_IDF_FILE_XLSX):
        df = pd.read_excel(RDF_IDF_FILE_XLSX, dtype=str)
    else:
        return pd.DataFrame(columns=required)

    df.columns = df.columns.str.upper().str.strip()

    for col in required:
        if col not in df.columns:
            df[col] = ''

    for col in required:
        df[col] = df[col].fillna('').astype(str).str.strip()

    df['AGENT_ID'] = normalize_agent_id(df['AGENT_ID'])
    df['CURR_METER_READ_REMARK'] = df['CURR_METER_READ_REMARK'].str.upper().str.strip()
    df['PREV_BILL_BASIS'] = df['PREV_BILL_BASIS'].str.upper().str.strip()

    df = df[
        df['AGENT_ID'].ne('') &
        df['CURR_METER_READ_REMARK'].isin(['RDF', 'IDF'])
    ].copy()

    df['RDF_COUNT'] = (df['CURR_METER_READ_REMARK'].eq('RDF')).astype(int)
    df['IDF_COUNT'] = (df['CURR_METER_READ_REMARK'].eq('IDF')).astype(int)
    df['NEWLY_RDF_COUNT'] = (df['CURR_METER_READ_REMARK'].eq('RDF') & df['PREV_BILL_BASIS'].eq('MU')).astype(int)
    df['NEWLY_IDF_COUNT'] = (df['CURR_METER_READ_REMARK'].eq('IDF') & df['PREV_BILL_BASIS'].eq('MU')).astype(int)

    return df


@st.cache_data(ttl=3600)
def load_same_location_file():
    empty_cols = ['DIV_CODE', 'AGENT_ID', 'LATITUDE', 'LONGITUDE', 'TOTAL_BILLS']

    if os.path.exists(SAME_LOCATION_FILE_XLSX):
        df = pd.read_excel(SAME_LOCATION_FILE_XLSX)
    elif os.path.exists(SAME_LOCATION_FILE_CSV):
        df = pd.read_csv(SAME_LOCATION_FILE_CSV)
    else:
        return pd.DataFrame(columns=empty_cols)

    df.columns = df.columns.str.upper().str.strip()

    required = ['DIV_CODE', 'AGENT_ID', 'LATITUDE', 'LONGITUDE', 'TOTAL_BILLS']

    for col in required:
        if col not in df.columns:
            df[col] = ''

    df['DIV_CODE'] = df['DIV_CODE'].fillna('').astype(str).str.strip()
    df['AGENT_ID'] = normalize_agent_id(df['AGENT_ID'])

    df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
    df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')
    df['TOTAL_BILLS'] = pd.to_numeric(df['TOTAL_BILLS'], errors='coerce').fillna(0)

    return df[
        (df['AGENT_ID'] != '') &
        (df['DIV_CODE'] != '')
    ].copy()


# ========== Load Agent Master ==========
@st.cache_data(ttl=3600)
def load_agent_master():
    if os.path.exists(AGENT_MASTER_FILE_XLSX):
        df = pd.read_excel(AGENT_MASTER_FILE_XLSX, dtype=str)
    elif os.path.exists(AGENT_MASTER_FILE_CSV):
        df = pd.read_csv(AGENT_MASTER_FILE_CSV, dtype=str)
    else:
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['AGENT_ID', 'AGENCY', 'DIVISION_CODE', 'NAME', 'MOBILE_NO'])

    df.columns = df.columns.str.upper().str.strip()
    # Ensure required columns exist
    for col in ['AGENT_ID', 'AGENCY', 'DIVISION_CODE', 'NAME', 'MOBILE_NO']:
        if col not in df.columns:
            df[col] = ''
    # Normalize AGENT_ID for merging
    df['AGENT_ID'] = normalize_agent_id(df['AGENT_ID'])
    # Keep only necessary columns
    df = df[['AGENT_ID', 'AGENCY', 'DIVISION_CODE', 'NAME', 'MOBILE_NO']].drop_duplicates(subset=['AGENT_ID'])
    return df


def merge_data(df_billed, df_billable, df_rdf_idf):
    if df_billed is not None and df_billable is not None:
        df_billed_grouped = df_billed.groupby('DIV_NAME').agg({
            'AGENT_ID': 'count',
            'BILLED': 'sum',
            'MOB_MRI': 'sum',
            'OCR': 'sum',
            'MANUAL_BILL': 'sum',
            'MU_BILLED': 'sum'
        }).reset_index()

        df_billed_grouped.columns = [
            'DIVISION', 'total_agents', 'billed_consumers',
            'mob_mri', 'ocr', 'manual_bill', 'mu_billed'
        ]

        df_merged = pd.merge(
            df_billable,
            df_billed_grouped,
            on='DIVISION',
            how='left'
        ).fillna(0)

        if df_rdf_idf is not None and len(df_rdf_idf) > 0:
            df_merged = pd.merge(
                df_merged,
                df_rdf_idf,
                on=['DIV_CODE', 'DIVISION'],
                how='left'
            ).fillna(0)
        else:
            for col in [
                'total_rdf_idf', 'rdf_count', 'idf_count',
                'newly_rdf_count', 'newly_idf_count', 'newly_total'
            ]:
                df_merged[col] = 0

        df_merged['billing_percentage'] = (
            (df_merged['billed_consumers'] / df_merged['BILLABLE']) * 100
        ).round(2).fillna(0)

        df_merged['unbilled_consumers'] = (
            df_merged['BILLABLE'] - df_merged['billed_consumers']
        )

        df_merged['auto_billing'] = (
            df_merged['mob_mri'] + df_merged['ocr']
        )

        df_merged['auto_percentage'] = (
            (df_merged['auto_billing'] / df_merged['billed_consumers']) * 100
        ).round(2).fillna(0)

        df_merged['probe_percentage'] = (
            (df_merged['mob_mri'] / df_merged['billed_consumers']) * 100
        ).round(2).fillna(0)

        df_merged['ocr_percentage'] = (
            (df_merged['ocr'] / df_merged['billed_consumers']) * 100
        ).round(2).fillna(0)

        df_merged['rdf_percentage'] = (
            (df_merged['rdf_count'] / df_merged['BILLABLE']) * 100
        ).round(2).fillna(0)

        df_merged['idf_percentage'] = (
            (df_merged['idf_count'] / df_merged['BILLABLE']) * 100
        ).round(2).fillna(0)

        df_merged['newly_rdf_percentage'] = (
            (df_merged['newly_rdf_count'] / df_merged['BILLABLE']) * 100
        ).round(2).fillna(0)

        df_merged['newly_idf_percentage'] = (
            (df_merged['newly_idf_count'] / df_merged['BILLABLE']) * 100
        ).round(2).fillna(0)

        return df_merged

    return None


with st.spinner("📂 Loading data..."):
    df_billed = load_billed_file()
    df_billable = load_billable_file()
    df_rdf_idf = load_rdf_idf_file()
    df_rdf_idf_mr = load_rdf_idf_mr_file()
    df_same_location = load_same_location_file()
    df_agent_master = load_agent_master()

if df_billed is None or df_billable is None:
    st.error("❌ Files not found! Please ensure all required files are in the same folder as app.py")
    st.info("""
    ### Required Files:
    - `billed_data.xlsx` or `billed_data.csv`
    - `billable_data.xlsx` or `billable_data.csv`
    - `rdf_idf.xlsx` or `rdf_idf.csv`
    - `same_location.xlsx` or `same_location.csv`
    - `agent_master.xlsx` or `agent_master.csv` (optional, but recommended)
    - `requirements.txt`
    """)
    st.stop()

with st.spinner("🔄 Merging data..."):
    df = merge_data(df_billed, df_billable, df_rdf_idf)

if df is None or len(df) == 0:
    st.warning("⚠️ No data found after merging.")
    st.stop()


current_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

st.markdown(f"""
<div class="header">
    <div>
        <div class="header-title">📊 <span class="highlight">Billing</span> Dashboard</div>
        <div class="header-sub">Real-time Electricity Meter Reading Analytics</div>
    </div>
    <div class="header-right">
        <div style="font-size:18px; font-weight:600;">FG Agency</div>
        <div class="date">📅 {current_date}</div>
        <div style="margin-top:4px;"><span class="badge">● Live</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

col_nav1, col_nav2 = st.columns([1, 1])

with col_nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'Home'
        st.rerun()

with col_nav2:
    if st.button("📊 MR Analysis", use_container_width=True):
        st.session_state.current_page = 'MR Analysis'
        st.rerun()

st.markdown("---")


# ============================================================
# ========== PAGE: HOME ==========
# ============================================================
def render_home():
    with st.container():
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;"><span style="color:#fbbf24;">🔍</span> <span style="color:#ffffff; font-size:12px; font-weight:600; letter-spacing:1px;">FILTERS</span></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        zone_col = 'ZONE' if 'ZONE' in df.columns else 'ZONE_NAME' if 'ZONE_NAME' in df.columns else None
        circle_col = 'CIRCLE' if 'CIRCLE' in df.columns else 'CIRCLE_NAME' if 'CIRCLE_NAME' in df.columns else None
        div_col = 'DIVISION' if 'DIVISION' in df.columns else 'DIV_NAME' if 'DIV_NAME' in df.columns else None

        if zone_col:
            with col1:
                zone_options = ['Overall'] + sorted(df[zone_col].dropna().unique().tolist())
                selected_zone = st.selectbox("🏢 Zone", zone_options, key="zone_filter_home")
            zone_df = df.copy() if selected_zone == 'Overall' else df[df[zone_col] == selected_zone]
        else:
            zone_df = df.copy()

        if circle_col:
            with col2:
                circle_options = ['All Circles'] + sorted(zone_df[circle_col].dropna().unique().tolist())
                selected_circle = st.selectbox("🔵 Circle", circle_options, key="circle_filter_home")
            circle_df = zone_df.copy() if selected_circle == 'All Circles' else zone_df[zone_df[circle_col] == selected_circle]
        else:
            circle_df = zone_df.copy()

        if div_col:
            with col3:
                div_options = ['All Divisions'] + sorted(circle_df[div_col].dropna().unique().tolist())
                selected_division = st.selectbox("📂 Division", div_options, key="div_filter_home")
            filtered_df = circle_df.copy() if selected_division == 'All Divisions' else circle_df[circle_df[div_col] == selected_division]
        else:
            filtered_df = circle_df.copy()
        
        st.markdown('</div>', unsafe_allow_html=True)

    total_billable = filtered_df['BILLABLE'].sum()
    total_billed = filtered_df['billed_consumers'].sum()
    total_unbilled = filtered_df['unbilled_consumers'].sum()
    total_auto = filtered_df['auto_billing'].sum()
    total_manual = filtered_df['manual_bill'].sum()
    total_mob = filtered_df['mob_mri'].sum()
    total_ocr = filtered_df['ocr'].sum()
    total_rdf = filtered_df['rdf_count'].sum()
    total_idf = filtered_df['idf_count'].sum()
    total_rdf_idf = filtered_df['total_rdf_idf'].sum()
    total_newly_rdf = filtered_df['newly_rdf_count'].sum()
    total_newly_idf = filtered_df['newly_idf_count'].sum()
    total_newly = filtered_df['newly_total'].sum()
    active_agents = df_billed['AGENT_ID'].nunique()

    st.markdown('<div class="section-title">📊 <span>Key Metrics</span></div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card gold">
            <div class="icon">📊</div>
            <div class="value">{total_billable:,.0f}</div>
            <div class="label">Total Billable</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        pct = (total_billed / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card green">
            <div class="icon">✅</div>
            <div class="value">{total_billed:,.0f} <span class="pct">({pct:.1f}%)</span></div>
            <div class="label">Total Billed</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        unbilled_pct = (total_unbilled / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card red">
            <div class="icon">❌</div>
            <div class="value">{total_unbilled:,.0f} <span class="pct">({unbilled_pct:.1f}%)</span></div>
            <div class="label">Total Unbilled</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        billing_pct = (total_billed / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card blue">
            <div class="icon">📈</div>
            <div class="value">{billing_pct:.1f}%</div>
            <div class="label">Billing %</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    
    probe_pct = (total_mob / total_billed * 100) if total_billed > 0 else 0
    with c1:
        st.markdown(f"""
        <div class="kpi-card cyan">
            <div class="icon">📱</div>
            <div class="value">{total_mob:,.0f} <span class="pct">({probe_pct:.1f}%)</span></div>
            <div class="label">Probe (MOB_MRI)</div>
        </div>
        """, unsafe_allow_html=True)
    
    ocr_pct = (total_ocr / total_billed * 100) if total_billed > 0 else 0
    with c2:
        st.markdown(f"""
        <div class="kpi-card purple">
            <div class="icon">🔍</div>
            <div class="value">{total_ocr:,.0f} <span class="pct">({ocr_pct:.1f}%)</span></div>
            <div class="label">OCR</div>
        </div>
        """, unsafe_allow_html=True)
    
    auto_pct = (total_auto / total_billed * 100) if total_billed > 0 else 0
    with c3:
        st.markdown(f"""
        <div class="kpi-card teal">
            <div class="icon">🤖</div>
            <div class="value">{total_auto:,.0f} <span class="pct">({auto_pct:.1f}%)</span></div>
            <div class="label">Auto Billing</div>
        </div>
        """, unsafe_allow_html=True)
    
    manual_pct = (total_manual / total_billed * 100) if total_billed > 0 else 0
    with c4:
        st.markdown(f"""
        <div class="kpi-card pink">
            <div class="icon">📝</div>
            <div class="value">{total_manual:,.0f} <span class="pct">({manual_pct:.1f}%)</span></div>
            <div class="label">Manual Billing</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔴 <span>RDF / IDF Analysis</span></div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        rdf_pct = (total_rdf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card red">
            <div class="icon">🔴</div>
            <div class="value">{total_rdf:,.0f} <span class="pct">({rdf_pct:.1f}%)</span></div>
            <div class="label">Total RDF</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        idf_pct = (total_idf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card purple">
            <div class="icon">🟣</div>
            <div class="value">{total_idf:,.0f} <span class="pct">({idf_pct:.1f}%)</span></div>
            <div class="label">Total IDF</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        rdfidf_pct = (total_rdf_idf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card gold">
            <div class="icon">📊</div>
            <div class="value">{total_rdf_idf:,.0f} <span class="pct">({rdfidf_pct:.1f}%)</span></div>
            <div class="label">RDF + IDF</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        rdf_only_pct = (total_rdf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card blue">
            <div class="icon">📈</div>
            <div class="value">{rdf_only_pct:.1f}%</div>
            <div class="label">RDF %</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🆕 <span>Newly RDF / IDF</span></div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        newly_rdf_pct = (total_newly_rdf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card green">
            <div class="icon">🆕</div>
            <div class="value">{total_newly_rdf:,.0f} <span class="pct">({newly_rdf_pct:.1f}%)</span></div>
            <div class="label">Newly RDF</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        newly_idf_pct = (total_newly_idf / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card cyan">
            <div class="icon">🆕</div>
            <div class="value">{total_newly_idf:,.0f} <span class="pct">({newly_idf_pct:.1f}%)</span></div>
            <div class="label">Newly IDF</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        newly_total_pct = (total_newly / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card gold">
            <div class="icon">📊</div>
            <div class="value">{total_newly:,.0f} <span class="pct">({newly_total_pct:.1f}%)</span></div>
            <div class="label">Newly Total</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        newly_only_pct = (total_newly / total_billable * 100) if total_billable > 0 else 0
        st.markdown(f"""
        <div class="kpi-card purple">
            <div class="icon">📈</div>
            <div class="value">{newly_only_pct:.1f}%</div>
            <div class="label">Newly %</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 <span>Summary Rings</span></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        fig1 = go.Figure(data=[go.Pie(
            labels=['Billed', 'Unbilled'],
            values=[total_billed, total_unbilled],
            hole=.6,
            marker_colors=['#34d399', '#f87171']
        )])
        fig1.update_layout(
            title_text="<b style='color:#34d399;'>✅ Billable vs Unbilled</b><br><span style='font-size:13px;color:#94a3b8;'>" + f"{total_billable:,.0f}" + " Total</span>",
            title_x=0.5,
            title_font_size=14,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            annotations=[dict(
                text=f"{(total_billed/total_billable*100) if total_billable > 0 else 0:.1f}%",
                x=0.5, y=0.5, font_size=28, showarrow=False,
                font_color='#34d399', font_weight='bold'
            )]
        )
        fig1.update_traces(textposition='inside', textinfo='percent', textfont_color='#ffffff')
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with c2:
        fig2 = go.Figure(data=[go.Pie(
            labels=['Auto (Probe+OCR)', 'Manual'],
            values=[total_auto, total_manual],
            hole=.6,
            marker_colors=['#60a5fa', '#fbbf24']
        )])
        fig2.update_layout(
            title_text="<b style='color:#60a5fa;'>🤖 Auto vs Manual</b><br><span style='font-size:13px;color:#94a3b8;'>" + f"{total_billed:,.0f}" + " Billed</span>",
            title_x=0.5,
            title_font_size=14,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            annotations=[dict(
                text=f"{(total_auto/total_billed*100) if total_billed > 0 else 0:.1f}%",
                x=0.5, y=0.5, font_size=28, showarrow=False,
                font_color='#60a5fa', font_weight='bold'
            )]
        )
        fig2.update_traces(textposition='inside', textinfo='percent', textfont_color='#ffffff')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with c3:
        fig3 = go.Figure(data=[go.Pie(
            labels=['Probe (MOB_MRI)', 'OCR'],
            values=[total_mob, total_ocr],
            hole=.6,
            marker_colors=['#2dd4bf', '#a78bfa']
        )])
        fig3.update_layout(
            title_text="<b style='color:#a78bfa;'>📱 Probe vs OCR</b><br><span style='font-size:13px;color:#94a3b8;'>" + f"{total_auto:,.0f}" + " Auto</span>",
            title_x=0.5,
            title_font_size=14,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            annotations=[dict(
                text=f"{(total_mob/total_auto*100) if total_auto > 0 else 0:.1f}%",
                x=0.5, y=0.5, font_size=28, showarrow=False,
                font_color='#a78bfa', font_weight='bold'
            )]
        )
        fig3.update_traces(textposition='inside', textinfo='percent', textfont_color='#ffffff')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="section-title">📋 <span>Click to View Reports</span></div>', unsafe_allow_html=True)
    
    a, b, c, d = st.columns(4)
    show_line = a.button("📈 Day-wise Trend", use_container_width=True)
    show_top_bill = b.button("🏆 Top 10 Billing %", use_container_width=True)
    show_worst_bill = c.button("📉 Worst 10 Billing %", use_container_width=True)
    show_top_auto = d.button("🤖 Top 10 Auto %", use_container_width=True)

    a, b, c, d = st.columns(4)
    show_worst_auto = a.button("📉 Worst 10 Auto %", use_container_width=True)
    show_top_probe = b.button("📱 Top 10 Probe %", use_container_width=True)
    show_worst_probe = c.button("📉 Worst 10 Probe %", use_container_width=True)
    show_top_ocr = d.button("📊 Top 10 OCR %", use_container_width=True)

    a, b, c, d = st.columns(4)
    show_worst_ocr = a.button("📉 Worst 10 OCR %", use_container_width=True)
    show_top_rdf = b.button("🔴 Top 10 RDF", use_container_width=True)
    show_worst_rdf = c.button("📉 Worst 10 RDF", use_container_width=True)
    show_top_idf = d.button("🟣 Top 10 IDF", use_container_width=True)

    st.markdown("---")

    def show_report(title, data, x_col, y_col, y_format=''):
        st.subheader(title)
        fig = px.bar(
            data, x=x_col, y=y_col, title=title, color=y_col,
            color_continuous_scale=['#f87171', '#fbbf24', '#34d399'],
            text=y_col, template='plotly_dark'
        )
        if y_format == '%':
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.dataframe(data, use_container_width=True)
        st.markdown("---")

    if show_line and 'BILL_DATE' in df_billed.columns:
        st.subheader("📈 Day-wise Billing Trend")
        df_billed['BILL_DATE'] = pd.to_datetime(df_billed['BILL_DATE'], errors='coerce')
        filtered_divs = filtered_df['DIVISION'].tolist() if 'DIVISION' in filtered_df.columns else []
        if filtered_divs:
            day_data = df_billed[df_billed['DIV_NAME'].isin(filtered_divs)]
            if len(day_data) > 0:
                day_wise = day_data.groupby('BILL_DATE').agg({
                    'BILLED': 'sum', 'MOB_MRI': 'sum', 'OCR': 'sum', 'MU_BILLED': 'sum'
                }).reset_index()
                day_wise['AUTO'] = day_wise['MOB_MRI'] + day_wise['OCR']
                day_wise = day_wise.sort_values('BILL_DATE')
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=day_wise['BILL_DATE'], y=day_wise['BILLED'],
                    mode='lines+markers', name='Billed',
                    line=dict(color='#34d399', width=3),
                    marker=dict(size=8, color='#34d399')
                ))
                fig.add_trace(go.Scatter(
                    x=day_wise['BILL_DATE'], y=day_wise['AUTO'],
                    mode='lines+markers', name='Auto',
                    line=dict(color='#60a5fa', width=3),
                    marker=dict(size=8, color='#60a5fa')
                ))
                if 'MU_BILLED' in day_wise.columns:
                    fig.add_trace(go.Scatter(
                        x=day_wise['BILL_DATE'], y=day_wise['MU_BILLED'],
                        mode='lines+markers', name='MU_Billed',
                        line=dict(color='#fbbf24', width=3),
                        marker=dict(size=8, color='#fbbf24')
                    ))
                fig.update_layout(
                    title="Day-wise Billing Trend",
                    xaxis_title="Date",
                    yaxis_title="Count",
                    hovermode='x unified',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)')
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")

    if show_top_bill:
        data = filtered_df.nlargest(10, 'billing_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'BILLABLE', 'billed_consumers', 'billing_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billable', 'Billed', 'Billing %']
        show_report("🏆 Top 10 Divisions by Billing %", data, 'Division', 'Billing %', '%')

    if show_worst_bill:
        data = filtered_df.nsmallest(10, 'billing_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'BILLABLE', 'billed_consumers', 'billing_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billable', 'Billed', 'Billing %']
        show_report("📉 Worst 10 Divisions by Billing %", data, 'Division', 'Billing %', '%')

    if show_top_auto:
        data = filtered_df.nlargest(10, 'auto_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'auto_billing', 'auto_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'Auto Billing', 'Auto %']
        show_report("🤖 Top 10 Divisions by Auto %", data, 'Division', 'Auto %', '%')

    if show_worst_auto:
        data = filtered_df.nsmallest(10, 'auto_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'auto_billing', 'auto_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'Auto Billing', 'Auto %']
        show_report("📉 Worst 10 Divisions by Auto %", data, 'Division', 'Auto %', '%')

    if show_top_probe:
        data = filtered_df.nlargest(10, 'probe_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'mob_mri', 'probe_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'Probe', 'Probe %']
        show_report("📱 Top 10 Divisions by Probe %", data, 'Division', 'Probe %', '%')

    if show_worst_probe:
        data = filtered_df.nsmallest(10, 'probe_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'mob_mri', 'probe_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'Probe', 'Probe %']
        show_report("📉 Worst 10 Divisions by Probe %", data, 'Division', 'Probe %', '%')

    if show_top_ocr:
        data = filtered_df.nlargest(10, 'ocr_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'ocr', 'ocr_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'OCR', 'OCR %']
        show_report("📊 Top 10 Divisions by OCR %", data, 'Division', 'OCR %', '%')

    if show_worst_ocr:
        data = filtered_df.nsmallest(10, 'ocr_percentage')[['DIVISION', 'ZONE', 'CIRCLE', 'billed_consumers', 'ocr', 'ocr_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'Billed', 'OCR', 'OCR %']
        show_report("📉 Worst 10 Divisions by OCR %", data, 'Division', 'OCR %', '%')

    if show_top_rdf:
        data = filtered_df.nlargest(10, 'rdf_count')[['DIVISION', 'ZONE', 'CIRCLE', 'rdf_count', 'rdf_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'RDF Count', 'RDF %']
        show_report("🔴 Top 10 Divisions by RDF Count", data, 'Division', 'RDF Count', '')

    if show_worst_rdf:
        data = filtered_df.nsmallest(10, 'rdf_count')[['DIVISION', 'ZONE', 'CIRCLE', 'rdf_count', 'rdf_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'RDF Count', 'RDF %']
        show_report("📉 Worst 10 Divisions by RDF Count", data, 'Division', 'RDF Count', '')

    if show_top_idf:
        data = filtered_df.nlargest(10, 'idf_count')[['DIVISION', 'ZONE', 'CIRCLE', 'idf_count', 'idf_percentage']]
        data.columns = ['Division', 'Zone', 'Circle', 'IDF Count', 'IDF %']
        show_report("🟣 Top 10 Divisions by IDF Count", data, 'Division', 'IDF Count', '')

    st.markdown('<div class="section-title">📋 <span>Complete Division-wise Report</span></div>', unsafe_allow_html=True)
    
    cols_to_show = ['DIV_CODE', 'DIVISION', 'ZONE', 'CIRCLE', 'BILLABLE', 'billed_consumers', 
                    'unbilled_consumers', 'mob_mri', 'ocr', 'auto_billing', 'manual_bill',
                    'total_agents', 'billing_percentage', 'probe_percentage', 'ocr_percentage', 
                    'auto_percentage', 'rdf_count', 'idf_count', 'total_rdf_idf',
                    'rdf_percentage', 'idf_percentage', 'newly_rdf_count', 'newly_idf_count', 
                    'newly_total', 'newly_rdf_percentage', 'newly_idf_percentage']

    display_df = filtered_df[[c for c in cols_to_show if c in filtered_df.columns]].copy()

    rename_dict = {
        'DIV_CODE': 'Div Code', 'DIVISION': 'Division', 'ZONE': 'Zone', 'CIRCLE': 'Circle',
        'BILLABLE': 'Billable', 'billed_consumers': 'Billed', 'unbilled_consumers': 'Unbilled',
        'mob_mri': 'Probe', 'ocr': 'OCR', 'auto_billing': 'Auto Billing', 'manual_bill': 'Manual Bill',
        'total_agents': 'Total Agents', 'billing_percentage': 'Billing %',
        'probe_percentage': 'Probe %', 'ocr_percentage': 'OCR %', 'auto_percentage': 'Auto %',
        'rdf_count': 'RDF Count', 'idf_count': 'IDF Count', 'total_rdf_idf': 'Total RDF/IDF',
        'rdf_percentage': 'RDF %', 'idf_percentage': 'IDF %',
        'newly_rdf_count': 'Newly RDF', 'newly_idf_count': 'Newly IDF', 'newly_total': 'Newly Total',
        'newly_rdf_percentage': 'Newly RDF %', 'newly_idf_percentage': 'Newly IDF %'
    }
    display_df.rename(columns={k: v for k, v in rename_dict.items() if k in display_df.columns}, inplace=True)
    st.dataframe(display_df, use_container_width=True)

    csv = display_df.to_csv(index=False)
    st.download_button("📥 Download Report as CSV", data=csv, file_name="billing_report.csv", mime="text/csv")


# ============================================================
# ========== PAGE: MR ANALYSIS ==========
# ============================================================
def render_mr_analysis():
    st.markdown(
        '<div class="section-title">📊 <span>MR Analysis</span></div>',
        unsafe_allow_html=True
    )

    # ---- MR SEARCH ----
    search_col, _ = st.columns([1, 3])
    with search_col:
        st.markdown("### 🔍 MR Search")
        search_agent = st.text_input(
            "Agent ID",
            placeholder="Enter Agent ID...",
            key="mr_agent_search"
        ).strip()

    # ---- BILLED DATA - AGENT LEVEL GROUPING ----
    df_excel = df_billed.copy()

    numeric_cols = ['BILLED', 'MOB_MRI', 'OCR', 'MANUAL_BILL', 'MU_BILLED']
    for col in numeric_cols:
        if col in df_excel.columns:
            df_excel[col] = pd.to_numeric(df_excel[col], errors='coerce').fillna(0)

    df_excel['AGENT_ID'] = normalize_agent_id(df_excel['AGENT_ID'])
    df_excel = df_excel[df_excel['AGENT_ID'] != ''].copy()

    mr_summary = df_excel.groupby('AGENT_ID', as_index=False).agg({
        'BILLED': 'sum',
        'MOB_MRI': 'sum',
        'OCR': 'sum',
        'ZONE_NAME': 'first',
        'CIRCLE_NAME': 'first',
        'DIV_NAME': 'first'
    })

    mr_summary['AUTO'] = mr_summary['MOB_MRI'] + mr_summary['OCR']

    active_mr = len(mr_summary)
    probe_zero = int((mr_summary['MOB_MRI'] == 0).sum())
    auto_zero = int((mr_summary['AUTO'] == 0).sum())

    # ---- Merge Agent Master ----
    if df_agent_master is not None and len(df_agent_master) > 0:
        mr_summary = mr_summary.merge(
            df_agent_master[['AGENT_ID', 'NAME', 'MOBILE_NO']],
            on='AGENT_ID',
            how='left'
        )
        mr_summary['NAME'] = mr_summary['NAME'].fillna('')
        mr_summary['MOBILE_NO'] = mr_summary['MOBILE_NO'].fillna('')
    else:
        mr_summary['NAME'] = ''
        mr_summary['MOBILE_NO'] = ''

    # ---- RDF/IDF - AGENT LEVEL GROUPING ----
    if df_rdf_idf_mr is not None and len(df_rdf_idf_mr) > 0:
        rdf_idf_mr = df_rdf_idf_mr.copy()
        rdf_idf_mr['AGENT_ID'] = normalize_agent_id(rdf_idf_mr['AGENT_ID'])
        
        rdf_idf_summary = rdf_idf_mr.groupby('AGENT_ID', as_index=False).agg({
            'RDF_COUNT': 'sum',
            'IDF_COUNT': 'sum',
            'NEWLY_RDF_COUNT': 'sum',
            'NEWLY_IDF_COUNT': 'sum',
            'DIV_CODE': 'first',
            'DIVISION': 'first'
        })
        
        if df_agent_master is not None and len(df_agent_master) > 0:
            rdf_idf_summary = rdf_idf_summary.merge(
                df_agent_master[['AGENT_ID', 'NAME', 'MOBILE_NO']],
                on='AGENT_ID',
                how='left'
            )
            rdf_idf_summary['NAME'] = rdf_idf_summary['NAME'].fillna('')
            rdf_idf_summary['MOBILE_NO'] = rdf_idf_summary['MOBILE_NO'].fillna('')
        else:
            rdf_idf_summary['NAME'] = ''
            rdf_idf_summary['MOBILE_NO'] = ''

        mr_full = pd.merge(
            mr_summary,
            rdf_idf_summary,
            on='AGENT_ID',
            how='left',
            suffixes=('', '_rdf')
        )
        
        for col in ['RDF_COUNT', 'IDF_COUNT', 'NEWLY_RDF_COUNT', 'NEWLY_IDF_COUNT']:
            if col in mr_full.columns:
                mr_full[col] = mr_full[col].fillna(0)
            else:
                mr_full[col] = 0
        
        # Ensure NAME and MOBILE_NO are present (from mr_summary)
        if 'NAME' not in mr_full.columns:
            mr_full['NAME'] = ''
        if 'MOBILE_NO' not in mr_full.columns:
            mr_full['MOBILE_NO'] = ''
        # Clean up duplicate NAME/MOBILE_NO from rdf side
        if 'NAME_rdf' in mr_full.columns:
            mr_full['NAME'] = mr_full['NAME'].fillna(mr_full['NAME_rdf'])
            mr_full.drop(columns=['NAME_rdf'], inplace=True)
        if 'MOBILE_NO_rdf' in mr_full.columns:
            mr_full['MOBILE_NO'] = mr_full['MOBILE_NO'].fillna(mr_full['MOBILE_NO_rdf'])
            mr_full.drop(columns=['MOBILE_NO_rdf'], inplace=True)

        # For rdf_merge_df (used in Top 25 RDF/IDF)
        rdf_merge_df = pd.merge(
            rdf_idf_summary,
            mr_summary[['AGENT_ID', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'NAME', 'MOBILE_NO']],
            on='AGENT_ID',
            how='inner'
        )
    else:
        mr_full = mr_summary.copy()
        for col in ['RDF_COUNT', 'IDF_COUNT', 'NEWLY_RDF_COUNT', 'NEWLY_IDF_COUNT']:
            mr_full[col] = 0
        rdf_merge_df = pd.DataFrame(columns=[
            'AGENT_ID', 'RDF_COUNT', 'IDF_COUNT', 'NEWLY_RDF_COUNT', 
            'NEWLY_IDF_COUNT', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO',
            'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'NAME', 'MOBILE_NO'
        ])

    mr_full['TOTAL_RDF'] = mr_full['RDF_COUNT']
    mr_full['TOTAL_RDF_IDF'] = mr_full['RDF_COUNT'] + mr_full['IDF_COUNT']

    # ---- SAME LOCATION ----
    same_location_mr_count = 0
    same_location_mr = pd.DataFrame()

    if df_same_location is not None and len(df_same_location) > 0:
        same_location_mr = df_same_location.groupby(
            ['DIV_CODE', 'AGENT_ID'], as_index=False
        ).agg({'TOTAL_BILLS': 'sum'})
        same_location_mr = same_location_mr[same_location_mr['TOTAL_BILLS'] > 0].copy()
        if df_agent_master is not None and len(df_agent_master) > 0:
            same_location_mr = same_location_mr.merge(
                df_agent_master[['AGENT_ID', 'NAME', 'MOBILE_NO']],
                on='AGENT_ID',
                how='left'
            )
            same_location_mr['NAME'] = same_location_mr['NAME'].fillna('')
            same_location_mr['MOBILE_NO'] = same_location_mr['MOBILE_NO'].fillna('')
        else:
            same_location_mr['NAME'] = ''
            same_location_mr['MOBILE_NO'] = ''
        same_location_mr_count = same_location_mr['AGENT_ID'].nunique()

    # ---- MR SEARCH RESULT ----
    if search_agent:
        search_key = normalize_agent_id(pd.Series([search_agent])).iloc[0]

        billed_match = mr_summary[mr_summary['AGENT_ID'].eq(search_key)].copy()
        
        if df_rdf_idf_mr is not None and len(df_rdf_idf_mr) > 0:
            rdf_raw = df_rdf_idf_mr.copy()
            rdf_raw['AGENT_ID'] = normalize_agent_id(rdf_raw['AGENT_ID'])
            rdf_match = rdf_raw[rdf_raw['AGENT_ID'].eq(search_key)].copy()
        else:
            rdf_match = pd.DataFrame()

        if len(billed_match) == 0 and len(rdf_match) == 0:
            billed_match = mr_summary[mr_summary['AGENT_ID'].str.contains(search_key, case=False, na=False, regex=False)].copy()
            if df_rdf_idf_mr is not None and len(df_rdf_idf_mr) > 0:
                rdf_match = rdf_raw[rdf_raw['AGENT_ID'].str.contains(search_key, case=False, na=False, regex=False)].copy()

        if len(billed_match) > 0 or len(rdf_match) > 0:
            if len(billed_match) > 0:
                billed_result = billed_match[['AGENT_ID', 'NAME', 'MOBILE_NO', 'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'BILLED', 'MOB_MRI', 'OCR']].copy()
            else:
                billed_result = pd.DataFrame(columns=['AGENT_ID', 'NAME', 'MOBILE_NO', 'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'BILLED', 'MOB_MRI', 'OCR'])

            if len(rdf_match) > 0:
                rdf_result = rdf_match.groupby('AGENT_ID', as_index=False).agg(
                    RDF_COUNT=('RDF_COUNT', 'sum'),
                    IDF_COUNT=('IDF_COUNT', 'sum'),
                    NEWLY_RDF_COUNT=('NEWLY_RDF_COUNT', 'sum')
                )
                if df_agent_master is not None and len(df_agent_master) > 0:
                    rdf_result = rdf_result.merge(
                        df_agent_master[['AGENT_ID', 'NAME', 'MOBILE_NO']],
                        on='AGENT_ID',
                        how='left'
                    )
                    rdf_result['NAME'] = rdf_result['NAME'].fillna('')
                    rdf_result['MOBILE_NO'] = rdf_result['MOBILE_NO'].fillna('')
                else:
                    rdf_result['NAME'] = ''
                    rdf_result['MOBILE_NO'] = ''
            else:
                rdf_result = pd.DataFrame(columns=['AGENT_ID', 'RDF_COUNT', 'IDF_COUNT', 'NEWLY_RDF_COUNT', 'NAME', 'MOBILE_NO'])

            search_result = pd.merge(billed_result, rdf_result, on='AGENT_ID', how='outer', suffixes=('', '_rdf'))
            search_result['NAME'] = search_result['NAME'].fillna(search_result['NAME_rdf'])
            search_result['MOBILE_NO'] = search_result['MOBILE_NO'].fillna(search_result['MOBILE_NO_rdf'])
            search_result.drop(columns=[col for col in search_result.columns if col.endswith('_rdf')], inplace=True, errors='ignore')

            for col in ['ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']:
                if col not in search_result.columns:
                    search_result[col] = ''
                search_result[col] = search_result[col].fillna('').astype(str).str.strip()

            for col in ['BILLED', 'MOB_MRI', 'OCR', 'RDF_COUNT', 'IDF_COUNT', 'NEWLY_RDF_COUNT']:
                if col not in search_result.columns:
                    search_result[col] = 0
                search_result[col] = pd.to_numeric(search_result[col], errors='coerce').fillna(0).astype(int)

            search_result = search_result[['AGENT_ID', 'NAME', 'MOBILE_NO', 'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'BILLED', 'MOB_MRI', 'OCR', 'IDF_COUNT', 'RDF_COUNT', 'NEWLY_RDF_COUNT']].copy()
            search_result.columns = ['Agent ID', 'Name', 'Mobile No', 'Zone', 'Circle', 'Division', 'Total Bill', 'Probe Count', 'OCR Count', 'IDF Count', 'RDF Count', 'Newly RDF Count']

            st.subheader("🔎 MR Search Result")
            st.dataframe(search_result, use_container_width=True, hide_index=True)
        else:
            st.warning(f"❌ Agent ID '{search_agent}' not found.")
        st.markdown("---")

    # ---- KPI CARDS ----
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card blue">
            <div class="icon">👥</div>
            <div class="value">{active_mr:,}</div>
            <div class="label">Active Meter Readers</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card red">
            <div class="icon">📱❌</div>
            <div class="value">{probe_zero:,}</div>
            <div class="label">Probe Zero MR</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card orange">
            <div class="icon">🤖❌</div>
            <div class="value">{auto_zero:,}</div>
            <div class="label">Auto Zero MR</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card purple">
            <div class="icon">📍</div>
            <div class="value">{same_location_mr_count:,}</div>
            <div class="label">Same Location MR (10+)</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ======================== NEW SECTION: Average Bills per Day per Agent Distribution ========================
    st.markdown('<div class="section-title">📊 <span>Average Bills per Day per Agent Distribution</span></div>', unsafe_allow_html=True)

    # --- NEW LOGIC: Count total rows per AGENT_ID as working days (ignoring dates) ---
    # Group by AGENT_ID: sum of BILLED and count of rows (occurrences)
    agent_stats = df_excel.groupby('AGENT_ID').agg(
        total_bills=('BILLED', 'sum'),
        days=('BILLED', 'count')   # counting rows per agent = number of working days
    ).reset_index()

    # Keep only active agents (those in mr_summary)
    agent_stats = agent_stats[agent_stats['AGENT_ID'].isin(mr_summary['AGENT_ID'])]

    # Calculate average per day
    agent_stats['avg_per_day'] = agent_stats['total_bills'] / agent_stats['days']

    # 🔥 FIX: Changed labels to English words so Excel doesn't treat them as dates!
    bins = [0, 10, 30, 50, 75, float('inf')]
    labels = ['one to ten', 'eleven to thirty', 'thirty one to fifty', 'fifty one to seventy five', 'seventy five and above']
    agent_stats['category'] = pd.cut(
        agent_stats['avg_per_day'],
        bins=bins,
        labels=labels,
        right=True,
        include_lowest=True
    )

    # Count per category
    category_counts = agent_stats['category'].value_counts().reindex(labels, fill_value=0)
    total_active = len(mr_summary)

    # Display as 5 KPI cards
    cols = st.columns(5)
    card_colors = ['blue', 'green', 'teal', 'purple', 'orange']
    for i, (label, count) in enumerate(category_counts.items()):
        pct = (count / total_active * 100) if total_active > 0 else 0
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card {card_colors[i]}">
                <div class="icon">📊</div>
                <div class="value">{count:,} <span class="pct">({pct:.1f}%)</span></div>
                <div class="label">{label} avg bills/day</div>
            </div>
            """, unsafe_allow_html=True)

    # Download button for the distribution data
    csv_data = agent_stats[['AGENT_ID', 'total_bills', 'days', 'avg_per_day', 'category']]
    if df_agent_master is not None and len(df_agent_master) > 0:
        csv_data = csv_data.merge(df_agent_master[['AGENT_ID', 'NAME', 'MOBILE_NO']], on='AGENT_ID', how='left')
        csv_data['NAME'] = csv_data['NAME'].fillna('')
        csv_data['MOBILE_NO'] = csv_data['MOBILE_NO'].fillna('')
    else:
        csv_data['NAME'] = ''
        csv_data['MOBILE_NO'] = ''
    csv = csv_data.to_csv(index=False)
    st.download_button(
        "📥 Download Agent Average Bills CSV",
        data=csv,
        file_name="agent_avg_bills.csv",
        mime="text/csv"
    )
    # ===========================================================================================================

    # ---- TOP 25 BUTTONS ----
    st.markdown('<div class="section-title">📋 <span>Top 25 MR Lists</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        show_top_bill_mr = st.button("🏆 Top 25 by Total Bills", use_container_width=True)
    with c2:
        show_top_rdf_mr = st.button("🔴 Top 25 by Total RDF", use_container_width=True)
    with c3:
        show_top_idf_mr = st.button("🟣 Top 25 by Total IDF", use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        show_top_newly_rdf_mr = st.button("🆕 Top 25 Newly RDF", use_container_width=True)
    with c2:
        show_probe_zero_top = st.button("📱❌ Top 25 Probe Zero MR", use_container_width=True)
    with c3:
        show_auto_zero_top = st.button("🤖❌ Top 25 Auto Zero MR", use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        show_same_location_top = st.button("📍 Top 25 Same Location MR", use_container_width=True)
    st.markdown("---")

    # ---- TABLE HELPER (with download button) ----
    def display_mr_table(df_table, title, columns, filename):
        if len(df_table) > 0:
            st.subheader(title)
            avail_cols = [col for col in columns if col in df_table.columns]
            st.dataframe(df_table[avail_cols].copy(), use_container_width=True, hide_index=True)
            # Download button
            csv = df_table[avail_cols].to_csv(index=False)
            st.download_button(
                f"📥 Download {title} as CSV",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
        else:
            st.info("ℹ️ No data found for this category.")
        st.markdown("---")

    # ---- 1. TOP 25 TOTAL BILLS ----
    if show_top_bill_mr:
        # Select and rename columns safely
        cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                        'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
        top = mr_full[cols_to_keep].sort_values('BILLED', ascending=False).head(25).copy()
        top.rename(columns={
            'AGENT_ID': 'Agent ID',
            'NAME': 'Name',
            'MOBILE_NO': 'Mobile No',
            'BILLED': 'Total Bills',
            'MOB_MRI': 'Probe',
            'OCR': 'OCR',
            'AUTO': 'Auto',
            'ZONE_NAME': 'Zone',
            'CIRCLE_NAME': 'Circle',
            'DIV_NAME': 'Division'
        }, inplace=True)
        display_mr_table(top, "🏆 Top 25 MR by Total Bills",
                        ['Agent ID', 'Name', 'Mobile No', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                        "top25_total_bills")

    # ---- 2. TOP 25 TOTAL RDF ----
    if show_top_rdf_mr:
        if len(rdf_merge_df) > 0 and rdf_merge_df['RDF_COUNT'].sum() > 0:
            cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'RDF_COUNT', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                            'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
            top = rdf_merge_df[cols_to_keep].sort_values('RDF_COUNT', ascending=False).head(25).copy()
            top.rename(columns={
                'AGENT_ID': 'Agent ID',
                'NAME': 'Name',
                'MOBILE_NO': 'Mobile No',
                'RDF_COUNT': 'RDF Count',
                'BILLED': 'Total Bills',
                'MOB_MRI': 'Probe',
                'OCR': 'OCR',
                'AUTO': 'Auto',
                'ZONE_NAME': 'Zone',
                'CIRCLE_NAME': 'Circle',
                'DIV_NAME': 'Division'
            }, inplace=True)
            display_mr_table(top, "🔴 Top 25 MR by Total RDF",
                            ['Agent ID', 'Name', 'Mobile No', 'RDF Count', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                            "top25_rdf")
        else:
            st.info("ℹ️ No RDF data found for agents.")
            st.markdown("---")

    # ---- 3. TOP 25 TOTAL IDF ----
    if show_top_idf_mr:
        if len(rdf_merge_df) > 0 and rdf_merge_df['IDF_COUNT'].sum() > 0:
            cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'IDF_COUNT', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                            'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
            top = rdf_merge_df[cols_to_keep].sort_values('IDF_COUNT', ascending=False).head(25).copy()
            top.rename(columns={
                'AGENT_ID': 'Agent ID',
                'NAME': 'Name',
                'MOBILE_NO': 'Mobile No',
                'IDF_COUNT': 'IDF Count',
                'BILLED': 'Total Bills',
                'MOB_MRI': 'Probe',
                'OCR': 'OCR',
                'AUTO': 'Auto',
                'ZONE_NAME': 'Zone',
                'CIRCLE_NAME': 'Circle',
                'DIV_NAME': 'Division'
            }, inplace=True)
            display_mr_table(top, "🟣 Top 25 MR by Total IDF",
                            ['Agent ID', 'Name', 'Mobile No', 'IDF Count', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                            "top25_idf")
        else:
            st.info("ℹ️ No IDF data found for agents.")
            st.markdown("---")

    # ---- 4. TOP 25 NEWLY RDF ----
    if show_top_newly_rdf_mr:
        if len(rdf_merge_df) > 0 and rdf_merge_df['NEWLY_RDF_COUNT'].sum() > 0:
            cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'NEWLY_RDF_COUNT', 'RDF_COUNT', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                            'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
            top = rdf_merge_df[cols_to_keep].sort_values('NEWLY_RDF_COUNT', ascending=False).head(25).copy()
            top.rename(columns={
                'AGENT_ID': 'Agent ID',
                'NAME': 'Name',
                'MOBILE_NO': 'Mobile No',
                'NEWLY_RDF_COUNT': 'Newly RDF',
                'RDF_COUNT': 'Total RDF',
                'BILLED': 'Total Bills',
                'MOB_MRI': 'Probe',
                'OCR': 'OCR',
                'AUTO': 'Auto',
                'ZONE_NAME': 'Zone',
                'CIRCLE_NAME': 'Circle',
                'DIV_NAME': 'Division'
            }, inplace=True)
            display_mr_table(top, "🆕 Top 25 MR by Newly RDF",
                            ['Agent ID', 'Name', 'Mobile No', 'Newly RDF', 'Total RDF', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                            "top25_newly_rdf")
        else:
            st.info("ℹ️ No Newly RDF data found for agents.")
            st.markdown("---")

    # ---- 5. TOP 25 PROBE ZERO ----
    if show_probe_zero_top:
        top = mr_full[mr_full['MOB_MRI'] == 0].sort_values('BILLED', ascending=False).head(25).copy()
        cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                        'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
        top = top[cols_to_keep]
        top.rename(columns={
            'AGENT_ID': 'Agent ID',
            'NAME': 'Name',
            'MOBILE_NO': 'Mobile No',
            'BILLED': 'Total Bills',
            'MOB_MRI': 'Probe',
            'OCR': 'OCR',
            'AUTO': 'Auto',
            'ZONE_NAME': 'Zone',
            'CIRCLE_NAME': 'Circle',
            'DIV_NAME': 'Division'
        }, inplace=True)
        display_mr_table(top, "📱❌ Top 25 Probe Zero MR",
                        ['Agent ID', 'Name', 'Mobile No', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                        "top25_probe_zero")

    # ---- 6. TOP 25 AUTO ZERO ----
    if show_auto_zero_top:
        top = mr_full[mr_full['AUTO'] == 0].sort_values('BILLED', ascending=False).head(25).copy()
        cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                        'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
        top = top[cols_to_keep]
        top.rename(columns={
            'AGENT_ID': 'Agent ID',
            'NAME': 'Name',
            'MOBILE_NO': 'Mobile No',
            'BILLED': 'Total Bills',
            'MOB_MRI': 'Probe',
            'OCR': 'OCR',
            'AUTO': 'Auto',
            'ZONE_NAME': 'Zone',
            'CIRCLE_NAME': 'Circle',
            'DIV_NAME': 'Division'
        }, inplace=True)
        display_mr_table(top, "🤖❌ Top 25 Auto Zero MR",
                        ['Agent ID', 'Name', 'Mobile No', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                        "top25_auto_zero")

    # ---- 7. TOP 25 SAME LOCATION ----
    if show_same_location_top:
        if len(same_location_mr) > 0:
            # Merge with mr_summary to get additional details
            agent_details = mr_summary[['AGENT_ID', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME', 'NAME', 'MOBILE_NO']].copy()
            same_loc_top = pd.merge(same_location_mr, agent_details, on='AGENT_ID', how='left')
            same_loc_top = same_loc_top.sort_values('TOTAL_BILLS', ascending=False).head(25)
            cols_to_keep = ['AGENT_ID', 'NAME', 'MOBILE_NO', 'DIV_CODE', 'TOTAL_BILLS', 'BILLED', 'MOB_MRI', 'OCR', 'AUTO', 
                            'ZONE_NAME', 'CIRCLE_NAME', 'DIV_NAME']
            top = same_loc_top[cols_to_keep].copy()
            top.rename(columns={
                'AGENT_ID': 'Agent ID',
                'NAME': 'Name',
                'MOBILE_NO': 'Mobile No',
                'DIV_CODE': 'Div Code',
                'TOTAL_BILLS': 'Same Location Bills',
                'BILLED': 'Total Bills',
                'MOB_MRI': 'Probe',
                'OCR': 'OCR',
                'AUTO': 'Auto',
                'ZONE_NAME': 'Zone',
                'CIRCLE_NAME': 'Circle',
                'DIV_NAME': 'Division'
            }, inplace=True)
            display_mr_table(top, "📍 Top 25 Same Location MR",
                            ['Agent ID', 'Name', 'Mobile No', 'Div Code', 'Same Location Bills', 'Total Bills', 'Probe', 'OCR', 'Auto', 'Zone', 'Circle', 'Division'],
                            "top25_same_location")
        else:
            st.info("ℹ️ No Same Location MR data found in same_location.csv.")
            st.markdown("---")


# ============================================================
# ========== RENDER ==========
# ============================================================
if st.session_state.current_page == 'Home':
    render_home()
else:
    render_mr_analysis()

# ============================================================
# ========== FOOTER ==========
# ============================================================
st.markdown("""
<div class="footer">
    <strong>📊 Billing Dashboard</strong> | © 2026 All Rights Reserved<br>
    Need help? 📧 <a href="mailto:da.puvvnl@fluentgrid.com" class="email">da.puvvnl@fluentgrid.com</a>
</div>
""", unsafe_allow_html=True)