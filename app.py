import streamlit as st
import matplotlib.pyplot as plt

st.title("LED 配置シミュレーター（STEP2）")

cols = st.number_input("横のLED枚数", min_value=1, max_value=50, value=10)
rows = st.number_input("縦のLED枚数（最大4）", min_value=1, max_value=4, value=3)

fig, ax = plt.subplots()

for y in range(rows):
    for x in range(cols):
        ax.add_patch(plt.Rectangle((x, rows - y - 1), 1, 1, fill=False))
        ax.text(
            x + 0.5,
            rows - y - 0.5,
            f"{y},{x}",
            ha="center",
            va="center",
            fontsize=8
        )

ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_aspect("equal")
ax.axis("off")

st.pyplot(fig)
