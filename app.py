import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
import datetime
from collections import Counter

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight ERP",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="auto",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --navy:     #050e0a;
    --navy2:    #071410;
    --card:     #0c1f17;
    --card2:    #112b1e;
    --border:   #1a3d2b;
    --accent:   #22c55e;
    --accent2:  #4ade80;
    --green:    #10b981;
    --red:      #ef4444;
    --yellow:   #f59e0b;
    --purple:   #34d399;
    --text:     #e2e8f0;
    --text2:    #86efac;
    --text3:    #4ade80;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--navy) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--navy2) !important;
    border-right: 1px solid var(--border) !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    color: #22c55e !important;
    background: #0c1f17 !important;
    border: 1px solid #1a3d2b !important;
    border-radius: 0 8px 8px 0 !important;
    z-index: 1000 !important;
}

[data-testid="collapsedControl"] svg { fill: #22c55e !important; }

.main .block-container { padding: 1.5rem 2rem !important; max-width: 1600px !important; }

h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: var(--text) !important; }

.metric-card {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #22c55e, #10b981);
}
.metric-card:hover { border-color: var(--accent); }

.metric-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #86efac;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: clamp(0.85rem, 1.6vw, 1.6rem);
    font-weight: 700;
    color: var(--text);
    line-height: 1.15;
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}
.metric-sub {
    font-size: 0.72rem;
    color: var(--text3);
    margin-top: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}
