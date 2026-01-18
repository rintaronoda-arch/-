import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ---------------------------------------------------------
# 1. アプリ設定
# ---------------------------------------------------------
st.set_page_config(page_title="事業計画・収支シミュレーター", layout="wide")
st.title("📊 事業計画・収支シミュレーター")
st.markdown("""
全項目を網羅したPLシミュレーション。設定した**目標利益率**を達成するための「値上げ幅」や「コスト削減額」を自動算出します。
""")

# ---------------------------------------------------------
# 2. 入力パネル（サイドバー）
# ---------------------------------------------------------
st.sidebar.header("📝 シミュレーション条件")

# --- ★追加機能：目標設定 ---
with st.sidebar.expander("0. 目標設定 (Target)", expanded=True):
    # ここで利益率を自由に設定できるようにしました
    target_rate_percent = st.slider("🎯 目標とする営業利益率 (%)", min_value=1, max_value=50, value=20, step=1)
    target_rate = target_rate_percent / 100

# --- A. 売上・マーケティング ---
with st.sidebar.expander("1. 売上・マーケティング (集客)", expanded=False):
    st.info("💡 広告費は「投資」として変動費とは分けて計算します")
    unit_price = st.number_input("平均客単価 (円)", value=5000, step=500)
    
    st.markdown("---")
    ad_budget = st.number_input("月間広告予算 (円)", value=1000000, step=100000)
    cpa = st.number_input("CPA (1件獲得単価)", value=2000, step=100)
    
    st.markdown("---")
    organic_start = st.number_input("自然流入による獲得数 (件/月)", value=50, step=10)
    organic_growth = st.slider("自然流入の月次成長率 (%)", 100.0, 120.0, 105.0, 0.1) / 100

# --- B. 変動費 (売上原価・配送・決済) ---
with st.sidebar.expander("2. 変動費 (売上に比例するコスト)", expanded=False):
    st.info("💡 売上1件ごとに必ずかかる費用")
    # 原価・物流
    vc_cogs = st.number_input("仕入原価/製造原価 (円)", value=1000, step=100)
    vc_shipping = st.number_input("配送料・梱包資材 (円)", value=600, step=50)
    vc_server_user = st.number_input("サーバー/システム原価 (円/件)", value=50, help="SaaS等の場合、1ユーザー増えるごとのインフラ負荷")
    
    # 手数料系（率）
    st.markdown("---")
    vc_payment_rate = st.number_input("決済手数料率 (%)", value=3.6, step=0.1) / 100
    vc_platform_fee = st.number_input("モール手数料/ロイヤリティ (%)", value=0.0, step=0.1) / 100

# --- C. 固定費 (人件費・家賃・SaaS等) ---
with st.sidebar.expander("3. 固定費 (売上に関わらずかかる費用)", expanded=False):
    st.info("💡 全て「月額」で入力してください")
    
    st.caption("🏢 組織・人件費")
    fc_salary = st.number_input("役員・従業員 給与合計 (月額)", value=2500000, step=100000)
    fc_insurance = st.number_input("社会保険料・法定福利費 (月額)", value=400000, step=50000, help="一般的に給与の15%程度")
    fc_outsourcing = st.number_input("業務委託費・外注費 (月額)", value=300000, step=50000)
    
    st.caption("💻 設備・インフラ")
    fc_rent = st.number_input("地代家賃 (月額)", value=150000, step=10000)
    fc_system = st.number_input("システム利用料 (SaaS/通信費)", value=50000, step=5000, help="Slack, Notion, AWS固定分など")
    
    st.caption("📎 その他")
    fc_misc = st.number_input("その他固定費 (顧問料/光熱費/雑費)", value=100000, step=10000)

    # 固定費合計
    total_fixed_cost = fc_salary + fc_insurance + fc_outsourcing + fc_rent + fc_system + fc_misc

# ---------------------------------------------------------
# 3. 計算ロジック (36ヶ月分)
# ---------------------------------------------------------
months = 36
data = []
cumulative_profit = 0

for i in range(months):
    m = i + 1
    
    # 1. 獲得数 (Units)
    units_ad = int(ad_budget / cpa) if cpa > 0 else 0
    units_org = int(organic_start * (organic_growth ** i))
    total_units = units_ad + units_org
    
    # 2. 売上高 (Sales)
    sales = total_units * unit_price
    
    # 3. 費用 (Cost)
    # 変動費 (1件あたり固定額 + 売上比率額)
    vc_per_unit = vc_cogs + vc_shipping + vc_server_user
    vc_ratio_total = vc_payment_rate + vc_platform_fee
    variable_cost = (total_units * vc_per_unit) + (sales * vc_ratio_total)
    
    # 利益計算
    gross_profit = sales - variable_cost # 売上総利益（粗利）
    operating_profit = gross_profit - ad_budget - total_fixed_cost # 営業利益
    cumulative_profit += operating_profit
    
    # 損益分岐点 (Break-even Point)
    # 限界利益率 = (売上 - 変動費) / 売上
    marginal_profit_ratio = (sales - variable_cost) / sales if sales > 0 else 0
    # 分岐点売上 = (固定費 + 広告費) / 限界利益率
    break_even_sales = (total_fixed_cost + ad_budget) / marginal_profit_ratio if marginal_profit_ratio > 0 else 0
    
    data.append({
        "月": f"{m}ヶ月目",
        "売上高": sales,
        "売上総利益": gross_profit,
        "営業利益": operating_profit,
        "累積利益": cumulative_profit,
        "販売数": total_units,
        "費用_変動費": variable_cost,
        "費用_広告宣伝費": ad_budget,
        "費用_固定費": total_fixed_cost,
        "損益分岐点売上": break_even_sales,
        "費用合計": variable_cost + ad_budget + total_fixed_cost
    })

