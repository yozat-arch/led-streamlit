import streamlit as st
import matplotlib.pyplot as plt

st.title("LED 配置シミュレーター（STEP3：蛇行）")

cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=10)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)

fig, ax = plt.subplots()

order = 1

for y in range(rows):
    # 偶数行は左→右、奇数行は右→左
    if y % 2 == 0:
        x_range = range(cols)
    else:
        x_range = range(cols - 1, -1, -1)

    for x in x_range:
        draw_x = x
        draw_y = rows - y - 1

        ax.add_patch(plt.Rectangle((draw_x, draw_y), 1, 1, fill=False))
        ax.text(
            draw_x + 0.5,
            draw_y + 0.5,
            str(order),
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold"
        )
        order += 1

ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_aspect("equal")
ax.axis("off")

st.pyplot(fig)