.metric-icon {
    position: absolute;
    top: 1rem; right: 1rem;
    font-size: 1.4rem;
    opacity: 0.35;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.8rem 0 1rem;
    padding: 0.5rem 0.8rem;
    border-bottom: 1px solid #1a3d2b;
    border-left: 3px solid #22c55e;
    background: linear-gradient(90deg, #0c1f1780, transparent);
    border-radius: 0 6px 6px 0;
}
.section-header h2 {
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4ade80;
    margin: 0;
}

.badge-high   { background:#ef444422; color:#ef4444; border:1px solid #ef444444; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:600; }
.badge-medium { background:#f59e0b22; color:#f59e0b; border:1px solid #f59e0b44; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:600; }
.badge-low    { background:#10b98122; color:#10b981; border:1px solid #10b98144; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:600; }

.insight-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}
.insight-title { font-size: 0.85rem; font-weight: 600; color: var(--text); margin-bottom: 0.25rem; }
.insight-body  { font-size: 0.8rem; color: var(--text2); line-height: 1.5; }
.insight-card.warn   { border-left-color: var(--yellow); }
.insight-card.danger { border-left-color: var(--red); }
.insight-card.good   { border-left-color: var(--green); }

.alert {
    background: #ef444415;
    border: 1px solid #ef444433;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #fca5a5;
    font-size: 0.82rem;
    margin-bottom: 0.5rem;
}
.alert-warn {
    background: #f59e0b15;
    border: 1px solid #f59e0b33;
    color: #fcd34d;
}

.query-result {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
}

.stPlotlyChart { border-radius: 10px; overflow: hidden; }

[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.8rem !important;
}

.styled-table { width:100%; border-collapse:collapse; font-size:0.8rem; }
.styled-table th {
    background: var(--card2);
    color: var(--text2);
    font-size:0.7rem;
    font-weight:600;
    letter-spacing:0.06em;
    text-transform:uppercase;
    padding:0.6rem 0.8rem;
    border-bottom:1px solid var(--border);
    text-align:left;
}
.styled-table td {
    padding:0.5rem 0.8rem;
    border-bottom:1px solid #1a2234;
    color:var(--text);
    vertical-align:middle;
}
.styled-table tr:hover td { background: var(--card2); }

.sidebar-section {
    font-size:0.65rem;
    font-weight:700;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color:var(--text3);
    margin:1.2rem 0 0.5rem;
}

.upload-hero {
    background: linear-gradient(135deg, #071410 0%, #0c1f17 100%);
    border: 1px dashed #1a3d2b;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 2rem 0;
}
.upload-hero h2 { font-size: 1.5rem; color: var(--text); margin-bottom: 0.5rem; }
.upload-hero p  { color: #94a3b8; font-size: 0.9rem; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Hide Streamlit chrome ── */
[data-testid="stToolbar"]    { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }

/* ── Tablet (769px – 1024px) ── */
@media (max-width: 1024px) and (min-width: 769px) {
    .main .block-container { padding: 1rem 1.2rem !important; }
    .metric-card  { height: 145px !important; }
    .metric-value { font-size: clamp(0.9rem, 1.8vw, 1.4rem) !important; }
}

/* ── Mobile (≤ 768px) — single block, no conflicts ── */
@media (max-width: 768px) {
    .main .block-container { padding: 0.75rem 0.75rem !important; }

    .metric-card  { height: auto !important; min-height: 110px !important; }
    .metric-value { font-size: clamp(1rem, 4.5vw, 1.4rem) !important; white-space: nowrap !important; overflow: hidden !important; text-overflow: ellipsis !important; }
    .metric-label { font-size: 0.65rem !important; }
    .metric-sub   { font-size: 0.65rem !important; white-space: normal !important; line-height: 1.3 !important; }
    .metric-icon  { font-size: 1rem !important; top: 0.6rem !important; right: 0.6rem !important; }

    .section-header    { margin: 1rem 0 0.6rem !important; padding: 0.4rem 0.6rem !important; }
    .section-header h2 { font-size: 0.75rem !important; }

    .insight-card  { padding: 0.75rem 0.9rem !important; }
    .insight-title { font-size: 0.8rem !important; }
    .insight-body  { font-size: 0.74rem !important; }

    .badge-high, .badge-medium, .badge-low { font-size: 0.65rem !important; padding: 1px 5px !important; }
    .styled-table th, .styled-table td     { padding: 0.4rem 0.5rem !important; font-size: 0.72rem !important; }
    .alert, .alert-warn  { font-size: 0.75rem !important; padding: 0.6rem 0.8rem !important; }
    .query-result        { padding: 0.75rem 0.9rem !important; }

    .upload-hero    { padding: 2rem 1rem !important; }
    .upload-hero h2 { font-size: 1.1rem !important; }
    .upload-hero p  { font-size: 0.8rem !important; }

    [data-testid="stSidebar"] {
        min-width: 78vw !important;
        max-width: 82vw !important;
        position: fixed !important;
        z-index: 999 !important;
        top: 0 !important;
        left: 0 !important;
        height: 100vh !important;
        overflow-y: auto !important;
        transform: none !important;
    }
    [data-testid="collapsedControl"] {
        position: fixed !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 1000 !important;
        padding: 0.5rem !important;
    }

    .stPlotlyChart { width: 100% !important; overflow-x: auto !important; }
    [data-testid="stDataFrame"] { overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }
    .stDownloadButton button { width: 100% !important; font-size: 0.8rem !important; }
    .stButton button   { font-size: 0.75rem !important; padding: 0.3rem 0.5rem !important; }
    .stTextInput input { font-size: 0.85rem !important; }
    ::-webkit-scrollbar { width: 3px; height: 3px; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", zerolinecolor="#1e2d45"),
    yaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", zerolinecolor="#1e2d45"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    title_font=dict(color="#e2e8f0", size=13, family="Inter"),
    colorway=["#22c55e","#10b981","#4ade80","#34d399","#ef4444","#f59e0b","#a3e635","#6ee7b7"],
)

# ─────────────────────────────────────────────
#  COLUMN DETECTION
# ─────────────────────────────────────────────
COL_KEYWORDS = {
    "amount":     ["amount","amt","total","cost","price","spend","expense","value","sum","payment","charge","fee","gross","net","amount_inr","amount_raw"],
    "vendor":     ["vendor","supplier","merchant","payee","company","provider","seller","vender","canonical_vendor","vendor_raw"],
    "department": ["department","dept","division","unit","team","group","business unit","bu","cost center"],
    "employee":   ["employee","emp","staff","person","name","submitted by","requestor","claimant","user","requester","submitted_by"],
    "category":   ["category","cat","type","expense type","class","classification","nature","purpose","expense category"],
    "invoice_id": ["invoice","inv","invoice id","invoice no","invoice num","receipt no","transaction id","txn","ref","reference","id","number","txn_id"],
    "date":       ["date","dt","transaction date","expense date","invoice date","period","posting","created","submitted","entry_date","txn_date","submission_date"],
    "receipt":    ["receipt","receipt status","attached","attachment","document","proof","support","receipt_attached"],
    "currency":   ["currency","curr","ccy","fx","foreign","usd","eur","gbp"],
    "status":     ["status","state","approval","approved","approval status","workflow","stage","approval_status"],
    "description":["description","desc","notes","memo","comment","narrative","details","particulars","remarks"],
}

def detect_columns(df):
    mapping = {}
    cols_lower = {c: c.lower().strip() for c in df.columns}
    for role, keywords in COL_KEYWORDS.items():
        for col, col_l in cols_lower.items():
            if any(kw in col_l for kw in keywords):
                if role not in mapping:
                    mapping[role] = col
    return mapping

# ─────────────────────────────────────────────
#  DATA CLEANING
# ─────────────────────────────────────────────
def clean_amount(series):
    s = series.astype(str).str.strip()
    s = s.str.replace(r"\b(USD|EUR|GBP|INR|AUD|CAD|JPY|CHF|CNY|SGD|AED)\b", "", regex=True, flags=re.IGNORECASE)
    s = s.str.replace(r"[£€$¥₹₩₪₫฿]", "", regex=True)
    s = s.str.replace(r"^\(([0-9,. ]+)\)$", r"-\1", regex=True)

    def _fix_number(val):
        v = str(val).strip()
        if not v or v in ("-", ".", "--", "N/A", "NA", "#VALUE!", "#REF!", "nan", "None", ""):
            return np.nan
        if re.search(r",\d{1,2}$", v):
            v = v.replace(".", "").replace(",", ".")
        else:
            v = v.replace(",", "")
        try:
            result = float(v)
            if abs(result) > 10_000_000:
                return np.nan
            return result
        except ValueError:
            return np.nan

    return s.apply(_fix_number)


def normalize_invoice_id(series):
    """Normalize invoice IDs for fuzzy duplicate detection."""
    _NULL_TOKENS = {"NAN", "NONE", "NULL", "NA", "N/A", "NIL", "-", "--",
                    "MISSING", "UNKNOWN", "TBD", "TBA", "0", ""}
    s = series.astype(str).str.strip().str.upper()
    s = s.str.replace(r"[^A-Z0-9]", "", regex=True)
    s = s.str.replace(r"^0+", "", regex=True)
    s = s.where(~s.isin(_NULL_TOKENS), other=np.nan)
    return s

def clean_dates(series):
    formats = [
        "%Y-%m-%d","%d/%m/%Y","%m/%d/%Y","%d-%m-%Y","%m-%d-%Y",
        "%d %b %Y","%d %B %Y","%b %d %Y","%B %d %Y",
        "%Y/%m/%d","%d.%m.%Y","%m.%d.%Y","%Y%m%d",
    ]
    for fmt in formats:
        try:
            parsed = pd.to_datetime(series, format=fmt, errors="coerce")
            if parsed.notna().sum() > len(series) * 0.5:
                return parsed
        except Exception:
            pass
    return pd.to_datetime(series, infer_datetime_format=True, errors="coerce")

def normalize_vendor(series):
    s = series.astype(str).str.strip().str.upper()
    s = s.str.replace(r"\s+", " ", regex=True)
    s = s.str.replace(r"[.,;:!?]$", "", regex=True)
    s = s.str.replace(r"\bLTD\.?\b|\bLIMITED\b|\bINC\.?\b|\bLLC\.?\b|\bCORP\.?\b", "", regex=True)
    s = s.str.strip()
    return s

@st.cache_data(show_spinner=False)
def load_and_clean(file_bytes, file_name):
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes), low_memory=False)
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))
    except Exception as e:
        return None, str(e), {}

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    col_map = detect_columns(df)

    if "amount" in col_map:
        ac = col_map["amount"]
        df[ac] = clean_amount(df[ac])

    if "date" in col_map:
        dc = col_map["date"]
        df[dc] = clean_dates(df[dc])

    if "vendor" in col_map:
        vc = col_map["vendor"]
        df[vc] = normalize_vendor(df[vc])

    desc_col = col_map.get("description")
    if "category" not in col_map and desc_col and desc_col in df.columns:
        def infer_category(text):
            if not isinstance(text, str):
                return "Uncategorized"
            t = text.lower()
            if any(k in t for k in ["flight","airline","hotel","lodging","airbnb","travel","taxi","uber","lyft","train","rail","airport"]):
                return "Travel"
            if any(k in t for k in ["software","license","subscription","saas","cloud","aws","azure","google cloud"]):
                return "Software"
            if any(k in t for k in ["restaurant","food","meal","lunch","dinner","breakfast","catering","coffee","cafe","snack"]):
                return "Meals"
            if any(k in t for k in ["transport","cab","car hire","rental","fuel","petrol","parking","toll"]):
                return "Transport"
            if any(k in t for k in ["office","supplies","stationery","printing","equipment","furniture"]):
                return "Office Supplies"
            if any(k in t for k in ["marketing","advertising","ad spend","campaign","event","conference","seminar"]):
                return "Marketing"
            if any(k in t for k in ["training","course","workshop","education","certification"]):
                return "Training"
            if any(k in t for k in ["consulting","professional","legal","audit","advisory"]):
                return "Professional Services"
            if any(k in t for k in ["medical","health","insurance","pharmacy"]):
                return "Health & Insurance"
            return "Other"
        df["_inferred_category"] = df[desc_col].apply(infer_category)
        col_map["category"] = "_inferred_category"

    if "amount" in col_map:
        ac = col_map["amount"]
        df["_is_refund"] = df[ac] < 0

    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({"nan": np.nan, "NaN": np.nan, "None": np.nan, "": np.nan})

    if "invoice_id" in col_map:
        ic = col_map["invoice_id"]
        df["_inv_key"] = normalize_invoice_id(df[ic])

    return df, None, col_map


# ─────────────────────────────────────────────
#  TRANSACTION-LEVEL DUPLICATE DETECTION
#  (mirrors Phase1.ipynb detect_duplicates logic)
#  Runs independently of invoice_id column presence
# ─────────────────────────────────────────────
def detect_transaction_duplicates(df, col_map):
    """
    Three-pass duplicate detection aligned with Phase1.ipynb:

    Pass A — Exact transaction duplicates:
        Same canonical vendor + rounded amount + date
        (same-day, same-vendor, same-amount = confirmed double-submit)

    Pass B — Near-duplicates:
        Same vendor + rounded amount, dates ≤7 days apart
        (likely re-submitted expense, requires review)

    Pass C — Invoice ID duplicates (when column available):
        Normalized invoice ID matching across formatting variants
        INV-001 = INV001 = inv 001

    Returns df with columns:
        _flag_duplicate_txn       bool  — exact txn match
        _flag_near_duplicate      bool  — near-dup (≤7d)
        _flag_duplicate_invoice   bool  — invoice ID dup
        _dup_of                   str   — reference txn for exact dups
        _dup_delta_days           int   — days apart for near-dups
    """
    n = len(df)
    df = df.copy()
    df["_flag_duplicate_txn"]     = False
    df["_flag_near_duplicate"]    = False
    df["_flag_duplicate_invoice"] = False
    df["_dup_of"]                 = ""
    df["_dup_delta_days"]         = 0

    amt_col  = col_map.get("amount")
    vend_col = col_map.get("vendor")
    date_col = col_map.get("date")
    emp_col  = col_map.get("employee")

    # ── Pass A: Exact duplicates (vendor + rounded_amount + date) ─────────────
    if amt_col and vend_col:
        df["_ramt"] = df[amt_col].round(0)

        # Build composite key — include employee if present
        key_cols = [vend_col, "_ramt"]
        if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df["_date_str"] = df[date_col].dt.strftime("%Y-%m-%d")
            key_cols.append("_date_str")
        if emp_col and emp_col in df.columns:
            key_cols.append(emp_col)

        # Only compare rows where all key columns have valid data
        valid_mask = df[amt_col].notna() & df[vend_col].notna()
        if date_col and "_date_str" in df.columns:
            valid_mask = valid_mask & df[date_col].notna()

        valid_df = df[valid_mask].copy()

        if len(valid_df) > 0:
            dup_mask_exact = valid_df.duplicated(subset=key_cols, keep=False)
            dup_indices    = valid_df[dup_mask_exact].index

            # For each dup group, record what the "original" txn index is
            first_of_group = valid_df.drop_duplicates(subset=key_cols, keep="first")
            first_idx_map  = {}
            for _, row in first_of_group.iterrows():
                group_key = tuple(row[k] for k in key_cols)
                first_idx_map[group_key] = row.name  # index of first occurrence

            for idx in dup_indices:
                row       = df.loc[idx]
                group_key = tuple(df.loc[idx, k] for k in key_cols)
                orig_idx  = first_idx_map.get(group_key, idx)
                if orig_idx != idx:  # skip the "first" occurrence
                    df.at[idx, "_flag_duplicate_txn"] = True
                    df.at[idx, "_dup_of"]             = str(orig_idx)
                else:
                    # Mark the first as duplicate too (keep=False means ALL are marked)
                    df.at[idx, "_flag_duplicate_txn"] = True

        # Clean temp cols
        df.drop(columns=["_ramt"], errors="ignore", inplace=True)
        if "_date_str" in df.columns:
            df.drop(columns=["_date_str"], errors="ignore", inplace=True)

    # ── Pass B: Near-duplicates (vendor + amount, Δdate ≤7 days) ──────────────
    if amt_col and vend_col and date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df["_ramt_b"] = df[amt_col].round(0)
        near_key_cols = [vend_col, "_ramt_b"]
        if emp_col and emp_col in df.columns:
            near_key_cols.append(emp_col)

        valid_near = df[
            df[amt_col].notna() & df[vend_col].notna() & df[date_col].notna()
            & (~df["_flag_duplicate_txn"])   # already flagged as exact — skip
        ].copy()
        valid_near["_ts_ns"] = valid_near[date_col].astype(np.int64)

        window_ns = 7 * 24 * 3600 * int(1e9)

        for _, grp in valid_near.groupby(near_key_cols, sort=False):
            if len(grp) < 2:
                continue
            grp_s = grp.sort_values(date_col)
            ts    = grp_s["_ts_ns"].values
            idxs  = grp_s.index.values

            for i in range(len(ts) - 1):
                delta_ns   = abs(int(ts[i + 1] - ts[i]))
                delta_days = delta_ns // (24 * 3600 * int(1e9))
                if 0 < delta_days <= 7:
                    for pos in (i, i + 1):
                        df.at[idxs[pos], "_flag_near_duplicate"] = True
                        if df.at[idxs[pos], "_dup_delta_days"] == 0:
                            df.at[idxs[pos], "_dup_delta_days"] = int(delta_days)

        df.drop(columns=["_ramt_b", "_ts_ns"], errors="ignore", inplace=True)

    # ── Pass C: Invoice ID normalization (existing logic — when column exists) ─
    inv_key = "_inv_key" if "_inv_key" in df.columns else None
    if inv_key:
        valid_inv = df[inv_key].notna()
        dup_inv   = df.duplicated(subset=[inv_key], keep=False) & valid_inv
        df["_flag_duplicate_invoice"] = dup_inv

    return df


# ─────────────────────────────────────────────
#  FRAUD DETECTION ENGINE  (updated)
# ─────────────────────────────────────────────
def compute_fraud_scores(df_raw, col_map):
    # Run transaction-level dup detection FIRST
    df = detect_transaction_duplicates(df_raw, col_map)

    n       = len(df)
    scores  = pd.Series(np.zeros(n), index=df.index, dtype=float)
    reasons = pd.Series([""] * n, index=df.index, dtype=str)
    flags   = {}

    amt_col  = col_map.get("amount")
    date_col = col_map.get("date")
    vend_col = col_map.get("vendor")
    inv_col  = col_map.get("invoice_id")
    rec_col  = col_map.get("receipt")
    dept_col = col_map.get("department")

    def _add_reason(mask, text):
        reasons[mask] = reasons[mask].apply(lambda r: (r + "; " + text).lstrip("; "))

    # ── 1a. Exact transaction duplicates (Pass A — new primary check) ──────────
    if "_flag_duplicate_txn" in df.columns:
        dup_txn_mask = df["_flag_duplicate_txn"].fillna(False)
        flags["duplicate_txn"] = dup_txn_mask
        scores[dup_txn_mask] += 35
        _add_reason(dup_txn_mask, "Exact duplicate transaction (vendor+amount+date)")

    # ── 1b. Near-duplicate transactions (Pass B) ───────────────────────────────
    if "_flag_near_duplicate" in df.columns:
        near_dup_mask = df["_flag_near_duplicate"].fillna(False)
        flags["near_duplicate"] = near_dup_mask
        scores[near_dup_mask] += 20
        _add_reason(near_dup_mask, "Near-duplicate transaction (≤7d same vendor/amount)")

    # ── 1c. Duplicate invoice IDs (Pass C) ────────────────────────────────────
    if "_flag_duplicate_invoice" in df.columns:
        dup_inv_mask = df["_flag_duplicate_invoice"].fillna(False)
        flags["duplicate_invoice"] = dup_inv_mask
        scores[dup_inv_mask] += 35
        _add_reason(dup_inv_mask, "Duplicate invoice ID (normalized match)")

    # ── 2. Outlier amounts (IQR on POSITIVE amounts) ──────────────────────────
    if amt_col and df[amt_col].notna().sum() > 10:
        pos = df[amt_col][df[amt_col] > 0].dropna()
        if len(pos) > 10:
            q1, q3 = pos.quantile(0.25), pos.quantile(0.75)
            iqr = q3 - q1
            upper_fence = q3 + 3.5 * iqr
            outlier_mask = (df[amt_col] > upper_fence) & df[amt_col].notna()
            flags["outlier_amount"] = outlier_mask
            scores[outlier_mask] += 25
            _add_reason(outlier_mask, f"Outlier amount (>{upper_fence:,.0f})")

    # ── 3. Suspicious round amounts (multiples of 500 > $1000) ───────────────
    if amt_col:
        round_mask = df[amt_col].apply(
            lambda x: pd.notna(x) and x > 1000 and x % 500 == 0
        )
        flags["round_amount"] = round_mask
        scores[round_mask] += 10
        _add_reason(round_mask, "Suspicious round amount")

    # ── 4. Weekend transactions ───────────────────────────────────────────────
    if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        weekend = df[date_col].dt.dayofweek >= 5
        flags["weekend_transaction"] = weekend
        scores[weekend] += 8
        _add_reason(weekend, "Weekend transaction")

    # ── 5. Missing receipts ───────────────────────────────────────────────────
    if rec_col and rec_col in df.columns:
        col_lower = df[rec_col].astype(str).str.lower().str.strip()
        missing_rec = col_lower.isin([
            "no","false","missing","n","0","none","nan",
            "not attached","not submitted","pending","required"
        ])
        flags["missing_receipt"] = missing_rec
        scores[missing_rec] += 12
        _add_reason(missing_rec, "Missing receipt")

    # ── 6. High-value transactions (99th percentile) ──────────────────────────
    if amt_col and df[amt_col].notna().sum() > 10:
        pos = df[amt_col][df[amt_col] > 0].dropna()
        if len(pos) > 10:
            p99 = pos.quantile(0.99)
            high_val = (df[amt_col] > p99) & df[amt_col].notna()
            flags["high_value"] = high_val
            scores[high_val] += 15
            _add_reason(high_val, f"Top 1% high value (>{p99:,.0f})")

    # ── 7. Rapid repeated vendor payments (≥3 times in 7 days) ───────────────
    if date_col and vend_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        rapid = pd.Series(False, index=df.index)
        try:
            tmp = df[[vend_col, date_col]].copy().sort_values(date_col)
            tmp["_ts"] = tmp[date_col].astype(np.int64)
            for vendor, grp in tmp.groupby(vend_col):
                if len(grp) >= 3:
                    ts = grp["_ts"].values
                    window_ns = 7 * 24 * 3600 * int(1e9)
                    for i in range(len(ts)):
                        count = ((ts >= ts[i]) & (ts <= ts[i] + window_ns)).sum()
                        if count >= 3:
                            rapid[grp.index[i]] = True
        except Exception:
            pass
        flags["rapid_payment"] = rapid
        scores[rapid] += 15
        _add_reason(rapid, "Rapid repeated vendor payments")

    # ── 8. Refund anomalies ───────────────────────────────────────────────────
    if "_is_refund" in df.columns:
        refund_mask = df["_is_refund"].fillna(False)
        flags["refund"] = refund_mask
        scores[refund_mask] += 10
        _add_reason(refund_mask, "Refund / negative transaction")

    # ── 9. Abnormal department spend ──────────────────────────────────────────
    if dept_col and amt_col and dept_col in df.columns:
        try:
            dept_medians = df[df[amt_col] > 0].groupby(dept_col)[amt_col].median()
            dept_means   = df[df[amt_col] > 0].groupby(dept_col)[amt_col].mean()
            dept_mapped_med = df[dept_col].map(dept_medians)
            dept_mapped_avg = df[dept_col].map(dept_means)
            abnormal_dept = (
                df[amt_col].notna() &
                (df[amt_col] > 0) &
                dept_mapped_med.notna() &
                (df[amt_col] > dept_mapped_med * 4) &
                (df[amt_col] > dept_mapped_avg * 2.5)
            )
            flags["abnormal_dept_spend"] = abnormal_dept
            scores[abnormal_dept] += 12
            _add_reason(abnormal_dept, "Abnormal vs dept median")
        except Exception:
            pass

    # ── 10. Vendor concentration (vendor >20% of total spend) ─────────────────
    if vend_col and amt_col and df[amt_col].notna().sum() > 0:
        total_positive = df[df[amt_col] > 0][amt_col].sum()
        if total_positive > 0:
            vendor_spend = df[df[amt_col] > 0].groupby(vend_col)[amt_col].transform("sum")
            conc = (vendor_spend / total_positive) > 0.20
            conc_full = pd.Series(False, index=df.index)
            conc_full[conc.index] = conc.values
            flags["vendor_concentration"] = conc_full
            scores[conc_full] += 8
            _add_reason(conc_full, "Vendor concentration >20% of spend")

    # ── Finalize ──────────────────────────────────────────────────────────────
    scores = scores.clip(0, 100)

    def risk_level(s):
        if s >= 40:   return "High"
        elif s >= 15: return "Medium"
        return "Low"

    df_out = df.copy()
    df_out["_fraud_score"]  = scores.values
    df_out["_risk_level"]   = scores.apply(risk_level).values
    df_out["_risk_reasons"] = reasons.values
    for k, v in flags.items():
        ser = v if isinstance(v, pd.Series) else pd.Series(v, index=df.index)
        df_out[f"_flag_{k}"] = ser.reindex(df.index, fill_value=False).values

    return df_out, flags


# ─────────────────────────────────────────────
#  INSIGHTS ENGINE  (updated to use all dup types)
# ─────────────────────────────────────────────
def generate_insights(df, col_map):
    insights = []
    amt_col    = col_map.get("amount")
    date_col   = col_map.get("date")
    vend_col   = col_map.get("vendor")
    dept_col   = col_map.get("department")
    cat_col    = col_map.get("category")
    inv_col    = col_map.get("invoice_id")
    rec_col    = col_map.get("receipt")
    status_col = col_map.get("status")

    if amt_col is None:
        return [{"title":"No Amount Column Detected","body":"Upload a dataset with an amount/cost column for full analytics.","type":"warn"}]

    pos = df[df[amt_col] > 0] if amt_col in df.columns else df
    total      = pos[amt_col].sum()
    n          = len(df)
    n_pos      = len(pos)
    median_txn = pos[amt_col].median() if n_pos > 0 else 0
    mean_txn   = pos[amt_col].mean()   if n_pos > 0 else 0

    # ── Exact transaction duplicates (Pass A) ──────────────────────────────────
    exact_dup_col = "_flag_duplicate_txn"
    if exact_dup_col in df.columns:
        exact_dups = df[df[exact_dup_col] == True]
        exact_cnt  = len(exact_dups)
        if exact_cnt > 0:
            exact_pct = exact_cnt / max(n, 1) * 100
            exact_amt = exact_dups[amt_col].sum() if amt_col else 0
            insights.append({
                "title": f"◉ {exact_cnt:,} Exact Duplicate Transactions ({exact_pct:.1f}%)",
                "body": (
                    f"Same vendor, same amount, same date — {exact_cnt:,} transactions are "
                    f"confirmed duplicates. Maximum double-payment exposure: ${exact_amt:,.2f}. "
                    f"These match the notebook's confirmed duplicate criteria "
                    f"(vendor + amount + date). Assign to AP for immediate review."
                ),
                "type": "danger"
            })

    # ── Near-duplicate transactions (Pass B) ───────────────────────────────────
    near_dup_col = "_flag_near_duplicate"
    if near_dup_col in df.columns:
        near_dups = df[df[near_dup_col] == True]
        near_cnt  = len(near_dups)
        if near_cnt > 0:
            near_pct = near_cnt / max(n, 1) * 100
            near_amt = near_dups[amt_col].sum() if amt_col else 0
            avg_days = df.loc[df[near_dup_col] == True, "_dup_delta_days"].mean() if "_dup_delta_days" in df.columns else "≤7"
            insights.append({
                "title": f"⚠︎ {near_cnt:,} Near-Duplicate Transactions ({near_pct:.1f}%) — Under Review",
                "body": (
                    f"Same vendor + amount, submitted within {avg_days:.0f}d of each other on average. "
                    f"Total value at risk: ${near_amt:,.2f}. "
                    f"These match the notebook's near-duplicate criteria (Δdate ≤7 days). "
                    f"Set to 'under_review' status pending finance sign-off."
                ),
                "type": "warn"
            })

    # ── Invoice ID duplicates (Pass C) ────────────────────────────────────────
    inv_key = "_inv_key" if "_inv_key" in df.columns else inv_col
    if inv_key and inv_key in df.columns:
        dup_mask  = df.duplicated(subset=[inv_key], keep=False) & df[inv_key].notna()
        dup_count = dup_mask.sum()
        if dup_count > 0:
            dup_pct = dup_count / max(n, 1) * 100
            dup_amt = df[dup_mask][amt_col].sum() if amt_col else 0
            insights.append({
                "title": f"⧉ {dup_count:,} Duplicate Invoice IDs ({dup_pct:.1f}%) — Normalized Match",
                "body": (
                    f"Normalized invoice matching (INV001 = INV-001 = inv 001) found "
                    f"{dup_count:,} records sharing duplicate IDs. "
                    f"Potential double-payment exposure: ${dup_amt:,.2f}. Immediate audit required."
                ),
                "type": "danger"
            })

    # ── Refund analytics ───────────────────────────────────────────────────────
    if "_is_refund" in df.columns:
        refund_df  = df[df["_is_refund"] == True]
        refund_cnt = len(refund_df)
        refund_pct = refund_cnt / max(n, 1) * 100
        if refund_cnt > 0:
            refund_amt = abs(refund_df[amt_col].sum())
            if refund_pct > 5:
                insights.append({
                    "title": f"↩ High Refund Rate: {refund_pct:.1f}% of Transactions",
                    "body": f"{refund_cnt:,} refund/credit transactions totaling ${refund_amt:,.2f}. Elevated refund rate may indicate vendor disputes, approval issues, or processing errors.",
                    "type": "danger" if refund_pct > 10 else "warn"
                })
            else:
                insights.append({
                    "title": f"↩ Refund Activity: {refund_cnt:,} Credits ({refund_pct:.1f}%)",
                    "body": f"${refund_amt:,.2f} in refunds/credits — within normal range. Monitor for sudden increases.",
                    "type": "good"
                })

    # ── Vendor concentration ───────────────────────────────────────────────────
    if vend_col and total > 0:
        vendor_totals = pos.groupby(vend_col)[amt_col].sum().sort_values(ascending=False)
        if len(vendor_totals) > 0:
            top_vendor = vendor_totals.index[0]
            top_pct    = vendor_totals.iloc[0] / total * 100
            if top_pct > 30:
                insights.append({
                    "title": f"◉ Critical Vendor Concentration: {top_vendor} ({top_pct:.1f}%)",
                    "body": f"{top_vendor} accounts for {top_pct:.1f}% of total spend (${vendor_totals.iloc[0]:,.2f}). Single-vendor dependency at this level is a supply-chain and compliance risk.",
                    "type": "danger"
                })
            elif top_pct > 15:
                n_vendors_80 = int((vendor_totals.cumsum() / total < 0.80).sum()) + 1
                insights.append({
                    "title": f"◎ Vendor Dependency Risk: {top_vendor} ({top_pct:.1f}%)",
                    "body": f"Top vendor at {top_pct:.1f}% of spend. {n_vendors_80} vendors account for 80% of total expenditure.",
                    "type": "warn"
                })

    # ── Monthly trend ──────────────────────────────────────────────────────────
    if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]) and amt_col:
        monthly = pos.groupby(pos[date_col].dt.to_period("M"))[amt_col].sum()
        if len(monthly) >= 3:
            last  = float(monthly.iloc[-1])
            prev  = float(monthly.iloc[-2])
            avg_3 = float(monthly.iloc[-3:].mean())
            if prev > 0:
                pct = (last - prev) / prev * 100
                if abs(pct) > 25:
                    direction = "spike" if pct > 0 else "drop"
                    insights.append({
                        "title": f"✔ {abs(pct):.0f}% Month-over-Month Spending {direction.title()}",
                        "body": f"Latest period: ${last:,.2f} vs prior: ${prev:,.2f} — a {abs(pct):.1f}% {direction}. 3-month average: ${avg_3:,.2f}.",
                        "type": "danger" if direction == "spike" and pct > 50 else "warn"
                    })

    # ── Skew indicator ─────────────────────────────────────────────────────────
    if n_pos > 10 and median_txn > 0:
        skew_ratio = mean_txn / median_txn
        if skew_ratio > 3:
            insights.append({
                "title": f"𓊍 Heavy Skew: Mean ${mean_txn:,.0f} vs Median ${median_txn:,.0f} ({skew_ratio:.1f}x)",
                "body": f"Large outlier transactions are inflating the average by {skew_ratio:.1f}x over median. Use IQR-based anomaly detection.",
                "type": "warn"
            })

    # ── Department anomaly ─────────────────────────────────────────────────────
    if dept_col and dept_col in df.columns and total > 0:
        dept_spend = pos.groupby(dept_col)[amt_col].sum().sort_values(ascending=False)
        if len(dept_spend) >= 2:
            top_dept     = dept_spend.index[0]
            top_dept_pct = dept_spend.iloc[0] / total * 100
            if top_dept_pct > 40:
                insights.append({
                    "title": f"🏠︎ Department Concentration: {top_dept} ({top_dept_pct:.1f}%)",
                    "body": f"{top_dept} accounts for {top_dept_pct:.1f}% of total expense (${dept_spend.iloc[0]:,.2f}). May indicate budget overage or misclassification.",
                    "type": "warn"
                })

    # ── Round-amount risk ──────────────────────────────────────────────────────
    if amt_col:
        round_mask = pos[amt_col].apply(lambda x: pd.notna(x) and x > 500 and x % 500 == 0)
        round_pct  = round_mask.mean() * 100
        if round_pct > 20:
            insights.append({
                "title": f"◯ {round_pct:.0f}% Suspiciously Round Amounts (>$500, multiple of 500)",
                "body": "High proportion of round numbers may indicate estimated or fabricated expenses. Real purchases rarely round so cleanly.",
                "type": "warn"
            })

    # ── Missing receipts ───────────────────────────────────────────────────────
    if rec_col and rec_col in df.columns:
        col_lower = df[rec_col].astype(str).str.lower().str.strip()
        missing_mask = col_lower.isin([
            "no","false","missing","n","0","none","nan","not attached","not submitted","pending","required"
        ])
        missing_pct = missing_mask.mean() * 100
        missing_amt = df[missing_mask][amt_col].sum() if amt_col else 0
        if missing_pct > 15:
            insights.append({
                "title": f"🗎 {missing_pct:.0f}% Missing Receipt Documentation",
                "body": f"{missing_mask.sum():,} transactions (${missing_amt:,.2f}) lack receipt proof. Above policy threshold — creates audit exposure.",
                "type": "danger" if missing_pct > 30 else "warn"
            })

    # ── Status analytics ───────────────────────────────────────────────────────
    if status_col and status_col in df.columns:
        status_counts = df[status_col].astype(str).str.lower().value_counts()
        unapproved_kws = ["pending","rejected","unapproved","review","hold","blocked","failed","under_review"]
        unapp_count = sum(status_counts.get(k, 0) for k in unapproved_kws)
        unapp_pct   = unapp_count / max(n, 1) * 100
        if unapp_pct > 5:
            insights.append({
                "title": f"🗒️ {unapp_pct:.1f}% Transactions Not Fully Approved",
                "body": f"{unapp_count:,} transactions are in pending/rejected/review state. Unapproved expenses processed outside normal workflow represent a compliance risk.",
                "type": "warn"
            })

    # ── Category insights ──────────────────────────────────────────────────────
    if cat_col and cat_col in df.columns and amt_col and total > 0:
        cat_spend = pos.groupby(cat_col)[amt_col].sum().sort_values(ascending=False)
        if len(cat_spend) > 0:
            top_cat = cat_spend.index[0]
            cat_pct = cat_spend.iloc[0] / total * 100
            insights.append({
                "title": f"ılıılıılıılıılıılı Top Category: {top_cat} ({cat_pct:.1f}% of spend)",
                "body": f"{top_cat} represents {cat_pct:.1f}% of total spend (${cat_spend.iloc[0]:,.2f}). Review budget allocation and policy limits.",
                "type": "good"
            })

    # ── Benchmark ─────────────────────────────────────────────────────────────
    insights.append({
        "title": f"𖡊 Typical Expense: ${median_txn:,.2f} (median) across {n_pos:,} positive transactions",
        "body": f"Total gross spend: ${total:,.2f} across {n:,} records. Mean ${mean_txn:,.2f} (use with caution if skewed).",
        "type": "good"
    })

    if len(insights) == 1:
        insights.append({"title":"Data Loaded Successfully","body":"No critical anomalies detected in initial scan. Use filters to drill down.","type":"good"})

    return insights


