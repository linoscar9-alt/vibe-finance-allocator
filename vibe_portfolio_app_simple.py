
import streamlit as st

st.set_page_config(page_title="極簡資產比例計算器", page_icon="💡", layout="wide")

st.title("💡 極簡資產比例計算器")

# ---- Input: current amounts ----
fi = st.number_input("固定收益 (TWD)", min_value=0.0, value=0.0, step=1000.0)
gr = st.number_input("成長性資產 (TWD)", min_value=0.0, value=0.0, step=1000.0)
hd = st.number_input("避險資產 (TWD)", min_value=0.0, value=0.0, step=1000.0)
cs = st.number_input("現金 (TWD)", min_value=0.0, value=0.0, step=1000.0)

current = {
    "固定收益": fi,
    "成長性資產": gr,
    "避險資產": hd,
    "現金": cs,
}

total = sum(current.values())

# ---- Target weights ----
w_fi = st.number_input("固定收益 %", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
w_gr = st.number_input("成長性資產 %", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
w_hd = st.number_input("避險資產 %", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
w_cs = st.number_input("現金 %", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

w_sum = w_fi + w_gr + w_hd + w_cs
if abs(w_sum - 100.0) > 1e-6:
    st.warning(f"比例合計 {w_sum:.1f}%，應等於 100%")

targets = {
    "固定收益": w_fi/100.0,
    "成長性資產": w_gr/100.0,
    "避險資產": w_hd/100.0,
    "現金": w_cs/100.0,
}

# ---- Results ----
st.markdown("---")
if total == 0:
    st.write("請先輸入資產金額")
else:
    st.write(f"總資產：{total:,.0f} TWD")
    for k in ["固定收益", "成長性資產", "避險資產", "現金"]:
        cur_amt = current[k]
        cur_w = cur_amt / total * 100
        tgt_w = targets[k] * 100
        tgt_amt = targets[k] * total
        diff = tgt_amt - cur_amt
        if diff > 0:
            msg = f"缺口 {diff:,.0f} TWD"
        elif diff < 0:
            msg = f"超標 {-diff:,.0f} TWD"
        else:
            msg = "剛好"
        st.write(f"{k}：{cur_amt:,.0f} TWD ({cur_w:.1f}%) → {msg}")
