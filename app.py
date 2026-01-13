import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================
# 基本設定
# ============================
st.set_page_config(layout="wide")
st.title("LED 配線図ジェネレーター Ver.2.1")

# ============================
# UI
# ============================
cols = st.number_input(
    "横のLED枚数",
    min_value=1,
    value=10,
    step=1
)

rows = st.selectbox(
    "縦のLED枚数（最大4）",
    options=[1, 2, 3, 4],
    index=3
)

# ============================
# 蛇行接続生成
# ============================
def generate_serpentine_connections(cols, rows):
    connections = []
    panel_id = lambda r, c: r * cols + c + 1

    for r in range(rows):
        col_range = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        prev = None

        for c in col_range:
            cur = panel_id(r, c)
            if prev is not None:
                connections.append({"from": prev, "to": cur, "dir": "H"})
            prev = cur

        if r < rows - 1:
            down = panel_id(r + 1, col_range[-1])
            connections.append({"from": prev, "to": down, "dir": "V"})

    return connections

connections = generate_serpentine_connections(cols, rows)

# ============================
# ケーブル計算
# ============================
def calc_cables(connections, rows):
    small = medium = 0
    for c in connections:
        if c["dir"] == "H":
            small += 1
        elif c["dir"] == "V":
            medium += 1
    large = max(rows - 1, 0)
    return small, medium, large

lan_small, lan_medium, lan_large = calc_cables(connections, rows)
pwr_small, pwr_medium, pwr_large = calc_cables(connections, rows)

# ============================
# 図面描画
# ============================
def draw_diagram(cols, rows, connections, title, color):
    fig, ax = plt.subplots(figsize=(cols * 0.9, rows * 2.2))

    panel_w = 1.0
    panel_h = 2.0

    # パネル描画
    for r in range(rows):
        for c in range(cols):
            x = c
            y = rows - r - 1
            pid = r * cols + c + 1
            rect = Rectangle((x, y), panel_w, panel_h, fill=False)
            ax.add_patch(rect)
            ax.text(x + 0.5, y + 1.0, str(pid),
                    ha="center", va="center", fontsize=9)

    # ケーブル描画
    pos = {}
    for r in range(rows):
        for c in range(cols):
            pid = r * cols + c + 1
            pos[pid] = (c + 0.5, rows - r - 1 + 1.0)

    for c in connections:
        x1, y1 = pos[c["from"]]
        x2, y2 = pos[c["to"]]
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=2)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows * 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)

    return fig

# ============================
# 表示
# ============================
st.subheader("LAN 配線図")
st.pyplot(draw_diagram(cols, rows, connections, "LAN 配線図", "blue"))

st.subheader("電源 配線図")
st.pyplot(draw_diagram(cols, rows, connections, "電源 配線図", "red"))

st.subheader("ケーブル本数")

st.markdown("### LANケーブル")
st.write(f"小：{lan_small} 本")
st.write(f"中：{lan_medium} 本")
st.write(f"大：{lan_large} 本")

st.markdown("### 電源ケーブル")
st.write(f"小：{pwr_small} 本")
st.write(f"中：{pwr_medium} 本")
st.write(f"大：{pwr_large} 本")