# ─────────────────────────────────────────────
#  NLP QUERY ENGINE
# ─────────────────────────────────────────────
def nlp_query(question, df, col_map):
    q = question.lower()
    amt_col    = col_map.get("amount")
    vend_col   = col_map.get("vendor")
    dept_col   = col_map.get("department")
    emp_col    = col_map.get("employee")
    cat_col    = col_map.get("category")
    inv_col    = col_map.get("invoice_id")
    date_col   = col_map.get("date")
    rec_col    = col_map.get("receipt")
    status_col = col_map.get("status")

    if any(x in q for x in ["refund","credit","negative","reversal","credit note"]):
        if "_is_refund" in df.columns:
            ref = df[df["_is_refund"] == True].copy()
            cols = [c for c in [amt_col, vend_col, dept_col, date_col] if c]
            ref_amt = abs(ref[amt_col].sum()) if amt_col and len(ref) > 0 else 0
            return "table", ref[cols].head(50) if cols else ref.head(50), f"**{len(ref):,} refund/credit transactions** totaling **${ref_amt:,.2f}**.", None, None
        return "text", None, "No refund data detected.", None, None

    if any(x in q for x in ["duplicate","dupl","repeated","double"]):
        # Show all duplicate types
        parts = []
        result_dfs = []

        for flag_col, label in [("_flag_duplicate_txn","Exact Dup Txn"), ("_flag_near_duplicate","Near-Dup Txn"), ("_flag_duplicate_invoice","Invoice ID Dup")]:
            if flag_col in df.columns:
                sub = df[df[flag_col] == True].copy()
                if len(sub) > 0:
                    parts.append(f"{len(sub):,} {label}")
                    result_dfs.append(sub)

        if result_dfs:
            all_dups = pd.concat(result_dfs).drop_duplicates()
            cols = [c for c in [inv_col, amt_col, vend_col, dept_col, date_col, "_dup_delta_days"] if c and c in all_dups.columns]
            dup_amt = all_dups[amt_col].sum() if amt_col else 0
            summary = f"**{len(all_dups):,} duplicate records** ({'; '.join(parts)}). Exposure: ${dup_amt:,.2f}."
            return "table", all_dups[cols].head(60), summary, None, None

        return "text", None, "No duplicates detected.", None, None

    if any(x in q for x in ["vendor","supplier","merchant","payee","concentration"]):
        if vend_col and amt_col:
            pos = df[df[amt_col] > 0] if amt_col else df
            result = pos.groupby(vend_col)[amt_col].agg(["sum","count","median"]).reset_index()
            result.columns = [vend_col, "Total Spend", "Transactions", "Median Spend"]
            result["% of Total"] = (result["Total Spend"] / result["Total Spend"].sum() * 100).round(1).astype(str) + "%"
            result = result.sort_values("Total Spend", ascending=False).head(20)
            summary = f"**Top vendors by spend.** Top vendor: {result.iloc[0][vend_col]} at {result.iloc[0]['% of Total']}."
            return "table+chart", result, summary, vend_col, "Total Spend"
        return "text", None, "No vendor or amount column detected.", None, None

    if any(x in q for x in ["department","dept","team","division"]):
        if dept_col and amt_col:
            pos = df[df[amt_col] > 0] if amt_col else df
            result = pos.groupby(dept_col)[amt_col].agg(["sum","count","median"]).reset_index()
            result.columns = [dept_col, "Total Spend", "Transactions", "Median Spend"]
            total = result["Total Spend"].sum()
            result["% of Total"] = (result["Total Spend"] / total * 100).round(1).astype(str) + "%"
            result = result.sort_values("Total Spend", ascending=False)
            summary = f"**Department spend breakdown** — {len(result)} departments. Top: {result.iloc[0][dept_col]} at {result.iloc[0]['% of Total']}."
            return "table+chart", result, summary, dept_col, "Total Spend"
        return "text", None, "No department column detected.", None, None

    if any(x in q for x in ["suspicious","fraud","risk","anomal","outlier","risky","abnormal"]):
        if "_risk_level" in df.columns:
            high = df[df["_risk_level"] == "High"].copy()
            cols = [c for c in [amt_col, vend_col, dept_col, "_fraud_score","_risk_level","_risk_reasons"] if c and c in df.columns]
            high_amt = high[amt_col].sum() if amt_col else 0
            pct = len(high) / max(len(df),1) * 100
            summary = f"**{len(high):,} high-risk transactions** ({pct:.1f}%) totaling **${high_amt:,.2f}**."
            return "table", high[cols].sort_values("_fraud_score", ascending=False).head(30), summary, None, None
        return "text", None, "Run fraud analysis first.", None, None

    if any(x in q for x in ["largest","biggest","top","highest","most expensive"]):
        if amt_col:
            top = df[df[amt_col] > 0].sort_values(amt_col, ascending=False).head(20) if amt_col else df.head(20)
            cols = [c for c in [amt_col, vend_col, dept_col, cat_col, date_col] if c and c in df.columns]
            summary = f"**Top 20 largest transactions.** Max: ${top.iloc[0][amt_col]:,.2f}." if len(top) > 0 else "No data."
            return "table", top[cols], summary, None, None
        return "text", None, "No amount column detected.", None, None

    if any(x in q for x in ["missing receipt","no receipt","unattached","receipt"]):
        if rec_col and rec_col in df.columns:
            col_lower = df[rec_col].astype(str).str.lower().str.strip()
            missing = df[col_lower.isin(["no","false","missing","n","0","none","nan","not attached","not submitted","pending","required"])]
            cols = [c for c in [amt_col, vend_col, dept_col, emp_col, rec_col] if c and c in df.columns]
            miss_amt = missing[amt_col].sum() if amt_col else 0
            pct = len(missing) / max(len(df),1) * 100
            summary = f"**{len(missing):,} transactions missing receipts** ({pct:.1f}%), value: ${miss_amt:,.2f}."
            return "table", missing[cols].head(30), summary, None, None
        return "text", None, "No receipt status column detected.", None, None

    if any(x in q for x in ["employee","staff","person","who","submitted by"]):
        if emp_col and amt_col:
            pos = df[df[amt_col] > 0] if amt_col else df
            result = pos.groupby(emp_col)[amt_col].agg(["sum","count","median"]).reset_index()
            result.columns = [emp_col, "Total Spend", "Transactions", "Median Spend"]
            result = result.sort_values("Total Spend", ascending=False).head(20)
            summary = f"**Top employees by expense.** Highest spender: {result.iloc[0][emp_col]} at ${result.iloc[0]['Total Spend']:,.2f}." if len(result) > 0 else ""
            return "table+chart", result, summary, emp_col, "Total Spend"
        return "text", None, "No employee column detected.", None, None

    if any(x in q for x in ["categor","type","class","nature","breakdown"]):
        if cat_col and amt_col:
            pos = df[df[amt_col] > 0] if amt_col else df
            result = pos.groupby(cat_col)[amt_col].agg(["sum","count"]).reset_index()
            result.columns = [cat_col, "Total Spend", "Count"]
            total = result["Total Spend"].sum()
            result["% of Total"] = (result["Total Spend"] / total * 100).round(1).astype(str) + "%"
            result = result.sort_values("Total Spend", ascending=False)
            return "table+chart", result, f"**Spend by category** — {len(result)} categories.", cat_col, "Total Spend"
        return "text", None, "No category column detected.", None, None

    if any(x in q for x in ["monthly","month","trend","time","over time"]):
        if date_col and amt_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            pos = df[df[amt_col] > 0] if amt_col else df
            monthly = pos.groupby(pos[date_col].dt.to_period("M"))[amt_col].sum().reset_index()
            monthly.columns = ["Month", "Total Spend"]
            monthly["Month"] = monthly["Month"].astype(str)
            monthly["MoM %"] = monthly["Total Spend"].pct_change().mul(100).round(1)
            return "table+chart", monthly, f"**Monthly spend trend** — {len(monthly)} periods.", "Month", "Total Spend"
        return "text", None, "No parseable date column detected.", None, None

    if any(x in q for x in ["weekend","saturday","sunday","off-day"]):
        if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            wknd = df[df[date_col].dt.dayofweek >= 5].copy()
            cols = [c for c in [amt_col, vend_col, dept_col, date_col] if c and c in df.columns]
            wknd_amt = wknd[amt_col].sum() if amt_col and len(wknd) > 0 else 0
            pct = len(wknd) / max(len(df),1) * 100
            summary = f"**{len(wknd):,} weekend transactions** ({pct:.1f}%), total ${wknd_amt:,.2f}."
            return "table", wknd[cols].head(30), summary, None, None
        return "text", None, "No parseable date column.", None, None

    if any(x in q for x in ["status","approval","pending","approved","rejected","unapproved"]):
        if status_col and status_col in df.columns:
            result = df.groupby(status_col).size().reset_index(name="Count")
            if amt_col:
                result = df.groupby(status_col)[amt_col].agg(["count","sum"]).reset_index()
                result.columns = [status_col, "Count", "Total Spend"]
            summary = f"**Approval/status distribution** — {result[status_col].nunique()} distinct states."
            return "table+chart", result, summary, status_col, "Count"
        return "text", None, "No status/approval column detected.", None, None

    pos = df[df[amt_col] > 0] if amt_col and amt_col in df.columns else df
    total  = pos[amt_col].sum() if amt_col else 0
    median = pos[amt_col].median() if amt_col and len(pos) > 0 else 0
    refund_cnt = (df["_is_refund"] == True).sum() if "_is_refund" in df.columns else 0
    summary_parts = [
        f"**Dataset contains {len(df):,} transactions** ({len(pos):,} positive, {refund_cnt:,} refunds/credits).",
        f"Gross spend: **${total:,.2f}** | Median transaction: **${median:,.2f}**" if amt_col else "",
    ]
    return "text", None, "\n\n".join(p for p in summary_parts if p), None, None


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def kpi_card(label, value, sub="", icon="🗠", color="var(--accent)"):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """

def badge(risk):
    if risk == "High":   return '<span class="badge-high">HIGH</span>'
    if risk == "Medium": return '<span class="badge-medium">MEDIUM</span>'
    return '<span class="badge-low">LOW</span>'

def section(icon, title):
    st.markdown(f"""<div class="section-header"><span>{icon}</span><h2>{title}</h2></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
