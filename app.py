import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================
# 基本設定
# ============================
st.set_page_config(layout="wide")
st.title("LED 配線図ジェネレーター Ver.2.2")

# ============================
# UI
# ============================
cols = st.number_input("横のLED枚数", min_value=1, value=10, step=1)
rows = st.selectbox("縦のLED枚数（最大4）", [1, 2, 3, 4], index=3)

# ============================
# 蛇行接続生成（生）
# ============================
def generate_serpentine(cols, rows):
    conns = []
    pid = lambda r, c: r * cols + c + 1

    for r in range(rows):
        col_range = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        prev = None

        for c in col_range:
            cur = pid(r, c)
            if prev:
                conns.append((prev, cur, "H"))
            prev = cur

        if r < rows - 1:
            conns.append((prev, pid(r + 1, col_range[-1]), "V"))

    return conns

raw_connections = generate_serpentine(cols, rows)

# ============================
# 系統分離（ここが核心）
# ============================
def split_by_rows(conns, rows):
    lan = []
    pwr = []

    row_breaks = rows - 1
    v_count = 0

    for f, t, d in conns:
        if d == "V":
            v_count += 1
            if v_count == row_breaks:
                continue  # 最終段は外部接続へ
        lan.append((f, t, d))
        pwr.append((f, t, d))

    return lan, pwr

lan_conns, pwr_conns = split_by_rows(raw_connections, rows)

# ============================
# ケーブル本数計算
# ============================
def count_cables(conns, rows):
    s = m = 0
    for _, _, d in conns:
        if d == "H":
            s += 1
        elif d == "V":
            m += 1
    l = max(rows - 1, 0)
    return s, m, l

lan_s, lan_m, lan_l = count_cables(lan_conns, rows)
pwr_s, pwr_m, pwr_l = count_cables(pwr_conns, rows)

# ============================
# 図面描画
# ============================
def draw(cols, rows, conns, title, color_map):
    fig, ax = plt.subplots(figsize=(cols * 0.9, rows * 2.2))
    pw, ph = 1, 2

    pos = {}
    for r in range(rows):
        for c in range(cols):
            x, y = c, rows - r - 1
            pid = r * cols + c + 1
            pos[pid] = (x + 0.5, y + 1)
            ax.add_patch(Rectangle((x, y), pw, ph, fill=False))
            ax.text(x + 0.5, y + 1, str(pid), ha="center", va="center", fontsize=9)

    for f, t, d in conns:
        x1, y1 = pos[f]
        x2, y2 = pos[t]
        style = "--" if d == "OUT" else "-"
        ax.plot([x1, x2], [y1, y2], color=color_map[d], linewidth=2, linestyle=style)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows * 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, pad=5)

    return fig

# ============================
# 表示
# ============================
st.subheader("LAN配線図")
st.pyplot(draw(
    cols, rows, lan_conns, "LAN配線図",
    {"H": "blue", "V": "green"}
))
st.write(f"小：{lan_s} 本　中：{lan_m} 本　大：{lan_l} 本")

st.subheader("電源配線図")
st.pyplot(draw(
    cols, rows, pwr_conns, "電源配線図",
    {"H": "red", "V": "orange"}
))
st.write(f"小：{pwr_s} 本　中：{pwr_m} 本　大：{pwr_l} 本")
