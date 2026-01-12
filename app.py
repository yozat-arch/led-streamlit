import streamlit as st
import matplotlib.pyplot as plt

st.title("LED 配置シミュレーター（視認性改善版）")

cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=30)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)

# ===== パネル比率（ここを実寸に近づけられる） =====
PANEL_W = 1.0
PANEL_H = 0.6   # ← 横長LED想定

# ===== フォントサイズ自動調整 =====
font_size = max(6, 12 - cols // 5)

# ===== 図サイズを動的に =====
fig_width = cols * 0.5
fig_height = rows * 0.8

# ===== 蛇行順データ =====
positions = []
order = 1

for y in range(rows):
    x_range = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)
    for x in x_range:
        positions.append({
            "order": order,
            "x": x * PANEL_W,
            "y": (rows - y - 1) * PANEL_H,
            "lan": (order - 1) // 11 + 1,
            "power": (order - 1) // 5 + 1
        })
        order += 1

# ===== LAN 図 =====
st.subheader("LAN 配線図")

fig1, ax1 = plt.subplots(figsize=(fig_width, fig_height))
lan_colors = ["#E3F2FD", "#E8F5E9", "#F3E5F5", "#FFFDE7", "#FCE4EC", "#E0F2F1"]

for p in positions:
    ax1.add_patch(
        plt.Rectangle(
            (p["x"], p["y"]),
            PANEL_W,
            PANEL_H,
            facecolor=lan_colors[(p["lan"] - 1) % len(lan_colors)],
            edgecolor="black"
        )
    )
    ax1.text(
        p["x"] + PANEL_W / 2,
        p["y"] + PANEL_H / 2,
        f'{p["order"]}\nLAN{p["lan"]}',
        ha="center",
        va="center",
        fontsize=font_size,
        fontweight="bold"
    )

ax1.set_xlim(0, cols * PANEL_W)
ax1.set_ylim(0, rows * PANEL_H)
ax1.set_aspect("equal")
ax1.axis("off")
st.pyplot(fig1)

# ===== 電源 図 =====
st.subheader("電源 配線図")

fig2, ax2 = plt.subplots(figsize=(fig_width, fig_height))
power_colors = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9"]

for p in positions:
    ax2.add_patch(
        plt.Rectangle(
            (p["x"], p["y"]),
            PANEL_W,
            PANEL_H,
            facecolor=power_colors[(p["power"] - 1) % len(power_colors)],
            edgecolor="black"
        )
    )
    ax2.text(
        p["x"] + PANEL_W / 2,
        p["y"] + PANEL_H / 2,
        f'{p["order"]}\nPWR{p["power"]}',
        ha="center",
        va="center",
        fontsize=font_size,
        fontweight="bold"
    )

ax2.set_xlim(0, cols * PANEL_W)
ax2.set_ylim(0, rows * PANEL_H)
ax2.set_aspect("equal")
ax2.axis("off")
st.pyplot(fig2)
