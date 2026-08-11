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

# ========== Custom CSS - Premium Dark Theme ==========
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

# ========== File Paths ==========
BASE_PATH = r"C:\Users\DELL\Desktop\Dashboard"

BILLED_FILE_XLSX = os.path.join(BASE_PATH, "billed_data.xlsx")
BILLED_FILE_CSV = os.path.join(BASE_PATH, "billed_data.csv")
BILLABLE_FILE_XLSX = os.path.join(BASE_PATH, "billable_data.xlsx")
BILLABLE_FILE_CSV = os.path.join(BASE_PATH, "billable_data.csv")

# ========== CSV Data Paths ==========
BASE_PATH = r"C:\Users\DELL\Desktop\Dashboard"

BILLED_FILE_XLSX = os.path.join(BASE_PATH, "billed_data.xlsx")
BILLED_FILE_CSV = os.path.join(BASE_PATH, "billed_data.csv")
BILLABLE_FILE_XLSX = os.path.join(BASE_PATH, "billable_data.xlsx")
BILLABLE_FILE_CSV = os.path.join(BASE_PATH, "billable_data.csv")

RDF_IDF_FILE_XLSX = os.path.join(BASE_PATH, "rdf_idf.xlsx")
RDF_IDF_FILE_CSV = os.path.join(BASE_PATH, "rdf_idf.csv")

SAME_LOCATION_FILE_XLSX = os.path.join(BASE_PATH, "same_location.xlsx")
SAME_LOCATION_FILE_CSV = os.path.join(BASE_PATH, "same_location.csv")


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


# ========== Load RDF / IDF from CSV ==========
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

    # Clean text columns
    for col in [
        'acct_id', 'agent_id', 'div_code', 'division',
        'curr_meter_read_remark', 'prev_meter_read_remark',
        'prev_bill_basis'
    ]:
        df[col] = df[col].fillna('').astype(str).str.strip()

    # Current month RDF / IDF
    df['curr_meter_read_remark'] = df['curr_meter_read_remark'].str.upper()
    df['prev_bill_basis'] = df['prev_bill_basis'].str.upper()

    # Only RDF / IDF records are relevant
    rdf_idf = df[
        df['curr_meter_read_remark'].isin(['RDF', 'IDF'])
    ].copy()

    if len(rdf_idf) == 0:
        return pd.DataFrame(columns=empty_cols)

    # MU in prev_bill_basis = Newly
    rdf_idf['is_rdf'] = (
        rdf_idf['curr_meter_read_remark'] == 'RDF'
    ).astype(int)

    rdf_idf['is_idf'] = (
        rdf_idf['curr_meter_read_remark'] == 'IDF'
    ).astype(int)

    rdf_idf['is_newly'] = (
        rdf_idf['prev_bill_basis'] == 'MU'
    ).astype(int)

    rdf_idf['newly_rdf'] = (
        (rdf_idf['is_rdf'] == 1) &
        (rdf_idf['is_newly'] == 1)
    ).astype(int)

    rdf_idf['newly_idf'] = (
        (rdf_idf['is_idf'] == 1) &
        (rdf_idf['is_newly'] == 1)
    ).astype(int)

    # Division-wise aggregation
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

    result['newly_total'] = (
        result['newly_rdf_count'] +
        result['newly_idf_count']
    )

    result.columns = [
        'DIV_CODE', 'DIVISION',
        'total_rdf_idf', 'rdf_count', 'idf_count',
        'newly_rdf_count', 'newly_idf_count', 'newly_total'
    ]

    return result


