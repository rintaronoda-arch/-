import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io

# âââ Altair ãã¼ã¯ãã¼ã ãã«ãã¼ âââ
def _dk(chart):
    """Altairãã£ã¼ãã«ãã¼ã¯ã¢ã¼ãè¨­å®ãé©ç¨"""
    return chart.configure(
        background="transparent",
        axis=alt.AxisConfig(
            labelColor="#8899bb", titleColor="#c8d8f0",
            gridColor="#1c2b44", domainColor="#3a4a6a",
            tickColor="#3a4a6a",
        ),
        legend=alt.LegendConfig(
            labelColor="#8899bb", titleColor="#c8d8f0",
            fillColor="#0d1526", strokeColor="#1c2b44",
        ),
        view=alt.ViewConfig(stroke="transparent"),
        title=alt.TitleConfig(color="#c8d8f0"),
    )

# âââââââââââââââââââââââââââââââââââââââââââââ
# PAGE CONFIG
# âââââââââââââââââââââââââââââââââââââââââââââ
st.set_page_config(
    page_title="Biz Maker â ãã¸ãã¹å±åµãã©ãããã©ã¼ã ",
    layout="wide",
    page_icon="ð",
    initial_sidebar_state="collapsed",
)

# âââââââââââââââââââââââââââââââââââââââââââââ
# GLOBAL CSS â Dark Mode (Plan A: Deep Navy Ã Amber)
# âââââââââââââââââââââââââââââââââââââââââââââ
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family:'Inter',sans-serif !important; }
#MainMenu, header, footer { visibility:hidden; }

