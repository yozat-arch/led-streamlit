import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

st.set_page_config(layout="wide")
st.title("LED 配置シミュレーター（縦長パネル・現場完全版）")

# -----------------------------
# パラメータ入力
# -----------------------------
cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=10)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=4)
show_numbers = st.checkbox("番号を表示する", value=True)
scale = st.slider("図の拡大倍率", 0.5, 2.0, 1.0)

# -----------------------------
# パネルサイズ（縦長）
# -----------------------------
PANEL_W = 0.6 * scale
PANEL_H = 1.0 * scale
font_size = max(6, int(12 - cols // 5))

# -----------------------------
# 蛇行順データ作成
# -----------------------------
positions = []
order = 1
for y in range(rows):
    x_range = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)
    for x in x_range:
        positions.append({
            "order": order,
            "x": x,
            "y": rows - 1 - y,
            "row": y
        })
        order += 1

# -----------------------------
# LANケーブル計算（横：小＋最後大、縦：必要列中、H5まで大）
# -----------------------------
def calc_lan_cables(positions, cols, rows):
    small = 0
    medium = 0
    large = 0

    # 横繋ぎ
    for y in range(rows):
        small += cols - 1  # 横は段ごとに小
        large += 1          # 横最後のパネルからH5まで大

    # 縦繋ぎ（H5ラインにのみ中ケーブル）
    # 例では2本だけ必要な場合
    medium = 2  # 実際の設営に応じて列を変えることも可能

    # H5までの大ケーブルは段ごと加算済みでOK
    return small, medium, large

lan_s, lan_m, lan_l = calc_lan_cables(positions, cols, rows)

# -----------------------------
# 電源ケーブル計算（横5枚単位で小、縦は中、最後大）
# -----------------------------
def calc_power_cables(positions, cols, rows):
    small = 0
    medium = 0
    large = 0

    # 横繋ぎ
    for y in range(rows):
        full_blocks = cols // 5
        remainder = cols % 5
        small += full_blocks * 4 + max(0, remainder - 1)  # 横5枚単位で小4本
        large += full_blocks + (1 if remainder > 0 else 0)  # 5枚毎最後は大

    # 縦繋ぎ
    medium = 2  # 今回の設営例に準拠

    # 最後のパネルから電源ボックスまで大ケーブル
    large += 1

    return small, medium, large

p_s, p_m, p_l = calc_power_cables(positions, cols, rows)

# -----------------------------
# 描画関数
# -----------------------------
def draw_figure(positions, kind="LAN"):
    if kind == "LAN":
        colors = ["#E3F2FD","#E8F5E9","#F3E5F5","#FFFDE7","#FCE4EC","#E0F2F1"]
        subheader = "LAN 配線図"
    else:
        colors = ["#FFCDD2","#F8BBD0","#E1BEE7","#D1C4E9","#C5CAE9"]
        subheader = "電源 配線図"

    st.subheader(subheader)
    fig, ax = plt.subplots(figsize=(cols*0.5*scale, rows*0.8*scale))

    for idx, p in enumerate(positions):
        color = colors[idx % len(colors)]
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
                f'{p["order"]}',
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
**LANケーブル:**  
小: {lan_s}本  
中: {lan_m}本  
大: {lan_l}本  

**電源ケーブル:**  
小: {p_s}本  
中: {p_m}本  
大: {p_l}本
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
        file_name="LED_図面_縦長完全版.pdf",
        mime="application/pdf"
    )
