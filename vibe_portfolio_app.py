
import streamlit as st
import pandas as pd

st.set_page_config(page_title="資產比例計算器（Vibe版）", page_icon="📊", layout="wide")

st.title("📊 資產比例計算器（Vibe Coding 版）")
st.caption("輸入當下金額 → 你自行輸入理想比例 → 立刻看到每一類該補/該減多少。")

# ---- Sidebar: global options ----
st.sidebar.header("⚙️ 設定")
fx = st.sidebar.number_input("USD→TWD 匯率", min_value=20.0, max_value=60.0, value=33.0, step=0.1)
lock_fixed_income = st.sidebar.checkbox("固定收益不可賣出（僅顯示缺口，不給賣出建議）", value=True)
lock_cash = st.sidebar.checkbox("現金不強制調整（只計算差距，不下賣出建議）", value=False)
tol = st.sidebar.number_input("再平衡容忍區（%）", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
st.sidebar.caption("差距低於容忍區時視為就地不動。")

# ---- Input: current amounts by category ----
st.subheader("① 目前資產金額（可直接輸入 TWD；若輸入 USD 會自動換算）")
col1, col2, col3, col4 = st.columns(4)
with col1:
    fi_twd = st.number_input("固定收益（TWD）", min_value=0.0, value=0.0, step=1000.0, key="fi_twd")
    fi_usd = st.number_input("固定收益（USD，選填）", min_value=0.0, value=0.0, step=100.0, key="fi_usd")
with col2:
    growth_twd = st.number_input("成長性資產（TWD）", min_value=0.0, value=0.0, step=1000.0, key="gr_twd")
    growth_usd = st.number_input("成長性資產（USD，選填）", min_value=0.0, value=0.0, step=100.0, key="gr_usd")
with col3:
    hedge_twd = st.number_input("避險資產（TWD）", min_value=0.0, value=0.0, step=1000.0, key="hd_twd")
    hedge_usd = st.number_input("避險資產（USD，選填）", min_value=0.0, value=0.0, step=100.0, key="hd_usd")
with col4:
    cash_twd = st.number_input("現金（TWD）", min_value=0.0, value=0.0, step=1000.0, key="cs_twd")
    cash_usd = st.number_input("現金（USD，選填）", min_value=0.0, value=0.0, step=100.0, key="cs_usd")

current = {
    "固定收益": fi_twd + fi_usd * fx,
    "成長性資產": growth_twd + growth_usd * fx,
    "避險資產": hedge_twd + hedge_usd * fx,
    "現金": cash_twd + cash_usd * fx,
}

total = sum(current.values())
st.info(f"目前資產總額：約 **{total:,.0f} TWD**")

# ---- Target weights input ----
st.subheader("② 輸入你的理想比例（你決定）")
c1, c2, c3, c4 = st.columns(4)
with c1:
    w_fi = st.number_input("固定收益 %", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
with c2:
    w_gr = st.number_input("成長性資產 %", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
with c3:
    w_hd = st.number_input("避險資產 %", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
with c4:
    w_cs = st.number_input("現金 %", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

w_sum = w_fi + w_gr + w_hd + w_cs
if abs(w_sum - 100.0) > 1e-6:
    st.warning(f"你的比例合計是 **{w_sum:.1f}%**（應該等於 100%）。可先調整後再看建議。")

targets = {
    "固定收益": w_fi / 100.0,
    "成長性資產": w_gr / 100.0,
    "避險資產": w_hd / 100.0,
    "現金": w_cs / 100.0,
}

# ---- Small calculators per category ----
st.subheader("③ 小計算機：比例 ↔ 金額 即時換算")
cc1, cc2, cc3, cc4 = st.columns(4)
for i, (name, default_w) in enumerate(targets.items()):
    with [cc1, cc2, cc3, cc4][i]:
        st.markdown(f"**{name}**")
        p = st.number_input(f"{name} 比例 %", min_value=0.0, max_value=100.0, value=float(default_w*100), step=0.5, key=f"calc_{name}_p")
        amt = total * (p/100.0)
        st.metric(label=f"{name} 金額", value=f"{amt:,.0f} TWD")
st.caption("左側調好比例，這裡立刻顯示對應金額。")

# ---- Compute current vs target ----
rows = []
for k in ["固定收益", "成長性資產", "避險資產", "現金"]:
    cur_amt = current[k]
    cur_w = (cur_amt / total * 100.0) if total > 0 else 0.0
    tgt_w = targets[k] * 100.0
    tgt_amt = targets[k] * total
    diff = tgt_amt - cur_amt  # (+) need add; (-) need reduce
    within_band = abs(cur_w - tgt_w) <= tol
    rows.append({
        "資產大類": k,
        "目前金額(TWD)": round(cur_amt, 2),
        "目前比例(%)": round(cur_w, 2),
        "理想比例(%)": round(tgt_w, 2),
        "理想金額(TWD)": round(tgt_amt, 2),
        "差距金額(TWD)": round(diff, 2),
        "容忍區內?": "是" if within_band else "否"
    })

df = pd.DataFrame(rows)

st.subheader("④ 目前 vs 理想 vs 差距")
st.dataframe(df, use_container_width=True)

# ---- Simple action hints ----
st.subheader("⑤ 簡易動作建議（依鎖定規則與容忍區）")
hints = []
for _, r in df.iterrows():
    name = r["資產大類"]
    diff = r["差距金額(TWD)"]
    within = (r["容忍區內?"] == "是")
    if within or diff == 0:
        continue
    if diff > 0:
        hints.append(f"🔺 **{name}** 建議加碼 **{diff:,.0f}** TWD")
    else:
        if (name == "固定收益" and lock_fixed_income) or (name == "現金" and lock_cash):
            hints.append(f"⏸️ **{name}** 超標 {-diff:,.0f} TWD（受鎖定規則限制，暫不建議賣出）")
        else:
            hints.append(f"🔻 **{name}** 建議減碼 **{-diff:,.0f}** TWD")

if hints:
    for h in hints:
        st.write(h)
else:
    st.success("所有大類均在容忍區內或無需動作。")

# ---- Export ----
st.subheader("⑥ 匯出結果")
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ 下載 CSV（可匯入 Notion）", data=csv, file_name="allocation_gap.csv", mime="text/csv")

st.caption("提示：把 CSV 丟進 Notion Database 後，未來只要更新本工具輸出再覆蓋即可。")
