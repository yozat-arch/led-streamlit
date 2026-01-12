import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

st.set_page_config(layout="wide")
st.title("LED 配置シミュレーター（縦長パネル版 完全版）")

# -----------------------------
# パラメータ入力
# -----------------------------
cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=30)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)
show_numbers = st.checkbox("番号を表示する", value=True)
scale = st.slider("図の拡大倍率", 0.5, 2.0, 1.0)

# -----------------------------
# パネルサイズ（縦長）
# -----------------------------
PANEL_W = 0.6 * scale  # 横幅を短く
PANEL_H = 1.0 * scale  # 縦を長く

# フォントサイズ自動調整
font_size = max(6, int(12 - cols // 5))

# -----------------------------
# 蛇行順データ
# -----------------------------
positions = []
order = 1
for y in range(rows):
    x_range = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)
    for x in x_range:
        positions.append({
            "order": order,
            "x": x,
            "y": rows - y - 1,
            "lan": (order - 1) // 11 + 1,
            "power": (order - 1) // 5 + 1,
            "vert": y  # 0=横繋ぎ、1以上=縦繋ぎ
        })
        order += 1

# -----------------------------
# ケーブル計算
# -----------------------------
def calc_cables(positions):
    power_small = 0
    power_medium = 0
    power_large = 0
    lan_small = 0
    lan_medium = 0
    lan_large = 0

    for p in positions:
        # 縦繋ぎ
        if p["vert"] > 0:
            power_medium += 1
            lan_medium += 1
        else:
            # 電源
            if p["order"] % 5 == 0:
                power_large += 1
            else:
                power_small += 1
            # LAN
            if p["order"] % 10 == 0:
                lan_large += 1
            else:
                lan_small += 1
    return power_small, power_medium, power_large, lan_small, lan_medium, lan_large

p_s, p_m, p_l, l_s, l_m, l_l = calc_cables(positions)

# -----------------------------
# 図を作る関数
# -----------------------------
def draw_figure(positions, kind="LAN"):
    if kind == "LAN":
        colors = ["#E3F2FD", "#E8F5E9", "#F3E5F5", "#FFFDE7", "#FCE4EC", "#E0F2F1"]
        label_key = "lan"
        subheader = "LAN 配線図"
    else:
        colors = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9"]
        label_key = "power"
        subheader = "電源 配線図"

    st.subheader(subheader)
    fig, ax = plt.subplots(figsize=(cols*0.5*scale, rows*0.8*scale))

    for p in positions:
        color = colors[(p[label_key]-1) % len(colors)]
        ax.add_patch(
            plt.Rectangle(
                (p["x"]*PANEL_W, p["y"]*PANEL_H),
                PANEL_W,
                PANEL_H,
                facecolor=color,
                edgecolor="black"
            )
        )
        if show_numbers:
            ax.text(
                p["x"]*PANEL_W + PANEL_W/2,
                p["y"]*PANEL_H + PANEL_H/2,
                f'{p["order"]}\n{label_key.upper()}{p[label_key]}',
                ha="center",
                va="center",
                fontsize=font_size,
                fontweight="bold"
            )
    ax.set_xlim(0, cols*PANEL_W)
    ax.set_ylim(0, rows*PANEL_H)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)
    return fig

# -----------------------------
# 描画
# -----------------------------
fig_lan = draw_figure(positions, kind="LAN")
fig_power = draw_figure(positions, kind="power")

# -----------------------------
# ケーブル本数表示
# -----------------------------
st.subheader("必要ケーブル本数")
st.markdown(f"""
**電源ケーブル:**  
小: {p_s}本  
中: {p_m}本  
大: {p_l}本  

**LANケーブル:**  
小: {l_s}本  
中: {l_m}本  
大: {l_l}本
""")

# -----------------------------
# PDF出力
# -----------------------------
pdf_buffer = io.BytesIO()
if st.button("PDF出力"):
    with PdfPages(pdf_buffer) as pdf:
        pdf.savefig(fig_lan)
        pdf.savefig(fig_power)
    pdf_buffer.seek(0)
    st.download_button(
        label="PDFダウンロード",
        data=pdf_buffer,
        file_name="LED_図面_縦長版.pdf",
        mime="application/pdf"
    )