/* ââ Global Dark Background ââ */
.main .block-container { padding:1.2rem 2rem 2rem; background:#0b1220; }
body, .stApp { background:#0b1220 !important; }
section[data-testid="stSidebar"] { background:#0d1526 !important; }

/* ââ ãããã¼ ââ */
.top-nav { display:flex; align-items:center; justify-content:space-between; padding:0.6rem 0; margin-bottom:1rem; border-bottom:1px solid #1c2b44; }
.top-nav .logo { font-size:2.0rem; font-weight:800; color:#fff; letter-spacing:-0.5px; }
.top-nav .logo span { color:#f5a623; }
.top-nav .tagline { font-size:0.85rem; color:#3a4a6a; margin-top:2px; }
.nav-badge { background:#1c2b44; color:#f5a623; border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:700; border:1px solid rgba(245,166,35,.35); }

/* ââ KPIã«ã¼ã ââ */
.kpi-grid { display:flex; gap:12px; flex-wrap:wrap; margin:1rem 0; }
.kpi-card { flex:1; min-width:140px; background:#0d1526; border:1px solid #1c2b44; border-radius:12px; padding:14px 16px; }
.kpi-card .label { font-size:0.72rem; color:#3a4a6a; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; }
.kpi-card .value { font-size:1.35rem; font-weight:700; color:#fff; margin:4px 0 2px; line-height:1.2; }
.kpi-card .delta { font-size:0.75rem; }
.kpi-card .delta.up   { color:#34d297; }
.kpi-card .delta.down { color:#f87171; }
.kpi-card .delta.neutral { color:#3a4a6a; }
.kpi-card.accent  { border-left:3px solid #f5a623; }
.kpi-card.success { border-left:3px solid #34d297; }
.kpi-card.danger  { border-left:3px solid #f87171; }
.kpi-card.warn    { border-left:3px solid #f5a623; }

/* ââ ã»ã¯ã·ã§ã³ã¿ã¤ãã« ââ */
.section-title { font-size:0.8rem; font-weight:700; color:#f5a623; text-transform:uppercase; letter-spacing:1px; margin:1.4rem 0 0.6rem; padding-bottom:6px; border-bottom:1px solid #1c2b44; }

/* ââ æ¹åææ¡ã«ã¼ã ââ */
.advice-card { background:#0d1526; border:1px solid #1c2b44; border-radius:10px; padding:14px 16px; margin:6px 0; }
.advice-card .advice-title { font-size:0.8rem; font-weight:600; color:#6a7a9a; margin-bottom:4px; }
.advice-card .advice-value { font-size:1.05rem; font-weight:700; color:#fff; }
.advice-card .advice-desc { font-size:0.75rem; color:#3a4a6a; margin-top:3px; }

/* ââ ã¹ããããã¼ ââ */
.step-bar { display:flex; gap:0; margin:0.8rem 0 1.2rem; }
.step-item { flex:1; text-align:center; padding:8px 4px; font-size:0.72rem; font-weight:500; border-bottom:3px solid #1c2b44; color:#3a4a6a; }
.step-item.active { border-bottom:3px solid #f5a623; color:#f5a623; font-weight:700; }
.step-item.done   { border-bottom:3px solid #34d297; color:#34d297; }

/* ââ ãã¡ãã«ãã¸ã¥ã¢ã« ââ */
.funnel-total { background:#0d1526; border:1px solid #f5a623; border-radius:12px; padding:16px 20px; margin:10px 0; }
.funnel-total-title { font-size:0.75rem; font-weight:700; color:#f5a623; margin-bottom:12px; letter-spacing:1px; }
.funnel-row { display:flex; align-items:center; gap:0; }
.funnel-step { flex:1; text-align:center; }
.funnel-num  { font-size:1.3rem; font-weight:800; font-family:monospace; }
.funnel-lbl  { font-size:0.65rem; color:#3a4a6a; margin-top:2px; }
.funnel-rate { font-size:0.68rem; font-weight:600; margin-top:2px; }
.funnel-arr  { color:#253d5c; font-size:1.1rem; padding:0 6px; flex-shrink:0; }

/* ââ ãã£ãã«ãã¡ãã«ï¼åãã£ãã«ï¼ ââ */
.ch-funnel { display:flex; align-items:center; background:#111e32; border:1px solid #1c2b44; border-radius:8px; padding:10px 14px; margin:6px 0; font-family:monospace; gap:0; }
.ch-funnel .cf-step { flex:1; text-align:center; }
.ch-funnel .cf-num { font-size:0.95rem; font-weight:700; }
.ch-funnel .cf-lbl { font-size:0.6rem; color:#3a4a6a; margin-top:1px; }
.ch-funnel .cf-sub { font-size:0.6rem; color:#4a5a7a; margin-top:1px; }
.ch-funnel .cf-arr { color:#1c2b44; padding:0 5px; flex-shrink:0; }

/* ââ AIãã£ãã ââ */
.ai-bubble { background:linear-gradient(135deg,#1c2b44,#162236); color:#c8d8f0; border-radius:0 14px 14px 14px; padding:14px 18px; margin:8px 0 8px 8px; font-size:0.88rem; line-height:1.65; border:1px solid rgba(245,166,35,.15); max-width:85%; }
.ai-label { font-size:0.7rem; font-weight:700; color:#f5a623; margin-bottom:6px; letter-spacing:0.5px; }
.user-bubble { background:#131e32; color:#c8d8f0; border-radius:14px 0 14px 14px; padding:12px 16px; margin:8px 8px 8px auto; font-size:0.87rem; max-width:75%; text-align:right; float:right; clear:both; border:1px solid #1c2b44; }
.chat-wrap { overflow:hidden; }

/* ââ ã³ã³ãµã«ã«ã¼ã ââ */
.consultant-card { background:#0d1526; border:1px solid #1c2b44; border-radius:14px; padding:20px; margin:10px 0; transition:all 0.2s; }
.consultant-card:hover { border-color:rgba(245,166,35,.5); box-shadow:0 0 20px rgba(245,166,35,.08); }
.cons-name { font-size:1.0rem; font-weight:700; color:#fff; }
.cons-field { font-size:0.75rem; color:#f5a623; font-weight:600; background:rgba(245,166,35,.1); padding:2px 8px; border-radius:20px; border:1px solid rgba(245,166,35,.2); }
.cons-desc { font-size:0.82rem; color:#5a6a8a; margin:8px 0; line-height:1.5; }
.cons-meta { font-size:0.78rem; color:#3a4a6a; }
.cons-badge { background:rgba(52,210,151,.1); color:#34d297; border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; border:1px solid rgba(52,210,151,.2); display:inline-block; margin:4px 0; }

/* ââ SNSæç¨¿ã«ã¼ã ââ */
.post-card { background:#0d1526; border:1px solid #1c2b44; border-radius:12px; padding:16px; margin:10px 0; }
.post-header { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.post-avatar { width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg,#1c2b44,#f5a623); display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.85rem; font-weight:700; }
.post-meta .name { font-weight:600; font-size:0.88rem; color:#fff; }
.post-meta .sub { font-size:0.72rem; color:#3a4a6a; }
.post-content { font-size:0.85rem; color:#6a7a9a; line-height:1.65; }
.post-actions { display:flex; gap:20px; margin-top:12px; padding-top:10px; border-top:1px solid #1c2b44; }
.post-action { font-size:0.78rem; color:#3a4a6a; cursor:pointer; font-weight:500; }
.tag { background:rgba(245,166,35,.1); color:#f5a623; border:1px solid rgba(245,166,35,.2); border-radius:4px; padding:1px 6px; font-size:0.7rem; font-weight:600; display:inline-block; margin:2px; }

/* ââ Coming Soonããã¸ ââ */
.cs-banner { background:rgba(245,166,35,.06); border:1px solid rgba(245,166,35,.2); border-radius:10px; padding:10px 16px; margin-bottom:16px; font-size:0.82rem; color:#6a7a9a; font-weight:500; }

/* ââ Metric override ââ */
div[data-testid="stMetric"] { background:#0d1526 !important; border-radius:10px; padding:12px 14px; border:1px solid #1c2b44 !important; }
div[data-testid="stMetric"] label { color:#3a4a6a !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color:#fff !important; }

/* ââ Button ââ */
div[data-testid="stButton"] > button { border-radius:8px !important; font-weight:600 !important; font-size:0.85rem !important; padding:6px 14px !important; background:#1c2b44 !important; color:#c8d8f0 !important; border:1px solid #2a3d58 !important; transition:all 0.2s !important; }
div[data-testid="stButton"] > button:hover { background:#253d5c !important; border-color:#f5a623 !important; color:#f5a623 !important; }

/* ââ Tab Orange Pill Style ââ */
div[data-testid="stTabs"] [data-baseweb="tab-list"] { gap:14px; border-bottom:none !important; background:transparent; padding:10px 0; }
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background:linear-gradient(180deg,#F97316 0%,#EA580C 100%); color:#fff !important;
    border-radius:50px; padding:14px 32px; font-weight:700; font-size:0.95rem;
    border:none !important; letter-spacing:0.5px;
    box-shadow:0 4px 14px rgba(234,88,12,0.35), inset 0 1px 0 rgba(255,255,255,0.25);
    transition:all 0.25s ease; cursor:pointer; position:relative; overflow:hidden;
}
div[data-testid="stTabs"] [data-baseweb="tab"]::before { content:""; position:absolute; top:0; left:0; right:0; bottom:0; background:linear-gradient(180deg,rgba(255,255,255,0.12) 0%,transparent 60%); border-radius:50px; pointer-events:none; }
div[data-testid="stTabs"] [data-baseweb="tab"]:hover { background:linear-gradient(180deg,#FB923C 0%,#F97316 100%); box-shadow:0 6px 22px rgba(249,115,22,0.45); transform:translateY(-2px); }
div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] { background:linear-gradient(180deg,#EA580C 0%,#C2410C 100%) !important; box-shadow:0 2px 8px rgba(194,65,12,0.4), inset 0 2px 4px rgba(0,0,0,0.15) !important; transform:translateY(1px); }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] { display:none !important; }
div[data-testid="stTabs"] [data-baseweb="tab"] > div { color:#fff !important; }

/* ââ Input dark override ââ */
div[data-baseweb="input"] > div { background:#111e32 !important; border-color:#1c2b44 !important; }
div[data-baseweb="input"] input { color:#c8d8f0 !important; }
div[data-baseweb="select"] > div { background:#111e32 !important; border-color:#1c2b44 !important; }
div[data-baseweb="select"] span { color:#c8d8f0 !important; }
textarea { background:#111e32 !important; color:#c8d8f0 !important; border-color:#1c2b44 !important; }
div[data-testid="stNumberInput"] input { color:#c8d8f0 !important; }
div[data-testid="stExpander"] { background:#0d1526 !important; border:1px solid #1c2b44 !important; border-radius:10px !important; }
div[data-testid="stExpander"] > details > summary { color:#c8d8f0 !important; }
div[data-testid="stExpander"] > details > summary:hover { color:#f5a623 !important; }
.stCheckbox label span { color:#c8d8f0 !important; }
.stRadio label { color:#c8d8f0 !important; }
div[data-testid="stDataFrame"] { background:#0d1526 !important; }
div[role="listbox"] { background:#111e32 !important; border:1px solid #1c2b44 !important; }

/* ââ Text dark ââ */
h1, h2, h3, h4, h5, h6 { color:#fff !important; }
.stMarkdown p { color:#8899bb; }
.stCaption { color:#4a5a7a !important; }
label[data-testid="stWidgetLabel"] { color:#8899bb !important; }

/* ââ è³éã¢ã©ã¼ã ââ */
.funding-alert { background:rgba(248,113,113,.07); border:1px solid rgba(248,113,113,.3); border-radius:12px; padding:16px 20px; margin:12px 0; }
.funding-alert .fa-title { font-size:0.9rem; font-weight:700; color:#f87171; margin-bottom:4px; }
.funding-alert .fa-body { font-size:0.82rem; color:#8899bb; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# æ¥­ç¨®ãã³ãã¬ã¼ãï¼A4 æ¡å¼µï¼é¸æå¼ã³ã¹ãé ç®ï¼
# âââââââââââââââââââââââââââââââââââââââââââââ
# å¤åè²»ãã¹ã¿ã¼ï¼å¨æ¥­ç¨®å±éã®ã³ã¹ãé ç®ãã¼ã«
VARIABLE_COST_ITEMS = {
    "ä»å¥åä¾¡":       {"key": "vc_cogs",     "unit": "å/ä»¶", "desc": "ååã®ä»å¥ãã»è£½é åä¾¡"},
    "ééæ":         {"key": "vc_shipping",  "unit": "å/ä»¶", "desc": "ééã»ç©æµè²»ç¨"},
    "ãµã¼ãã¼åä¾¡":   {"key": "vc_server",    "unit": "å/ä»¶", "desc": "SaaSã»ã¯ã©ã¦ãã®å¾éèª²é"},
    "æ±ºæ¸ææ°æ":     {"key": "vc_payment",   "unit": "%",     "desc": "ã¯ã¬ã¸ããã«ã¼ãç­ã®æ±ºæ¸ææ°æ"},
    "ã¢ã¼ã«ææ°æ":   {"key": "vc_platform",  "unit": "%",     "desc": "ECã¢ã¼ã«ç­ã®ãã©ãããã©ã¼ã ææ°æ"},
    "å¤æ³¨å å·¥è²»":     {"key": "vc_outsource", "unit": "å/ä»¶", "desc": "å¤é¨ã¸ã®å å·¥ã»å¶ä½å§è¨"},
    "æ¢±åè³æè²»":     {"key": "vc_packaging", "unit": "å/ä»¶", "desc": "æ¢­åæã»ããã±ã¼ã¸è²»ç¨"},
    "ã­ã¤ã¤ã«ãã£":   {"key": "vc_royalty",   "unit": "%",     "desc": "ã©ã¤ã»ã³ã¹ã»ã­ã¤ã¤ã«ãã£è²»ç¨"},
    "è²©å£²ææ°æ":     {"key": "vc_sales_fee", "unit": "%",     "desc": "è²©å£²ä»£çåºã»ã¢ãã£ãªã¨ã¤ãææ°æ"},
    "è¿åã³ã¹ã":     {"key": "vc_returns",   "unit": "å/ä»¶", "desc": "è¿åã»äº¤æã«ä¼´ãè²»ç¨"},
}

FIXED_COST_ITEMS = {
    "çµ¦ä¸åè¨":       {"key": "fc_salary",      "desc": "æ­£ç¤¾å¡ã»ãã¼ãçµ¦ä¸ã®åè¨"},
    "ç¤¾ä¼ä¿éºæ":     {"key": "fc_insurance",    "desc": "å¥åº·ä¿éºã»åçå¹´éç­"},
    "æ¥­åå§è¨è²»":     {"key": "fc_outsourcing",  "desc": "ããªã¼ã©ã³ã¹ã»å¤æ³¨ã¸ã®åºå®æã"},
    "å®¶è³":           {"key": "fc_rent",         "desc": "ãªãã£ã¹ã»åºèã®è³æ"},
    "ã·ã¹ãã å©ç¨æ": {"key": "fc_system",       "desc": "SaaSæé¡ã»ãã¼ã«å©ç¨æ"},
    "ãã®ä»åºå®è²»":   {"key": "fc_misc",         "desc": "éè²»ã»äº¤éè²»ã»éä¿¡è²»ç­"},
    "ãªã¼ã¹æ":       {"key": "fc_lease",        "desc": "è¨­åã»è»ä¸¡ãªã¼ã¹æ"},
    "åºåå®£ä¼è²»ï¼åºå®ï¼": {"key": "fc_ad_fixed", "desc": "ãã©ã³ãã£ã³ã°ã»PRç­ã®åºå®åºåè²»"},
    "ç ç©¶éçºè²»":     {"key": "fc_rd",           "desc": "R&Dã»æ°è¦éçºã®åºå®æè³"},
    "ä¿éºæ":         {"key": "fc_business_ins", "desc": "äºæ¥­ä¿éºã»è³ åä¿éºç­"},
    "æ°´éåç±è²»":     {"key": "fc_utilities",    "desc": "é»æ°ã»ã¬ã¹ã»æ°´éæé"},
    "éä¿¡è²»":         {"key": "fc_telecom",      "desc": "é»è©±ã»ã¤ã³ã¿ã¼ãããåç·è²»"},
    "äº¤éè²»":         {"key": "fc_transport",    "desc": "åºå¼µã»éå¤äº¤éè²»"},
    "é¡§åæ":         {"key": "fc_advisory",     "desc": "ç¨çå£«ã»å¼è­·å£«ç­ã®é¡§åå¥ç´"},
    "æ¡ç¨è²»":         {"key": "fc_recruiting",   "desc": "æ±äººåºåã»äººæç´¹ä»ææ°æ"},
}

INDUSTRY_TEMPLATES = {
    "ã«ã¹ã¿ã ": {
        "unit_price": 5000, "ad_budget": 1_000_000, "cpa": 2000,
        "organic_start": 50, "organic_growth": 5.0, "churn_rate": 5.0,
        "vc_items": {"ä»å¥åä¾¡": 1000, "ééæ": 600, "ãµã¼ãã¼åä¾¡": 50, "æ±ºæ¸ææ°æ": 3.6, "ã¢ã¼ã«ææ°æ": 0.0},
        "fc_items": {"çµ¦ä¸åè¨": 2_500_000, "ç¤¾ä¼ä¿éºæ": 400_000, "æ¥­åå§è¨è²»": 300_000, "å®¶è³": 150_000, "ã·ã¹ãã å©ç¨æ": 50_000, "ãã®ä»åºå®è²»": 100_000},
        "seasonal": [1.0]*12,
    },
    "SaaS / ãµãã¹ã¯": {
        "unit_price": 9800, "ad_budget": 800_000, "cpa": 8000,
        "organic_start": 30, "organic_growth": 8.0, "churn_rate": 3.0,
        "vc_items": {"ãµã¼ãã¼åä¾¡": 200, "æ±ºæ¸ææ°æ": 3.6},
        "fc_items": {"çµ¦ä¸åè¨": 3_000_000, "ç¤¾ä¼ä¿éºæ": 450_000, "æ¥­åå§è¨è²»": 500_000, "å®¶è³": 100_000, "ã·ã¹ãã å©ç¨æ": 150_000, "ãã®ä»åºå®è²»": 100_000},
        "seasonal": [1.0,1.0,1.05,1.0,1.0,1.0,0.95,0.95,1.05,1.05,1.0,0.95],
    },
    "EC / éè²©": {
        "unit_price": 4500, "ad_budget": 1_500_000, "cpa": 2500,
        "organic_start": 100, "organic_growth": 3.0, "churn_rate": 15.0,
        "vc_items": {"ä»å¥åä¾¡": 1800, "ééæ": 800, "ãµã¼ãã¼åä¾¡": 30, "æ±ºæ¸ææ°æ": 3.6, "ã¢ã¼ã«ææ°æ": 8.0, "æ¢±åè³æè²»": 150},
        "fc_items": {"çµ¦ä¸åè¨": 2_000_000, "ç¤¾ä¼ä¿éºæ": 300_000, "æ¥­åå§è¨è²»": 200_000, "å®¶è³": 200_000, "ã·ã¹ãã å©ç¨æ": 80_000, "ãã®ä»åºå®è²»": 120_000},
        "seasonal": [0.8,0.8,1.0,0.9,0.9,1.0,1.1,0.9,0.9,1.0,1.2,1.5],
    },
    "é£²é£åº": {
        "unit_price": 1200, "ad_budget": 300_000, "cpa": 500,
        "organic_start": 200, "organic_growth": 2.0, "churn_rate": 25.0,
        "vc_items": {"ä»å¥åä¾¡": 400, "æ±ºæ¸ææ°æ": 3.6, "æ¢±åè³æè²»": 30},
        "fc_items": {"çµ¦ä¸åè¨": 1_800_000, "ç¤¾ä¼ä¿éºæ": 270_000, "æ¥­åå§è¨è²»": 50_000, "å®¶è³": 300_000, "ã·ã¹ãã å©ç¨æ": 30_000, "ãã®ä»åºå®è²»": 150_000},
        "seasonal": [0.8,0.85,1.0,1.0,1.0,0.9,0.95,0.85,0.95,1.0,1.1,1.5],
    },
    "ã³ã³ãµã«ãã£ã³ã°": {
        "unit_price": 300_000, "ad_budget": 500_000, "cpa": 50_000,
        "organic_start": 5, "organic_growth": 5.0, "churn_rate": 8.0,
        "vc_items": {"æ±ºæ¸ææ°æ": 3.6},
        "fc_items": {"çµ¦ä¸åè¨": 3_500_000, "ç¤¾ä¼ä¿éºæ": 525_000, "æ¥­åå§è¨è²»": 200_000, "å®¶è³": 200_000, "ã·ã¹ãã å©ç¨æ": 50_000, "ãã®ä»åºå®è²»": 100_000},
        "seasonal": [0.7,0.8,1.2,1.1,1.0,1.0,0.9,0.7,1.0,1.1,1.1,1.2],
    },
    "ãã¼ãã¦ã§ã¢": {
        "unit_price": 25_000, "ad_budget": 2_000_000, "cpa": 5000,
        "organic_start": 30, "organic_growth": 3.0, "churn_rate": 0.0,
        "vc_items": {"ä»å¥åä¾¡": 10_000, "ééæ": 1500, "æ±ºæ¸ææ°æ": 3.6, "æ¢±åè³æè²»": 500},
        "fc_items": {"çµ¦ä¸åè¨": 4_000_000, "ç¤¾ä¼ä¿éºæ": 600_000, "æ¥­åå§è¨è²»": 1_000_000, "å®¶è³": 500_000, "ã·ã¹ãã å©ç¨æ": 100_000, "ãã®ä»åºå®è²»": 300_000},
        "seasonal": [0.9,0.8,1.0,1.0,1.0,1.0,1.0,0.9,1.0,1.0,1.1,1.3],
    },
    "è²·ãåãï¼ãµãã¹ã¯": {
        "unit_price": 35_000, "ad_budget": 1_200_000, "cpa": 4000,
        "organic_start": 20, "organic_growth": 4.0, "churn_rate": 5.0,
        "vc_items": {"ä»å¥åä¾¡": 12_000, "ééæ": 1_000, "ãµã¼ãã¼åä¾¡": 100, "æ±ºæ¸ææ°æ": 3.6},
        "fc_items": {"çµ¦ä¸åè¨": 3_000_000, "ç¤¾ä¼ä¿éºæ": 450_000, "æ¥­åå§è¨è²»": 500_000, "å®¶è³": 200_000, "ã·ã¹ãã å©ç¨æ": 100_000, "ãã®ä»åºå®è²»": 150_000},
        "seasonal": [0.9,0.85,1.0,1.0,1.0,1.0,1.0,0.9,1.0,1.05,1.1,1.2],
    },
}

MONTH_LABELS = ["1æ","2æ","3æ","4æ","5æ","6æ","7æ","8æ","9æ","10æ","11æ","12æ"]

# âââ æ¸ä¾¡åå´ã®ç¨®å¥å®ç¾© (A3) âââ
DEPRECIATION_CATEGORIES = {
    "è¨­åã»æ©æ¢°": {"useful_life": 7, "examples": "è£½é æ©æ¢°ãå å·¥è¨­åãå¨æ¿è¨­å"},
    "ITè³ç£": {"useful_life": 4, "examples": "PCããµã¼ãã¼ããããã¯ã¼ã¯æ©å¨"},
    "è»ä¸¡": {"useful_life": 6, "examples": "å¶æ¥­è»ãééãã©ãã¯"},
    "ä¸åç£ï¼å»ºç©ï¼": {"useful_life": 22, "examples": "åºèåè£ããªãã£ã¹åè£"},
    "ã½ããã¦ã§ã¢": {"useful_life": 5, "examples": "èªç¤¾éçºã½ãããã©ã¤ã»ã³ã¹"},
    "ãã®ä»": {"useful_life": 5, "examples": "å·¥å·ãååãä»å¨"},
}

# âââââââââââââââââââââââââââââââââââââââââââââ
# SESSION STATE
# âââââââââââââââââââââââââââââââââââââââââââââ
defaults = {
    "step": 1,
    "industry": "SaaS / ãµãã¹ã¯",
    "revenue_sources": [{"name": "ã¡ã¤ã³åå", "unit_price": 9800, "weight": 100}],
    "hire_plan": [],
    "depreciation_assets": [],
    "acq_mode": "funnel",
    "channels": [
        {"name": "ãªã¹ãã£ã³ã°åºå", "budget": 500_000, "cpm": 600, "ctr": 2.5, "cvr": 2.5},
    ],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# âââââââââââââââââââââââââââââââââââââââââââââ
# TOP NAV
# âââââââââââââââââââââââââââââââââââââââââââââ
st.markdown("""
<div class="top-nav">
  <div>
    <div class="logo">Biz<span>Maker</span></div>
    <div class="tagline">ãã¸ãã¹å±åµãã©ãããã©ã¼ã </div>
  </div>
  <div><span class="nav-badge">v6.0 â Dark Edition</span></div>
</div>
""", unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# MAIN TABS
# âââââââââââââââââââââââââââââââââââââââââââââ
tab_sim, tab_ai, tab_cons, tab_sns = st.tabs([
    " ã·ãã¥ã¬ã¼ã¿ã¼ ", " AI ã¢ããã¤ã¶ã¼ ",
    " å°éå®¶ã«ç¸è« ", " ã³ãã¥ããã£ ",
])


# âââââââââââââââââââââââââââââââââââââââââââââââ
# TAB 1 â ã·ãã¥ã¬ã¼ã¿ã¼
# âââââââââââââââââââââââââââââââââââââââââââââââ
with tab_sim:
    # ââ æ¥­ç¨®ãã³ãã¬ã¼ã & ã·ããªãª ââ
    col_ind, col_sc = st.columns([3, 1])
    with col_ind:
        industry = st.selectbox(
            "æ¥­ç¨®ãã³ãã¬ã¼ã",
            list(INDUSTRY_TEMPLATES.keys()),
            index=list(INDUSTRY_TEMPLATES.keys()).index(st.session_state.industry),
        )
        st.session_state.industry = industry
        tmpl = INDUSTRY_TEMPLATES[industry]
    with col_sc:
        scenario = st.radio("ã·ããªãª", ["ä¸­åº¸", "æ¥½è¦³ +20%", "æ²è¦³ -20%"], horizontal=False)

    # ââ ã¹ããããã¼ (7ã¹ãããã«æ¡å¼µ) ââ
    step_labels = [
        "Step 1 åºæ¬æå ±",
        "Step 2 å£²ä¸è¨­è¨",
        "Step 3 ã³ã¹ãè¨­è¨",
        "Step 4 äººå¡è¨ç»",
        "Step 5 è¨­åæè³",
        "Step 6 è³éç¹°ã",
        "Step 7 ç¨åæ",
    ]
    step_html = '<div class="step-bar">'
    for i, sl in enumerate(step_labels, 1):
        cls = "active" if i == st.session_state.step else ("done" if i < st.session_state.step else "")
        step_html += f'<div class="step-item {cls}">{sl}</div>'
    step_html += "</div>"
    st.markdown(step_html, unsafe_allow_html=True)

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 1 â åºæ¬æå ± (A2 + A5)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 1 â åºæ¬æå ±", expanded=(st.session_state.step == 1)):
        c1, c2, c3 = st.columns(3)
        with c1:
            sim_months = st.selectbox("ã·ãã¥ã¬ã¼ã·ã§ã³æé", [12, 24, 36, 60, 84, 120], index=2)
        with c2:
            target_pct = st.slider("ç®æ¨å¶æ¥­å©çç (%)", 1, 50, 20)
            target_rate = target_pct / 100
        with c3:
            initial_inv = st.number_input("åææè³é¡ (å)", value=5_000_000, step=500_000)

        # A5: å¥åç²åº¦ã®é¸æ
        input_mode = st.radio(
            "å¥åã¢ã¼ã",
            ["ææ¬¡å¥åï¼è©³ç´°ï¼", "å¹´æ¬¡å¥åï¼æ¦ç®ï¼"],
            horizontal=True,
            help="å¹´æ¬¡å¥åãé¸ã¶ã¨ãå£²ä¸ã»ã³ã¹ããå¹´é¡ã§å¥åãèªåã§æå²ãè¨ç®ãã¾ã",
        )
        is_annual_input = input_mode == "å¹´æ¬¡å¥åï¼æ¦ç®ï¼"
        annual_divisor = 12 if is_annual_input else 1
        annual_label = " (å¹´é¡)" if is_annual_input else ""

        _, nb = st.columns([8, 1])
        with nb:
            if st.button("æ¬¡ã¸", key="n1"):
                st.session_state.step = 2; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 2 â å£²ä¸è¨­è¨ (B2: è¤æ°åçæº + IMPROVEMENT 5: å¹´åº¦å¥æé·ç)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 2 â å£²ä¸è¨­è¨ï¼è¤æ°åçæºå¯¾å¿ï¼", expanded=(st.session_state.step == 2)):
        st.caption("åçæºãè¿½å ãã¦ãè¤æ°ã®ãã­ãã¯ãã»ãµã¼ãã¹ã®å£²ä¸ãåå¥ã«ã·ãã¥ã¬ã¼ã·ã§ã³ã§ãã¾ãã")

        # åçæºã®æ°ãç®¡ç
        if "n_revenue" not in st.session_state:
            st.session_state.n_revenue = 1

        rev_sources = []
        for ridx in range(st.session_state.n_revenue):
            with st.container():
                st.markdown(f"**åçæº {ridx+1}**")
                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    rname = st.text_input("åç§°", value=f"åå{ridx+1}" if ridx > 0 else "ã¡ã¤ã³åå", key=f"rname_{ridx}")
                with rc2:
                    rprice = st.number_input(
                        f"å¹³åå®¢åä¾¡{annual_label} (å)", value=tmpl["unit_price"] * annual_divisor,
                        step=500, key=f"rprice_{ridx}"
                    )
                    rprice_monthly = rprice / annual_divisor
                with rc3:
                    rweight = st.slider("å£²ä¸æ§ææ¯ (%)", 1, 100, 100 if ridx == 0 else 20, key=f"rweight_{ridx}")
                with rc4:
                    rchurn = st.slider("æéè§£ç´ç (%)", 0.0, 50.0, tmpl["churn_rate"], 0.5, key=f"rchurn_{ridx}")

                rev_sources.append({
                    "name": rname,
                    "unit_price": rprice_monthly,
                    "weight": rweight / 100,
                    "churn_rate": rchurn / 100,
                })

        rcol1, rcol2 = st.columns(2)
        with rcol1:
            if st.button("ï¼ åçæºãè¿½å ", key="add_rev"):
                st.session_state.n_revenue += 1; st.rerun()
        with rcol2:
            if st.session_state.n_revenue > 1 and st.button("ï¼ æå¾ã®åçæºãåé¤", key="del_rev"):
                st.session_state.n_revenue -= 1; st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-title">éå®¢è¨­è¨</div>', unsafe_allow_html=True)

        # âââ ãã£ãã«ã¿ã¤ãå®ç¾© âââ
        CHANNEL_TYPES = {
            "ãªã¹ãã£ã³ã°åºå": {"icon": "ð", "color": "#4285f4", "default_cpm": 600,  "default_ctr": 3.0, "default_cvr": 2.5},
            "SNSåºå":         {"icon": "ð±", "color": "#ea4335", "default_cpm": 400,  "default_ctr": 1.5, "default_cvr": 1.8},
            "ãã£ã¹ãã¬ã¤åºå": {"icon": "ð¥",  "color": "#34a853", "default_cpm": 250,  "default_ctr": 0.5, "default_cvr": 1.2},
            "åç»åºå":         {"icon": "â¶",  "color": "#fbbc04", "default_cpm": 800,  "default_ctr": 1.0, "default_cvr": 1.5},
            "ã¡ã¼ã«/LINE":      {"icon": "ð§", "color": "#9b59b6", "default_cpm": 100,  "default_ctr": 5.0, "default_cvr": 3.0},
        }

        # âââ éå®¢ã¢ã¼ãåæ¿ âââ
        acq_mode_label = st.radio(
            "éå®¢ã¢ã¼ã",
            ["ã·ã³ãã« (CPAç´å¥å)", "ãã¡ãã«ã¢ã¼ã (CTR/CVR)"],
            horizontal=True,
            index=1 if st.session_state.acq_mode == "funnel" else 0,
            key="acq_mode_radio",
        )
        st.session_state.acq_mode = "funnel" if "ãã¡ãã«" in acq_mode_label else "simple"

        if st.session_state.acq_mode == "simple":
            # ââââ ã·ã³ãã«ã¢ã¼ã ââââ
            s2a, s2b = st.columns(2)
            with s2a:
                ad_budget = st.number_input(f"æéåºåäºç®{annual_label} (å)", value=tmpl["ad_budget"] * annual_divisor, step=100_000)
                ad_budget_monthly = ad_budget / annual_divisor
                cpa = st.number_input("CPA (å)", value=tmpl["cpa"], step=100)
            with s2b:
                organic_start = st.number_input("èªç¶æµå¥ç²å¾æ° (ä»¶/æ)", value=tmpl["organic_start"], step=10)
                org_growth_pct = st.slider("èªç¶æµå¥ææ¬¡æé·ç (%)", 0.0, 20.0, tmpl["organic_growth"], 0.5)
                organic_growth = 1 + org_growth_pct / 100
                k_factor = st.slider("ãã¤ã©ã«ä¿æ° K factor", 0.0, 0.9, 0.0, 0.05,
                                     help="1ã¦ã¼ã¶ã¼ãç´¹ä»ããå¹³åæ°è¦ã¦ã¼ã¶ã¼æ°")
            effective_cpa = cpa
            total_ad_budget_monthly = ad_budget_monthly

        else:
            # ââââ ãã¡ãã«ã¢ã¼ã ââââ
            st.markdown("**ãã£ãã«è¿½å **")
            ch_btn_cols = st.columns(len(CHANNEL_TYPES))
            for idx, (ch_type, ch_info) in enumerate(CHANNEL_TYPES.items()):
                with ch_btn_cols[idx]:
                    if st.button(f"{ch_info['icon']} {ch_type}", key=f"add_ch_{idx}", use_container_width=True):
                        existing = [ch["name"] for ch in st.session_state.channels]
                        if ch_type not in existing:
                            st.session_state.channels.append({
                                "name": ch_type,
                                "budget": 300_000,
                                "cpm": ch_info["default_cpm"],
                                "ctr": ch_info["default_ctr"],
                                "cvr": ch_info["default_cvr"],
                            })
                            st.rerun()

            # âââ åãã£ãã«ã®å¥å âââ
            channels_data = []
            channels_to_remove = []
            for cidx, ch in enumerate(st.session_state.channels):
                ch_info = CHANNEL_TYPES.get(ch["name"], {"icon": "ð¢", "color": "#f5a623"})
                c_hdr, c_rm = st.columns([9, 1])
                with c_hdr:
                    st.markdown(f"**{ch_info['icon']} {ch['name']}**")
                with c_rm:
                    if len(st.session_state.channels) > 1 and st.button("â", key=f"rm_ch_{cidx}"):
                        channels_to_remove.append(cidx)

                cc1, cc2, cc3, cc4 = st.columns(4)
                with cc1:
                    ch_budget = st.number_input("æéäºç® (å)", value=int(ch["budget"]), step=50_000, key=f"ch_b_{cidx}")
                with cc2:
                    ch_cpm = st.number_input("CPM (å)", value=float(ch["cpm"]), step=50.0, key=f"ch_cpm_{cidx}", help="1,000ã¤ã³ãã¬ãã·ã§ã³ãããã®åä¾¡")
                with cc3:
                    ch_ctr = st.number_input("CTR (%)", value=float(ch["ctr"]), step=0.1, min_value=0.01, key=f"ch_ctr_{cidx}", help="ã¯ãªãã¯ç")
                with cc4:
                    ch_cvr = st.number_input("CVR (%)", value=float(ch["cvr"]), step=0.1, min_value=0.01, key=f"ch_cvr_{cidx}", help="ã³ã³ãã¼ã¸ã§ã³ç")

                # èªåè¨ç®
                ch_imps = int(ch_budget / ch_cpm * 1000) if ch_cpm > 0 else 0
                ch_clicks = int(ch_imps * ch_ctr / 100)
                ch_cvs = int(ch_clicks * ch_cvr / 100)
                ch_eff_cpa = int(ch_budget / ch_cvs) if ch_cvs > 0 else 0

                # ãã£ãã«å¥ãããã¡ãã«
                clr = ch_info.get("color", "#f5a623")
                st.markdown(f"""
                <div class="ch-funnel">
                  <div class="cf-step"><div class="cf-num" style="color:{clr}">Â¥{ch_budget:,}</div><div class="cf-lbl">äºç®</div></div>
                  <div class="cf-arr">â¶</div>
                  <div class="cf-step"><div class="cf-num" style="color:#8899bb">{ch_imps:,}</div><div class="cf-lbl">imp</div></div>
                  <div class="cf-arr">â¶</div>
                  <div class="cf-step"><div class="cf-num" style="color:#8899bb">{ch_clicks:,}</div><div class="cf-lbl">click</div><div class="cf-sub">CTR {ch_ctr}%</div></div>
                  <div class="cf-arr">â¶</div>
                  <div class="cf-step"><div class="cf-num" style="color:#34d297">{ch_cvs:,}</div><div class="cf-lbl">CV</div><div class="cf-sub">CVR {ch_cvr}%</div></div>
                  <div class="cf-arr">â¶</div>
                  <div class="cf-step"><div class="cf-num" style="color:#fff">Â¥{ch_eff_cpa:,}</div><div class="cf-lbl">CPA</div></div>
                </div>""", unsafe_allow_html=True)

                channels_data.append({
                    "name": ch["name"], "budget": ch_budget, "cpm": ch_cpm,
                    "ctr": ch_ctr, "cvr": ch_cvr,
                    "impressions": ch_imps, "clicks": ch_clicks, "cvs": ch_cvs, "eff_cpa": ch_eff_cpa,
                })

            # ãã£ãã«åé¤å¦ç
            if channels_to_remove:
                for ci in sorted(channels_to_remove, reverse=True):
                    st.session_state.channels.pop(ci)
                st.rerun()

            # ã»ãã·ã§ã³æ´æ°
            for cidx, cd in enumerate(channels_data):
                if cidx < len(st.session_state.channels):
                    st.session_state.channels[cidx] = {
                        "name": cd["name"], "budget": cd["budget"],
                        "cpm": cd["cpm"], "ctr": cd["ctr"], "cvr": cd["cvr"],
                    }

            # âââ åè¨ãã¡ãã«ãµããªã¼ âââ
            total_ad_budget_monthly = sum(cd["budget"] for cd in channels_data)
            total_imps  = sum(cd["impressions"] for cd in channels_data)
            total_clicks_all = sum(cd["clicks"] for cd in channels_data)
            total_cvs   = sum(cd["cvs"] for cd in channels_data)
            effective_cpa = int(total_ad_budget_monthly / total_cvs) if total_cvs > 0 else 0
            ad_budget_monthly = total_ad_budget_monthly
            cpa = effective_cpa

            st.markdown(f"""
            <div class="funnel-total">
              <div class="funnel-total-title">â ãã£ãã«åè¨ãã¡ãã«</div>
              <div class="funnel-row">
                <div class="funnel-step"><div class="funnel-num" style="color:#f5a623">Â¥{total_ad_budget_monthly:,}</div><div class="funnel-lbl">ç·åºåæä¸</div></div>
                <div class="funnel-arr">â¶</div>
                <div class="funnel-step"><div class="funnel-num" style="color:#4285f4">{total_imps:,}</div><div class="funnel-lbl">ã¤ã³ãã¬ãã·ã§ã³</div></div>
                <div class="funnel-arr">â¶</div>
                <div class="funnel-step"><div class="funnel-num" style="color:#9b59b6">{total_clicks_all:,}</div><div class="funnel-lbl">ã¯ãªãã¯</div></div>
                <div class="funnel-arr">â¶</div>
                <div class="funnel-step"><div class="funnel-num" style="color:#34d297">{total_cvs:,}</div><div class="funnel-lbl">CVç²å¾</div></div>
                <div class="funnel-arr">â¶</div>
                <div class="funnel-step"><div class="funnel-num" style="color:#fff">Â¥{effective_cpa:,}</div><div class="funnel-lbl" style="color:#34d297;font-weight:700;">å®è³ªCPAï¼èªåï¼</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

            # âââ èªç¶æµå¥ + ãã¤ã©ã« âââ
            st.markdown("**èªç¶æµå¥ + ãã¤ã©ã«è¨­å®**")
            s2b1, s2b2, s2b3 = st.columns(3)
            with s2b1:
                organic_start = st.number_input("èªç¶æµå¥ç²å¾æ° (ä»¶/æ)", value=tmpl["organic_start"], step=10)
            with s2b2:
                org_growth_pct = st.slider("èªç¶æµå¥ææ¬¡æé·ç (%)", 0.0, 20.0, tmpl["organic_growth"], 0.5)
                organic_growth = 1 + org_growth_pct / 100
            with s2b3:
                k_factor = st.slider("ãã¤ã©ã«ä¿æ° K factor", 0.0, 0.9, 0.0, 0.05,
                                     help="1ã¦ã¼ã¶ã¼ãç´¹ä»ããå¹³åæ°è¦ã¦ã¼ã¶ã¼æ° (K=0.3 â 10äººâ3äººç´¹ä»)")

        # IMPROVEMENT 5: Year-by-Year Growth Rate Settings
        use_yearly_growth = st.checkbox("å¹´åº¦å¥æé·çãè¨­å®", value=False)
        yearly_growth_rates = {}
        if use_yearly_growth:
            st.markdown("**å¹´åº¦å¥æé·çèª¿æ´ï¼ææ©æé·ã®åçï¼**")
            yr_cols = st.columns(5)
            for year in range(2, 11):
                with yr_cols[(year - 2) % 5]:
                    yearly_growth_rates[year] = st.number_input(
                        f"Year {year}", value=100.0, min_value=0.0, step=10.0, key=f"yr_growth_{year}"
                    ) / 100.0
        else:
            for year in range(2, 11):
                yearly_growth_rates[year] = 1.0

        use_churn = st.checkbox("è§£ç´çãåæ ãã", value=True)
        use_season = st.checkbox("å­£ç¯å¤åãåæ ãã", value=True)
        if use_season:
            sf_cols = st.columns(6)
            seasonal = []
            for idx, ml in enumerate(MONTH_LABELS):
                with sf_cols[idx % 6]:
                    seasonal.append(st.number_input(ml, 0.1, 3.0, tmpl["seasonal"][idx], 0.05, key=f"sf{idx}"))
        else:
            seasonal = [1.0] * 12

        bc, _, nc = st.columns([1, 7, 1])
        with bc:
            if st.button("æ»ã", key="b2"):
                st.session_state.step = 1; st.rerun()
        with nc:
            if st.button("æ¬¡ã¸", key="n2"):
                st.session_state.step = 3; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 3 â ã³ã¹ãè¨­è¨ (A4: ãã§ãã¯ããã¯ã¹é¸æå¼ + IMPROVEMENT 3: More items)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 3 â ã³ã¹ãè¨­è¨ï¼é¸æå¼ï¼", expanded=(st.session_state.step == 3)):
        st.caption("æ¥­ç¨®ãã³ãã¬ã¼ãã®é ç®ãããã©ã«ãã§é¸æããã¦ãã¾ããè¿½å ã»åé¤ã¯èªç±ã§ãã")

        s3a, s3b = st.columns(2)

        # --- å¤åè²» ---
        with s3a:
            st.markdown("**å¤åè²»ï¼1ä»¶ãã¨ / å£²ä¸æ¯çï¼**")
            vc_values = {}
            for item_name, item_info in VARIABLE_COST_ITEMS.items():
                tmpl_vc = tmpl.get("vc_items", {})
                default_on = item_name in tmpl_vc
                enabled = st.checkbox(
                    f"{item_name}",
                    value=default_on,
                    key=f"vc_chk_{item_info['key']}",
                    help=item_info["desc"],
                )
                if enabled:
                    default_val = tmpl_vc.get(item_name, 0)
                    label = f"  â {item_name} ({item_info['unit']})"
                    val = st.number_input(
                        label, value=float(default_val), step=0.1 if item_info["unit"] == "%" else 100.0,
                        key=f"vc_val_{item_info['key']}"
                    )
                    vc_values[item_name] = {"value": val, "unit": item_info["unit"]}

            st.markdown("**ã«ã¹ã¿ã å¤åè²»ã®è¿½å **")
            custom_vc_name = st.text_input("ã«ã¹ã¿ã é ç®å", value="", key="custom_vc_name")
            if custom_vc_name:
                custom_vc_unit = st.radio("åä½", ["å/ä»¶", "%"], horizontal=True, key="custom_vc_unit")
                custom_vc_val = st.number_input(f"{custom_vc_name} ({custom_vc_unit})", value=0.0, step=100.0 if custom_vc_unit == "å/ä»¶" else 0.1, key="custom_vc_val")
                if custom_vc_val > 0:
                    vc_values[custom_vc_name] = {"value": custom_vc_val, "unit": custom_vc_unit}

        # --- åºå®è²» ---
        with s3b:
            st.markdown("**åºå®è²»ï¼æé¡ï¼**")
            fc_values = {}
            for item_name, item_info in FIXED_COST_ITEMS.items():
                tmpl_fc = tmpl.get("fc_items", {})
                default_on = item_name in tmpl_fc
                enabled = st.checkbox(
                    f"{item_name}",
                    value=default_on,
                    key=f"fc_chk_{item_info['key']}",
                    help=item_info["desc"],
                )
                if enabled:
                    default_val = tmpl_fc.get(item_name, 0)
                    label = f"  â {item_name}{annual_label} (å)"
                    val = st.number_input(
                        label, value=default_val * annual_divisor, step=10_000,
                        key=f"fc_val_{item_info['key']}"
                    )
                    fc_values[item_name] = val / annual_divisor  # æé¡ã«å¤æ

            st.markdown("**ã«ã¹ã¿ã åºå®è²»ã®è¿½å **")
            custom_fc_name = st.text_input("ã«ã¹ã¿ã é ç®å", value="", key="custom_fc_name")
            if custom_fc_name:
                custom_fc_val = st.number_input(f"{custom_fc_name} (å/æ)", value=0.0, step=10_000, key="custom_fc_val")
                if custom_fc_val > 0:
                    fc_values[custom_fc_name] = custom_fc_val / annual_divisor

        # åºå®è²»åè¨ãè¨ç®
        total_fixed = sum(fc_values.values())

        # å¤åè²»ã®åä¾¡ã»çãæ´ç
        vc_per_unit_fixed = 0  # å/ä»¶ãã¼ã¹ã®å¤åè²»åè¨
        vc_pct_of_sales = 0    # %ãã¼ã¹ã®å¤åè²»åè¨
        for item_name, item_data in vc_values.items():
            if item_data["unit"] == "%":
                vc_pct_of_sales += item_data["value"] / 100
            else:
                vc_per_unit_fixed += item_data["value"]

        bc3, _, nc3 = st.columns([1, 7, 1])
        with bc3:
            if st.button("æ»ã", key="b3"):
                st.session_state.step = 2; st.rerun()
        with nc3:
            if st.button("æ¬¡ã¸", key="n3"):
                st.session_state.step = 4; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 4 â äººå¡è¨ç» (B1)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 4 â äººå¡è¨ç»ï¼æ¡ç¨ã¿ã¤ãã³ã°ï¼", expanded=(st.session_state.step == 4)):
        st.caption("ä½ã¶æç®ã«ä½äººæ¡ç¨ããããè¨­å®ããã¨ãäººä»¶è²»ãã¹ãããé¢æ°ã§åæ ããã¾ãã")

        if "n_hires" not in st.session_state:
            st.session_state.n_hires = 1

        hire_plan = []
        for hidx in range(st.session_state.n_hires):
            hc1, hc2, hc3, hc4 = st.columns(4)
            with hc1:
                h_month = st.number_input("æ¡ç¨æ", min_value=1, max_value=120, value=min(1 + hidx * 6, 120), key=f"hire_month_{hidx}")
            with hc2:
                h_count = st.number_input("äººæ°", min_value=1, max_value=50, value=1, key=f"hire_count_{hidx}")
            with hc3:
                h_salary = st.number_input("æçµ¦ (å/äºº)", value=350_000, step=50_000, key=f"hire_salary_{hidx}")
            with hc4:
                h_role = st.text_input("å½¹è·", value="ã¨ã³ã¸ãã¢" if hidx == 0 else "å¶æ¥­", key=f"hire_role_{hidx}")
            hire_plan.append({"month": h_month, "count": h_count, "salary": h_salary, "role": h_role})

        hcol1, hcol2 = st.columns(2)
        with hcol1:
            if st.button("ï¼ æ¡ç¨æ ãè¿½å ", key="add_hire"):
                st.session_state.n_hires += 1; st.rerun()
        with hcol2:
            if st.session_state.n_hires > 1 and st.button("ï¼ æå¾ã®æ ãåé¤", key="del_hire"):
                st.session_state.n_hires -= 1; st.rerun()

        # äººå¡è¨ç»ãã¬ãã¥ã¼
        if hire_plan:
            st.markdown("**äººä»¶è²»ã·ãã¥ã¬ã¼ã·ã§ã³ï¼ãã¬ãã¥ã¼ï¼**")
            preview_months = min(sim_months if 'sim_months' in dir() else 36, 60)
            headcount_data = []
            for m in range(1, preview_months + 1):
                total_heads = 0
                total_salary = 0
                for hp in hire_plan:
                    if m >= hp["month"]:
                        total_heads += hp["count"]
                        total_salary += hp["count"] * hp["salary"]
                # ç¤¾ä¼ä¿éºæï¼ç´15%ãèªåå ç®ï¼
                total_cost = total_salary * 1.15
                headcount_data.append({"æ": m, "äººæ°": total_heads, "äººä»¶è²»ï¼ç¤¾ä¿è¾¼ï¼": total_cost})
            hc_df = pd.DataFrame(headcount_data)
            st.altair_chart(
                _dk(alt.Chart(hc_df).mark_area(opacity=0.4, color="#f5a623").encode(
                    x=alt.X("æ:Q", title="æ"),
                    y=alt.Y("äººä»¶è²»ï¼ç¤¾ä¿è¾¼ï¼:Q", axis=alt.Axis(format="~s", title="Â¥ æé¡äººä»¶è²»")),
                    tooltip=["æ", "äººæ°", alt.Tooltip("äººä»¶è²»ï¼ç¤¾ä¿è¾¼ï¼:Q", format=",")]
                ).interactive()),
                use_container_width=True
            )

        bc4, _, nc4 = st.columns([1, 7, 1])
        with bc4:
            if st.button("æ»ã", key="b4"):
                st.session_state.step = 3; st.rerun()
        with nc4:
            if st.button("æ¬¡ã¸", key="n4"):
                st.session_state.step = 5; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 5 â è¨­åæè³ã»æ¸ä¾¡åå´ (A3 + IMPROVEMENT 2)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 5 â è¨­åæè³ã»æ¸ä¾¡åå´", expanded=(st.session_state.step == 5)):
        st.caption("è³ç£ãç»é²ããã¨ãå®é¡æ³ã¾ãã¯å®çæ³ã§æå²ãæ¸ä¾¡åå´è²»ãèªåè¨ç®ããP&Lã¨ã­ã£ãã·ã¥ãã­ã¼ã«åæ ãã¾ãã")

        if "n_assets" not in st.session_state:
            st.session_state.n_assets = 0

        dep_assets = []
        for aidx in range(st.session_state.n_assets):
            ac1, ac2, ac3, ac4, ac5 = st.columns(5)
            with ac1:
                a_name = st.text_input("è³ç£å", value=f"è³ç£{aidx+1}", key=f"asset_name_{aidx}")
            with ac2:
                a_cat = st.selectbox("ç¨®å¥", list(DEPRECIATION_CATEGORIES.keys()), key=f"asset_cat_{aidx}")
            with ac3:
                a_cost = st.number_input("åå¾åä¾¡ (å)", value=1_000_000, step=100_000, key=f"asset_cost_{aidx}")
            with ac4:
                default_life = DEPRECIATION_CATEGORIES[a_cat]["useful_life"]
                a_life = st.number_input("èç¨å¹´æ°", min_value=1, max_value=50, value=default_life, key=f"asset_life_{aidx}")
            with ac5:
                a_start = st.number_input("åå¾æ", min_value=0, max_value=120, value=0, key=f"asset_start_{aidx}",
                                          help="0=äºæ¥­éå§åï¼åææè³ï¼ã1=1ã¶æç®...")

            # IMPROVEMENT 2: Depreciation method choice
            a_method = st.radio(f"è³ç£{aidx+1} æ¸ä¾¡åå´æ¹æ³", ["å®é¡½æ³", "å®çæ³ (200%)"], horizontal=True, key=f"asset_method_{aidx}")
            a_residual = st.number_input(f"è³ç£{aidx+1} æ®å­ä¾¡é¡ (å)", value=1, step=1, key=f"asset_residual_{aidx}", min_value=1)

            if a_method == "å®é¡½æ³":
                monthly_dep = (a_cost - a_residual) / (a_life * 12) if a_life > 0 else 0
            else:  # å®çæ³
                declining_rate = 2.0 / a_life
                monthly_dep = a_cost * declining_rate / 12

            dep_assets.append({
                "name": a_name, "category": a_cat, "cost": a_cost,
                "useful_life": a_life, "start_month": a_start,
                "method": a_method, "residual_value": a_residual,
                "monthly_dep": monthly_dep,
            })

        acol1, acol2 = st.columns(2)
        with acol1:
            if st.button("ï¼ è³ç£ãè¿½å ", key="add_asset"):
                st.session_state.n_assets += 1; st.rerun()
        with acol2:
            if st.session_state.n_assets > 0 and st.button("ï¼ æå¾ã®è³ç£ãåé¤", key="del_asset"):
                st.session_state.n_assets -= 1; st.rerun()

        if dep_assets:
            st.markdown("**æ¸ä¾¡åå´ã¹ã±ã¸ã¥ã¼ã«**")
            dep_summary = []
            for a in dep_assets:
                dep_summary.append({
                    "è³ç£å": a["name"],
                    "ç¨®å¥": a["category"],
                    "åå¾åä¾¡": f"Â¥{a['cost']:,}",
                    "æ®å­ä¾¡é¡": f"Â¥{a['residual_value']:,}",
                    "èç¨å¹´æ°": f"{a['useful_life']}å¹´",
                    "æ¹æ³": a["method"],
                    "æé¡åå´è²»": f"Â¥{a['monthly_dep']:,.0f}",
                    "åå¾æ": f"{a['start_month']}ã¶æç®" if a["start_month"] > 0 else "åææè³",
                })
            st.dataframe(pd.DataFrame(dep_summary), hide_index=True, use_container_width=True)

            # IMPROVEMENT 2: Show depreciation schedule chart for each asset
            for a in dep_assets:
                with st.expander(f"æ¸ä¾¡åå´ã¹ã±ã¸ã¥ã¼ã«è©³ç´° â {a['name']}", expanded=False):
                    dep_schedule = []
                    remaining_value = a['cost']
                    for month in range(1, min(a['useful_life'] * 12 + 1, sim_months + 1)):
                        if a['method'] == "å®é¡½æ³":
                            monthly_depr = (a['cost'] - a['residual_value']) / (a['useful_life'] * 12)
                        else:
                            declining_rate = 2.0 / a['useful_life']
                            monthly_depr = remaining_value * declining_rate / 12
                        remaining_value = max(a['residual_value'], remaining_value - monthly_depr)
                        dep_schedule.append({
                            "æ": month,
                            "æé¡åå´è²»": monthly_depr,
                            "ç´¯ç©åå´é¡": a['cost'] - remaining_value,
                            "å¸³ç°¿ä¾¡é¡": remaining_value,
                        })
                    dep_sch_df = pd.DataFrame(dep_schedule)
                    st.altair_chart(
                        _dk(alt.Chart(dep_sch_df).mark_line().encode(
                            x=alt.X("æ:Q", title="æ"),
                            y=alt.Y("å¸³ç°¿ä¾¡é¡:Q", axis=alt.Axis(format="~s", title="Â¥ å¸³ç°¿ä¾¡é¡")),
                            color=alt.value("#8B5CF6"),
                            tooltip=["æ", alt.Tooltip("æé¡åå´è²»:Q", format=",.0f"), alt.Tooltip("å¸³ç°¿ä¾¡é¡:Q", format=",.0f")]
                        ).interactive()),
                        use_container_width=True
                    )

        bc5, _, nc5 = st.columns([1, 7, 1])
        with bc5:
            if st.button("æ»ã", key="b5"):
                st.session_state.step = 4; st.rerun()
        with nc5:
            if st.button("æ¬¡ã¸", key="n5"):
                st.session_state.step = 6; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 6 â è³éç¹°ã
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 6 â è³éç¹°ãï¼ã­ã£ãã·ã¥ãã­ã¼ï¼", expanded=(st.session_state.step == 6)):
        s6a, s6b = st.columns(2)
        with s6a:
            cash_init = st.number_input("æåç¾é (å)", value=10_000_000, step=1_000_000)
            pay_cyc = st.selectbox("å¥éãµã¤ã¯ã«", ["å½æ", "ç¿æ", "ç¿ãæ"])
        with s6b:
            exp_cyc = st.selectbox("æ¯æãµã¤ã¯ã«", ["å½æ", "ç¿æ"])
            fundraise_alert = st.number_input(
                "è³éèª¿éã¢ã©ã¼ãæ®é« (å)", value=3_000_000, step=500_000,
                help="ã­ã£ãã·ã¥æ®é«ããã®éé¡ãä¸åãã¨è­¦åãè¡¨ç¤ºãã¾ã (B4)"
            )
        pay_delay = {"å½æ": 0, "ç¿æ": 1, "ç¿ãæ": 2}[pay_cyc]
        exp_delay = {"å½æ": 0, "ç¿æ": 1}[exp_cyc]

        bc6, _, nc6 = st.columns([1, 7, 1])
        with bc6:
            if st.button("æ»ã", key="b6"):
                st.session_state.step = 5; st.rerun()
        with nc6:
            if st.button("æ¬¡ã¸", key="n6"):
                st.session_state.step = 7; st.rerun()

    # âââââââââââââââââââââââââââââââââââââââ
    # STEP 7 â ç¨å¹æ (B3)
    # âââââââââââââââââââââââââââââââââââââââ
    with st.expander("Step 7 â ç¨å¹æã¢ãã«", expanded=(st.session_state.step == 7)):
        st.caption("æ³äººç¨ç­ã®å®å¹ç¨çãè¨­å®ããæ¸ä¾¡åå´ã«ããç¨ã·ã¼ã«ãå¹æãå¯è¦åãã¾ãã")
        tc1, tc2 = st.columns(2)
        with tc1:
            tax_rate_pct = st.slider("å®å¹ç¨ç (%)", 0, 50, 30, help="æ³äººç¨ã»ä½æ°ç¨ã»äºæ¥­ç¨ã®åè¨å®å¹ç¨ç")
            tax_rate = tax_rate_pct / 100
        with tc2:
            st.info(f"æ¸ä¾¡åå´è²»ã¯è²»ç¨ã¨ãã¦è¨ä¸ãããèª²ç¨æå¾ãæ¸å°ããã¾ãã\n"
                    f"ç¨ã·ã¼ã«ãå¹æ = æ¸ä¾¡åå´è²» Ã å®å¹ç¨ç ({tax_rate_pct}%)")

        bc7, _ = st.columns([1, 8])
        with bc7:
            if st.button("æ»ã", key="b7"):
                st.session_state.step = 6; st.rerun()

    # âââ ããã©ã«ãè£å® âââ
    try:
        _ = sim_months
    except NameError:
        sim_months = 36; target_rate = 0.20; target_pct = 20; initial_inv = 5_000_000
        is_annual_input = False; annual_divisor = 1

    try:
        _ = ad_budget_monthly
    except NameError:
        ad_budget_monthly = tmpl["ad_budget"]; cpa = tmpl["cpa"]
        organic_start = tmpl["organic_start"]; organic_growth = 1 + tmpl["organic_growth"] / 100
        use_churn = True; use_season = True; seasonal = tmpl["seasonal"]
        rev_sources = [{"name": "ã¡ã¤ã³åå", "unit_price": tmpl["unit_price"], "weight": 1.0, "churn_rate": tmpl["churn_rate"] / 100}]

    try:
        _ = effective_cpa
    except NameError:
        effective_cpa = cpa
        total_ad_budget_monthly = ad_budget_monthly

    try:
        _ = k_factor
    except NameError:
        k_factor = 0.0

    try:
        _ = yearly_growth_rates
    except NameError:
        yearly_growth_rates = {year: 1.0 for year in range(2, 11)}

    try:
        _ = total_fixed
    except NameError:
        total_fixed = sum(tmpl.get("fc_items", {}).values())
        vc_per_unit_fixed = sum(v for k, v in tmpl.get("vc_items", {}).items() if k not in ["æ±ºæ¸ææ°æ", "ã¢ã¼ã«ææ°æ", "ã­ã¤ã¤ãªãã£"])
        vc_pct_of_sales = sum(v / 100 for k, v in tmpl.get("vc_items", {}).items() if k in ["æ±ºæ¸ææ°æ", "ã¢ã¼ã«ææ°æ", "ã­ã¤ã¤ãªãã£"])

    try:
        _ = cash_init
    except NameError:
        cash_init = 10_000_000; pay_delay = 0; exp_delay = 0; fundraise_alert = 3_000_000

    try:
        _ = hire_plan
    except NameError:
        hire_plan = []

    try:
        _ = dep_assets
    except NameError:
        dep_assets = []

    try:
        _ = tax_rate
    except NameError:
        tax_rate = 0.30; tax_rate_pct = 30

    # âââ ã·ããªãªä¿®æ° âââ
    if scenario == "æ¥½è¦³ +20%":
        s_mult, c_mult = 1.2, 0.9
    elif scenario == "æ²è¦³ -20%":
        s_mult, c_mult = 0.8, 1.1
    else:
        s_mult, c_mult = 1.0, 1.0

    # âââ è¨ç®ã­ã¸ãã¯ï¼å¨æ©è½çµ±åï¼ âââ
    rows = []
    cum_profit = 0
    cum_profit_after_tax = 0
    # åçæºå¥ã®ã¢ã¯ãã£ãé¡§å®¢ãç®¡ç
    active_by_source = [0] * len(rev_sources)
    cash = cash_init
    s_buf = [0] * (pay_delay + 1)
    e_buf = [0] * (exp_delay + 1)
    bep_m = rec_m = None
    cash_alert_month = None

    # ã¦ãããã¨ã³ããã¯ã¹ç¨ã®å éå¹³ååä¾¡
    weighted_price = sum(rs["unit_price"] * rs["weight"] for rs in rev_sources)
    weighted_churn = sum(rs["churn_rate"] * rs["weight"] for rs in rev_sources) if use_churn else 0

    for i in range(sim_months):
        m = i + 1
        cal = i % 12
        sf = seasonal[cal] if use_season else 1.0

        # IMPROVEMENT 5: Apply yearly growth rate multiplier
        current_year = ((m - 1) // 12) + 1
        year_growth_mult = yearly_growth_rates.get(current_year, 1.0)

        # éå®¢ï¼å¨åçæºå±éã®æ°è¦ç²å¾ï¼
        u_ad = int(ad_budget_monthly / cpa) if cpa > 0 else 0
        u_org = int(organic_start * (organic_growth ** i) * year_growth_mult)
        # K factor: ãã¤ã©ã«ä¿æ°ã«ããå¢å¹
        total_new = int((u_ad + u_org) * (1 + k_factor))

        # åçæºå¥ã®å£²ä¸è¨ç®
        total_sales = 0
        total_units = 0
        total_churn = 0
        total_active = 0
        for sidx, rs in enumerate(rev_sources):
            src_new = int(total_new * rs["weight"])
            src_churn = int(active_by_source[sidx] * rs["churn_rate"]) if use_churn and active_by_source[sidx] > 0 else 0
            active_by_source[sidx] = max(0, active_by_source[sidx] + src_new - src_churn)
            src_units = int((active_by_source[sidx] if use_churn else src_new) * sf)
            src_sales = int(src_units * rs["unit_price"] * s_mult)
            total_sales += src_sales
            total_units += src_units
            total_churn += src_churn
            total_active += active_by_source[sidx]

        # å¤åè²»
        vc = (total_units * vc_per_unit_fixed + total_sales * vc_pct_of_sales) * c_mult
        gp = total_sales - vc

        # B1: äººä»¶è²»ã¹ãããé¢æ°
        hire_salary_total = 0
        total_headcount = 0
        for hp in hire_plan:
            if m >= hp["month"]:
                total_headcount += hp["count"]
                hire_salary_total += hp["count"] * hp["salary"]
        hire_cost = hire_salary_total * 1.15  # ç¤¾ä¿è¾¼ã¿

        # A3: æ¸ä¾¡åå´è²»ï¼å®é¡æ³ã»å®çæ³å¯¾å¿ï¼
        monthly_depreciation = 0
        for asset in dep_assets:
            if m > asset["start_month"]:
                months_elapsed = m - asset["start_month"]
                total_dep_months = asset["useful_life"] * 12
                if months_elapsed <= total_dep_months:
                    monthly_depreciation += asset["monthly_dep"]

        # åºå®è²»ï¼ãã³ãã¬åºå®è²» + äººä»¶è²»è¿½å åï¼
        total_fixed_with_hire = total_fixed * c_mult + hire_cost

        # å¶æ¥­å©çï¼æ¸ä¾¡åå´è²»ãå«ãï¼
        op = gp - ad_budget_monthly - total_fixed_with_hire - monthly_depreciation
        cum_profit += op

        # B3: ç¨å¹æ
        taxable_income = max(0, op)  # æ¬ æã®å ´åã¯ç¨ã¼ã­ï¼ç°¡æã¢ãã«ï¼
        tax_amount = taxable_income * tax_rate
        tax_shield = monthly_depreciation * tax_rate  # æ¸ä¾¡åå´ã«ããç¨ã·ã¼ã«ã
        net_income = op - tax_amount
        cum_profit_after_tax += net_income

        # æçåå²ç¹
        mr = gp / total_sales if total_sales > 0 else 0
        bep = (total_fixed_with_hire + ad_budget_monthly + monthly_depreciation) / mr if mr > 0 else 0
        if bep_m is None and op > 0:
            bep_m = m
        if rec_m is None and cum_profit > 0:
            rec_m = m

        # CFï¼æ¸ä¾¡åå´ã¯éç¾éãªã®ã§CFã«ã¯å ç®ï¼
        cf_in = total_sales
        cf_out = abs(vc) + ad_budget_monthly + total_fixed_with_hire + tax_amount
        # è¨­åæè³ã®ç¾éæ¯åº
        for asset in dep_assets:
            if m == max(1, asset["start_month"]):
                cf_out += asset["cost"]

        s_buf.append(cf_in)
        e_buf.append(cf_out)
        cash = cash + s_buf.pop(0) - e_buf.pop(0)

        # B4: è³éèª¿éã¢ã©ã¼ã
        if cash_alert_month is None and cash < fundraise_alert:
            cash_alert_month = m

        rows.append({
            "æ": f"{m}ã¶æç®", "æçªå·": m, "æ¦æ": MONTH_LABELS[cal],
            "å¹´": ((m - 1) // 12) + 1,
            "å­£ç¯ä¿æ°": sf, "æ°è¦ç²å¾": total_new, "è§£ç´æ°": total_churn,
            "ã¢ã¯ãã£ãé¡§å®¢æ°": total_active, "äººå¡æ°": total_headcount,
            "è²©å£²æ°": total_units, "å£²ä¸é«": total_sales,
            "å¤åè²»": vc, "éçå©ç": gp,
            "åºåå®£ä¼è²»": ad_budget_monthly,
            "äººä»¶è²»ï¼è¿½å æ¡ç¨ï¼": hire_cost,
            "åºå®è²»åè¨": total_fixed_with_hire,
            "æ¸ä¾¡åå´è²»": monthly_depreciation,
            "å¶æ¥­å©ç": op, "ç´¯ç©å©ç": cum_profit,
            "ç¨é¡": tax_amount, "ç¨ã·ã¼ã«ã": tax_shield,
            "ç¨å¼å¾å©ç": net_income, "ç´¯ç©ç¨å¼å¾å©ç": cum_profit_after_tax,
            "æçåå²ç¹å£²ä¸": bep,
            "ã­ã£ãã·ã¥æ®é«": cash,
            "è²»ç¨_å¤åè²»": vc,
            "è²»ç¨_åºåå®£ä¼è²»": ad_budget_monthly,
            "è²»ç¨_åºå®è²»": total_fixed_with_hire,
            "è²»ç¨_æ¸ä¾¡åå´è²»": monthly_depreciation,
        })

    df = pd.DataFrame(rows)
    last = df.iloc[-1]
    cur_sales = last["å£²ä¸é«"]
    cur_profit = last["å¶æ¥­å©ç"]
    cur_rate = cur_profit / cur_sales if cur_sales > 0 else 0
    gap = cur_sales * target_rate - cur_profit

    # ã¦ãããã¨ã³ããã¯ã¹è¨ç®
    ltv = weighted_price / weighted_churn if weighted_churn > 0 else weighted_price * 120
    ltv_cac = ltv / cpa if cpa > 0 else 999

    # âââ B4: è³éèª¿éã¢ã©ã¼ã âââ
    if cash_alert_month:
        months_to_alert = cash_alert_month - 1  # ç¾å¨=0ã¶æç®ã¨ãã¦
        st.markdown(f"""
        <div class="funding-alert">
            <div class="fa-title">â  è³éèª¿éã¢ã©ã¼ã â {cash_alert_month}ã¶æç®ã«ã­ã£ãã·ã¥ã Â¥{fundraise_alert:,} ãä¸åãã¾ã</div>
            <div class="fa-body">
                ç¾å¨ã®ãã¼ã³ã¬ã¼ãã§ã¯ <strong>{cash_alert_month}ã¶æç®</strong> ã«è³éãä¸è¶³ããè¦è¾¼ã¿ã§ãã<br>
                è³éèª¿éã®æºåã«ã¯éå¸¸3ã6ã¶æãããããã<strong>{max(1, cash_alert_month - 6)}ã¶æçN</strong> ã¾ã§ã«èª¿éæ´»åãéå§ãããã¨ãæ¨å¥¨ãã¾ãã<br>
                å¯¾ç­: â  ã¨ã¯ã¤ãã£èª¿é â¡ ããããã¡ã¤ãã³ã¹ â¢ ã³ã¹ãåæ¸ â£ å£²ä¸å é
            </div>
        </div>
        """, unsafe_allow_html=True)

    # âââ ã¦ãããã¨ã³ããã¯ã¹ âââ
    st.markdown('<div class="section-title">ã¦ãããã¨ã³ããã¯ã¹</div>', unsafe_allow_html=True)
    margin_per_unit = weighted_price - vc_per_unit_fixed - weighted_price * vc_pct_of_sales
    margin_pct = margin_per_unit / weighted_price * 100 if weighted_price > 0 else 0
    cac_val = cpa
    ltv_val = ltv
    ltv_cac_ratio = ltv_val / cac_val if cac_val > 0 else 999
    payback = cac_val / margin_per_unit if margin_per_unit > 0 else 999
    avg_life = 1 / weighted_churn if weighted_churn > 0 else 120

    ue_html = '<div class="kpi-grid">'
    ue_html += f"""<div class="kpi-card accent">
        <div class="label">å®¢åä¾¡ (ARPU)</div><div class="value">Â¥{weighted_price:,.0f}</div>
        <div class="delta neutral">å éå¹³åï¼{len(rev_sources)}åçæºï¼</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if margin_pct > 50 else 'warn'}">
        <div class="label">éçå©ç / ä»¶</div><div class="value">Â¥{margin_per_unit:,.0f}</div>
        <div class="delta {'up' if margin_pct > 50 else 'down'}">å©çé {margin_pct:.1f}%</div></div>"""
    ue_html += f"""<div class="kpi-card accent">
        <div class="label">LTV (é¡§å®¢çæ¶¯ä¾¡å¤)</div><div class="value">Â¥{ltv_val:,.0f}</div>
        <div class="delta neutral">å¹³å {avg_life:.1f}ã¶æ</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if cac_val < ltv_val / 3 else 'danger'}">
        <div class="label">CAC (ç²å¾åä¾¡)</div><div class="value">Â¥{cac_val:,}</div>
        <div class="delta {'up' if cac_val < ltv_val / 3 else 'down'}">CPA = Â¥{cpa:,}</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if ltv_cac_ratio >= 3 else 'danger'}">
        <div class="label">LTV / CAC</div><div class="value">{ltv_cac_ratio:.1f}x</div>
        <div class="delta {'up' if ltv_cac_ratio >= 3 else 'down'}">{'â å¥å¨ (3xä»¥ä¸)' if ltv_cac_ratio >= 3 else 'â½ æ¹åãå¿è¦ (3xæªæº)'}</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if payback < 12 else 'warn'}">
        <div class="label">ãã¤ããã¯æé</div><div class="value">{payback:.1f}ã¶æ</div>
        <div class="delta {'up' if payback < 12 else 'down'}">{'â 12ã¶æä»¥å' if payback < 12 else 'â½ 12ã¶æè¶'}</div></div>"""
    ue_html += "</div>"
    st.markdown(ue_html, unsafe_allow_html=True)

    with st.expander("ã¦ãããã¨ã³ããã¯ã¹è©³ç´°ãè¡¨ç¤º"):
        ue_c1, ue_c2 = st.columns(2)
        with ue_c1:
            st.markdown("**åçæ§é ï¼1é¡§å®¢ãããï¼**")
            ue_items = {"å£²ä¸åä¾¡ï¼å éå¹³åï¼": weighted_price}
            for item_name, item_data in vc_values.items() if 'vc_values' in dir() else []:
                if item_data["unit"] == "%":
                    ue_items[item_name] = -int(weighted_price * item_data["value"] / 100)
                else:
                    ue_items[item_name] = -item_data["value"]
            ue_items["**éçå©ç**"] = margin_per_unit
            ue_df = pd.DataFrame({"é ç®": ue_items.keys(), "éé¡ (å)": [f"Â¥{v:,.0f}" for v in ue_items.values()]})
            st.dataframe(ue_df, hide_index=True, use_container_width=True)
        with ue_c2:
            st.markdown("**å¤å®åºæº**")
            checks = [
                ("LTV / CAC â¥ 3.0", ltv_cac_ratio >= 3, f"{ltv_cac_ratio:.1f}x"),
                ("ãã¤ããã¯ â¤ 12ã¶æ", payback <= 12, f"{payback:.1f}ã¶æ"),
                ("éçå©çç â¥ 50%", margin_pct >= 50, f"{margin_pct:.1f}%"),
                ("è§£ç´ç â¤ 5%", weighted_churn * 100 <= 5, f"{weighted_churn*100:.1f}%"),
            ]
            for label, ok, val in checks:
                icon = "â" if ok else "â ï¸"
                st.markdown(f"{icon} **{label}** â ç¾å¨: {val}")

    # âââ KPI CARDS (IMPROVEMENT 6: Burn rate metrics) âââ
    st.markdown('<div class="section-title">KPI ããã·ã¥ãã¼ã</div>', unsafe_allow_html=True)

    def kpi(label, value, delta="", delta_type="neutral", accent="accent"):
        return f"""
        <div class="kpi-card {accent}">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="delta {delta_type}">{delta}</div>
        </div>"""

    profit_ok = cur_rate >= target_rate
    ltv_ok = ltv_cac >= 3
    run_val = int(cash_init / abs(df["å¶æ¥­å©ç"].mean())) if df["å¶æ¥­å©ç"].mean() < 0 else 999
    total_dep_annual = sum(a["monthly_dep"] for a in dep_assets) * 12

    # IMPROVEMENT 6: Calculate burn rate metrics
    last_3_months = df.tail(3)["å¶æ¥­å©ç"].mean()
    monthly_burn = max(0, -last_3_months) if last_3_months < 0 else 0
    gross_burn = df.tail(1)["è²»ç¨_å¤åè²»"].iloc[0] + df.tail(1)["è²»ç¨_åºåå®£ä¼è²»"].iloc[0] + df.tail(1)["è²»ç¨_åºå®è²»"].iloc[0] + df.tail(1)["è²»ç¨_æ¸ä¾¡åå´è²»"].iloc[0]
    net_burn = gross_burn - df.tail(1)["å£²ä¸é«"].iloc[0]

    kpi_html = '<div class="kpi-grid">'
    kpi_html += kpi("æå", f"Â¥{cur_sales:,.0f}", f"ç®æ¨å©çç {target_pct}%", "neutral", "accent")
    kpi_html += kpi("å¶æ¥­å©ç", f"Â¥{cur_profit:,.0f}",
                     f"å©çç {cur_rate*100:.1f}% {'âéæ' if profit_ok else 'â½æªé'}",
                     "up" if profit_ok else "down", "success" if profit_ok else "danger")
    kpi_html += kpi("LTV / CAC", f"{ltv_cac:.1f}x", "3xä»¥ä¸ãå¥å¨",
                     "up" if ltv_ok else "down", "success" if ltv_ok else "warn")
    kpi_html += kpi("é»å­å", f"{bep_m}ã¶æç®" if bep_m else "æéå¤", "", "neutral", "accent")
    kpi_html += kpi("ã©ã³ã¦ã§ã¤", f"{run_val}ã¶æ" if run_val < 999 else "é»å­éå¶", "",
                     "down" if 0 < run_val < 6 else "neutral",
                     "danger" if 0 < run_val < 6 else "accent")
    kpi_html += kpi("ãã¼ã äººæ°", f"{int(last['äººå¡æ°'])} äºº",
                     f"è¿½å äººä»¶è²» Â¥{last['äººä»¶è²»ï¼è¿½å æ¡ç¨ï¼']:,.0f}/æ", "neutral", "accent")
    kpi_html += kpi("æéãã¼ã³ã¬ã¼ã", f"Â¥{monthly_burn:,.0f}",
                     "ç´è¿3ã¶æå¹³åã®å¶æ¥­æå¤±", "down" if monthly_burn > 0 else "neutral",
                     "warn" if monthly_burn > 0 else "success")
    kpi_html += kpi("ã°ã­ã¹ãã¼ã³ã¬ã¼ã", f"Â¥{gross_burn:,.0f}",
                     "æçµæã®ç·æ¯åº", "neutral", "accent")
    kpi_html += kpi("ããããã¼ã³ã¬ã¼ã", f"Â¥{net_burn:,.0f}",
                     "æ¯åº-åå¥ï¼è² =é»å­ï¼", "down" if net_burn > 0 else "up",
                     "danger" if net_burn > 0 else "success")
    kpi_html += "</div>"
    st.markdown(kpi_html, unsafe_allow_html=True)

    # âââ æ¹åææ¡ âââ
    st.markdown('<div class="section-title">ç®æ¨éæã·ãã¥ã¬ã¼ã·ã§ã³</div>', unsafe_allow_html=True)
    if profit_ok:
        st.success(f"ç®æ¨ã® {target_pct}% ãéæãã¦ãã¾ãï¼ç¾å¨ {cur_rate*100:.1f}%ï¼")
    else:
        st.warning(f"ç®æ¨ {target_pct}% ã¾ã§ ãã¨ Â¥{gap:,.0f}/æ å¿è¦ã§ã")

    ac1, ac2, ac3, ac4 = st.columns(4)
    pu = gap / last["è²©å£²æ°"] if last["è²©å£²æ°"] > 0 else 0
    with ac1:
        st.markdown(f"""<div class="advice-card">
            <div class="advice-title">åä¾¡ã¢ãã</div>
            <div class="advice-value">Â¥{weighted_price+pu:,.0f}</div>
            <div class="advice-desc">+{pu:,.0f}å/ä»¶ ã®å¤ä¸ã</div></div>""", unsafe_allow_html=True)
    with ac2:
        st.markdown(f"""<div class="advice-card">
            <div class="advice-title">åºå®è²»åæ¸</div>
            <div class="advice-value">Â¥{max(0,total_fixed-gap):,.0f}</div>
            <div class="advice-desc">æé¡ {gap:,.0f}å ã®åæ¸</div></div>""", unsafe_allow_html=True)
    with ac3:
        ncpa = cpa * max(0, 1 - gap / ad_budget_monthly) if ad_budget_monthly > 0 else cpa
        st.markdown(f"""<div class="advice-card">
            <div class="advice-title">CPA æ¹å</div>
            <div class="advice-value">Â¥{ncpa:,.0f}</div>
            <div class="advice-desc">ç¾å¨ Â¥{cpa:,} â ç®æ¨ Â¥{ncpa:,.0f}</div></div>""", unsafe_allow_html=True)
    with ac4:
        nc_rate = weighted_churn * 0.5
        st.markdown(f"""<div class="advice-card">
            <div class="advice-title">è§£ç´çåæ¸</div>
            <div class="advice-value">{nc_rate*100:.1f}%</div>
            <div class="advice-desc">ç¾å¨ {weighted_churn*100:.1f}% â {nc_rate*100:.1f}%</div></div>""", unsafe_allow_html=True)

    # âââ ã°ã©ã (IMPROVEMENT 1: Proper legends + IMPROVEMENT 4: Sensitivity analysis) âââ
    st.markdown('<div class="section-title">ã°ã©ãåæ</div>', unsafe_allow_html=True)

    graph_col1, graph_col2 = st.columns([3, 1])
    with graph_col2:
        default_view = "å¹´åä½" if sim_months >= 60 else "æåä½"
        view_mode = st.radio("è¡¨ç¤ºåä½", ["æåä½", "å¹´åä½"], horizontal=True, key="view_mode",
                             index=0 if default_view == "æåä½" else 1)

    if view_mode == "å¹´åä½":
        df_yearly = df.groupby("å¹´").agg({
            "å£²ä¸é«": "sum", "å¤åè²»": "sum", "éçå©ç": "sum",
            "åºåå®£ä¼è²»": "sum", "åºå®è²»åè¨": "sum", "æ¸ä¾¡åå´è²»": "sum",
            "å¶æ¥­å©ç": "sum", "ç´¯ç©å©ç": "last", "ç´¯ç©ç¨å¼å¾å©ç": "last",
            "ç¨é¡": "sum", "ç¨ã·ã¼ã«ã": "sum", "ç¨å¼å¾å©ç": "sum",
            "æçåå²ç¹å£²ä¸": "mean", "ã­ã£ãã·ã¥æ®é«": "last",
            "æ°è¦ç²å¾": "sum", "è§£ç´æ°": "sum", "ã¢ã¯ãã£ãé¡§å®¢æ°": "last",
            "è²©å£²æ°": "sum", "äººå¡æ°": "last",
            "è²»ç¨_å¤åè²»": "sum", "è²»ç¨_åºåå®£ä¼è²»": "sum",
            "è²»ç¨_åºå®è²»": "sum", "è²»ç¨_æ¸ä¾¡åå´è²»": "sum",
            "äººä»¶è²»ï¼è¿½å æ¡ç¨ï¼": "sum",
        }).reset_index()
        df_yearly["æ"] = df_yearly["å¹´"].apply(lambda y: f"{int(y)}å¹´ç®")
        df_yearly["æçªå·"] = df_yearly["å¹´"]
        df_view = df_yearly
        x_field = "æçªå·:Q"
        x_title = "å¹´"
    else:
        df_view = df
        x_field = "æçªå·:Q"
        x_title = "æ"

    # IMPROVEMENT 1 & 4: ã°ã©ãã¿ãã«æåº¦åæãè¿½å 
    g1, g2, g3, g4, g5, g6, g7, g8, g9 = st.tabs([
        "åæ¯æ¨ç§»", "ã­ã£ãã·ã¥ãã­ã¼", "ã·ããªãªæ¯è¼",
        "ã³ã¹ãæ§é ", "é¡§å®¢æ¨ç§»", "ç¨å¹æ",
        "LTV/CACæ¨ç§»", "æåº¦åæ", "ãã¼ã¿è¡¨",
    ])

    with g1:
        # IMPROVEMENT 1: å¡ä¾ä»ãåæ¯æ¨ç§»ãã£ã¼ã
        sales_line = alt.Chart(df_view).mark_line(strokeWidth=2.5).encode(
            x=alt.X(x_field, title=x_title),
            y=alt.Y("å£²ä¸é«:Q", axis=alt.Axis(format="~s", title="éé¡ (Â¥)")),
            color=alt.value("#2196F3"),
            tooltip=["æ", alt.Tooltip("å£²ä¸é«:Q", format=",")]
        )
        bep_line = alt.Chart(df_view).mark_line(strokeDash=[4, 4]).encode(
            x=alt.X(x_field),
            y=alt.Y("æçåå²ç¹å£²ä¸:Q"),
            color=alt.value("#94A3B8"),
        )
        profit_area = alt.Chart(df_view).mark_area(opacity=0.25).encode(
            x=alt.X(x_field),
            y=alt.Y("å¶æ¥­å©ç:Q"),
            color=alt.condition(alt.datum.å¶æ¥­å©ç > 0, alt.value("#16A34A"), alt.value("#DC2626")),
        )
        # å¡ä¾ãã¼ã¿
        legend_df = pd.DataFrame([
            {"label": "å£²ä¸é«", "y": 0, "x": 0},
            {"label": "æçåå²ç¹", "y": 0, "x": 0},
            {"label": "å¶æ¥­å©ç", "y": 0, "x": 0},
        ])
        legend_chart = alt.Chart(legend_df).mark_point(size=0).encode(
            color=alt.Color("label:N",
                scale=alt.Scale(domain=["å£²ä¸é«", "æçåå²ç¹", "å¶æ¥­å©ç"],
                                range=["#2196F3", "#94A3B8", "#16A34A"]),
                legend=alt.Legend(title="å¡ä¾", orient="top"))
        )
        st.altair_chart(_dk((profit_area + sales_line + bep_line + legend_chart).interactive()), use_container_width=True)

    with g2:
        # IMPROVEMENT 1: ã­ã£ãã·ã¥ãã­ã¼ with å¡ä¾ + B4: ã¢ã©ã¼ãã©ã¤ã³
        cf_chart = alt.Chart(df_view).mark_area(opacity=0.5).encode(
            x=alt.X(x_field, title=x_title),
            y=alt.Y("ã­ã£ãã·ã¥æ®é«:Q", axis=alt.Axis(format="~s", title="Â¥ ã­ã£ãã·ã¥æ®é«")),
            color=alt.condition(alt.datum.ã­ã£ãã·ã¥æ®é« > 0, alt.value("#2196F3"), alt.value("#DC2626")),
            tooltip=["æ", alt.Tooltip("ã­ã£ãã·ã¥æ®é«:Q", format=",")]
        )
        zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#DC2626", strokeDash=[3, 3]).encode(y="y:Q")
        alert_line = alt.Chart(pd.DataFrame({"y": [fundraise_alert if 'fundraise_alert' in dir() else 3_000_000]})).mark_rule(
            color="#F59E0B", strokeDash=[6, 3], strokeWidth=2
        ).encode(y="y:Q")

        alert_label = alt.Chart(pd.DataFrame({"y": [fundraise_alert if 'fundraise_alert' in dir() else 3_000_000], "label": ["èª¿éã¢ã©ã¼ãã©ã¤ã³"]})).mark_text(
            align="left", dx=5, dy=-8, fontSize=11, color="#F59E0B", fontWeight="bold"
        ).encode(y="y:Q", text="label:N")

        st.altair_chart(_dk((cf_chart + zero_line + alert_line + alert_label).interactive()), use_container_width=True)

    with g3:
        def sc_calc(sm, cm, label):
            r = []; cum = 0; ac_list = [0] * len(rev_sources)
            for i in range(sim_months):
                u_ad2 = int(ad_budget_monthly / cpa) if cpa > 0 else 0
                nc2 = u_ad2 + int(organic_start * (organic_growth ** i))
                total_s = 0
                for sidx, rs in enumerate(rev_sources):
                    sn = int(nc2 * rs["weight"])
                    sch = int(ac_list[sidx] * rs["churn_rate"]) if use_churn else 0
                    ac_list[sidx] = max(0, ac_list[sidx] + sn - sch)
                    su = int((ac_list[sidx] if use_churn else sn) * (seasonal[i % 12] if use_season else 1))
                    total_s += int(su * rs["unit_price"] * sm)
                vc2 = (total_s * vc_pct_of_sales + int(nc2 * (seasonal[i % 12] if use_season else 1)) * vc_per_unit_fixed) * cm
                hc2 = sum(hp["count"] * hp["salary"] * 1.15 for hp in hire_plan if (i + 1) >= hp["month"])
                dep2 = sum(a["monthly_dep"] for a in dep_assets if (i + 1) > a["start_month"] and (i + 1 - a["start_month"]) <= a["useful_life"] * 12)
                cum += total_s - vc2 - ad_budget_monthly - total_fixed * cm - hc2 - dep2
                r.append({"æçªå·": i + 1, "ç´¯ç©å©ç": cum, "ã·ããªãª": label})
            return pd.DataFrame(r)

        df_all = pd.concat([sc_calc(1.2, 0.9, "æ¥½è¦³"), sc_calc(1.0, 1.0, "ä¸­åº¸"), sc_calc(0.8, 1.1, "æ²è¦³")])
        sc_ch = alt.Chart(df_all).mark_line(strokeWidth=2).encode(
            x=alt.X("æçªå·:Q", title="æ"),
            y=alt.Y("ç´¯ç©å©ç:Q", axis=alt.Axis(format="~s", title="Â¥ ç´¯ç©å©ç")),
            color=alt.Color("ã·ããªãª:N",
                scale=alt.Scale(domain=["æ¥½è¦³", "ä¸­åº¸", "æ²è¦³"],
                                range=["#16A34A", "#2196F3", "#DC2626"]),
                legend=alt.Legend(title="ã·ããªãª", orient="top")),
            tooltip=["æçªå·", "ã·ããªãª", alt.Tooltip("ç´¯ç©å©ç:Q", format=",")]
        )
        st.altair_chart(_dk(sc_ch.interactive()), use_container_width=True)

    with g4:
        # IMPROVEMENT 1: ã³ã¹ãæ§é  with æç¤ºå¡ä¾
        cost_cols = ["è²»ç¨_å¤åè²»", "è²»ç¨_åºåå®£ä¼è²»", "è²»ç¨_åºå®è²»", "è²»ç¨_æ¸ä¾¡åå´è²»"]
        cost_labels = ["å¤åè²»", "åºåå®£ä¼è²»", "åºå®è²»ï¼äººä»¶è²»è¾¼ï¼", "æ¸ä¾¡åå´è²»"]
        cost_colors = ["#F59E0B", "#EF4444", "#6366F1", "#8B5CF6"]

        cd = df_view.melt(id_vars=["æ"], value_vars=cost_cols, var_name="è²»ç¨ç¨®å¥", value_name="éé¡")
        cd["è²»ç¨ç¨®å¥"] = cd["è²»ç¨ç¨®å¥"].map(dict(zip(cost_cols, cost_labels)))

        st.altair_chart(
            _dk(alt.Chart(cd).mark_area().encode(
                x=alt.X("æ:N", sort=None, title=x_title),
                y=alt.Y("éé¡:Q", axis=alt.Axis(format="~s", title="Â¥ éé¡")),
                color=alt.Color("è²»ç¨ç¨®å¥:N",
                    scale=alt.Scale(domain=cost_labels, range=cost_colors),
                    legend=alt.Legend(title="è²»ç¨åºå", orient="top")),
                tooltip=["æ", "è²»ç¨ç¨®å¥", alt.Tooltip("éé¡:Q", format=",")]
            )),
            use_container_width=True
        )

    with g5:
        if use_churn:
            # IMPROVEMENT 1: é¡§å®¢æ¨ç§» with å¡ä¾
            cust_base = alt.Chart(df_view).encode(x=alt.X(x_field, title=x_title))
            new_bar = cust_base.mark_bar(opacity=0.6).encode(
                y=alt.Y("æ°è¦ç²å¾:Q", axis=alt.Axis(format=",", title="äººæ°")),
                color=alt.value("#BBF7D0"),
            )
            active_line = cust_base.mark_line(strokeWidth=2.5).encode(
                y=alt.Y("ã¢ã¯ãã£ãé¡§å®¢æ°:Q"),
                color=alt.value("#2196F3"),
            )
            legend_cust = alt.Chart(pd.DataFrame([
                {"label": "æ°è¦ç²å¾", "y": 0}, {"label": "ã¢ã¯ãã£ãé¡§å®¢æ°", "y": 0}
            ])).mark_point(size=0).encode(
                color=alt.Color("label:N",
                    scale=alt.Scale(domain=["æ°è¦ç²å¾", "ã¢ã¯ãã£ãé¡§å®¢æ°"],
                                    range=["#BBF7D0", "#2196F3"]),
                    legend=alt.Legend(title="å¡ä¾", orient="top"))
            )
            st.altair_chart(_dk((new_bar + active_line + legend_cust).interactive()), use_container_width=True)
        else:
            st.info("è§£ç´çãONã«ããã¨é¡§å®¢æ¨ç§»ã°ã©ããè¡¨ç¤ºããã¾ã")

    with g6:
        # B3: ç¨å¹æãã£ã¼ã
        tax_base = alt.Chart(df_view).encode(x=alt.X(x_field, title=x_title))
        op_line = tax_base.mark_line(strokeWidth=2).encode(
            y=alt.Y("å¶æ¥­å©ç:Q", axis=alt.Axis(format="~s", title="éé¡ (Â¥)")),
            color=alt.value("#2196F3"),
        )
        net_line = tax_base.mark_line(strokeWidth=2).encode(
            y=alt.Y("ç¨å¼å¾å©ç:Q"),
            color=alt.value("#16A34A"),
        )
        tax_bar = tax_base.mark_bar(opacity=0.3).encode(
            y=alt.Y("ç¨é¡:Q"),
            color=alt.value("#EF4444"),
        )
        shield_line = tax_base.mark_line(strokeDash=[4, 4], strokeWidth=1.5).encode(
            y=alt.Y("ç¨ã·ã¼ã«ã:Q"),
            color=alt.value("#8B5CF6"),
        )
        legend_tax = alt.Chart(pd.DataFrame([
            {"label": "å¶æ¥­å©ç", "y": 0}, {"label": "ç¨å¼å¾å©ç", "y": 0},
            {"label": "ç¨é¡", "y": 0}, {"label": "ç¨ã·ã¼ã«ãï¼åå´ï¼", "y": 0},
        ])).mark_point(size=0).encode(
            color=alt.Color("label:N",
                scale=alt.Scale(
                    domain=["å¶æ¥­å©ç", "ç¨å¼å¾å©ç", "ç¨é¡", "ç¨ã·ã¼ã«ãï¼åå´ï¼"],
                    range=["#2196F3", "#16A34A", "#EF4444", "#8B5CF6"]),
                legend=alt.Legend(title="å¡ä¾", orient="top"))
        )
        st.altair_chart(_dk((tax_bar + op_line + net_line + shield_line + legend_tax).interactive()), use_container_width=True)

    with g7:
        # B5: LTV/CACæ¨ç§»ãã£ã¼ã
        ltv_cac_data = []
        ac_tracking = [0] * len(rev_sources)
        for i in range(sim_months):
            m = i + 1
            sf = seasonal[i % 12] if use_season else 1.0
            u_ad2 = int(ad_budget_monthly / cpa) if cpa > 0 else 0
            nc2 = u_ad2 + int(organic_start * (organic_growth ** i))
            total_s = 0; total_u = 0; w_churn = 0
            for sidx, rs in enumerate(rev_sources):
                sn = int(nc2 * rs["weight"])
                sch = int(ac_tracking[sidx] * rs["churn_rate"]) if use_churn else 0
                ac_tracking[sidx] = max(0, ac_tracking[sidx] + sn - sch)
                su = int((ac_tracking[sidx] if use_churn else sn) * sf)
                total_s += int(su * rs["unit_price"])
                total_u += su
                w_churn += rs["churn_rate"] * rs["weight"]

            if total_u > 0 and w_churn > 0:
                arpu = total_s / total_u
                m_ltv = arpu / w_churn
                m_cac = cpa
                m_ratio = m_ltv / m_cac if m_cac > 0 else 0
            else:
                m_ltv = 0; m_cac = cpa; m_ratio = 0

            ltv_cac_data.append({"æçªå·": m, "LTV": m_ltv, "CAC": m_cac, "LTV/CACæ¯ç": m_ratio})

        lc_df = pd.DataFrame(ltv_cac_data)
        # LTV/CACæ¯çã®æ¨ç§»
        ratio_line = alt.Chart(lc_df).mark_line(strokeWidth=2.5, color="#2196F3").encode(
            x=alt.X("æçªå·:Q", title="æ"),
            y=alt.Y("LTV/CACæ¯ç:Q", title="LTV / CAC æ¯ç"),
            tooltip=["æçªå·", alt.Tooltip("LTV/CACæ¯ç:Q", format=".1f"),
                      alt.Tooltip("LTV:Q", format=",.0f"), alt.Tooltip("CAC:Q", format=",")]
        )
        health_line = alt.Chart(pd.DataFrame({"y": [3.0], "label": ["å¥å¨ã©ã¤ã³ (3.0x)"]})).mark_rule(
            color="#16A34A", strokeDash=[6, 3], strokeWidth=2
        ).encode(y="y:Q")
        health_text = alt.Chart(pd.DataFrame({"y": [3.0], "label": ["3.0x å¥å¨ã©ã¤ã³"]})).mark_text(
            align="left", dx=5, dy=-8, fontSize=11, color="#16A34A", fontWeight="bold"
        ).encode(y="y:Q", text="label:N")

        st.altair_chart(_dk((ratio_line + health_line + health_text).interactive()), use_container_width=True)

        # LTV vs CAC éé¡æ¨ç§»
        lc_melt = lc_df.melt(id_vars=["æçªå·"], value_vars=["LTV", "CAC"], var_name="ææ¨", value_name="éé¡")
        lc_chart2 = alt.Chart(lc_melt).mark_line(strokeWidth=2).encode(
            x=alt.X("æçªå·:Q", title="æ"),
            y=alt.Y("éé¡:Q", axis=alt.Axis(format="~s", title="Â¥ éé¡")),
            color=alt.Color("ææ¨:N",
                scale=alt.Scale(domain=["LTV", "CAC"], range=["#2196F3", "#EF4444"]),
                legend=alt.Legend(title="ææ¨", orient="top")),
            tooltip=["æçªå·", "ææ¨", alt.Tooltip("éé¡:Q", format=",")]
        )
        st.altair_chart(_dk(lc_chart2.interactive()), use_container_width=True)

    with g8:
        # IMPROVEMENT 4: æåº¦åæ (ãã«ãã¼ããã£ã¼ã)
        st.markdown("**ãã©ã¡ã¼ã¿ã®Â±20%å¤åããã¡ã¤ãã«æã®å¶æ¥­å©çã«ä¸ããå½±é¿**")

        sensitivity_params = {
            "å®¢åä¾¡": ("weighted_price", 0.8, 1.2),
            "CPA": ("cpa", 0.8, 1.2),
            "åºåäºç®": ("ad_budget_monthly", 0.8, 1.2),
            "åºå®è²»": ("total_fixed", 0.8, 1.2),
            "å¤åè²»ç": ("vc_pct_of_sales", 0.8, 1.2),
            "è§£ç´ç": ("weighted_churn", 0.8, 1.2),
        }

        sensitivity_results = []
        baseline_profit = last["å¶æ¥­å©ç"]

        for param_name, (param_var, low_mult, high_mult) in sensitivity_params.items():
            # ã·ãã¥ã¬ã¼ã·ã§ã³ç¨ã®ãã¼ã¹å¤ãåå¾
            base_val = eval(param_var) if param_var in ["weighted_price", "cpa", "ad_budget_monthly", "total_fixed", "vc_pct_of_sales", "weighted_churn"] else 0

            # ä½ã·ããªãªã¨é«ã·ããªãªãè¨ç®
            for scenario_mult, scenario_name in [(low_mult, "Low"), (high_mult, "High")]:
                temp_profit = baseline_profit
                if param_var == "weighted_price":
                    temp_price = weighted_price * scenario_mult
                    temp_margin = temp_price - vc_per_unit_fixed - temp_price * vc_pct_of_sales
                    temp_profit = (last["è²©å£²æ°"] * temp_margin) - ad_budget_monthly - total_fixed_with_hire - monthly_depreciation
                elif param_var == "cpa":
                    temp_cpa = cpa * scenario_mult
                    temp_new = int(ad_budget_monthly / temp_cpa) if temp_cpa > 0 else 0
                    temp_profit = last["å£²ä¸é«"] - last["å¤åè²»"] - ad_budget_monthly - total_fixed_with_hire - monthly_depreciation
                elif param_var == "ad_budget_monthly":
                    temp_ad = ad_budget_monthly * scenario_mult
                    temp_profit = last["å£²ä¸é«"] - last["å¤åè²»"] - temp_ad - total_fixed_with_hire - monthly_depreciation
                elif param_var == "total_fixed":
                    temp_fixed = total_fixed * scenario_mult
                    temp_profit = last["å£²ä¸é«"] - last["å¤åè²»"] - ad_budget_monthly - (temp_fixed + hire_cost) - monthly_depreciation
                elif param_var == "vc_pct_of_sales":
                    temp_vc_pct = vc_pct_of_sales * scenario_mult
                    temp_vc = last["è²©å£²æ°"] * vc_per_unit_fixed + last["å£²ä¸é«"] * temp_vc_pct
                    temp_profit = last["å£²ä¸é«"] - temp_vc - ad_budget_monthly - total_fixed_with_hire - monthly_depreciation
                elif param_var == "weighted_churn":
                    temp_churn = weighted_churn * scenario_mult
                    temp_profit = baseline_profit

                sensitivity_results.append({
                    "parameter": param_name,
                    "scenario": scenario_name,
                    "profit_change": temp_profit - baseline_profit
                })

        sens_df = pd.DataFrame(sensitivity_results)
        sens_pivot = sens_df.pivot(index="parameter", columns="scenario", values="profit_change").reset_index()
        sens_pivot["Impact Range"] = sens_pivot["High"] - sens_pivot["Low"]
        sens_pivot = sens_pivot.sort_values("Impact Range", ascending=True)

        # ãã«ãã¼ããã£ã¼ãã®æç»
        tornado_data = []
        for idx, row in sens_pivot.iterrows():
            tornado_data.append({"Parameter": row["parameter"], "Impact": row["Low"], "Direction": "Low"})
            tornado_data.append({"Parameter": row["parameter"], "Impact": row["High"], "Direction": "High"})

        tornado_df = pd.DataFrame(tornado_data)
        tornado_chart = alt.Chart(tornado_df).mark_bar().encode(
            x=alt.X("Impact:Q", title="å¶æ¥­å©çã¸ã®å½±é¿ (Â¥)"),
            y=alt.Y("Parameter:N", title="ãã©ã¡ã¼ã¿", sort=list(sens_pivot["parameter"])),
            color=alt.Color("Direction:N",
                scale=alt.Scale(domain=["Low", "High"], range=["#EF4444", "#16A34A"]),
                legend=alt.Legend(title="å¤åæ¹å", orient="right")),
            tooltip=["Parameter", alt.Tooltip("Impact:Q", format=",.0f"), "Direction"]
        )
        st.altair_chart(_dk(tornado_chart), use_container_width=True)

    with g9:
        st.dataframe(df_view, use_container_width=True)

    # âââ ã¨ã¯ã¹ãã¼ã âââ
    st.markdown('<div class="section-title">ãã¼ã¿ã¨ã¯ã¹ãã¼ã</div>', unsafe_allow_html=True)
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.download_button("CSV ãã¦ã³ã­ã¼ã", df.to_csv(index=False).encode("utf-8-sig"),
                           "simulation.csv", "text/csv", use_container_width=True)
    with ec2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df.to_excel(w, index=False, sheet_name="PL")
        st.download_button("Excel ãã¦ã³ã­ã¼ã", buf.getvalue(), "simulation.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with ec3:
        st.button("PDF ã¬ãã¼ãï¼Phase 2ï¼", disabled=True, use_container_width=True)


# âââââââââââââââââââââââââââââââââââââââââââââââ
# TAB 2 â AI ã¢ããã¤ã¶ã¼ï¼UI ã¢ãã¯ï¼
# âââââââââââââââââââââââââââââââââââââââââââââââ
with tab_ai:
    st.markdown("""
    <div class="cs-banner">
        â¡ <strong>Coming Soon â Phase 2</strong>
        ãã®ã¿ãã¯æ©è½ã¤ã¡ã¼ã¸ã§ãããã¢ãªã³ã°ç¨ãã¬ãã¥ã¼ã¨ãã¦ãç¢ºèªãã ããã
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### AI ã¢ããã¤ã¶ã¼")
    st.caption("ããªãã®äºæ¥­è¨ç»ããªã¢ã«ã¿ã¤ã ã§åæããå·ä½çãªæ¹åææ¡ãèªåçæãã¾ãã")

    st.markdown("""
    <div style="max-width:680px; margin-top:8px;">
        <div class="ai-bubble">
            <div class="ai-label">Biz Maker AI Â· åæçµæ</div>
            å¥åãããäºæ¥­è¨ç»ãåæãã¾ãããä»¥ä¸ãä¸»ãªæè¦ã§ãã<br><br>
            <strong>1. ã­ã£ãã·ã¥ãã­ã¼è­¦å</strong><br>
            ç¾å¨ã®å¥éãµã¤ã¯ã«ã¨æ¯æãµã¤ã¯ã«ã®ãºã¬ã«ããã4ã6ã¶æç®ã«ã­ã£ãã·ã¥ãã¿ã¤ãã«ãªãå¯è½æ§ãããã¾ãã
            éè»¢è³éã¨ãã¦ 300ã500ä¸åã®äºåãç¢ºä¿ãããã¨ãæ¨å¥¨ãã¾ãã<br><br>
            <strong>2. LTV / CAC æ¯ç</strong><br>
            ç¾å¨ã®æ¯çã¯ 2.4x ã§ãæ¥­çå¥å¨ã©ã¤ã³ã® 3.0x ãä¸åã£ã¦ãã¾ãã
            è§£ç´çã 1ã2% æ¹åããã ãã§æ¯çã 3.6x ã¾ã§æ¹åããåçæ§ãå¤§å¹ã«åä¸ãã¾ãã<br><br>
            <strong>3. å­£ç¯å¤åãªã¹ã¯</strong><br>
            SaaSæ¥­ç¨®ã®å ´åã7ã8æã«å£²ä¸ãç´ 5% ä½ä¸ããå¾åãããã¾ãã
            ãã®ææã«åãããå¹´æ¬¡å¥ç´ãã©ã³ã®æä¾ãæ¤è¨ãã¦ã¿ã¦ãã ããã
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**AI ã«è³ªåãã**")
    col_q, col_send = st.columns([6, 1])
    with col_q:
        user_q = st.text_input("", placeholder="ä¾: è§£ç´çãæ¹åããããã®å·ä½çãªæ½ç­ãæãã¦", label_visibility="collapsed")
    with col_send:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("éä¿¡", use_container_width=True):
            st.info("Phase 2 ã§ã¯ Claude API ãæ¥ç¶ãããªã¢ã«ã¿ã¤ã ã§åç­ãã¾ãã")

    st.markdown('<div class="section-title">ããããè³ªå</div>', unsafe_allow_html=True)
    qa_cols = st.columns(3)
    questions = [
        ("è§£ç´çã®æ¹åç­", "ã«ã¹ã¿ãã¼ãµã¯ã»ã¹ã®å¼·åã¨ãªã³ãã¼ãã£ã³ã°æ¹åãæãå¹æçã§ãã"),
        ("è³éèª¿éã®ã¿ã¤ãã³ã°", "ã©ã³ã¦ã§ã¤ã6ã¶æãä¸åãåã«èª¿éæ´»åãå§ãããã¨ãæ¨å¥¨ãã¾ãã"),
        ("CPA ãä¸ããæ¹æ³", "SEOå¼·åã«ããèªç¶æµå¥ã®å¢å ã¨ããªã¿ã¼ã²ãã£ã³ã°åºåã®æé©åãæå¹ã§ãã"),
    ]
    for col, (q, a) in zip(qa_cols, questions):
        with col:
            with st.expander(q):
                st.markdown(f"<div style='font-size:0.83rem;color:#374151;line-height:1.6;'>{a}<br><br><em style='color:#9CA3AF;'>Phase 2 ã§ã¯ AIãäºæ¥­è¨ç»ãã¼ã¿ãåç§ããä¸ã§åç­ãã¾ãã</em></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">ä¼è©±ä¾ãã¬ãã¥ã¼</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-wrap" style="background:#F8FAFC;border-radius:12px;padding:16px;border:1px solid #E8ECF0;">
        <div style="float:right;clear:both;">
            <div class="user-bubble">è§£ç´çãä¸ããã«ã¯ã©ãããã°ããã§ããï¼</div>
        </div>
        <div style="clear:both; margin-top:8px;">
            <div class="ai-bubble" style="max-width:90%;">
                <div class="ai-label">Biz Maker AI</div>
                è§£ç´çæ¹åã«ã¯ä¸»ã«3ã¤ã®ã¢ãã­ã¼ããå¹æçã§ãï¼<br>
                â  ãªã³ãã¼ãã£ã³ã°ã®å¼·åï¼æåã®30æ¥ãéµï¼<br>
                â¡ ãã­ãã¯ãåã§ã®ä¾¡å¤æä¾ã®å¯è¦åï¼ããã·ã¥ãã¼ãç­ï¼<br>
                â¢ ãã«ã¹ã¹ã³ã¢ã«ããæ©æãã£ã¼ã³äºæ¸¬ã¨ä»å¥<br><br>
                å¾¡ç¤¾ã®ç¾å¨ã®è§£ç´çãæ¹åããå ´åãLTVãå¤§å¹ã«åä¸ããåçæ§ãæ¹åãã¾ãã
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# âââââââââââââââââââââââââââââââââââââââââââââââ
# TAB 3 â å°éå®¶ã«ç¸è«ï¼UI ã¢ãã¯ï¼
# âââââââââââââââââââââââââââââââââââââââââââââââ
with tab_cons:
    st.markdown("""
    <div class="cs-banner">
        â¡ <strong>Coming Soon â Phase 2</strong>
        ãã®ã¿ãã¯æ©è½ã¤ã¡ã¼ã¸ã§ãããã¢ãªã³ã°ç¨ãã¬ãã¥ã¼ã¨ãã¦ãç¢ºèªãã ããã
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### å°éå®¶ãããã³ã°")
    st.caption("ããªãã®äºæ¥­ãã§ã¼ãºã¨èª²é¡ã«åã£ãå°éå®¶ãè¦ã¤ãã¦ãç´æ¥ç¸è«ã§ãã¾ãã")

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.selectbox("å°éåé", ["ãã¹ã¦","è²¡åã»ä¼è¨","ãã¼ã±ãã£ã³ã°","æ³å","ITã»éçº","äººäºã»çµç¹"])
    with fc2:
        st.selectbox("æéå¸¯", ["ãã¹ã¦","ã5,000å/30å","5,000ã10,000å","10,000åã"])
    with fc3:
        st.selectbox("è©ä¾¡", ["ãã¹ã¦","â 4.5ä»¥ä¸","â 4.0ä»¥ä¸"])
    with fc4:
        st.selectbox("å¯¾å¿å½¢å¼", ["ãã¹ã¦","ãªã³ã©ã¤ã³","å¯¾é¢","é»è©±"])

    st.markdown("---")
    consultants = [
        {"initials":"TT","name":"ç°ä¸­ å¤ªé","field":"è²¡åã»ä¼è¨",
         "desc":"å¸èªä¼è¨å£«ãã¹ã¿ã¼ãã¢ããã®è³éèª¿éã»äºæ¥­è¨ç»ç­å®ã 200ç¤¾ä»¥ä¸æ¯æ´ãåBigFouråºèº«ãSaaSãã¸ãã¹ã®è²¡åã¢ãã«è¨­è¨ãå°éã",
         "rating":"4.9","reviews":128,"price":"Â¥8,000 / 30å","badge":"ããªãã®äºæ¥­è¨ç»ã«ããã","tags":["è²¡åã¢ãã«","è³éèª¿é","SaaS"]},
        {"initials":"HK","name":"é´æ¨ è±å­","field":"ãã¼ã±ãã£ã³ã°",
         "desc":"åGoogleãD2Cã»SaaSã®ã°ã­ã¼ã¹ãã¼ã±ãã£ã³ã°ãå°éã¨ããCPAæ¹åã»LTVåä¸ã®å®ç¸¾å¤æ°ãã³ã³ãã³ãSEOããPaid Socialã¾ã§å¹åºãå¯¾å¿ã",
         "rating":"4.8","reviews":94,"price":"Â¥10,000 / 30å","badge":"CPAæ¹åã®å®ç¸¾å¤æ°","tags":["ã°ã­ã¼ã¹","SEO","åºåéç¨"]},
        {"initials":"IY","name":"å±±ç° ä¸é","field":"æ³å",
         "desc":"å¼è­·å£«ãã¹ã¿ã¼ãã¢ããã®æ³åå¨è¬ï¼å©ç¨è¦ç´ã»ãã©ã¤ãã·ã¼ããªã·ã¼ã»å¥ç´æ¸ä½æï¼ããIPOæºåã¾ã§ä¸æ°éè²«ã§å¯¾å¿ãåå30åç¡æã",
         "rating":"4.6","reviews":67,"price":"Â¥12,000 / 30å","badge":"ååç¡æç´è«ãã","tags":["å¥ç´æ¸","IPO","è¦ç´ä½æ"]},
    ]
    for cons in consultants:
        st.markdown(f"""
        <div class="consultant-card">
            <div style="display:flex; gap:16px; align-items:flex-start;">
                <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#667EEA,#764BA2);
                    display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:1.1rem;flex-shrink:0;">
                    {cons['initials']}
                </div>
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                        <span class="cons-name">{cons['name']}</span>
                        <span class="cons-field">{cons['field']}</span>
                        <span class="cons-badge">{cons['badge']}</span>
                    </div>
                    <div class="cons-desc">{cons['desc']}</div>
                    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
                        <div class="cons-meta">â {cons['rating']} ({cons['reviews']} ä»¶ã®ã¬ãã¥ã¼)</div>
                        <div class="cons-meta" style="font-weight:600;color:#1A1A2E;">{cons['price']}</div>
                        <div>{''.join(f'<span class="tag">{t}</span>' for t in cons['tags'])}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"ç¸è«ãäºç´ãã â {cons['name']}", key=f"book_{cons['name']}"):
            st.info("Phase 2 ã§ã¯å°éå®¶ã®ã«ã¬ã³ãã¼ã¨é£æºãã¦ç´æ¥äºç´ã§ãã¾ãã")


# âââââââââââââââââââââââââââââââââââââââââââââââ
# TAB 4 â ã³ãã¥ããã£ï¼UI ã¢ãã¯ï¼
# âââââââââââââââââââââââââââââââââââââââââââââââ
with tab_sns:
    st.markdown("""
    <div class="cs-banner">
        â¡ <strong>Coming Soon â Phase 2</strong>
        ãã®ã¿ãã¯æ©è½ã¤ã¡ã¼ã¸ã§ãããã¢ãªã³ã°ç¨ãã¬ãã¥ã¼ã¨ãã¦ãç¢ºèªãã ããã
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ã³ãã¥ããã£")
    st.caption("åããã§ã¼ãºã®èµ·æ¥­å®¶ã»çµå¶èã¨ç¹ãããäºæ¥­è¨ç»ã®ãã£ã¼ãããã¯ãäº¤æãã¾ãããã")

    with st.expander("æç¨ãä½æãã", expanded=False):
        post_txt = st.text_area("åå®¹", placeholder="äºæ¥­è¨ç»ã«ã¤ãã¦ç¸è«ããããã¨ãå­¦ãã ãã¨ãã·ã§ã¢ãã¾ãããâ¦", height=100)
        tag_opts = st.multiselect("ã¿ã°", ["#SaaS","#EC","#é££é£","#ã³ã³ãµã«","#è³éèª¿é","#ãã¼ã±","#è§£ç´çæ¹å","#åæé¡§å®¢ç²å¾"])
        if st.button("æç¨¿ãã", key="post_btn"):
            st.info("Phase 2 ã§å®è£äºå®ã§ãã")

    st.markdown("---")
    posts = [
        {"initials":"SM","name":"ä½è¤ ç¾å²","sub":"SaaS Â· åµæ¥­2å¹´ç®",
         "content":"è§£ç´çã 8% â 2.8% ã«æ¹åã§ãã¾ãã\næ½ç­ã¯ããªã³ãã¼ãã£ã³ã°ãã­ã¼ãã®ææ¬çãªè¦ç´ããç¹ã«ååã­ã°ã¤ã³ãã7æ¥éã®ã¡ã¼ã«èªååãå¹ãã¾ããã",
         "tags":["#SaaS","#è§£ç´çæ¹å"],"likes":38,"comments":14,"time":"2æéå"},
        {"initials":"KT","name":"é«æ© å¥å¤ª","sub":"é£²é£åº Â· 2åºèéå¶",
         "content":"ãã®ã·ãã¥ã¬ã¼ã¿ã¼ã§12æã®å­£ç¯å¤åãå¥ãã¦ã·ãã¥ã¬ã¼ã·ã§ã³ãã¦ã¿ãããåºå®è²»ã®æ¯çãé«ããããã¨ã«æ°ã¥ãã¾ãããæ¥­åå§è¨ã®æ¯çãè¦ç´ãã¦æ30ä¸åã®ã³ã¹ãæ¹åãã§ãããã§ãã",
         "tags":["#é£²é£","#åºå®è²»åæ¸"],"likes":22,"comments":9,"time":"5æéå"},
        {"initials":"RW","name":"æ¸¡è¾º ç¿","sub":"ã³ã³ãµã«ãã£ã³ã° Â· ç¬ç«1å¹´ç®",
         "content":"LTV/CAC ã 2.1x ã§æ©ãã§ãã¾ããã³ã³ãµã«ãã¸ãã¹ã§CACãä¸ããæ¹æ³ãæãã¦ãã ãããä»ã¯ç´¹ä»ãã­ã°ã©ã ã®å°å¥ãæ¤è¨ä¸­ã§ãã",
         "tags":["#ã³ã³ãµã«","#LTV","#CAC"],"likes":45,"comments":21,"time":"1æ¥å"},
    ]
    for post in posts:
        content_html = post["content"].replace("\n", "<br>")
        tags_html = " ".join(f'<span class="tag">{t}</span>' for t in post["tags"])
        st.markdown(f"""
        <div class="post-card">
            <div class="post-header">
                <div class="post-avatar">{post['initials']}</div>
                <div class="post-meta">
                    <div class="name">{post['name']}</div>
                    <div class="sub">{post['sub']} Â· {post['time']}</div>
                </div>
            </div>
            <div class="post-content">{content_html}</div>
            <div style="margin-top:8px;">{tags_html}</div>
            <div class="post-actions">
                <span class="post-action">ð {post['likes']}</span>
                <span class="post-action">ð¬ {post['comments']} ã³ã¡ã³ã</span>
                <span class="post-action">ð ä¿å­</span>
                <span class="post-action">â ã·ã§ã¢</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"ã³ã¡ã³ããã â {post['name']}", key=f"cmt_{post['name']}", type="secondary"):
            st.info("Phase 2 ã§å®è£äºå®ã§ãã")

# âââ ããã¿ã¼ âââ
st.markdown("""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #E8ECF0;text-align:center;color:#9CA3AF;font-size:0.75rem;">
    Biz Maker â ãã¸ãã¹ãµåµãã©ãããã©ã¼ã  v5.0 â ãã©ãã·ã¥ã¢ããç &nbsp;|&nbsp; Phase 1 Enhanced &nbsp;|&nbsp; Powered by Streamlit
</div>
""", unsafe_allow_html=True)