def main():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True
    with st.sidebar:
        st.markdown("## 🌿 FinSight ERP")
        st.markdown('<div class="sidebar-section">Data Upload</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"], label_visibility="collapsed")

        st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)
        nav = st.radio("", [" Executive Dashboard", " Fraud Analysis", " Business Insights", "Ask Your Data", " Data Explorer"],
                       label_visibility="collapsed")

        filters_placeholder = st.container()

    st.markdown("""
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;background:linear-gradient(90deg,#0c1f17,#071410);border:1px solid #1a3d2b;border-radius:12px;padding:0.9rem 1.2rem;">
            <div style="background:linear-gradient(135deg,#22c55e,#10b981);width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;">🌿</div>
            <div>
                <h1 style="margin:0;font-size:1.4rem;font-weight:700;background:linear-gradient(90deg,#22c55e,#4ade80);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">FinSight ERP</h1>
                <p style="margin:0;color:#86efac;font-size:0.78rem;letter-spacing:0.03em;">AI-Powered Financial Audit &amp; Expense Intelligence Platform</p>
            </div>
            <div style="margin-left:auto;display:flex;gap:0.5rem;align-items:center;">
                <span style="background:#0f2d1a;border:1px solid #22c55e33;color:#22c55e;font-size:0.65rem;font-weight:600;padding:3px 10px;border-radius:20px;letter-spacing:0.06em;">● LIVE</span>
                <span style="background:#0f2d1a;border:1px solid #1a3d2b;color:#4ade80;font-size:0.65rem;padding:3px 10px;border-radius:20px;">Enterprise v2.0</span>
            </div>
        </div>
        <div style="height:0.75rem;"></div>
                if not st.sidebar._is_collapsed if hasattr(st.sidebar, '_is_collapsed') else False:
        pass
    
    col_btn, col_rest = st.columns([0.05, 0.95])
    with col_btn:
        if st.button("☰", key="open_sidebar", help="Open sidebar"):
            st.session_state.sidebar_open = True
            st.rerun()
    """, unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
        <div class="upload-hero">
            <div style="font-size:3rem;margin-bottom:1rem;">🗁</div>
            <h2>Upload Your Financial Dataset</h2>
            <p>Drag & drop a CSV or XLSX file using the sidebar uploader.<br>
            Supports dirty enterprise data: inconsistent formats, duplicate invoices,<br>multiple currencies, messy vendor names, malformed dates.</p>
            <br>
            <p style="color:#3b82f6;font-size:0.8rem;font-family:'JetBrains Mono',monospace;">
                Supports up to 100,000 rows • Auto-cleans & normalizes data • Real-time fraud detection
            </p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        feats = [
            ("🔍︎", "Fraud Detection","Exact + near-duplicate detection, IQR outliers, vendor concentration"),
            ("〽","Trend Analytics","Monthly spend trends, department analysis, vendor concentration"),
            ("✦","NLP Queries","Ask plain-English questions about your expense data"),
            ("⬇","Export Reports","Download cleaned datasets and filtered reports as CSV"),
        ]
        for col, (ico, title, desc) in zip(cols, feats):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center;padding:1.5rem 1rem;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">{ico}</div>
                    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.4rem;">{title}</div>
                    <div style="font-size:0.75rem;color:#64748b;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        return

    file_bytes = uploaded_file.read()
    with st.spinner("◯ Loading and cleaning data..."):
        df_raw, err, col_map = load_and_clean(file_bytes, uploaded_file.name)

    if err:
        st.error(f"⌘ Failed to load file: {err}")
        return
    if df_raw is None or len(df_raw) == 0:
        st.warning(" The uploaded file appears to be empty.")
        return

    with st.spinner("🛡 Running fraud analysis (3-pass duplicate detection)..."):
        df_fraud, flags = compute_fraud_scores(df_raw, col_map)

    amt_col  = col_map.get("amount")
    date_col = col_map.get("date")
    vend_col = col_map.get("vendor")
    dept_col = col_map.get("department")
    cat_col  = col_map.get("category")
    emp_col  = col_map.get("employee")
    inv_col  = col_map.get("invoice_id")
    rec_col  = col_map.get("receipt")

    # ── SIDEBAR FILTERS ───────────────────────
    with filters_placeholder:
        st.markdown('<div class="sidebar-section">Filters</div>', unsafe_allow_html=True)
        df_filtered = df_fraud.copy()

        if dept_col and dept_col in df_filtered.columns:
            depts = sorted([x for x in df_filtered[dept_col].dropna().unique() if str(x) != "nan"])
            if depts:
                sel_dept = st.multiselect("Department", depts, placeholder="All")
                if sel_dept:
                    df_filtered = df_filtered[df_filtered[dept_col].isin(sel_dept)]

        if vend_col and vend_col in df_filtered.columns:
            vendors = sorted([x for x in df_filtered[vend_col].dropna().unique() if str(x) != "nan"])[:200]
            if vendors:
                sel_vendor = st.multiselect("Vendor", vendors, placeholder="All")
                if sel_vendor:
                    df_filtered = df_filtered[df_filtered[vend_col].isin(sel_vendor)]

        if cat_col and cat_col in df_filtered.columns:
            cats = sorted([x for x in df_filtered[cat_col].dropna().unique() if str(x) != "nan"])
            if cats:
                sel_cat = st.multiselect("Category", cats, placeholder="All")
                if sel_cat:
                    df_filtered = df_filtered[df_filtered[cat_col].isin(sel_cat)]

        if date_col and pd.api.types.is_datetime64_any_dtype(df_filtered[date_col]):
            valid_dates = df_filtered[date_col].dropna()
            if len(valid_dates) > 0:
                min_d = valid_dates.min().date()
                max_d = valid_dates.max().date()
                date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
                if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                    df_filtered = df_filtered[
                        (df_filtered[date_col].dt.date >= date_range[0]) &
                        (df_filtered[date_col].dt.date <= date_range[1])
                    ]

        if amt_col and amt_col in df_filtered.columns:
            amt_vals = df_filtered[amt_col].dropna()
            if len(amt_vals) > 0:
                mn, mx = float(amt_vals.min()), float(amt_vals.max())
                if mn < mx:
                    amt_range = st.slider("Amount Range", mn, mx, (mn, mx), format="$%.0f")
                    df_filtered = df_filtered[(df_filtered[amt_col] >= amt_range[0]) & (df_filtered[amt_col] <= amt_range[1])]

        if "_risk_level" in df_filtered.columns:
            risk_filter = st.multiselect("Risk Level", ["High","Medium","Low"], placeholder="All")
            if risk_filter:
                df_filtered = df_filtered[df_filtered["_risk_level"].isin(risk_filter)]

        st.markdown('<div class="sidebar-section">Data Info</div>', unsafe_allow_html=True)
        st.caption(f"🗒 Rows: **{len(df_filtered):,}** / {len(df_raw):,}")
        st.caption(f"🗂 Columns: **{len(df_raw.columns)}**")
        missing = df_raw.isnull().sum().sum()
        st.caption(f"⚠ Missing Values: **{missing:,}**")
        detected = [f"{k}: `{v}`" for k, v in col_map.items()]
        with st.expander("Detected Columns"):
            for d in detected:
                st.caption(d)

    # ── KPI CALCULATIONS ─────────────────────
    n_total = max(len(df_filtered), 1)

    if amt_col and "_is_refund" in df_filtered.columns:
        _pos_df = df_filtered[df_filtered[amt_col].notna() & (df_filtered[amt_col] > 0)]
    elif amt_col:
        _pos_df = df_filtered[df_filtered[amt_col].notna() & (df_filtered[amt_col] > 0)]
    else:
        _pos_df = df_filtered

    total_spend    = _pos_df[amt_col].sum()    if amt_col else 0
    median_expense = _pos_df[amt_col].median() if amt_col and len(_pos_df) > 0 else 0
    mean_expense   = _pos_df[amt_col].mean()   if amt_col and len(_pos_df) > 0 else 0

    refund_count = 0
    refund_amt   = 0.0
    if "_is_refund" in df_filtered.columns and amt_col:
        _ref_df      = df_filtered[df_filtered["_is_refund"] == True]
        refund_count = len(_ref_df)
        refund_amt   = abs(_ref_df[amt_col].sum())

    fraud_count    = (df_filtered["_risk_level"] == "High").sum() if "_risk_level" in df_filtered.columns else 0
    med_risk_count = (df_filtered["_risk_level"] == "Medium").sum() if "_risk_level" in df_filtered.columns else 0

    # ── UNIFIED DUPLICATE COUNT (all 3 passes combined, de-duped) ─────────────
    all_dup_mask = pd.Series(False, index=df_filtered.index)
    for dup_col in ["_flag_duplicate_txn", "_flag_near_duplicate", "_flag_duplicate_invoice"]:
        if dup_col in df_filtered.columns:
            all_dup_mask = all_dup_mask | df_filtered[dup_col].fillna(False)
    dup_count = int(all_dup_mask.sum())

    # Exact-only for the primary KPI (higher confidence)
    exact_dup_count = int(df_filtered["_flag_duplicate_txn"].sum()) if "_flag_duplicate_txn" in df_filtered.columns else 0
    near_dup_count  = int(df_filtered["_flag_near_duplicate"].sum()) if "_flag_near_duplicate" in df_filtered.columns else 0
    inv_dup_count   = int(df_filtered["_flag_duplicate_invoice"].sum()) if "_flag_duplicate_invoice" in df_filtered.columns else 0

    vendor_count = df_filtered[vend_col].nunique() if vend_col else 0
    missing_rec  = int(df_filtered["_flag_missing_receipt"].sum()) if "_flag_missing_receipt" in df_filtered.columns else 0
    high_risk_v  = 0
    if vend_col and "_risk_level" in df_filtered.columns:
        high_risk_v = df_filtered[df_filtered["_risk_level"]=="High"][vend_col].nunique()

    dup_pct_c   = dup_count   / n_total * 100
    rec_pct_c   = missing_rec / n_total * 100
    fraud_pct_c = fraud_count / n_total * 100
    compliance  = max(0, min(100, 100 - (dup_pct_c * 1.5) - (rec_pct_c * 0.8) - (fraud_pct_c * 1.2)))

    fraud_pct_label = f"{fraud_count / n_total * 100:.1f}% of transactions"
    dup_sub = f"Exact: {exact_dup_count:,} · Near: {near_dup_count:,} · Inv ID: {inv_dup_count:,}"
    rec_pct_label   = f"{missing_rec / n_total * 100:.1f}% without proof"

    # ═══════════════════════════════════════════
    #  TAB: EXECUTIVE DASHBOARD
    # ═══════════════════════════════════════════
    if "Dashboard" in nav:
        section("▤", "Executive Summary")

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(kpi_card("Gross Spend (Excl. Refunds)", f"${total_spend:,.0f}", f"{len(_pos_df):,} positive transactions", "$", "#3b82f6"), unsafe_allow_html=True)
        with c2: st.markdown(kpi_card("Median Expense", f"${median_expense:,.2f}", f"Mean: ${mean_expense:,.2f} — skew indicator", "〽", "#10b981"), unsafe_allow_html=True)
        with c3: st.markdown(kpi_card("High-Risk Transactions", f"{fraud_count:,}", fraud_pct_label, "⚠", "#ef4444"), unsafe_allow_html=True)
        with c4: st.markdown(kpi_card("Duplicate Transactions", f"{dup_count:,}", dup_sub, "↳↰", "#f59e0b"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        comp_color = "#10b981" if compliance >= 80 else ("#f59e0b" if compliance >= 60 else "#ef4444")
        with c5: st.markdown(kpi_card("Compliance Score", f"{compliance:.0f}%", f"Dup {dup_pct_c:.1f}% · Missing Rec {rec_pct_c:.1f}% · Risk {fraud_pct_c:.1f}%", "✓", comp_color), unsafe_allow_html=True)
        with c6: st.markdown(kpi_card("High-Risk Vendors", f"{high_risk_v:,}", f"of {vendor_count:,} total vendors", "⚠︎", "#f59e0b"), unsafe_allow_html=True)
        with c7: st.markdown(kpi_card("Missing Receipts", f"{missing_rec:,}", rec_pct_label, "🗒", "#ef4444" if rec_pct_c > 20 else "#f59e0b"), unsafe_allow_html=True)
        with c8: st.markdown(kpi_card("Refunds / Credits", f"{refund_count:,}", f"${refund_amt:,.0f} credited back", "↩", "#8b5cf6"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns([3, 2])

        with col_a:
            section("〽", "Monthly Spending Trend")
            if date_col and pd.api.types.is_datetime64_any_dtype(df_filtered[date_col]) and amt_col:
                _trend_pos = df_filtered[df_filtered[amt_col] > 0].copy()
                monthly = _trend_pos.groupby(_trend_pos[date_col].dt.to_period("M"))[amt_col].sum().reset_index()
                monthly.columns = ["Month","Spend"]
                monthly["Month"] = monthly["Month"].astype(str)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Spend"],
                    mode="lines+markers", line=dict(color="#3b82f6", width=2.5),
                    marker=dict(size=6, color="#3b82f6"), fill="tozeroy",
                    fillcolor="rgba(59,130,246,0.08)", name="Gross Spend"))
                if "_is_refund" in df_filtered.columns:
                    _trend_ref = df_filtered[df_filtered["_is_refund"] == True].copy()
                    if len(_trend_ref) > 0:
                        monthly_ref = _trend_ref.groupby(_trend_ref[date_col].dt.to_period("M"))[amt_col].apply(lambda x: abs(x.sum())).reset_index()
                        monthly_ref.columns = ["Month","Refunds"]
                        monthly_ref["Month"] = monthly_ref["Month"].astype(str)
                        fig.add_trace(go.Bar(x=monthly_ref["Month"], y=monthly_ref["Refunds"],
                            name="Refunds", marker=dict(color="rgba(239,68,68,0.5)")))
                fig.update_layout(**PLOTLY_LAYOUT, title="Monthly Gross Spend (Excl. Refunds)", height=280)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("🗓 No parseable date column for trend chart.")

        with col_b:
            section("🏠︎", "Department Spend")
            if dept_col and amt_col:
                dept_spend = df_filtered.groupby(dept_col)[amt_col].sum().sort_values(ascending=True).tail(10).reset_index()
                fig2 = go.Figure(go.Bar(
                    x=dept_spend[amt_col], y=dept_spend[dept_col], orientation="h",
                    marker=dict(color="#3b82f6", opacity=0.85),
                    text=dept_spend[amt_col].apply(lambda x: f"${x:,.0f}"),
                    textfont=dict(color="#e2e8f0", size=10), textposition="outside"))
                fig2.update_layout(**PLOTLY_LAYOUT, title="Spend by Department", height=280)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No department column detected.")

        col_c, col_d = st.columns([2, 3])

        with col_c:
            section("⬢", "Category Distribution")
            if cat_col and amt_col:
                cat_spend = df_filtered.groupby(cat_col)[amt_col].sum().sort_values(ascending=False).head(8).reset_index()
                fig3 = go.Figure(go.Pie(
                    labels=cat_spend[cat_col], values=cat_spend[amt_col], hole=0.55,
                    textinfo="label+percent", textfont=dict(size=10, color="#e2e8f0"),
                    marker=dict(colors=["#3b82f6","#10b981","#f59e0b","#8b5cf6","#ef4444","#06b6d4","#ec4899","#84cc16"])))
                fig3.update_layout(**PLOTLY_LAYOUT, title="Spend by Category", height=310, showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No category column detected.")

        with col_d:
            section("𖠿", "Top Vendors by Spend")
            if vend_col and amt_col:
                vend_spend = df_filtered.groupby(vend_col)[amt_col].sum().sort_values(ascending=False).head(10).reset_index()
                fig4 = go.Figure(go.Bar(
                    x=vend_spend[vend_col], y=vend_spend[amt_col],
                    marker=dict(color=vend_spend[amt_col],
                        colorscale=[[0,"#1e3a5f"],[0.5,"#3b82f6"],[1,"#60a5fa"]], showscale=False),
                    text=vend_spend[amt_col].apply(lambda x: f"${x:,.0f}"),
                    textfont=dict(color="#e2e8f0", size=9), textposition="outside"))
                fig4.update_layout(**PLOTLY_LAYOUT, title="Top 10 Vendors", height=310,
                                   xaxis_tickangle=-35)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No vendor column detected.")

        section("𖠿", "Top Transactions")
        display_cols = [c for c in [amt_col, vend_col, dept_col, cat_col, date_col, emp_col] if c and c in df_filtered.columns]
        if display_cols and amt_col:
            top_txns = df_filtered[display_cols].sort_values(amt_col, ascending=False).head(20).copy()
            if date_col in top_txns.columns:
                top_txns[date_col] = top_txns[date_col].astype(str).str[:10]
            if amt_col in top_txns.columns:
                top_txns[amt_col] = top_txns[amt_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
            st.dataframe(top_txns, use_container_width=True, height=320)

        # ── EXECUTIVE RISK SUMMARY ─────────────────────────────────────────────
        section("ᗢ", "Executive Risk Summary")
        risk_items = []

        if compliance >= 80:
            comp_label, comp_cls = " Compliant", "good"
        elif compliance >= 60:
            comp_label, comp_cls = " Moderate Risk", "warn"
        else:
            comp_label, comp_cls = " High Compliance Risk", "danger"

        risk_items.append({
            "title": f"{comp_label} — Score: {compliance:.0f}/100",
            "body": (f"Compliance penalized by: duplicates ({dup_pct_c:.1f}%), "
                     f"missing receipts ({rec_pct_c:.1f}%), high-risk transactions ({fraud_pct_c:.1f}%). "
                     f"{'No immediate remediation required.' if compliance >= 80 else 'Remediation plan recommended before next audit.'}"),
            "type": comp_cls
        })

        if dup_count > 0:
            _dup_exposure = 0
            if amt_col:
                _dup_exposure = df_filtered[all_dup_mask][amt_col].sum()
            risk_items.append({
                "title": f" Duplicate Risk — {dup_count:,} Records ({dup_pct_c:.1f}%)",
                "body": (f"3-pass detection found {exact_dup_count:,} exact duplicates, "
                         f"{near_dup_count:,} near-duplicates (≤7d), "
                         f"and {inv_dup_count:,} invoice ID duplicates. "
                         f"Maximum exposure: ${_dup_exposure:,.2f}. Assign to AP team immediately."),
                "type": "danger" if dup_pct_c > 3 else "warn"
            })

        if vend_col and amt_col and total_spend > 0:
            _vc = _pos_df.groupby(vend_col)[amt_col].sum().sort_values(ascending=False)
            if len(_vc) > 0:
                top_v_pct = _vc.iloc[0] / total_spend * 100
                n_vendors_80 = max(1, int((_vc.cumsum() / total_spend < 0.80).sum()) + 1)
                risk_items.append({
                    "title": f" Vendor Concentration — Top: {_vc.index[0]} ({top_v_pct:.1f}%)",
                    "body": (f"{n_vendors_80} vendor(s) account for 80% of total spend. "
                             f"{'Critical — single point of failure risk.' if top_v_pct > 30 else 'Moderate — monitor quarterly.'} "
                             f"Total vendor base: {vendor_count:,} suppliers."),
                    "type": "danger" if top_v_pct > 30 else "warn"
                })

        if refund_count > 0 and n_total > 0:
            refund_pct_r = refund_count / n_total * 100
            risk_items.append({
                "title": f"↩ Refund Activity — {refund_count:,} Credits ({refund_pct_r:.1f}%)",
                "body": (f"${refund_amt:,.2f} in refunds/credits detected. "
                         f"{'Elevated refund rate may indicate vendor disputes or processing errors.' if refund_pct_r > 5 else 'Refund rate within normal range — continue monitoring.'} "
                         f"Cross-reference against original invoices."),
                "type": "danger" if refund_pct_r > 10 else ("warn" if refund_pct_r > 5 else "good")
            })

        if missing_rec > 0:
            risk_items.append({
                "title": f" Receipt Gap — {missing_rec:,} Transactions ({rec_pct_c:.1f}%)",
                "body": (f"{missing_rec:,} expense transactions lack receipt documentation. "
                         f"{'High exposure — auditor will flag these.' if rec_pct_c > 25 else 'Moderate gap — implement automated receipt reminders.'} "
                         f"Policy threshold typically ≤10%."),
                "type": "danger" if rec_pct_c > 25 else "warn"
            })

        if dept_col and "_risk_level" in df_filtered.columns and amt_col:
            _dept_risk = df_filtered[df_filtered["_risk_level"] == "High"].groupby(dept_col).size().sort_values(ascending=False)
            if len(_dept_risk) > 0:
                top_risk_dept = _dept_risk.index[0]
                top_risk_cnt  = int(_dept_risk.iloc[0])
                dept_total    = max(df_filtered[df_filtered[dept_col] == top_risk_dept].shape[0], 1)
                risk_items.append({
                    "title": f" Highest Risk Dept: {top_risk_dept}",
                    "body": (f"{top_risk_dept} has {top_risk_cnt:,} high-risk transactions "
                             f"({top_risk_cnt / dept_total * 100:.1f}% of its own transactions flagged). "
                             f"Recommend department-level expense policy review."),
                    "type": "warn"
                })

        _ri_cols = st.columns(2)
        for i, ri in enumerate(risk_items):
            with _ri_cols[i % 2]:
                st.markdown(f"""
                <div class="insight-card {ri['type']}">
                    <div class="insight-title">{ri['title']}</div>
                    <div class="insight-body">{ri['body']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB: FRAUD ANALYSIS
    # ═══════════════════════════════════════════
    elif "Fraud" in nav:
        section("🔎︎", "Fraud & Risk Analysis")

        c1, c2, c3, c4 = st.columns(4)
        high_r  = (df_filtered["_risk_level"] == "High").sum() if "_risk_level" in df_filtered.columns else 0
        med_r   = (df_filtered["_risk_level"] == "Medium").sum() if "_risk_level" in df_filtered.columns else 0
        low_r   = (df_filtered["_risk_level"] == "Low").sum() if "_risk_level" in df_filtered.columns else 0
        _fn = max(len(df_filtered), 1)

        with c1: st.markdown(kpi_card("High Risk", f"{high_r:,}", f"{high_r/_fn*100:.1f}% of filtered", "🔴", "#ef4444"), unsafe_allow_html=True)
        with c2: st.markdown(kpi_card("Medium Risk", f"{med_r:,}", f"{med_r/_fn*100:.1f}% — review patterns", "🟡", "#f59e0b"), unsafe_allow_html=True)
        with c3: st.markdown(kpi_card("Low / Clear", f"{low_r:,}", f"{low_r/_fn*100:.1f}% pass all checks", "🟢", "#10b981"), unsafe_allow_html=True)
        with c4: st.markdown(kpi_card("All Duplicates", f"{dup_count:,}", dup_sub, "🔁", "#8b5cf6"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            section("↗", "Fraud Score Distribution")
            if "_fraud_score" in df_filtered.columns:
                fig = go.Figure(go.Histogram(
                    x=df_filtered["_fraud_score"], nbinsx=30,
                    marker=dict(color=df_filtered["_fraud_score"],
                        colorscale=[[0,"#10b981"],[0.4,"#f59e0b"],[1,"#ef4444"]],
                        showscale=True, colorbar=dict(title="Score", tickfont=dict(color="#94a3b8")))))
                fig.update_layout(**PLOTLY_LAYOUT, title="Distribution of Fraud Scores", height=280)
                st.plotly_chart(fig, use_container_width=True)

        with col_b:
            section("𖣠", "Risk Level Breakdown")
            if "_risk_level" in df_filtered.columns:
                risk_counts = df_filtered["_risk_level"].value_counts().reset_index()
                risk_counts.columns = ["Risk Level","Count"]
                colors = {"High":"#ef4444","Medium":"#f59e0b","Low":"#10b981"}
                fig2 = go.Figure(go.Bar(
                    x=risk_counts["Risk Level"], y=risk_counts["Count"],
                    marker=dict(color=[colors.get(r,"#3b82f6") for r in risk_counts["Risk Level"]]),
                    text=risk_counts["Count"], textposition="outside", textfont=dict(color="#e2e8f0")))
                fig2.update_layout(**PLOTLY_LAYOUT, title="Transactions by Risk Level", height=280)
                st.plotly_chart(fig2, use_container_width=True)

        if dept_col and "_risk_level" in df_filtered.columns:
            section("🌡", "Department Risk Heatmap")
            heat = df_filtered.groupby([dept_col, "_risk_level"]).size().reset_index(name="Count")
            pivot = heat.pivot(index=dept_col, columns="_risk_level", values="Count").fillna(0)
            for col in ["High","Medium","Low"]:
                if col not in pivot.columns: pivot[col] = 0
            pivot = pivot[["High","Medium","Low"]]
            fig3 = go.Figure(go.Heatmap(
                z=pivot.values, x=["High","Medium","Low"], y=pivot.index.tolist(),
                colorscale=[[0,"#0d1221"],[0.5,"#3b82f6"],[1,"#ef4444"]],
                text=pivot.values.astype(int), texttemplate="%{text}",
                textfont=dict(color="#e2e8f0", size=10)))
            fig3.update_layout(**PLOTLY_LAYOUT, title="Risk Transactions by Department", height=350)
            st.plotly_chart(fig3, use_container_width=True)

        # ── Duplicate Detail — All 3 Passes ───────────────────────────────────
        section("⿻", "Duplicate Detection Detail (3-Pass)")

        tab1, tab2, tab3 = st.tabs([
            f"Exact Duplicates ({exact_dup_count:,})",
            f"Near-Duplicates ≤7d ({near_dup_count:,})",
            f"Invoice ID Dups ({inv_dup_count:,})"
        ])

        with tab1:
            if "_flag_duplicate_txn" in df_filtered.columns:
                _exact = df_filtered[df_filtered["_flag_duplicate_txn"] == True].copy()
                if len(_exact) > 0:
                    _cols = [c for c in [amt_col, vend_col, dept_col, date_col, emp_col, "_dup_of"] if c and c in _exact.columns]
                    if amt_col in _exact.columns:
                        _exact_disp = _exact[_cols].copy()
                        _exact_disp[amt_col] = _exact_disp[amt_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
                    else:
                        _exact_disp = _exact[_cols]
                    if date_col and date_col in _exact_disp.columns:
                        _exact_disp[date_col] = _exact_disp[date_col].astype(str).str[:10]
                    st.markdown(f"""<div class="alert alert-warn">⚠ {len(_exact):,} exact duplicate transactions (same vendor + amount + date). Double-payment exposure: ${_exact[amt_col].sum() if amt_col else 0:,.2f}</div>""", unsafe_allow_html=True)
                    st.dataframe(_exact_disp.head(60), use_container_width=True, height=300)
                else:
                    st.success("✔ No exact duplicate transactions detected.")
            else:
                st.info("Exact duplicate detection requires vendor and amount columns.")

        with tab2:
            if "_flag_near_duplicate" in df_filtered.columns:
                _near = df_filtered[df_filtered["_flag_near_duplicate"] == True].copy()
                if len(_near) > 0:
                    _cols = [c for c in [amt_col, vend_col, dept_col, date_col, emp_col, "_dup_delta_days"] if c and c in _near.columns]
                    _near_disp = _near[_cols].copy()
                    if amt_col in _near_disp.columns:
                        _near_disp[amt_col] = _near_disp[amt_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
                    if date_col and date_col in _near_disp.columns:
                        _near_disp[date_col] = _near_disp[date_col].astype(str).str[:10]
                    st.markdown(f"""<div class="alert alert-warn">🔎︎ {len(_near):,} near-duplicate transactions (same vendor/amount, dates ≤7 days apart). Set to 'under_review' per notebook policy.</div>""", unsafe_allow_html=True)
                    st.dataframe(_near_disp.head(60), use_container_width=True, height=300)
                else:
                    st.success("✔ No near-duplicate transactions detected.")
            else:
                st.info("Near-duplicate detection requires vendor, amount, and date columns.")

        with tab3:
            inv_key_col = "_inv_key" if "_inv_key" in df_filtered.columns else None
            if inv_key_col and "_flag_duplicate_invoice" in df_filtered.columns:
                _inv_dups = df_filtered[df_filtered["_flag_duplicate_invoice"] == True].copy()
                if len(_inv_dups) > 0:
                    _cols = [c for c in [inv_col, inv_key_col, amt_col, vend_col, dept_col, date_col] if c and c in _inv_dups.columns]
                    _inv_disp = _inv_dups[list(dict.fromkeys(_cols))].copy()
                    if amt_col in _inv_disp.columns:
                        _inv_disp[amt_col] = _inv_disp[amt_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
                    if date_col and date_col in _inv_disp.columns:
                        _inv_disp[date_col] = _inv_disp[date_col].astype(str).str[:10]
                    st.markdown(f"""<div class="alert alert-warn">⚠ {len(_inv_dups):,} invoice ID duplicates (normalized: INV-001 = INV001 = inv 001).</div>""", unsafe_allow_html=True)
                    st.dataframe(_inv_disp.sort_values(inv_key_col).head(60), use_container_width=True, height=300)
                else:
                    st.success("✔ No duplicate invoice IDs detected.")
            else:
                st.info("No invoice ID column detected — invoice ID duplicate check skipped.")

        section("(ᵕ⚆_⚆).ᐟ.ᐟ", "High Risk Transactions")
        if "_risk_level" in df_filtered.columns:
            high_risk_df = df_filtered[df_filtered["_risk_level"] == "High"].copy()
            flag_cols    = [c for c in df_filtered.columns if c.startswith("_flag_")]
            show_cols    = [c for c in [amt_col, vend_col, dept_col, cat_col, date_col, "_fraud_score","_risk_level","_risk_reasons"] if c and c in high_risk_df.columns]
            show_cols   += flag_cols
            if len(high_risk_df) > 0:
                display_df = high_risk_df[show_cols].sort_values("_fraud_score", ascending=False).head(50).copy()
                if amt_col in display_df.columns:
                    display_df[amt_col] = display_df[amt_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "—")
                if date_col in display_df.columns:
                    display_df[date_col] = display_df[date_col].astype(str).str[:10]
                st.dataframe(display_df, use_container_width=True, height=350)
            else:
                st.success("✔ No high-risk transactions in current filter.")

        section("⎙", "Export Fraud Report")
        if "_risk_level" in df_filtered.columns:
            csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button("🡻 Download Fraud Analysis Report (CSV)", data=csv_bytes,
                file_name=f"finsight_fraud_report_{datetime.date.today()}.csv", mime="text/csv")

    # ═══════════════════════════════════════════
    #  TAB: BUSINESS INSIGHTS
    # ═══════════════════════════════════════════
    elif "Insights" in nav:
        section("𖡊", "Business Insights & Observations")
        insights = generate_insights(df_filtered, col_map)
        cols = st.columns(2)
        for i, ins in enumerate(insights):
            with cols[i % 2]:
                cls = ins.get("type","good")
                st.markdown(f"""
                <div class="insight-card {cls}">
                    <div class="insight-title">{ins['title']}</div>
                    <div class="insight-body">{ins['body']}</div>
                </div>
                """, unsafe_allow_html=True)

        if date_col and pd.api.types.is_datetime64_any_dtype(df_filtered[date_col]) and amt_col:
            section("𝄜", "Quarterly Spend Analysis")
            df_filtered_q = df_filtered.copy()
            df_filtered_q["_quarter"] = df_filtered_q[date_col].dt.to_period("Q").astype(str)
            q_spend = df_filtered_q.groupby("_quarter")[amt_col].sum().reset_index()
            q_spend.columns = ["Quarter","Spend"]
            fig = go.Figure(go.Bar(x=q_spend["Quarter"], y=q_spend["Spend"],
                marker=dict(color="#3b82f6", opacity=0.85),
                text=q_spend["Spend"].apply(lambda x: f"${x:,.0f}"),
                textposition="outside", textfont=dict(color="#e2e8f0", size=10)))
            fig.update_layout(**PLOTLY_LAYOUT, title="Quarterly Expense Totals", height=280)
            st.plotly_chart(fig, use_container_width=True)

        if vend_col and amt_col:
            section("◯", "Vendor Spend vs Transaction Count")
            scatter_df = df_filtered.groupby(vend_col)[amt_col].agg(["sum","count","mean"]).reset_index()
            scatter_df.columns = [vend_col, "Total Spend","Transactions","Avg Spend"]
            fig2 = go.Figure(go.Scatter(
                x=scatter_df["Transactions"], y=scatter_df["Total Spend"], mode="markers+text",
                marker=dict(size=scatter_df["Avg Spend"].clip(5,80) / scatter_df["Avg Spend"].max() * 40 + 5,
                    color=scatter_df["Total Spend"], colorscale=[[0,"#1e3a5f"],[1,"#3b82f6"]],
                    opacity=0.7, showscale=True, colorbar=dict(title="Spend", tickfont=dict(color="#94a3b8"))),
                text=scatter_df[vend_col].str[:15],
                textfont=dict(size=8, color="#94a3b8"), textposition="top center",
                hovertemplate="<b>%{text}</b><br>Txns: %{x}<br>Total: $%{y:,.0f}<extra></extra>"))
            fig2.update_layout(**PLOTLY_LAYOUT, title="Vendor Bubble Chart: Spend vs Frequency", height=360,
                               xaxis_title="Transaction Count", yaxis_title="Total Spend ($)")
            st.plotly_chart(fig2, use_container_width=True)

        if emp_col and amt_col:
            section("☻", "Top Employee Spending")
            emp_spend = df_filtered[df_filtered[amt_col] > 0].groupby(emp_col)[amt_col].sum().sort_values(ascending=False).head(15).reset_index()
            fig3 = go.Figure(go.Bar(x=emp_spend[amt_col], y=emp_spend[emp_col], orientation="h",
                marker=dict(color="#8b5cf6", opacity=0.85),
                text=emp_spend[amt_col].apply(lambda x: f"${x:,.0f}"),
                textfont=dict(color="#e2e8f0", size=10), textposition="outside"))
            fig3.update_layout(**PLOTLY_LAYOUT, title="Top 15 Employees by Expense", height=350)
            st.plotly_chart(fig3, use_container_width=True)

    # ═══════════════════════════════════════════
    #  TAB: ASK YOUR DATA
    # ═══════════════════════════════════════════
    elif "Ask" in nav:
        section("𖠌", "Ask Your Data")
        st.markdown('<div style="color:#94a3b8;font-size:0.85rem;margin-bottom:1rem;">Ask plain-English questions about your expense dataset.</div>', unsafe_allow_html=True)

        suggestions = [
            "highest spending vendors","top departments by spend","largest transactions",
            "duplicate invoices","suspicious expenses","missing receipts",
            "travel expenses","monthly trend","category breakdown",
            "employee spending","refund transactions","weekend expenses",
        ]

        st.markdown("**💬 Try asking:**")
        cols = st.columns(4)
        for i, s in enumerate(suggestions):
            with cols[i % 4]:
                if st.button(s, key=f"sug_{i}", use_container_width=True):
                    st.session_state["nlp_query"] = s

        question = st.text_input("Your question:", value=st.session_state.get("nlp_query", ""),
            placeholder="e.g. 'show me duplicate invoices' or 'highest spending vendors'")

        if question:
            with st.spinner(" Analyzing..."):
                result_type, result_df, summary, x_col, y_col = nlp_query(question, df_filtered, col_map)

            st.markdown('<div class="query-result">', unsafe_allow_html=True)
            st.markdown(f"**Query:** _{question}_")
            st.markdown(summary)

            if result_df is not None and len(result_df) > 0:
                if result_type in ("table+chart",) and x_col and y_col and x_col in result_df.columns and y_col in result_df.columns:
                    fig = go.Figure(go.Bar(x=result_df[x_col], y=result_df[y_col],
                        marker=dict(color="#3b82f6", opacity=0.85),
                        text=result_df[y_col].apply(lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else str(x)),
                        textposition="outside", textfont=dict(color="#e2e8f0", size=10)))
                    fig.update_layout(**PLOTLY_LAYOUT, height=280, xaxis_tickangle=-30)
                    st.plotly_chart(fig, use_container_width=True)

                st.dataframe(result_df, use_container_width=True, height=300)
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download Result", csv, "query_result.csv", "text/csv")

            st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB: DATA EXPLORER
    # ═══════════════════════════════════════════
    elif "Explorer" in nav:
        section("🗒", "Data Explorer")

        st.markdown(f"""
        <div style="display:flex;gap:1rem;margin-bottom:1rem;">
            <div class="metric-card" style="flex:1;text-align:center;"><div class="metric-label">Rows</div><div class="metric-value">{len(df_filtered):,}</div></div>
            <div class="metric-card" style="flex:1;text-align:center;"><div class="metric-label">Columns</div><div class="metric-value">{len(df_filtered.columns)}</div></div>
            <div class="metric-card" style="flex:1;text-align:center;"><div class="metric-label">Missing Values</div><div class="metric-value">{df_filtered.isnull().sum().sum():,}</div></div>
            <div class="metric-card" style="flex:1;text-align:center;"><div class="metric-label">File</div><div class="metric-value" style="font-size:0.9rem;">{uploaded_file.name}</div></div>
        </div>
        """, unsafe_allow_html=True)

        section("⌘", "Column Summary Statistics")
        num_cols = [c for c in df_filtered.select_dtypes(include=[np.number]).columns if not c.startswith("_")]
        if num_cols:
            stats = df_filtered[num_cols].describe().T.reset_index()
            stats.columns = [str(c) for c in stats.columns]
            st.dataframe(stats.round(2), use_container_width=True)

        section("👁", "Data Preview")
        preview_rows = st.slider("Rows to display", 10, min(500, len(df_filtered)), 50)
        display_cols = [c for c in df_filtered.columns if not c.startswith("_flag_")]
        st.dataframe(df_filtered[display_cols].head(preview_rows), use_container_width=True, height=400)

        section("⚠︎", "Missing Value Analysis")
        miss = df_filtered[[c for c in df_filtered.columns if not c.startswith("_")]].isnull().sum().reset_index()
        miss.columns = ["Column","Missing Count"]
        miss["Missing %"] = (miss["Missing Count"] / len(df_filtered) * 100).round(1)
        miss = miss[miss["Missing Count"] > 0].sort_values("Missing Count", ascending=False)
        if len(miss) > 0:
            fig = go.Figure(go.Bar(x=miss["Column"], y=miss["Missing %"],
                marker=dict(color="#ef4444", opacity=0.8),
                text=miss["Missing %"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside", textfont=dict(color="#e2e8f0")))
            fig.update_layout(**PLOTLY_LAYOUT, title="Missing Values by Column (%)", height=280)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✔ No missing values in current filtered dataset.")

        section("⎙", "Export")
        c1, c2 = st.columns(2)
        with c1:
            csv_all = df_filtered[[c for c in df_filtered.columns if not c.startswith("_flag_")]].to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download Filtered Dataset (CSV)", csv_all,
                f"finsight_filtered_{datetime.date.today()}.csv", "text/csv", use_container_width=True)
        with c2:
            full_csv = df_fraud.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download Full Dataset with Scores (CSV)", full_csv,
                f"finsight_full_{datetime.date.today()}.csv", "text/csv", use_container_width=True)

    st.markdown("""
    <hr style="border:none;border-top:1px solid #1e2d45;margin-top:3rem;">
    <div style="text-align:center;color:#334155;font-size:0.72rem;padding:0.5rem;">
        🌿 FinSight ERP — Financial Audit & Expense Intelligence Platform &nbsp;|&nbsp;
        Built with Streamlit · Pandas · Plotly · NumPy
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()