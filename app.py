import streamlit as st
import matplotlib.pyplot as plt

st.title("LED 配置シミュレーター（LAN図 / 電源図 分離）")

cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=10)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)

# ===== 共通：蛇行順の座標リストを作る =====
positions = []
order = 1

for y in range(rows):
    x_range = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)
    for x in x_range:
        draw_x = x
        draw_y = rows - y - 1
        positions.append({
            "order": order,
            "x": draw_x,
            "y": draw_y,
            "lan": (order - 1) // 11 + 1,
            "power": (order - 1) // 5 + 1
        })
        order += 1

# ===== LAN 図 =====
st.subheader("LAN 配線図")

fig1, ax1 = plt.subplots()
lan_colors = ["#E3F2FD", "#E8F5E9", "#F3E5F5", "#FFFDE7", "#FCE4EC", "#E0F2F1"]

for p in positions:
    color = lan_colors[(p["lan"] - 1) % len(lan_colors)]
    ax1.add_patch(
        plt.Rectangle((p["x"], p["y"]), 1, 1, facecolor=color, edgecolor="black")
    )
    ax1.text(
        p["x"] + 0.5,
        p["y"] + 0.5,
        f'{p["order"]}\nLAN{p["lan"]}',
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

ax1.set_xlim(0, cols)
ax1.set_ylim(0, rows)
ax1.set_aspect("equal")
ax1.axis("off")
st.pyplot(fig1)

# ===== 電源 図 =====
st.subheader("電源 配線図")

fig2, ax2 = plt.subplots()
power_colors = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9"]

for p in positions:
    color = power_colors[(p["power"] - 1) % len(power_colors)]
    ax2.add_patch(
        plt.Rectangle((p["x"], p["y"]), 1, 1, facecolor=color, edgecolor="black")
    )
    ax2.text(
        p["x"] + 0.5,
        p["y"] + 0.5,
        f'{p["order"]}\nPWR{p["power"]}',
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

ax2.set_xlim(0, cols)
ax2.set_ylim(0, rows)
ax2.set_aspect("equal")
ax2.axis("off")
st.pyplot(fig2)
