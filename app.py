import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Biz Maker — ビジネス共創プラットフォーム",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ── フォント・ベース ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ── ヘッダーを非表示 ── */
  #MainMenu, header, footer { visibility: hidden; }

  /* ── ページ余白 ── */
  .main .block-container { padding: 1.2rem 2rem 2rem; }

  /* ── ナビバー ── */
  .top-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 0; margin-bottom: 1rem;
    border-bottom: 2px solid #E8ECF0;
  }
  .top-nav .logo { font-size: 2.0rem; font-weight: 700; color: #1A1A2E; letter-spacing: -0.5px; }
  .top-nav .logo span { color: #2196F3; }
  .top-nav .tagline { font-size: 0.85rem; color: #8A94A6; margin-top: 2px; }
  .nav-badge {
    background: #FFF3CD; color: #856404; border-radius: 20px;
    padding: 2px 10px; font-size: 0.7rem; font-weight: 600; border: 1px solid #FFECB5;
  }

  /* ── KPIカード ── */
  .kpi-grid { display: flex; gap: 12px; flex-wrap: wrap; margin: 1rem 0; }
  .kpi-card {
    flex: 1; min-width: 140px;
    background: #FFFFFF; border: 1px solid #E8ECF0; border-radius: 12px;
    padding: 14px 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .kpi-card .label { font-size: 0.72rem; color: #8A94A6; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
  .kpi-card .value { font-size: 1.35rem; font-weight: 700; color: #1A1A2E; margin: 4px 0 2px; line-height: 1.2; }
  .kpi-card .delta { font-size: 0.75rem; }
  .kpi-card .delta.up { color: #16A34A; }
  .kpi-card .delta.down { color: #DC2626; }
  .kpi-card .delta.neutral { color: #8A94A6; }
  .kpi-card.accent { border-left: 4px solid #2196F3; }
  .kpi-card.success { border-left: 4px solid #16A34A; }
  .kpi-card.danger { border-left: 4px solid #DC2626; }
  .kpi-card.warn { border-left: 4px solid #F59E0B; }

  /* ── セクションタイトル ── */
  .section-title {
    font-size: 0.85rem; font-weight: 600; color: #4B5563;
    text-transform: uppercase; letter-spacing: 0.8px; margin: 1.4rem 0 0.6rem;
    padding-bottom: 6px; border-bottom: 1px solid #F0F2F5;
  }

  /* ── 改善提案カード ── */
  .advice-card {
    background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
    padding: 14px 16px; margin: 6px 0;
  }
  .advice-card .advice-title { font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 4px; }
  .advice-card .advice-value { font-size: 1.05rem; font-weight: 700; color: #1A1A2E; }
  .advice-card .advice-desc { font-size: 0.75rem; color: #94A3B8; margin-top: 3px; }

  /* ── ステップバー ── */
  .step-bar { display: flex; gap: 0; margin: 0.8rem 0 1.2rem; }
  .step-item { flex: 1; text-align: center; padding: 8px 4px; font-size: 0.72rem; font-weight: 500;
    border-bottom: 3px solid #E8ECF0; color: #9CA3AF; }
  .step-item.active { border-bottom: 3px solid #2196F3; color: #2196F3; font-weight: 600; }
  .step-item.done { border-bottom: 3px solid #16A34A; color: #16A34A; }

  /* ── AIチャット ── */
  .ai-bubble {
    background: linear-gradient(135deg, #667EEA, #764BA2);
    color: #fff; border-radius: 0 14px 14px 14px;
    padding: 14px 18px; margin: 8px 0 8px 8px;
    font-size: 0.88rem; line-height: 1.65;
    box-shadow: 0 2px 8px rgba(102,126,234,0.3);
    max-width: 85%;
  }
  .ai-label { font-size: 0.7rem; font-weight: 700; opacity: 0.8; margin-bottom: 6px; letter-spacing: 0.5px; }
  .user-bubble {
    background: #F1F5F9; color: #1E293B; border-radius: 14px 0 14px 14px;
    padding: 12px 16px; margin: 8px 8px 8px auto; font-size: 0.87rem;
    max-width: 75%; text-align: right; float: right; clear: both;
  }
  .chat-wrap { overflow: hidden; }

  /* ── コンサルカード ── */
  .consultant-card {
    background: #FFFFFF; border: 1px solid #E8ECF0; border-radius: 14px;
    padding: 20px; margin: 10px 0; transition: all 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .consultant-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.09); border-color: #CBD5E1; }
  .cons-name { font-size: 1.0rem; font-weight: 700; color: #1A1A2E; }
  .cons-field { font-size: 0.75rem; color: #2196F3; font-weight: 600; background: #EFF6FF; padding: 2px 8px; border-radius: 20px; }
  .cons-desc { font-size: 0.82rem; color: #64748B; margin: 8px 0; line-height: 1.5; }
  .cons-meta { font-size: 0.78rem; color: #94A3B8; }
  .cons-badge { background: #ECFDF5; color: #16A34A; border-radius: 20px; padding: 2px 10px;
    font-size: 0.72rem; font-weight: 600; border: 1px solid #BBF7D0; display: inline-block; margin: 4px 0; }

  /* ── SNS投稿カード ── */
  .post-card {
    background: #FFFFFF; border: 1px solid #E8ECF0; border-radius: 12px;
    padding: 16px; margin: 10px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .post-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .post-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #667EEA, #764BA2);
    display: flex; align-items: center; justify-content: center; color: white; font-size: 0.85rem; font-weight: 700; }
  .post-meta .name { font-weight: 600; font-size: 0.88rem; color: #1A1A2E; }
  .post-meta .sub { font-size: 0.72rem; color: #94A3B8; }
  .post-content { font-size: 0.85rem; color: #374151; line-height: 1.65; }
  .post-actions { display: flex; gap: 20px; margin-top: 12px; padding-top: 10px; border-top: 1px solid #F1F5F9; }
  .post-action { font-size: 0.78rem; color: #9CA3AF; cursor: pointer; font-weight: 500; }
  .tag { background: #EFF6FF; color: #3B82F6; border-radius: 4px; padding: 1px 6px;
    font-size: 0.7rem; font-weight: 600; display: inline-block; margin: 2px; }

  /* ── Coming Soonバッジ ── */
  .cs-banner {
    background: linear-gradient(90deg, #FFF7ED, #FFF3CD);
    border: 1px solid #FED7AA; border-radius: 10px;
    padding: 10px 16px; margin-bottom: 16px;
    font-size: 0.82rem; color: #92400E; font-weight: 500;
  }

  /* ── エクスポートボタンエリア ── */
  .export-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 0.5rem; }

  /* ── Metric override ── */
  div[data-testid="stMetric"] {
    background: #F8FAFC; border-radius: 10px; padding: 12px 14px;
    border: 1px solid #E8ECF0; box-shadow: none;
  }

  /* ── Button styling ── */
  div[data-testid="stButton"] > button {
    border-radius: 8px; font-weight: 500; font-size: 0.85rem;
    padding: 6px 14px; transition: all 0.2s;
  }

/* -- Tab Orange Button Style -- */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 14px; border-bottom: none !important;
    background: transparent; padding: 10px 0;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background: linear-gradient(180deg, #F97316 0%, #EA580C 100%);
    color: #fff !important; border-radius: 50px;
    padding: 14px 32px; font-weight: 700; font-size: 0.95rem;
    border: none !important; letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(234,88,12,0.35), inset 0 1px 0 rgba(255,255,255,0.25);
    transition: all 0.25s ease; text-shadow: 0 1px 2px rgba(0,0,0,0.15);
    cursor: pointer; position: relative; overflow: hidden;
}
div[data-testid="stTabs"] [data-baseweb="tab"]::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, transparent 60%);
    border-radius: 50px; pointer-events: none;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: linear-gradient(180deg, #FB923C 0%, #F97316 100%);
    box-shadow: 0 6px 22px rgba(249,115,22,0.45);
    transform: translateY(-2px);
}
div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, #EA580C 0%, #C2410C 100%) !important;
    box-shadow: 0 2px 8px rgba(194,65,12,0.4), inset 0 2px 4px rgba(0,0,0,0.15) !important;
    transform: translateY(1px);
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] > div { color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 業種テンプレート
# ─────────────────────────────────────────────
INDUSTRY_TEMPLATES = {
    "カスタム": {
        "unit_price": 5000, "ad_budget": 1_000_000, "cpa": 2000,
        "organic_start": 50, "organic_growth": 5.0, "churn_rate": 5.0,
        "vc_cogs": 1000, "vc_shipping": 600, "vc_server": 50,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 2_500_000, "fc_insurance": 400_000, "fc_outsourcing": 300_000,
        "fc_rent": 150_000, "fc_system": 50_000, "fc_misc": 100_000,
        "seasonal": [1.0]*12,
    },
    "SaaS / サブスク": {
        "unit_price": 9800, "ad_budget": 800_000, "cpa": 8000,
        "organic_start": 30, "organic_growth": 8.0, "churn_rate": 3.0,
        "vc_cogs": 0, "vc_shipping": 0, "vc_server": 200,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 3_000_000, "fc_insurance": 450_000, "fc_outsourcing": 500_000,
        "fc_rent": 100_000, "fc_system": 150_000, "fc_misc": 100_000,
        "seasonal": [1.0,1.0,1.05,1.0,1.0,1.0,0.95,0.95,1.05,1.05,1.0,0.95],
    },
    "EC / 通販": {
        "unit_price": 4500, "ad_budget": 1_500_000, "cpa": 2500,
        "organic_start": 100, "organic_growth": 3.0, "churn_rate": 15.0,
        "vc_cogs": 1800, "vc_shipping": 800, "vc_server": 30,
        "vc_payment_rate": 3.6, "vc_platform_fee": 8.0,
        "fc_salary": 2_000_000, "fc_insurance": 300_000, "fc_outsourcing": 200_000,
        "fc_rent": 200_000, "fc_system": 80_000, "fc_misc": 120_000,
        "seasonal": [0.8,0.8,1.0,0.9,0.9,1.0,1.1,0.9,0.9,1.0,1.2,1.5],
    },
    "飲食店": {
        "unit_price": 1200, "ad_budget": 300_000, "cpa": 500,
        "organic_start": 200, "organic_growth": 2.0, "churn_rate": 25.0,
        "vc_cogs": 400, "vc_shipping": 0, "vc_server": 0,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 1_800_000, "fc_insurance": 270_000, "fc_outsourcing": 50_000,
        "fc_rent": 300_000, "fc_system": 30_000, "fc_misc": 150_000,
        "seasonal": [0.8,0.85,1.0,1.0,1.0,0.9,0.95,0.85,0.95,1.0,1.1,1.5],
    },
    "コンサルティング": {
        "unit_price": 300_000, "ad_budget": 500_000, "cpa": 50_000,
        "organic_start": 5, "organic_growth": 5.0, "churn_rate": 8.0,
        "vc_cogs": 0, "vc_shipping": 0, "vc_server": 0,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 3_500_000, "fc_insurance": 525_000, "fc_outsourcing": 200_000,
        "fc_rent": 200_000, "fc_system": 50_000, "fc_misc": 100_000,
        "seasonal": [0.7,0.8,1.2,1.1,1.0,1.0,0.9,0.7,1.0,1.1,1.1,1.2],
    },
    "ハードウェア": {
        "unit_price": 25_000, "ad_budget": 2_000_000, "cpa": 5000,
        "organic_start": 30, "organic_growth": 3.0, "churn_rate": 0.0,
        "vc_cogs": 10_000, "vc_shipping": 1500, "vc_server": 0,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 4_000_000, "fc_insurance": 600_000, "fc_outsourcing": 1_000_000,
        "fc_rent": 500_000, "fc_system": 100_000, "fc_misc": 300_000,
        "seasonal": [0.9,0.8,1.0,1.0,1.0,1.0,1.0,0.9,1.0,1.0,1.1,1.3],
    },
    "買い切り＋サブスク": {
        "unit_price": 35_000, "ad_budget": 1_200_000, "cpa": 4000,
        "organic_start": 20, "organic_growth": 4.0, "churn_rate": 5.0,
        "vc_cogs": 12_000, "vc_shipping": 1_000, "vc_server": 100,
        "vc_payment_rate": 3.6, "vc_platform_fee": 0.0,
        "fc_salary": 3_000_000, "fc_insurance": 450_000, "fc_outsourcing": 500_000,
        "fc_rent": 200_000, "fc_system": 100_000, "fc_misc": 150_000,
        "seasonal": [0.9,0.85,1.0,1.0,1.0,1.0,1.0,0.9,1.0,1.05,1.1,1.2],
    },
}
MONTH_LABELS = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, val in [("step", 1), ("industry", "SaaS / サブスク")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────
# TOP NAV
# ─────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
  <div>
    <div class="logo">Biz<span>Maker</span></div>
    <div class="tagline">ビジネス共創プラットフォーム</div>
  </div>
  <div><span class="nav-badge">Phase 1 Preview</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab_sim, tab_ai, tab_cons, tab_sns = st.tabs([
    "  シミュレーター  ",
    "  AI アドバイザー  ",
    "  専門家に相談  ",
    "  コミュニティ  ",
])

# ═══════════════════════════════════════════════
# TAB 1 — シミュレーター
# ═══════════════════════════════════════════════
with tab_sim:
    # ── 業種テンプレート ──
    col_ind, col_sc = st.columns([3, 1])
    with col_ind:
        industry = st.selectbox(
            "業種テンプレート",
            list(INDUSTRY_TEMPLATES.keys()),
            index=list(INDUSTRY_TEMPLATES.keys()).index(st.session_state.industry),
        )
        st.session_state.industry = industry
        tmpl = INDUSTRY_TEMPLATES[industry]
    with col_sc:
        scenario = st.radio("シナリオ", ["中庸", "楽観 +20%", "悲観 -20%"], horizontal=False)

    # ── ステップバー ──
    step_labels = ["Step 1  基本情報", "Step 2  売上設計", "Step 3  コスト設計", "Step 4  資金繰り"]
    step_html = '<div class="step-bar">'
    for i, sl in enumerate(step_labels, 1):
        cls = "active" if i == st.session_state.step else ("done" if i < st.session_state.step else "")
        step_html += f'<div class="step-item {cls}">{sl}</div>'
    step_html += "</div>"
    st.markdown(step_html, unsafe_allow_html=True)

    # ══ STEP 1 ══
    with st.expander("Step 1 — 基本情報", expanded=(st.session_state.step == 1)):
        c1, c2, c3 = st.columns(3)
        with c1:
            sim_months = st.selectbox("シミュレーション期間", [12, 24, 36, 60, 84, 120], index=2)
        with c2:
            target_pct = st.slider("目標営業利益率 (%)", 1, 50, 20)
            target_rate = target_pct / 100
        with c3:
            initial_inv = st.number_input("初期投資額 (円)", value=5_000_000, step=500_000)
        _, nb = st.columns([8, 1])
        with nb:
            if st.button("次へ", key="n1"): st.session_state.step = 2; st.rerun()

    # ══ STEP 2 ══
    with st.expander("Step 2 — 売上設計", expanded=(st.session_state.step == 2)):
        s2a, s2b = st.columns(2)
        with s2a:
            unit_price   = st.number_input("平均客単価 (円)", value=tmpl["unit_price"], step=500)
            ad_budget    = st.number_input("月間広告予算 (円)", value=tmpl["ad_budget"], step=100_000)
            cpa          = st.number_input("CPA (円)", value=tmpl["cpa"], step=100)
        with s2b:
            organic_start = st.number_input("自然流入獲得数 (件/月)", value=tmpl["organic_start"], step=10)
            org_growth_pct = st.slider("自然流入月次成長率 (%)", 0.0, 20.0, tmpl["organic_growth"], 0.5)
            organic_growth = 1 + org_growth_pct / 100
            churn_pct    = st.slider("月間解約率 (%)", 0.0, 50.0, tmpl["churn_rate"], 0.5)
            churn_rate   = churn_pct / 100

        use_churn  = st.checkbox("解約率を反映する", value=True)
        use_season = st.checkbox("季節変動を反映する", value=True)
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
            if st.button("戻る", key="b2"): st.session_state.step = 1; st.rerun()
        with nc:
            if st.button("次へ", key="n2"): st.session_state.step = 3; st.rerun()

    # ══ STEP 3 ══
    with st.expander("Step 3 — コスト設計（固定費 / 変動費）", expanded=(st.session_state.step == 3)):
        s3a, s3b = st.columns(2)
        with s3a:
            st.caption("変動費（1件ごと）")
            vc_cogs    = st.number_input("仕入原価 (円)", value=tmpl["vc_cogs"], step=100)
            vc_ship    = st.number_input("配送料 (円)", value=tmpl["vc_shipping"], step=50)
            vc_srv     = st.number_input("サーバー原価 (円/件)", value=tmpl["vc_server"], step=10)
            vc_pay     = st.number_input("決済手数料 (%)", value=tmpl["vc_payment_rate"], step=0.1) / 100
            vc_plat    = st.number_input("モール手数料 (%)", value=tmpl["vc_platform_fee"], step=0.1) / 100
        with s3b:
            st.caption("固定費（月額）")
            fc_sal  = st.number_input("給与合計 (円)", value=tmpl["fc_salary"], step=100_000)
            fc_ins  = st.number_input("社会保険料 (円)", value=tmpl["fc_insurance"], step=50_000)
            fc_out  = st.number_input("業務委託費 (円)", value=tmpl["fc_outsourcing"], step=50_000)
            fc_rent = st.number_input("家賃 (円)", value=tmpl["fc_rent"], step=10_000)
            fc_sys  = st.number_input("システム利用料 (円)", value=tmpl["fc_system"], step=5_000)
            fc_misc = st.number_input("その他固定費 (円)", value=tmpl["fc_misc"], step=10_000)
        total_fixed = fc_sal + fc_ins + fc_out + fc_rent + fc_sys + fc_misc

        bc3, _, nc3 = st.columns([1, 7, 1])
        with bc3:
            if st.button("戻る", key="b3"): st.session_state.step = 2; st.rerun()
        with nc3:
            if st.button("次へ", key="n3"): st.session_state.step = 4; st.rerun()

    # ══ STEP 4 ══
    with st.expander("Step 4 — 資金繰り（キャッシュフロー）", expanded=(st.session_state.step == 4)):
        s4a, s4b = st.columns(2)
        with s4a:
            cash_init = st.number_input("手元現金 (円)", value=10_000_000, step=1_000_000)
            pay_cyc   = st.selectbox("入金サイクル", ["当月", "翌月", "翌々月"])
        with s4b:
            exp_cyc   = st.selectbox("支払サイクル", ["当月", "翌月"])
        pay_delay = {"当月":0,"翌月":1,"翌々月":2}[pay_cyc]
        exp_delay = {"当月":0,"翌月":1}[exp_cyc]
        bc4, _ = st.columns([1, 8])
        with bc4:
            if st.button("戻る", key="b4"): st.session_state.step = 3; st.rerun()

    # ─── デフォルト補完（Stepを飛ばした場合） ───
    try:
        _ = unit_price
    except NameError:
        unit_price = tmpl["unit_price"]; ad_budget = tmpl["ad_budget"]; cpa = tmpl["cpa"]
        organic_start = tmpl["organic_start"]; organic_growth = 1 + tmpl["organic_growth"]/100
        churn_rate = tmpl["churn_rate"]/100; use_churn = True; use_season = True
        seasonal = tmpl["seasonal"]
    try:
        _ = total_fixed
    except NameError:
        vc_cogs = tmpl["vc_cogs"]; vc_ship = tmpl["vc_shipping"]; vc_srv = tmpl["vc_server"]
        vc_pay = tmpl["vc_payment_rate"]/100; vc_plat = tmpl["vc_platform_fee"]/100
        fc_sal = tmpl["fc_salary"]; fc_ins = tmpl["fc_insurance"]; fc_out = tmpl["fc_outsourcing"]
        fc_rent = tmpl["fc_rent"]; fc_sys = tmpl["fc_system"]; fc_misc = tmpl["fc_misc"]
        total_fixed = fc_sal + fc_ins + fc_out + fc_rent + fc_sys + fc_misc
    try:
        _ = cash_init
    except NameError:
        cash_init = 10_000_000; pay_delay = 0; exp_delay = 0
    try:
        _ = sim_months; _ = target_rate
    except NameError:
        sim_months = 36; target_rate = 0.20; target_pct = 20; initial_inv = 5_000_000

    # ─── シナリオ係数 ───
    if scenario == "楽観 +20%":
        s_mult, c_mult = 1.2, 0.9
    elif scenario == "悲観 -20%":
        s_mult, c_mult = 0.8, 1.1
    else:
        s_mult, c_mult = 1.0, 1.0

    # ─── 計算ロジック ───
    rows = []
    cum_profit = 0
    active_cust = 0
    cash = cash_init
    s_buf = [0] * (pay_delay + 1)
    e_buf = [0] * (exp_delay + 1)
    bep_m = rec_m = None

    for i in range(sim_months):
        m = i + 1
        cal = i % 12
        sf = seasonal[cal] if use_season else 1.0
        u_ad  = int(ad_budget / cpa) if cpa > 0 else 0
        u_org = int(organic_start * (organic_growth ** i))
        nc    = u_ad + u_org
        ch    = int(active_cust * churn_rate) if use_churn and active_cust > 0 else 0
        active_cust = max(0, active_cust + nc - ch)
        tu    = int((active_cust if use_churn else nc) * sf)
        sales = int(tu * unit_price * s_mult)
        vc    = (tu*(vc_cogs+vc_ship+vc_srv) + sales*(vc_pay+vc_plat)) * c_mult
        gp    = sales - vc
        op    = gp - ad_budget - total_fixed * c_mult
        cum_profit += op
        mr    = gp / sales if sales > 0 else 0
        bep   = (total_fixed*c_mult + ad_budget) / mr if mr > 0 else 0
        if bep_m is None and op > 0: bep_m = m
        if rec_m is None and cum_profit > 0: rec_m = m
        # CF
        s_buf.append(sales); e_buf.append(abs(vc) + ad_budget + total_fixed*c_mult)
        cash = cash + s_buf.pop(0) - e_buf.pop(0)
        rows.append({"月":f"{m}ヶ月目","月番号":m,"暦月":MONTH_LABELS[cal],
                     "季節係数":sf,"新規獲得":nc,"解約数":ch,"アクティブ顧客数":active_cust,
                     "販売数":tu,"売上高":sales,"変動費":vc,"限界利益":gp,
                     "広告宣伝費":ad_budget,"固定費合計":total_fixed*c_mult,
                     "営業利益":op,"累積利益":cum_profit,"損益分岐点売上":bep,
                     "キャッシュ残高":cash,"費用_変動費":vc,
                     "費用_広告宣伝費":ad_budget,"費用_固定費":total_fixed*c_mult})

    df = pd.DataFrame(rows)
    last = df.iloc[-1]
    cur_sales  = last["売上高"]
    cur_profit = last["営業利益"]
    cur_rate   = cur_profit / cur_sales if cur_sales > 0 else 0
    gap        = cur_sales * target_rate - cur_profit
    ltv        = unit_price / churn_rate if churn_rate > 0 else 999_999
    ltv_cac    = ltv / cpa if cpa > 0 else 999

    # ─── ユニットエコノミクス ───
    st.markdown('<div class="section-title">ユニットエコノミクス</div>', unsafe_allow_html=True)
    vc_per_unit = vc_cogs + vc_ship + vc_srv + unit_price * (vc_pay + vc_plat)
    margin_per_unit = unit_price - vc_per_unit
    margin_pct = margin_per_unit / unit_price * 100 if unit_price > 0 else 0
    ltv_val = unit_price / churn_rate if churn_rate > 0 else unit_price * 120
    cac_val = cpa
    ltv_cac_ratio = ltv_val / cac_val if cac_val > 0 else 999
    payback = cac_val / margin_per_unit if margin_per_unit > 0 else 999
    avg_life = 1 / churn_rate if churn_rate > 0 else 120

    ue_html = '<div class="kpi-grid">'
    ue_html += f"""<div class="kpi-card accent">
      <div class="label">客単価 (ARPU)</div><div class="value">¥{unit_price:,}</div>
      <div class="delta neutral">1取引あたり</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if margin_pct > 50 else 'warn'}">
      <div class="label">限界利益 / 件</div><div class="value">¥{margin_per_unit:,.0f}</div>
      <div class="delta {'up' if margin_pct > 50 else 'down'}">利益率 {margin_pct:.1f}%</div></div>"""
    ue_html += f"""<div class="kpi-card accent">
      <div class="label">LTV (顧客生涯価値)</div><div class="value">¥{ltv_val:,.0f}</div>
      <div class="delta neutral">平均 {avg_life:.1f}ヶ月</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if cac_val < ltv_val / 3 else 'danger'}">
      <div class="label">CAC (獲得単価)</div><div class="value">¥{cac_val:,}</div>
      <div class="delta {'up' if cac_val < ltv_val / 3 else 'down'}">CPA = ¥{cpa:,}</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if ltv_cac_ratio >= 3 else 'danger'}">
      <div class="label">LTV / CAC</div><div class="value">{ltv_cac_ratio:.1f}x</div>
      <div class="delta {'up' if ltv_cac_ratio >= 3 else 'down'}">{'✓ 健全 (3x以上)' if ltv_cac_ratio >= 3 else '▽ 改善が必要 (3x未満)'}</div></div>"""
    ue_html += f"""<div class="kpi-card {'success' if payback < 12 else 'warn'}">
      <div class="label">ペイバック期間</div><div class="value">{payback:.1f}ヶ月</div>
      <div class="delta {'up' if payback < 12 else 'down'}">{'✓ 12ヶ月以内' if payback < 12 else '▽ 12ヶ月超'}</div></div>"""
    ue_html += "</div>"
    st.markdown(ue_html, unsafe_allow_html=True)

    # ユニットエコノミクス詳細
    with st.expander("ユニットエコノミクス詳細を表示"):
        ue_c1, ue_c2 = st.columns(2)
        with ue_c1:
            st.markdown("**収益構造（1顧客あたり）**")
            ue_items = {
                "売上単価": unit_price,
                "仕入原価": -vc_cogs,
                "配送料": -vc_ship,
                "サーバー原価": -vc_srv,
                "決済手数料": -int(unit_price * vc_pay),
                "モール手数料": -int(unit_price * vc_plat),
                "**限界利益**": margin_per_unit,
            }
            ue_df = pd.DataFrame({"項目": ue_items.keys(), "金額 (円)": ue_items.values()})
            st.dataframe(ue_df, hide_index=True, use_container_width=True)
        with ue_c2:
            st.markdown("**判定基準**")
            checks = [
                ("LTV / CAC ≥ 3.0", ltv_cac_ratio >= 3, f"{ltv_cac_ratio:.1f}x"),
                ("ペイバック ≤ 12ヶ月", payback <= 12, f"{payback:.1f}ヶ月"),
                ("限界利益率 ≥ 50%", margin_pct >= 50, f"{margin_pct:.1f}%"),
                ("解約率 ≤ 5%", churn_rate * 100 <= 5, f"{churn_rate*100:.1f}%"),
            ]
            for label, ok, val in checks:
                icon = "✅" if ok else "⚠️"
                st.markdown(f"{icon} **{label}** → 現在: {val}")

    # ─── KPI CARDS ───
    st.markdown('<div class="section-title">KPI ダッシュボード</div>', unsafe_allow_html=True)

    def kpi(label, value, delta="", delta_type="neutral", accent="accent"):
        return f"""
        <div class="kpi-card {accent}">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
          <div class="delta {delta_type}">{delta}</div>
        </div>"""

    profit_ok = cur_rate >= target_rate
    ltv_ok = ltv_cac >= 3
    run_val = int(cash_init / abs(df["営業利益"].mean())) if df["営業利益"].mean() < 0 else 999

    kpi_html = '<div class="kpi-grid">'
    kpi_html += kpi("月商", f"¥{cur_sales:,.0f}", f"瞮標利益'�y{target_pct}%", "neutral", "accent")
    kpi_html += kpi("営業利益", f"¥{cur_profit:,.0f}",
                    f"利益率 {cur_rate*100:.1f}% {'✓達成' if profit_ok else '▽未達'}",
                    "up" if profit_ok else "down", "success" if profit_ok else "danger")
    kpi_html += kpi("LTV / CAC", f"{ltv_cac:.1f}x", "3x以上が健全",
                    "up" if ltv_ok else "down", "success" if ltv_ok else "warn")
    kpi_html += kpi("黒字化", f"{bep_m}ヶ月目" if bep_m else "期間外", "", "neutral", "accent")
    kpi_html += kpi("ランウェイ", f"{run_val}ヶ月" if run_val < 999 else "黒字運営", "",
                    "down" if 0 < run_val < 6 else "neutral", "danger" if 0 < run_val < 6 else "accent")
    kpi_html += kpi("アクティブ顧客", f"{last['アクティブ顧客数']:,} 人",
                    f"月{last['新規獲得']:,}件獲得 / {last['解約数']:,}件解約", "neutral", "accent")
    kpi_html += "</div>"
    st.markdown(kpi_html, unsafe_allow_html=True)

    # ─── 改善提案 ───
    st.markdown('<div class="section-title">目標達成シミュレーション</div>', unsafe_allow_html=True)
    if profit_ok:
        st.success(f"目標の {target_pct}% を達成しています（現在 {cur_rate*100:.1f}%）")
    else:
        st.warning(f"目標 {target_pct}% まで あと ¥{gap:,.0f}/月 必要です")
        ac1, ac2, ac3, ac4 = st.columns(4)
        pu = gap / last["販売数"] if last["販売数"] > 0 else 0
        with ac1:
            st.markdown(f"""<div class="advice-card">
              <div class="advice-title">単価アップ</div>
              <div class="advice-value">¥{unit_price+pu:,.0f}</div>
              <div class="advice-desc">+{pu:,.0f}円/件 の値上し</div>
            </div>""", unsafe_allow_html=True)
        with ac2:
            st.markdown(f"""<div class="advice-card">
              <div class="advice-title">固定費削減 </div>
              <div class="advice-value">¥{max(0,total_fixed-gap):,.0f}</div>
              <div class="advice-desc">月額 {gap:,.0f}円 の削減</div>
            </div>""", unsafe_allow_html=True)
        with ac3:
            ncpa = cpa * max(0, 1 - gap/ad_budget) if ad_budget > 0 else cpa
            st.markdown(f"""<div class="advice-card">
              <div class="advice-title">CPA 改善</div>
              <div class="advice-value">¥{ncpa:,.0f}</div>
              <div class="advice-desc">現在 ¥{cpa:,} → 目標 ¥{ncpa:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with ac4:
            nc_rate = churn_rate * 0.5
            st.markdown(f"""<div class="advice-card">
              <div class="advice-title">解約率半減 </div>
              <div class="advice-value">{nc_rate*100:.1f}%</div>
              <div class="advice-desc">現在 {churn_rate*100:.1f}% → {nc_rate*100:.1f}%</div>
            </div>""", unsafe_allow_html=True)

    # ─── グラフ ───
    st.markdown('<div class="section-title">グラフ分析</div>', unsafe_allow_html=True)

    # 月/年 切り替え
    graph_col1, graph_col2 = st.columns([3, 1])
    with graph_col2:
        view_mode = st.radio("表示単位", ["月単位", "年単位"], horizontal=True, key="view_mode")

    if view_mode == "年単位":
        # 年単位に集約
        df["年"] = ((df["月番号"] - 1) // 12) + 1
        df_yearly = df.groupby("年").agg({
            "売上高": "sum", "変動費": "sum", "限界利益": "sum",
            "広告宣伝費": "sum", "固定費合計": "sum", "営業利益": "sum",
            "累積利益": "last", "損益分岐点売上": "mean",
            "キャッシュ残高": "last", "新規獲得": "sum", "解約数": "sum",
            "アクティブ顧客数": "last", "販売数": "sum",
            "費用_変動費": "sum", "費用_広告宣伝費": "sum", "費用_固定費": "sum",
        }).reset_index()
        df_yearly["月"] = df_yearly["年"].apply(lambda y: f"{y}年目")
        df_yearly["月番号"] = df_yearly["年"]
        df_view = df_yearly
        x_title = "年"
    else:
        df_view = df
        x_title = "月"

    g1, g2, g3, g4, g5, g6 = st.tabs(["収支推移","キャッシュフロー","シナリオ比較","コスト構造","顧客推移","データ表"])

    with g1:
        base = alt.Chart(df_view).encode(x=alt.X("月番号:Q",title=x_title))
        ls = base.mark_line(color="#2196F3",strokeWidth=2.5).encode(y=alt.Y("売上高:Q",axis=alt.Axis(format="~s",title="¥ 売上高")),tooltip=["月",alt.Tooltip("売上高:Q",format=",")])
        lb = base.mark_line(color="#94A3B8",strokeDash=[4,4]).encode(y=alt.Y("損益分岐点売上:Q",axis=alt.Axis(format="~s")))
        ap = base.mark_area(opacity=0.25).encode(y=alt.Y("営業利益:Q",axis=alt.Axis(format="~s")),
             color=alt.condition(alt.datum.営業利益>0,alt.value("#16A34A"),alt.value("#DC2626")))
        st.altair_chart((ap+ls+lb).interactive(),use_container_width=True)

    with g2:
        cf = alt.Chart(df_view).mark_area(opacity=0.5).encode(
            x=alt.X("月番号:Q",title=x_title),y=alt.Y("キャッシュ残高:Q",axis=alt.Axis(format="~s",title="¥ キャッシュ残高")),
            color=alt.condition(alt.datum.キャッシュ残高>0,alt.value("#2196F3"),alt.value("#DC2626")),
            tooltip=["月",alt.Tooltip("キャッシュ残高:Q",format=",")])
        st.altair_chart((cf+alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(color="#DC2626",strokeDash=[3,3]).encode(y="y:Q")).interactive(),use_container_width=True)

    with g3:
        def sc(sm, cm, label):
            r=[]; cum=0; ac=0
            for i in range(sim_months):
                u_ad2 = int(ad_budget/cpa) if cpa>0 else 0
                nc2 = u_ad2 + int(organic_start*(organic_growth**i))
                ch2 = int(ac*churn_rate) if use_churn and ac>0 else 0
                ac = max(0,ac+nc2-ch2)
                tu2 = int((ac if use_churn else nc2)*(seasonal[i%12] if use_season else 1))
                s2 = int(tu2*unit_price*sm)
                vc2 = (tu2*(vc_cogs+vc_ship+vc_srv)+s2*(vc_pay+vc_plat))*cm
                cum += s2-vc2-ad_budget-total_fixed*cm
                r.append({"月番号":i+1,"累積利益":cum,"シナリオ":label})
            return pd.DataFrame(r)
        df_all = pd.concat([sc(1.2,0.9,"楽観"),sc(1.0,1.0,"中庸"),sc(0.8,1.1,"悲観")])
        sc_ch = alt.Chart(df_all).mark_line(strokeWidth=2).encode(
            x="月番号:Q",y=alt.Y("累積利益:Q",axis=alt.Axis(format="~s",title="¥ 累積利益")),
            color=alt.Color("シナリオ:N",scale=alt.Scale(range=["#16A34A","#2196F3","#DC2626"])),
            tooltip=["月番号","シナリオ",alt.Tooltip("累積利益:Q",format=",")])
        st.altair_chart(sc_ch.interactive(),use_container_width=True)

    with g4:
        cd = df_view.melt(id_vars=["月"],value_vars=["費用_変動費","費用_広告宣伝費","費用_固定費"],var_name="費用種別",value_name="金額")
        st.altair_chart(alt.Chart(cd).mark_area().encode(
            x=alt.X("月:N",sort=None),y=alt.Y("金額:Q",axis=alt.Axis(format="~s",title="¥ 金額")),
            color=alt.Color("費用種別:N",scale=alt.Scale(range=["#F59E0B","#EF4444","#6366F1"])),
            tooltip=["月","費用種別",alt.Tooltip("金額:Q",format=",")]),use_container_width=True)

    with g5:
        if use_churn:
            cb = alt.Chart(df_view).encode(x=alt.X("月番号:Q",title=x_title))
            st.altair_chart((cb.mark_bar(color="#BBF7D0",opacity=0.7).encode(y=alt.Y("新規獲得:Q",axis=alt.Axis(format=",",title="人数")))+
                             cb.mark_line(color="#2196F3",strokeWidth=2.5).encode(y=alt.Y("アクティブ顧客数:Q",axis=alt.Axis(format=",")))).interactive(),use_container_width=True)
        else:
            st.info("解約率をONにすると顧客推移グラフが表示されます")

    with g6:
        st.dataframe(df_view,use_container_width=True)

    # ─── エクスポート ───
    st.markdown('<div class="section-title">データエクスポート</div>', unsafe_allow_html=True)
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.download_button("CSV ダウンロード", df.to_csv(index=False).encode("utf-8-sig"),
                           "simulation.csv", "text/csv", use_container_width=True)
    with ec2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w: df.to_excel(w, index=False, sheet_name="PL")
        st.download_button("Excel ダウンロード", buf.getvalue(), "simulation.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with ec3:
        st.button("PDF レポート（Phase 2）", disabled=True, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 2 — AI アドバイザー（UI モック）
# ═══════════════════════════════════════════════
with tab_ai:
    st.markdown("""
    <div class="cs-banner">
      ⚡ <strong>Coming Soon — Phase 2</strong>  このタブは機能イメージです。ヒアリング用プレビューとしてご確認ください。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### AI アドバイザー")
    st.caption("あなたの事業計画をリアルタイムで分析し、具体的な改善提案を自動生成します。")

    # AI分析コメント（サンプル）
    st.markdown("""
    <div style="max-width:680px; margin-top:8px;">
      <div class="ai-bubble">
        <div class="ai-label">Biz Maker AI · 分析結果</div>
        入力された事業計画を分析しました。以下が主な所見です。<br><br>
        <strong>1. キャッシュフロー警告</strong><br>
        現在の入金サイクルと支払サイクルのズレにより、4〜6ヶ月目にキャッシュがタイトになる可能性があります。
        運転資金として 300〜500万円の予備を確保することを推奨します。<br><br>
        <strong>2. LTV / CAC 比率</strong><br>
        現在の比率は 2.4x で、業界健全ラインの 3.0x を下回っています。
        解約率を 1〜2% 改善するだけで比率が 3.6x まで改善し、収益性が大幅に向上します。<br><br>
        <strong>3. 季節変動リスク</strong><br>
        SaaS業種の場合、7〜8月に売上が約 5% 低下する傾向があります。
        この時期に合わせた年次契約プランの提供を検討してみてください。
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ユーザー入力エリア（モック）
    st.markdown("**AI に質問する**")
    col_q, col_send = st.columns([6, 1])
    with col_q:
        user_q = st.text_input("", placeholder="例: 解約率を改善するための具体的な施策を教えて", label_visibility="collapsed")
    with col_send:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("送信", use_container_width=True):
            st.info("Phase 2 では Claude API を接続し、リアルタイムで回答します。")

    # よくある質問
    st.markdown('<div class="section-title">よくある質問</div>', unsafe_allow_html=True)
    qa_cols = st.columns(3)
    questions = [
        ("解約率の改善策", "カスタマーサクセスの強化とオンボーディング改善が最も効果的です。"),
        ("資金調達のタイミング", "ランウェイが6ヶ月を下回る前に調達活動を始めることを推奨します。"),
        ("CPA を下げる方法", "SEO強化による自然流入の増加と、リターゲティング広告の最適化が有効です。"),
    ]
    for col, (q, a) in zip(qa_cols, questions):
        with col:
            with st.expander(q):
                st.markdown(f"<div style='font-size:0.83rem;color:#374151;line-height:1.6;'>{a}<br><br><em style='color:#9CA3AF;'>Phase 2 では AIが事業計画データを参照した上で回答します。</em></div>", unsafe_allow_html=True)

    # 追加の会話例
    st.markdown('<div class="section-title">会話例プレビュー</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-wrap" style="background:#F8FAFC;border-radius:12px;padding:16px;border:1px solid #E8ECF0;">
      <div style="float:right;clear:both;">
        <div class="user-bubble">解約率を下げるにはどうすればいいですか？</div>
      </div>
      <div style="clear:both; margin-top:8px;">
        <div class="ai-bubble" style="max-width:90%;">
          <div class="ai-label">Biz Maker AI</div>
          解約率改善には主に3つのアプローチが効果的です：<br>
          ① オンボーディングの強化（最初の30日が鍵）<br>
          ② プロダクト内での価値提供の可視化（ダッシュボード等）<br>
          ③ ヘルススコアによる早期チャーン予測と介入<br><br>
          御社の現在の解約率 3% を 2% に改善した場合、LTV が 33% 向上し、36ヶ月後の累積利益は約 800万円改善します。
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# TAB 3 — 専門家に相談（UI モック）
# ═══════════════════════════════════════════════
with tab_cons:
    st.markdown("""
    <div class="cs-banner">
      ⚡ <strong>Coming Soon — Phase 2</strong>  このタブは機能イメージです。ヒアリング用プレビューとしてご確認ください。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 専門家マッチング")
    st.caption("あなたの事業フェーズと課題に合った専門家を見つけて。直接相談できます。")

    # フィルター
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.selectbox("専門分野", ["すべて","財務・会計","マーケティング","法務","IT・開発","人事・組織"])
    with fc2:
        st.selectbox("料金帯", ["すべて","〜5,000円/30分","5,000〜10,000円","10,000円〜"])
    with fc3:
        st.selectbox("評価", ["すべて","★ 4.5以上","★ 4.0以上"])
    with fc4:
        st.selectbox("対応形式", ["すべて","オンライン","対面","電話"])

    st.markdown("---")

    # コンサルタントカード
    consultants = [
        {
            "initials": "TT",
            "name": "田中 太郎",
            "field": "財務・会計",
            "desc": "公認会計士。スタートアップの資金調達・事業計画策定を 200社以上支援。元BigFour出身。SaaSビジネスの財務モデル設計が専門。",
            "rating": "4.9",
            "reviews": 128,
            "price": "¥8,000 / 30分",
            "badge": "あなたの事業計画にマッチ",
            "tags": ["財務モデル", "資金調達", "SaaS"],
        },
        {
            "initials": "HK",
            "name": "鈴木 花子",
            "field": "マーケティング",
            "desc": "元Google。D2C・SaaSのグロースマーケティングを専門とし、CPA改善・LTV向上の実績多数。コンテンツSEOからPaid Socialまで幅広く対応。",
            "rating": "4.8",
            "reviews": 94,
            "price": "¥10,000 / 30分",
            "badge": "CPA改善の実績多数",
            "tags": ["グロース", "SEO", "広告運用"],
        },
        {
            "initials": "IY",
            "name": "山田 一郎",
            "field": "法務",
            "desc": "弁護士。スタートアップの法務全般（利用規約・プライバシーポリシー・契約書作成）からIPO準備まで一気通貫で対応。初回30分無料。",
            "rating": "4.6",
            "reviews": 67,
            "price": "¥12,000 / 30分",
            "badge": "初回無料相談あり",
            "tags": ["契約書", "IPO", "規約作成"],
        },
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
                <div class="cons-meta">★ {cons['rating']}  ({cons['reviews']} 件のレビュー)</div>
                <div class="cons-meta" style="font-weight:600;color:#1A1A2E;">{cons['price']}</div>
                <div>{''.join(f'<span class="tag">{t}</span>' for t in cons['tags'])}</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"相談を予約する — {cons['name']}", key=f"book_{cons['name']}"):
            st.info("Phase 2 では専销家のカレンダーと連携して直接予約できます。")


# ═══════════════════════════════════════════════
# TAB 4 — コミュニティ（UI モック）
# ═══════════════════════════════════════════════
with tab_sns:
    st.markdown("""
    <div class="cs-banner">
      ⚡ <strong>Coming Soon — Phase 2</strong>  このタブは機能イメージです。ヒアリング用プレビューとしてご確認ください。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### コミュニティ")
    st.caption("同じフェーズの起業宷・経営者と繋がり、事業計画のフィードバックを交換しましょう。")

    # 新規投稿フォーム
    with st.expander("投稿を作成する", expanded=False):
        post_txt = st.text_area("内容", placeholder="事業計画について相談したいこと、学んだことをシェアしましょう…", height=100)
        tag_opts = st.multiselect("タグ", ["#SaaS","#EC","#飲食","#コンサル","#資金調達","#マーケ","#解約率改善","#初期顧客獲得"])
        if st.button("投稿する", key="post_btn"):
            st.info("Phase 2 で実装予定です。")

    st.markdown("---")

    # 投稿カード
    posts = [
        {
            "initials": "SM",
            "name": "佐藤 美咲",
            "sub": "SaaS · 創業2年目",
            "content": "解約率を 8% → 2.8% に改善できました🎉\n施策は「オンボーディングフロー」の抜本的な見直し。特に初回ログインから7日間のメール自動化が効きました。同じ課題を抱えている方、詳細をシェアします。",
            "tags": ["#SaaS", "#解約率改善"],
            "likes": 38,
            "comments": 14,
            "time": "2時間前",
        },
        {
            "initials": "KT",
            "name": "高橋 健太",
            "sub": "飲食店 · 2店舗運営",
            "content": "このシミュレーターで12月の季節変動を入れてシミュレーションしてみたら、固定費の比率が高すぎることに気づきました。業務委託の比率を見直して月30万円のコスト改善ができそうです。",
            "tags": ["#飲食", "#固定費削減"],
            "likes": 22,
            "comments": 9,
            "time": "5時間前",
        },
        {
            "initials": "RW",
            "name": "渡辺 翔",
            "sub": "コンサルティング · 独立1年目",
            "content": "LTV/CAC が 2.1x で悩んでいます。コンサルビジネスでCACを下げた方法を教えてください。今は紹介プログラムの導入を検討中です。",
            "tags": ["#コンサル", "#LTV", "#CAC"],
            "likes": 45,
            "comments": 21,
            "time": "1日前",
        },
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
              <div class="sub">{post['sub']} · {post['time']}</div>
            </div>
          </div>
          <div class="post-content">{content_html}</div>
          <div style="margin-top:8px;">{tags_html}</div>
          <div class="post-actions">
            <span class="post-action">👍 {post['likes']}</span>
            <span class="post-action">💬 {post['comments']} コメント</span>
            <span class="post-action">🔖 保存</span>
            <span class="post-action">↗ シェア</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"コメントする — {post['name']}", key=f"cmt_{post['name']}", type="secondary"):
            st.info("Phase 2 で実装予定です。")

# ─── フッター ───
st.markdown("""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #E8ECF0;text-align:center;color:#9CA3AF;font-size:0.75rem;">
  Biz Maker — ビジネス共創プラットフォーム v3.1 &nbsp;|&nbsp; Phase 1 Preview &nbsp;|&nbsp; Powered by Streamlit
</div>
""", unsafe_allow_html=True)