# ========== Load Same Location from CSV ==========
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

    required = [
        'DIV_CODE', 'AGENT_ID',
        'LATITUDE', 'LONGITUDE', 'TOTAL_BILLS'
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ''

    df['DIV_CODE'] = df['DIV_CODE'].fillna('').astype(str).str.strip()
    df['AGENT_ID'] = df['AGENT_ID'].fillna('').astype(str).str.strip()

    df['LATITUDE'] = pd.to_numeric(
        df['LATITUDE'], errors='coerce'
    )

    df['LONGITUDE'] = pd.to_numeric(
        df['LONGITUDE'], errors='coerce'
    )

    df['TOTAL_BILLS'] = pd.to_numeric(
        df['TOTAL_BILLS'], errors='coerce'
    ).fillna(0)

    # CSV already contains only 10+ same-location records.
    # No additional location filtering is required here.

    return df[
        (df['AGENT_ID'] != '') &
        (df['DIV_CODE'] != '')
    ].copy()


# ========== Merge Function ==========
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


# ========== Load All Data ==========
with st.spinner("📂 Loading data..."):
    df_billed = load_billed_file()
    df_billable = load_billable_file()
    df_rdf_idf = load_rdf_idf_file()
    df_same_location = load_same_location_file()

if df_billed is None or df_billable is None:
    st.error(
        "❌ Files not found! Please place billed_data and billable_data "
        "files in: `C:/Users/DELL/Desktop/Dashboard`"
    )
    st.stop()

with st.spinner("🔄 Merging data..."):
    df = merge_data(df_billed, df_billable, df_rdf_idf)

if df is None or len(df) == 0:
    st.warning("⚠️ No data found after merging.")
    st.stop()

# ========== Load Excel Files ==========
@st.cache_data(ttl=3600)
def load_billed_file():
    if os.path.exists(BILLED_FILE_XLSX):
        df = pd.read_excel(BILLED_FILE_XLSX)
        df.columns = df.columns.str.upper().str.strip()
        return df
    elif os.path.exists(BILLED_FILE_CSV):
        df = pd.read_csv(BILLED_FILE_CSV)
        df.columns = df.columns.str.upper().str.strip()
        return df
    return None

@st.cache_data(ttl=3600)
def load_billable_file():
    if os.path.exists(BILLABLE_FILE_XLSX):
        df = pd.read_excel(BILLABLE_FILE_XLSX)
        df.columns = df.columns.str.upper().str.strip()
        return df
    elif os.path.exists(BILLABLE_FILE_CSV):
        df = pd.read_csv(BILLABLE_FILE_CSV)
        df.columns = df.columns.str.upper().str.strip()
        return df
    return None

# ========== Merge Function ==========
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
        
        df_billed_grouped.columns = ['DIVISION', 'total_agents', 'billed_consumers', 'mob_mri', 'ocr', 'manual_bill', 'mu_billed']
        
        df_merged = pd.merge(
            df_billable,
            df_billed_grouped,
            on='DIVISION',
            how='left'
        ).fillna(0)
        
        if df_rdf_idf is not None and len(df_rdf_idf) > 0:
            df_rdf_idf.rename(columns={'div_name': 'DIVISION'}, inplace=True)
            df_merged = pd.merge(
                df_merged,
                df_rdf_idf,
                on='DIVISION',
                how='left'
            ).fillna(0)
        else:
            for col in ['total_rdf_idf', 'rdf_count', 'idf_count', 
                       'newly_rdf_count', 'newly_idf_count', 'newly_total']:
                df_merged[col] = 0
        
        df_merged['billing_percentage'] = ((df_merged['billed_consumers'] / df_merged['BILLABLE']) * 100).round(2)
        df_merged['unbilled_consumers'] = df_merged['BILLABLE'] - df_merged['billed_consumers']
        df_merged['auto_billing'] = df_merged['mob_mri'] + df_merged['ocr']
        df_merged['auto_percentage'] = ((df_merged['auto_billing'] / df_merged['billed_consumers']) * 100).round(2).fillna(0)
        df_merged['probe_percentage'] = ((df_merged['mob_mri'] / df_merged['billed_consumers']) * 100).round(2).fillna(0)
        df_merged['ocr_percentage'] = ((df_merged['ocr'] / df_merged['billed_consumers']) * 100).round(2).fillna(0)
        df_merged['rdf_percentage'] = ((df_merged['rdf_count'] / df_merged['BILLABLE']) * 100).round(2).fillna(0)
        df_merged['idf_percentage'] = ((df_merged['idf_count'] / df_merged['BILLABLE']) * 100).round(2).fillna(0)
        df_merged['newly_rdf_percentage'] = ((df_merged['newly_rdf_count'] / df_merged['BILLABLE']) * 100).round(2).fillna(0)
        df_merged['newly_idf_percentage'] = ((df_merged['newly_idf_count'] / df_merged['BILLABLE']) * 100).round(2).fillna(0)
        
        return df_merged
    return None

# ============================================================
# ========== HEADER ==========
# ============================================================

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

# ============================================================
# ========== NAVIGATION ==========
# ============================================================

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
# ========== PAGE: HOME (UNTOUCHED) ==========
# ============================================================

def render_home():
    # ---- FILTERS ----
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

    # ---- KPIs ----
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

    # ---- Row 1 ----
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

    # ---- Row 2 ----
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

    # ---- Row 3: RDF/IDF ----
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

    # ---- Row 4: Newly ----
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

    # ---- RING CHARTS ----
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

    # ============================================================
    # ========== KEYS (BUTTONS) ==========
    # ============================================================
    
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

    # ---- DISPLAY REPORTS ----
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

    # ---- Day-wise Line Chart ----
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

    # ---- All Reports ----
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

    # ---- DATA TABLE ----
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
    st.markdown('<div class="section-title">📊 <span>MR Analysis</span></div>', unsafe_allow_html=True)
    
    # ---- Excel se data (mob_mri, ocr, etc.) ----
    df_excel = df_billed.copy()
    
    # Ensure numeric columns
    numeric_cols = ['BILLED', 'MOB_MRI', 'OCR', 'MANUAL_BILL', 'MU_BILLED']
    for col in numeric_cols:
        if col in df_excel.columns:
            df_excel[col] = pd.to_numeric(df_excel[col], errors='coerce').fillna(0)
    
    # ---- 1. Active Meter Readers ----
    active_mr = df_excel['AGENT_ID'].nunique()
    
    # ---- 2. Probe Zero MR (MOB_MRI = 0) ----
    probe_zero = df_excel[df_excel['MOB_MRI'] == 0]['AGENT_ID'].nunique()
    
    # ---- 3. Auto Zero MR (MOB_MRI + OCR = 0) ----
    df_excel['AUTO'] = df_excel['MOB_MRI'] + df_excel['OCR']
    auto_zero = df_excel[df_excel['AUTO'] == 0]['AGENT_ID'].nunique()
    
    # ---- 4. Same Location MR (CSV se) ----
    same_location_mr_count = 0
    same_location_mr = pd.DataFrame()

    # same_location.csv me 10+ same-location records already filtered hain.
    # Agent + Division wise grouping ki ja rahi hai.
    if df_same_location is not None and len(df_same_location) > 0:
        same_location_mr = df_same_location.groupby(
            ['DIV_CODE', 'AGENT_ID'],
            as_index=False
        ).agg({
            'TOTAL_BILLS': 'sum'
        })

        same_location_mr = same_location_mr[
            same_location_mr['TOTAL_BILLS'] > 0
        ].copy()

        same_location_mr_count = same_location_mr['AGENT_ID'].nunique()

    # ---- KPI Cards ----
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
    
    # ============================================================
    # ========== MR AVERAGE DAILY BILLING ==========
    # ============================================================
    # Agent ID jitni baar billed data me repeat hota hai = working days.
    # Average Daily Bill = Total Bills / Working Days.
    mr_daily_avg = df_excel.groupby('AGENT_ID').agg(
        TOTAL_BILLS=('BILLED', 'sum'),
        WORKING_DAYS=('AGENT_ID', 'size'),
        ZONE=('ZONE_NAME', 'first'),
        CIRCLE=('CIRCLE_NAME', 'first'),
        DIVISION=('DIV_NAME', 'first')
    ).reset_index()

    mr_daily_avg['AVG_DAILY_BILL'] = (
        mr_daily_avg['TOTAL_BILLS'] /
        mr_daily_avg['WORKING_DAYS'].replace(0, pd.NA)
    ).fillna(0).round(2)

    avg_categories = [
        ('1 to 10 Bills', 0, 10),
        ('11 to 30 Bills', 10, 30),
        ('31 to 50 Bills', 30, 50),
        ('51 to 75 Bills', 50, 75),
        ('75 and Above Bills', 75, float('inf'))
    ]

    def get_avg_category_data(category_name, low, high):
        if high == float('inf'):
            mask = mr_daily_avg['AVG_DAILY_BILL'] > low
        else:
            mask = (
                (mr_daily_avg['AVG_DAILY_BILL'] > low) &
                (mr_daily_avg['AVG_DAILY_BILL'] <= high)
            )
        result = mr_daily_avg[mask].copy()
        return result.sort_values('AVG_DAILY_BILL', ascending=False)

    st.markdown(
        '<div class="section-title">📅 <span>MR Average Daily Billing</span></div>',
        unsafe_allow_html=True
    )

    avg_cols = st.columns(5)
    for idx, ((category_name, low, high), col) in enumerate(zip(avg_categories, avg_cols)):
        category_df = get_avg_category_data(category_name, low, high)
        count = len(category_df)
        pct = (count / active_mr * 100) if active_mr else 0

        with col:
            if st.button(
                f"📊 {category_name}\n{count:,} MR ({pct:.1f}%)",
                key=f"mr_avg_category_{idx}",
                use_container_width=True
            ):
                st.session_state['selected_mr_avg_category'] = category_name

    selected_category = st.session_state.get('selected_mr_avg_category')
    if selected_category:
        selected_range = next(
            item for item in avg_categories if item[0] == selected_category
        )
        selected_df = get_avg_category_data(
            selected_range[0], selected_range[1], selected_range[2]
        )

        export_df = selected_df[[
            'AGENT_ID', 'ZONE', 'CIRCLE', 'DIVISION',
            'TOTAL_BILLS', 'WORKING_DAYS', 'AVG_DAILY_BILL'
        ]].copy()
        export_df.columns = [
            'Agent ID', 'Zone', 'Circle', 'Division',
            'Total Bills', 'Working Days', 'Average Daily Bills'
        ]

        st.markdown(
            f"### 📋 {selected_category} — {len(export_df):,} MR "
            f"({(len(export_df) / active_mr * 100) if active_mr else 0:.1f}% of Active MR)"
        )
        st.dataframe(export_df, use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Selected Category CSV",
            data=export_df.to_csv(index=False).encode('utf-8'),
            file_name=selected_category.lower().replace(' ', '_').replace('-', '_') + '_mr.csv',
            mime='text/csv',
            use_container_width=True,
            key='download_selected_mr_avg_category'
        )

    st.caption(
        "Average Daily Bill = Total Bills ÷ Agent ID repeat count "
        "(repeat count ko working days maana gaya hai)."
    )

    st.markdown("---")
    
    # ============================================================
    # ========== TOP 25 LISTS (WITH BUTTONS) ==========
    # ============================================================
    
    st.markdown('<div class="section-title">📋 <span>Top 25 MR Lists</span></div>', unsafe_allow_html=True)
    
    # ---- Buttons ----
    c1, c2, c3 = st.columns(3)
    
    with c1:
        show_top_bill_mr = st.button("🏆 Top 25 by Total Bills", use_container_width=True)
    with c2:
        show_probe_zero_top = st.button("📱❌ Top 25 Probe Zero MR", use_container_width=True)
    with c3:
        show_auto_zero_top = st.button("🤖❌ Top 25 Auto Zero MR", use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        show_same_location_top = st.button("📍 Top 25 Same Location MR", use_container_width=True)
    
    st.markdown("---")
    
    # ---- Helper function ----
    def display_mr_table(df_table, title, columns):
        if len(df_table) > 0:
            st.subheader(title)
            avail_cols = [col for col in columns if col in df_table.columns]
            display_df = df_table[avail_cols].copy()
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("ℹ️ No data found for this category.")
        st.markdown("---")
    
    # ---- 1. Top 25 by Total Bills (Excel se) ----
    if show_top_bill_mr:
        top_bill_mr = df_excel.groupby('AGENT_ID').agg({
            'BILLED': 'sum',
            'ZONE_NAME': 'first',
            'CIRCLE_NAME': 'first',
            'DIV_NAME': 'first'
        }).reset_index()
        top_bill_mr = top_bill_mr.sort_values('BILLED', ascending=False).head(25)
        top_bill_mr.columns = ['Agent ID', 'Total Bills', 'Zone', 'Circle', 'Division']
        display_mr_table(top_bill_mr, "🏆 Top 25 MR by Total Bills", 
                        ['Agent ID', 'Total Bills', 'Zone', 'Circle', 'Division'])
    
    # ---- 2. Top 25 Probe Zero MR (Excel se) ----
    if show_probe_zero_top:
        probe_zero_df = df_excel[df_excel['MOB_MRI'] == 0]
        probe_zero_top = probe_zero_df.groupby('AGENT_ID').agg({
            'BILLED': 'sum',
            'ZONE_NAME': 'first',
            'CIRCLE_NAME': 'first',
            'DIV_NAME': 'first'
        }).reset_index()
        probe_zero_top = probe_zero_top.sort_values('BILLED', ascending=False).head(25)
        probe_zero_top.columns = ['Agent ID', 'Total Bills (Probe=0)', 'Zone', 'Circle', 'Division']
        display_mr_table(probe_zero_top, "📱❌ Top 25 Probe Zero MR", 
                        ['Agent ID', 'Total Bills (Probe=0)', 'Zone', 'Circle', 'Division'])
    
    # ---- 3. Top 25 Auto Zero MR (Excel se) ----
    if show_auto_zero_top:
        auto_zero_df = df_excel[df_excel['AUTO'] == 0]
        auto_zero_top = auto_zero_df.groupby('AGENT_ID').agg({
            'BILLED': 'sum',
            'ZONE_NAME': 'first',
            'CIRCLE_NAME': 'first',
            'DIV_NAME': 'first'
        }).reset_index()
        auto_zero_top = auto_zero_top.sort_values('BILLED', ascending=False).head(25)
        auto_zero_top.columns = ['Agent ID', 'Total Bills (Auto=0)', 'Zone', 'Circle', 'Division']
        display_mr_table(auto_zero_top, "🤖❌ Top 25 Auto Zero MR", 
                        ['Agent ID', 'Total Bills (Auto=0)', 'Zone', 'Circle', 'Division'])
    
    # ---- 4. Top 25 Same Location MR (CSV se) ----
    if show_same_location_top:
        if len(same_location_mr) > 0:
            # Agent + Division already grouped from same_location.csv.
            same_loc_top = same_location_mr.copy()

            # Get MR details from billed_data using Agent ID.
            # Division code is retained from same_location.csv.
            agent_details = df_excel.groupby('AGENT_ID').agg({
                'BILLED': 'sum',
                'ZONE_NAME': 'first',
                'CIRCLE_NAME': 'first',
                'DIV_NAME': 'first'
            }).reset_index()

            same_loc_top = pd.merge(
                same_loc_top,
                agent_details,
                on='AGENT_ID',
                how='left'
            )

            # If multiple divisions exist for one agent, keep the
            # division from same_location.csv as the authoritative code.
            same_loc_top = same_loc_top.sort_values(
                'TOTAL_BILLS',
                ascending=False
            ).head(25)

            same_loc_top.columns = [
                'Div Code',
                'Agent ID',
                'Same Location Bills',
                'Total Bills',
                'Zone',
                'Circle',
                'Division'
            ]

            display_mr_table(
                same_loc_top,
                "📍 Top 25 Same Location MR",
                [
                    'Div Code',
                    'Agent ID',
                    'Same Location Bills',
                    'Total Bills',
                    'Zone',
                    'Circle',
                    'Division'
                ]
            )
        else:
            st.info(
                "ℹ️ No Same Location MR data found in same_location.csv."
            )
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