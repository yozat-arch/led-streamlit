import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("LED 配置シミュレーター（縦長パネル・安定版）")

# -----------------------------
# UI
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
# 蛇行配置データ
# -----------------------------
positions = []
order = 1

for row in range(rows):
    x_range = range(cols) if row % 2 == 0 else range(cols - 1, -1, -1)
    for x in x_range:
        positions.append({
            "order": order,
            "x": x,
            "y": rows - 1 - row,
            "row": row,
            "col": x
        })
        order += 1

# -----------------------------
# 描画関数
# -----------------------------
def draw_figure(title):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(cols * 0.6 * scale, rows * 1.0 * scale))

    for p in positions:
        ax.add_patch(
            plt.Rectangle(
                (p["col"] * PANEL_W, p["y"] * PANEL_H),
                PANEL_W,
                PANEL_H,
                edgecolor="black",
                facecolor="#E3F2FD"
            )
        )
        if show_numbers:
            ax.text(
                p["col"] * PANEL_W + PANEL_W / 2,
                p["y"] * PANEL_H + PANEL_H / 2,
                str(p["order"]),
                ha="center",
                va="center",
                fontsize=font_size,
                fontweight="bold"
            )

    ax.set_xlim(0, cols * PANEL_W)
    ax.set_ylim(0, rows * PANEL_H)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)

# -----------------------------
# 図面表示
# -----------------------------
draw_figure("LAN 配線図（仮）")
draw_figure("電源 配線図（仮）")


def generate_serpentine_connections(cols, rows):
    """
    蛇行順でパネル同士の接続リストを生成する
    戻り値: list of dict
    """
    connections = []

    panel_id = lambda r, c: r * cols + c + 1

    for r in range(rows):
        if r % 2 == 0:
            col_range = range(cols)
        else:
            col_range = range(cols - 1, -1, -1)

        prev_panel = None

        for c in col_range:
            current = panel_id(r, c)

            # 横接続
            if prev_panel is not None:
                connections.append({
                    "from": prev_panel,
                    "to": current,
                    "dir": "H"
                })

            prev_panel = current

        # 行の終端で次の行へ（蛇行）
        if r < rows - 1:
            next_col = col_range[-1]
            down_panel = panel_id(r + 1, next_col)

            connections.append({
                "from": prev_panel,
                "to": down_panel,
                "dir": "V"
            })

    return connections




#---------------
# 確認入力
#---------------

st.subheader("接続リスト（デバッグ表示）")

lan_connections = generate_serpentine_connections(cols, rows)

for c in lan_connections:
    st.write(f'{c["from"]} -> {c["to"]} ({c["dir"]})')


def calc_lan_cables(connections, rows):
    small = 0
    medium = 0
    large = 0

    # パネル同士
    for c in connections:
        if c["dir"] == "H":
            small += 1
        elif c["dir"] == "V":
            medium += 1

    # H5への大ケーブル（系統数）
    large = rows - 1

    return {
        "small": small,
        "medium": medium,
        "large": large
    }


st.subheader("LANケーブル本数")

lan_counts = calc_lan_cables(lan_connections, rows)

st.write(f"小ケーブル: {lan_counts['small']} 本")
st.write(f"中ケーブル: {lan_counts['medium']} 本")
st.write(f"大ケーブル: {lan_counts['large']} 本")