df = pd.DataFrame(data)
last = df.iloc[-1]

# ---------------------------------------------------------
# 4. 分析ロジック (目標利益率への提案)
# ---------------------------------------------------------
# target_rate はサイドバーの設定値を使用
current_sales = last['売上高']
current_profit = last['営業利益']
current_rate = current_profit / current_sales if current_sales > 0 else 0
gap_profit = (current_sales * target_rate) - current_profit

# ---------------------------------------------------------
# 5. 画面表示
# ---------------------------------------------------------
# KPI
k1, k2, k3, k4 = st.columns(4)
k1.metric("3年後 月商", f"¥{current_sales:,.0f}")
k2.metric("3年後 営業利益", f"¥{current_profit:,.0f}", delta=f"利益率 {current_rate*100:.1f}%")
k3.metric("損益分岐点売上", f"¥{last['損益分岐点売上']:,.0f}")
k4.metric("月間販売数", f"{last['販売数']:,} 件")

# 利益率アドバイス
st.subheader(f"🎯 営業利益率 {target_rate_percent}% 達成シミュレーション")
if current_rate >= target_rate:
    st.success(f"素晴らしいです！現在の利益率は **{current_rate*100:.1f}%** で、目標({target_rate_percent}%)をクリアしています。")
else:
    st.warning(f"現在の利益率は **{current_rate*100:.1f}%** です。目標の {target_rate_percent}% にするには、月間利益があと **¥{gap_profit:,.0f}** 必要です。")
    c1, c2, c3 = st.columns(3)
    
    # 値上げ提案
    needed_price_up = gap_profit / last['販売数'] if last['販売数'] > 0 else 0
    c1.info(f"**🅰️ 単価アップ戦略**\n\n単価を **¥{unit_price + needed_price_up:,.0f}** (+{needed_price_up:,.0f}円) に値上げすれば達成できます。")
    
    # 固定費削減
    c2.info(f"**🅱️ 固定費削減戦略**\n\n固定費(人件費・家賃等)を **¥{total_fixed_cost - gap_profit:,.0f}** まで削減(-{gap_profit:,.0f}円)すれば達成できます。")

    # CPA改善
    current_units_from_ad = ad_budget / cpa if cpa > 0 else 0
    if current_units_from_ad > 0:
        new_budget = ad_budget - gap_profit
        new_cpa = new_budget / current_units_from_ad
        c3.info(f"**🆎 CPA改善戦略**\n\n獲得数を維持しつつ、CPAを **¥{new_cpa:,.0f}** まで下げれば達成できます。")
    else:
        c3.info("**🆎 CPA改善戦略**\n\n広告予算のみでの調整は困難です。")

# グラフ
tab1, tab2, tab3 = st.tabs(["📈 収支・損益分岐点", "🍩 コスト構造分析", "📋 詳細データ表"])

with tab1:
    st.markdown("##### 売上と費用のデッドヒート (損益分岐点分析)")
    base = alt.Chart(df).encode(x=alt.X('月', sort=None))
    line_sales = base.mark_line(color='#29b5e8', strokeWidth=3).encode(y='売上高', tooltip=['月', '売上高'])
    line_be = base.mark_line(color='gray', strokeDash=[5,5]).encode(y='損益分岐点売上', tooltip=['月', '損益分岐点売上'])
    area_profit = base.mark_area(opacity=0.3).encode(
        y='営業利益',
        color=alt.condition(alt.datum.営業利益 > 0, alt.value("green"), alt.value("red"))
    )
    st.altair_chart((area_profit + line_sales + line_be).interactive(), use_container_width=True)

with tab2:
    st.markdown("##### 費用の内訳 (どこにお金がかかっているか)")
    cost_df = df.melt(id_vars=["月"], value_vars=["費用_変動費", "費用_広告宣伝費", "費用_固定費"], var_name="費用種別", value_name="金額")
    chart_stack = alt.Chart(cost_df).mark_area().encode(
        x=alt.X('月', sort=None),
        y='金額',
        color=alt.Color('費用種別', scale=alt.Scale(range=['#f28e2b', '#e15759', '#76b7b2'])),
        tooltip=['月', '費用種別', '金額']
    )
    st.altair_chart(chart_stack, use_container_width=True)

with tab3:
    st.dataframe(df)
