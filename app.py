import streamlit as st
import matplotlib.pyplot as plt

st.title("LED 配置シミュレーター（STEP4：LAN系統）")

cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=10)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)

fig, ax = plt.subplots()

order = 1

colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#FFCCFF", "#CCFFFF"]

for y in range(rows):
    x_range = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)

    for x in x_range:
        draw_x = x
        draw_y = rows - y - 1

        lan_group = (order - 1) // 11
        color = colors[lan_group % len(colors)]

        ax.add_patch(
            plt.Rectangle(
                (draw_x, draw_y),
                1,
                1,
                facecolor=color,
                edgecolor="black"
            )
        )

        ax.text(
            draw_x + 0.5,
            draw_y + 0.5,
            f"{order}\nLAN{lan_group+1}",
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold"
        )

        order += 1

ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_aspect("equal")
ax.axis("off")

st.pyplot(fig)
