import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ----------------------------
# 基本設定
# ----------------------------
st.set_page_config(layout="wide")
st.title("LED 配線図ジェネレーター Ver.2")

# ----------------------------
# UI
# ----------------------------
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

# ----------------------------
# 蛇行接続リスト生成
# ----------------------------
def generate_serpentine_connections(cols, rows):
    connections = []

    panel_id = lambda r, c: r * cols + c + 1

    for r in range(rows):
        col_range = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        prev = None

        for c in col_range:
            current = panel_id(r, c)
            if prev is not None:
                connections.append({
                    "from": prev,
                    "to": current,
                    "dir": "H"
                })
            prev = current

        if r < rows - 1:
            next_panel = panel_id(r + 1, col_range[-1])
            connections.append({
                "from": prev,
                "to": next_panel,
                "dir": "V"
            })

    return connections

connections = generate_serpentine_connections(cols, rows)

# ----------------------------
# LANケーブル計算（確定版）
# ----------------------------
def calc_lan_cables(connections, rows):
    small = 0
    medium = 0

    for c in connections:
        if c["dir"] == "H":
            small += 1
        elif c["dir"] == "V":
            medium += 1

    large = max(rows - 1, 0)

    return small, medium, large

lan_small, lan_medium, lan_large = calc_lan_cables(connections, rows)

# ----------------------------
# 電源ケーブル計算（暫定・LAN思想準拠）
# ----------------------------
def calc_power_cables(connections, rows):
    small = 0
    medium = 0

    for c in connections:
        if c["dir"] == "H":
            small += 1
        elif c["dir"] == "V":
            medium += 1

    large = max(rows - 1, 0)

    return small, medium, large

pwr_small, pwr_medium, pwr_large = calc_power_cables(connections, rows)

# ----------------------------
# 図面描画
# ----------------------------
def draw_led_diagram(cols, rows, title):
    fig, ax = plt.subplots(figsize=(cols * 0.8, rows * 1.6))

    panel_w = 1.0
    panel_h = 2.0  # 縦長

    for r in range(rows):
        for c in range(cols):
            x = c
            y = rows - r - 1
            rect = Rectangle((x, y), panel_w, panel_h, fill=False)
            ax.add_patch(rect)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title)

    return fig

# ----------------------------
# 表示
# ----------------------------
st.subheader("LAN 配線図")
st.pyplot(draw_led_diagram(cols, rows, "LAN Diagram"))

st.subheader("電源 配線図")
st.pyplot(draw_led_diagram(cols, rows, "Power Diagram"))

st.subheader("ケーブル本数")

st.markdown("### LANケーブル")
st.write(f"小：{lan_small} 本")
st.write(f"中：{lan_medium} 本")
st.write(f"大：{lan_large} 本")

st.markdown("### 電源ケーブル")
st.write(f"小：{pwr_small} 本")
st.write(f"中：{pwr_medium} 本")
st.write(f"大：{pwr_large} 本")
