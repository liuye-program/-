#!/usr/bin/env python3
"""
AlphaHerb Phase 0 — cross-functional swimlane flowchart (Visio-like), PNG export.

Regenerate: python3 scripts/generate_alphaherb_swimlane.py
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patches import Ellipse

# Chinese-capable font
for fname in (
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
):
    try:
        font_manager.fontManager.addfont(fname)
    except OSError:
        continue

plt.rcParams["font.sans-serif"] = [
    "WenQuanYi Micro Hei",
    "WenQuanYi Zen Hei",
    "Droid Sans Fallback",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


def rounded_box(ax, xy, w, h, face, edge="#334155", lw=1.05, radius=0.01):
    x, y = xy
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.003,rounding_size={radius}",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
        mutation_aspect=1,
    )
    ax.add_patch(box)
    return box


def db_shape(ax, xy, w, h, face, edge="#334155"):
    x, y = xy
    eh = min(h * 0.18, 0.028)
    top = Ellipse((x + w / 2, y + h), w * 0.85, eh * 2, facecolor=face, edgecolor=edge, linewidth=1.05)
    bot = Ellipse((x + w / 2, y), w * 0.85, eh * 2, facecolor=face, edgecolor=edge, linewidth=1.05)
    body = mpatches.Rectangle((x + w * 0.075, y), w * 0.85, h, facecolor=face, edgecolor=edge, linewidth=0)
    ax.add_patch(body)
    ax.add_patch(
        mpatches.Rectangle((x + w * 0.075, y), w * 0.85, h, fill=False, edgecolor=edge, linewidth=1.05)
    )
    ax.add_patch(top)
    ax.add_patch(bot)


def center_text(ax, xy, w, h, lines, fontsize=7.0, color="#0f172a", weight="normal"):
    x, y = xy
    ax.text(
        x + w / 2,
        y + h / 2,
        "\n".join(lines),
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        weight=weight,
        linespacing=1.12,
    )


def arrow(ax, p0, p1, text="", color="#1d4ed8", lw=1.25, dashed=False):
    arr = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="->",
        mutation_scale=11,
        linewidth=lw,
        color=color,
        linestyle="--" if dashed else "-",
        shrinkA=4,
        shrinkB=4,
        connectionstyle="arc3,rad=0",
    )
    ax.add_patch(arr)
    if text:
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        ax.text(
            mx,
            my + 0.014,
            text,
            ha="center",
            va="bottom",
            fontsize=6.1,
            color="#1e293b",
            bbox=dict(boxstyle="round,pad=0.12", facecolor="#ffffff", edgecolor="#cbd5e1", alpha=0.95),
        )


def curved_arrow(ax, p0, p1, rad=0.12, text="", color="#1d4ed8", dashed=False):
    arr = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="->",
        mutation_scale=10,
        linewidth=1.15,
        color=color,
        linestyle="--" if dashed else "-",
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arr)
    if text:
        mx = (p0[0] + p1[0]) / 2 + rad * 0.12
        my = (p0[1] + p1[1]) / 2 + abs(rad) * 0.1
        ax.text(
            mx,
            my,
            text,
            ha="center",
            va="center",
            fontsize=5.9,
            color="#1e293b",
            bbox=dict(boxstyle="round,pad=0.1", facecolor="#ffffff", edgecolor="#cbd5e1", alpha=0.95),
        )


def draw_diagram(ax):
    """Draw swimlane diagram on given axes (0..1)."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    lanes = [
        (0.885, 0.998, "#e0e7ff", "1  硬件层  Hardware"),
        (0.685, 0.875, "#ede9fe", "2  计算机视觉引擎  AlphaHerb AI"),
        (0.545, 0.672, "#d1fae5", "3  数据服务层  Data services"),
        (0.255, 0.528, "#dbeafe", "4  HerbMain 云  Platform / DB / Terminals"),
        (0.038, 0.238, "#ffedd5", "5  会诊管理控制  Consultation control"),
    ]
    lane_x0 = 0.125
    for y0, y1, color, title in lanes:
        ax.add_patch(
            mpatches.Rectangle(
                (lane_x0, y0),
                1 - lane_x0 - 0.018,
                y1 - y0,
                facecolor=color,
                edgecolor="#94a3b8",
                linewidth=0.75,
                alpha=0.52,
            )
        )
        ax.text(
            lane_x0 + 0.0085,
            (y0 + y1) / 2,
            title,
            ha="left",
            va="center",
            fontsize=8.2,
            weight="bold",
            color="#334155",
            rotation=90,
        )

    # Nodes (x, y, w, h)
    hw1 = (0.155, 0.902, 0.098, 0.062)
    hw2 = (0.27, 0.902, 0.118, 0.062)
    rounded_box(ax, (hw1[0], hw1[1]), hw1[2], hw1[3], "#a5b4fc")
    center_text(ax, (hw1[0], hw1[1]), hw1[2], hw1[3], ["门口摄像头", "Entrance camera"])
    rounded_box(ax, (hw2[0], hw2[1]), hw2[2], hw2[3], "#a5b4fc")
    center_text(ax, (hw2[0], hw2[1]), hw2[2], hw2[3], ["店内摄像头（多角度）", "In-store cameras"])

    det = (0.405, 0.738, 0.108, 0.072)
    face = (0.535, 0.778, 0.108, 0.064)
    beh = (0.535, 0.652, 0.115, 0.072)
    gait = (0.535, 0.558, 0.115, 0.068)
    for box, lines in (
        (det, ["人体检测模块", "Human body detection"]),
        (face, ["人脸特征提取", "Face embedding"]),
        (beh, ["行为分析模块", "Path + heat zone"]),
        (gait, ["步态分析模块", "Pose / gait / stride"]),
    ):
        rounded_box(ax, (box[0], box[1]), box[2], box[3], "#c4b5fd")
        center_text(ax, (box[0], box[1]), box[2], box[3], lines)

    persona = (0.695, 0.568, 0.138, 0.09)
    rounded_box(ax, (persona[0], persona[1]), persona[2], persona[3], "#34d399", edge="#047857", lw=1.2)
    center_text(
        ax,
        (persona[0], persona[1]),
        persona[2],
        persona[3],
        ["行为画像生成引擎", "Behavior persona engine"],
        fontsize=7.3,
        weight="bold",
    )

    ff_db = (0.695, 0.798, 0.108, 0.052)
    db_shape(ax, (ff_db[0], ff_db[1]), ff_db[2], ff_db[3], "#93c5fd")
    center_text(ax, (ff_db[0], ff_db[1] + 0.008), ff_db[2], ff_db[3] - 0.016, ["人脸特征库", "Face feature store"])

    beh_db = (0.855, 0.448, 0.098, 0.05)
    db_shape(ax, (beh_db[0], beh_db[1]), beh_db[2], beh_db[3], "#93c5fd")
    center_text(ax, (beh_db[0], beh_db[1] + 0.008), beh_db[2], beh_db[3] - 0.016, ["行为数据库", "Behavior DB"])

    staff = (0.695, 0.348, 0.108, 0.06)
    doc = (0.695, 0.258, 0.108, 0.06)
    rounded_box(ax, (staff[0], staff[1]), staff[2], staff[3], "#7dd3fc")
    center_text(ax, (staff[0], staff[1]), staff[2], staff[3], ["店员终端", "Staff PC / platform"])
    rounded_box(ax, (doc[0], doc[1]), doc[2], doc[3], "#7dd3fc")
    center_text(ax, (doc[0], doc[1]), doc[2], doc[3], ["中医师手持设备", "Phone / tablet"])

    pat = (0.855, 0.328, 0.098, 0.05)
    vis = (0.855, 0.248, 0.098, 0.05)
    db_shape(ax, (pat[0], pat[1]), pat[2], pat[3], "#93c5fd")
    center_text(ax, (pat[0], pat[1] + 0.008), pat[2], pat[3] - 0.016, ["患者档案库", "Patient records"])
    db_shape(ax, (vis[0], vis[1]), vis[2], vis[3], "#93c5fd")
    center_text(ax, (vis[0], vis[1] + 0.008), vis[2], vis[3] - 0.016, ["就诊记录库", "Consultation records"])

    fusion = (0.545, 0.368, 0.108, 0.064)
    rounded_box(ax, (fusion[0], fusion[1]), fusion[2], fusion[3], "#38bdf8", edge="#0369a1")
    center_text(ax, (fusion[0], fusion[1]), fusion[2], fusion[3], ["多源数据融合处理", "Multi-source fusion"])

    sess = (0.545, 0.092, 0.115, 0.072)
    voice = (0.695, 0.102, 0.098, 0.052)
    env_m = (0.835, 0.102, 0.098, 0.052)
    rounded_box(ax, (sess[0], sess[1]), sess[2], sess[3], "#fb923c", edge="#c2410c", lw=1.15)
    center_text(ax, (sess[0], sess[1]), sess[2], sess[3], ["诊疗会话控制", "Consultation session"], weight="bold")
    rounded_box(ax, (voice[0], voice[1]), voice[2], voice[3], "#fdba74")
    center_text(ax, (voice[0], voice[1]), voice[2], voice[3], ["实时语音引擎", "Real-time voice"])
    rounded_box(ax, (env_m[0], env_m[1]), env_m[2], env_m[3], "#fdba74")
    center_text(ax, (env_m[0], env_m[1]), env_m[2], env_m[3], ["环境感知模块", "Environment perception"])

    # --- Flows ---
    arrow(ax, (hw1[0] + hw1[2], hw1[1] + hw1[3] / 2), (hw2[0], hw2[1] + hw2[3] / 2), "视频流")
    arrow(ax, (hw2[0] + hw2[2], hw2[1] + hw2[3] / 2), (det[0], det[1] + det[3] / 2), "视频流")

    curved_arrow(
        ax,
        (det[0] + det[2], det[1] + det[3] * 0.72),
        (face[0], face[1] + face[3] * 0.5),
        rad=0.07,
        text="人脸区域",
    )
    arrow(
        ax,
        (det[0] + det[2] * 0.32, det[1]),
        (beh[0] + beh[2] * 0.15, beh[1] + beh[3]),
        "检测到的人体",
        color="#5b21b6",
    )
    arrow(
        ax,
        (det[0] + det[2] * 0.68, det[1]),
        (gait[0] + gait[2] * 0.15, gait[1] + gait[3]),
        "检测到的人体",
        color="#5b21b6",
    )

    arrow(
        ax,
        (face[0] + face[2], face[1] + face[3] / 2),
        (ff_db[0], ff_db[1] + ff_db[3] / 2),
        "特征向量\n512 维",
    )
    arrow(
        ax,
        (ff_db[0] + ff_db[2] / 2, ff_db[1]),
        (persona[0] + persona[2] * 0.28, persona[1] + persona[3]),
        "匹配结果\n患者ID / 未访",
        color="#b45309",
    )

    arrow(
        ax,
        (beh[0] + beh[2], beh[1] + beh[3] / 2),
        (persona[0], persona[1] + persona[3] * 0.75),
        "行为轨迹\n商品·停留",
    )
    arrow(
        ax,
        (gait[0] + gait[2], gait[1] + gait[3] / 2),
        (persona[0], persona[1] + persona[3] * 0.28),
        "步态 / 步幅 / 姿态",
    )

    arrow(
        ax,
        (persona[0] + persona[2], persona[1] + persona[3] / 2),
        (beh_db[0], beh_db[1] + beh_db[3] / 2),
        "行为画像切片\nJSON",
    )

    curved_arrow(
        ax,
        (persona[0] + persona[2] * 0.42, persona[1]),
        (staff[0] + staff[2] * 0.5, staff[1] + staff[3]),
        rad=-0.22,
        text="到店感知 / 行为录像切片\nWebSocket",
    )
    curved_arrow(
        ax,
        (persona[0] + persona[2] * 0.82, persona[1]),
        (doc[0] + doc[2] * 0.5, doc[1] + doc[3]),
        rad=-0.18,
        text="WebSocket",
    )

    arrow(ax, (staff[0] + staff[2], staff[1] + staff[3] / 2), (pat[0], pat[1] + pat[3] / 2), "搜索结果\n患者档案")
    arrow(ax, (doc[0] + doc[2], doc[1] + doc[3] / 2), (pat[0], pat[1] + pat[3] / 2), "搜索请求\n姓名 / 手机")

    arrow(ax, (pat[0] + pat[2] / 2, pat[1]), (vis[0] + vis[2] / 2, vis[1] + vis[3]), "关联", color="#64748b")
    arrow(ax, (vis[0] + vis[2] / 2, vis[1] + vis[3]), (pat[0] + pat[2] / 2, pat[1]), "", color="#94a3b8")

    arrow(ax, (staff[0] + staff[2] * 0.35, staff[1]), (fusion[0] + fusion[2] / 2, fusion[1] + fusion[3]), "鉴权 / 查询\nREST", color="#0369a1")
    arrow(ax, (doc[0] + doc[2] * 0.65, doc[1]), (fusion[0] + fusion[2] * 0.55, fusion[1] + fusion[3]), "REST", color="#0369a1")

    arrow(ax, (fusion[0] + fusion[2], fusion[1] + fusion[3] * 0.68), (pat[0], pat[1] + pat[3] * 0.72), "更新档案")
    arrow(ax, (fusion[0] + fusion[2], fusion[1] + fusion[3] * 0.32), (vis[0], vis[1] + vis[3] * 0.62), "写入就诊记录")

    arrow(
        ax,
        (staff[0] + staff[2] / 2, staff[1]),
        (sess[0] + sess[2] * 0.32, sess[1] + sess[3]),
        "开始诊疗\nREST",
        color="#c2410c",
    )
    arrow(
        ax,
        (doc[0] + doc[2] / 2, doc[1]),
        (sess[0] + sess[2] * 0.68, sess[1] + sess[3]),
        "开始诊疗\nREST",
        color="#c2410c",
    )

    curved_arrow(
        ax,
        (fusion[0] + fusion[2] / 2, fusion[1]),
        (sess[0] + sess[2] / 2, sess[1] + sess[3]),
        rad=0.14,
        text="会话元数据 / 关联\nREST",
        color="#c2410c",
        dashed=True,
    )

    arrow(ax, (sess[0] + sess[2], sess[1] + sess[3] * 0.58), (voice[0], voice[1] + voice[3] / 2), "启动", color="#c2410c")
    arrow(ax, (sess[0] + sess[2], sess[1] + sess[3] * 0.38), (env_m[0], env_m[1] + env_m[3] / 2), "启动", color="#c2410c")

    ax.text(
        0.125,
        0.012,
        "图例：蓝色=数据流  |  紫色=检测分支  |  棕色=身份匹配反馈  |  青/橙=REST 与控制  |  虚线=会话侧写  |  圆柱=数据库",
        fontsize=6.6,
        color="#475569",
    )


def export_png(path: str, dpi: int = 220) -> None:
    fig_w, fig_h = 20, 12.5
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=100)
    fig.patch.set_facecolor("#f8fafc")

    fig.text(
        0.5,
        0.97,
        "AlphaHerb Phase 0 — 系统流程及数据流转图（跨职能泳道）",
        ha="center",
        va="top",
        fontsize=14.5,
        weight="bold",
        color="#0f172a",
    )
    fig.text(
        0.5,
        0.945,
        "Visio-style swimlane · left → right: capture → AI → services → cloud → session control",
        ha="center",
        va="top",
        fontsize=9.2,
        color="#64748b",
        style="italic",
    )

    ax_content = fig.add_axes((0.04, 0.02, 0.92, 0.90))
    draw_diagram(ax_content)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.patch.get_facecolor(), edgecolor="none")
    plt.close(fig)


def main():
    out_png = "/workspace/docs/alphaherb_phase0_swimlane.png"
    export_png(out_png, dpi=220)
    print("Wrote", out_png)


if __name__ == "__main__":
    main()
