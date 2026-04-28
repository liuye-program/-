#!/usr/bin/env python3
"""
Generate AlphaHerb Phase 0 cross-functional swimlane flowchart (Visio-style) -> PNG.
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

# Chinese-capable sans
plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# --- Theme (Visio-like dark swimlane) ---
BG = "#1a1d24"
LANE_COLORS = {
    "hw": (0.95, 0.55, 0.35, 0.12),
    "ai": (0.95, 0.45, 0.65, 0.12),
    "store": (0.45, 0.75, 0.95, 0.12),
    "svc": (0.45, 0.85, 0.55, 0.12),
    "cms": (0.95, 0.45, 0.45, 0.12),
}
NODE_FILL = "#2d333b"
NODE_EDGE = "#5c6370"
TEXT = "#f0f0f0"
LABEL_PILL = "#4a5058"
ARROW = "#8b949e"


def rounded_box(ax, xy, w, h, text, fontsize=8, lw=1.2, zbase=3):
    x, y = xy
    box = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.015",
        facecolor=NODE_FILL,
        edgecolor=NODE_EDGE,
        linewidth=lw,
        zorder=zbase,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=TEXT,
        zorder=zbase + 1,
        linespacing=1.12,
    )
    return (x + w / 2, y + h / 2, w, h)


def arrow(ax, p0, p1, label=None, rad=0.0, z=2):
    style = "arc3,rad=%.2f" % rad
    arr = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="-|>",
        mutation_scale=11,
        linewidth=1.25,
        color=ARROW,
        connectionstyle=style,
        zorder=z,
    )
    ax.add_patch(arr)
    if label:
        mx = (p0[0] + p1[0]) / 2
        my = (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        length = (dx * dx + dy * dy) ** 0.5 or 1
        px, py = -dy / length * 0.018, dx / length * 0.018
        ax.text(
            mx + px,
            my + py,
            label,
            ha="center",
            va="center",
            fontsize=6.5,
            color="#c9d1d9",
            bbox=dict(boxstyle="round,pad=0.22", facecolor=LABEL_PILL, edgecolor="none", alpha=0.96),
            zorder=z + 3,
        )


def swimlane_rect(ax, x0, y0, w, h, color_rgba):
    r, g, b, a = color_rgba
    rect = mpatches.Rectangle((x0, y0), w, h, facecolor=(r, g, b, a), edgecolor="none", zorder=0)
    ax.add_patch(rect)


def main():
    fig_w, fig_h = 24, 15
    fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    lanes = [
        ("硬件端 / Hardware", 0.78, 1.0, "hw"),
        ("AlphaHerb AI（计算机视觉）", 0.58, 0.78, "ai"),
        ("HerbMan Store · 数据存储", 0.42, 0.58, "store"),
        ("数据服务层", 0.24, 0.42, "svc"),
        ("会诊管理系统", 0.0, 0.24, "cms"),
    ]
    for title, y0, y1, key in lanes:
        swimlane_rect(ax, 0, y0, 1, y1 - y0, LANE_COLORS[key])
        ax.text(
            0.012,
            (y0 + y1) / 2,
            title,
            ha="left",
            va="center",
            fontsize=11,
            color="#8b949e",
            fontweight="600",
            zorder=1,
        )

    t = ax.text(
        0.5,
        0.987,
        "AlphaHerb Phase 0 — 跨职能泳道与数据流（系统流程及数据流转）",
        ha="center",
        va="top",
        fontsize=16,
        color=TEXT,
        fontweight="bold",
        zorder=20,
    )
    t.set_path_effects([pe.withStroke(linewidth=3, foreground=BG)])

    # --- Hardware: cameras left, terminals right ---
    b1 = rounded_box(ax, (0.04, 0.855), 0.11, 0.095, "门口摄像头\n(视频采集)")
    b2 = rounded_box(ax, (0.18, 0.855), 0.11, 0.095, "店内摄像头\n(多路视频流)")
    t_clerk = rounded_box(ax, (0.66, 0.855), 0.12, 0.095, "店员终端\nPC / 平板", fontsize=7.8)
    t_doc = rounded_box(ax, (0.81, 0.855), 0.12, 0.095, "中医师手持设备\n(搜索患者)", fontsize=7.5)

    # --- AI: CV cluster ---
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (0.32, 0.62),
            0.45,
            0.13,
            boxstyle="round,pad=0.01,rounding_size=0.008",
            facecolor=(0.15, 0.12, 0.14, 0.45),
            edgecolor="#6e7681",
            linewidth=0.8,
            linestyle="--",
            zorder=1,
        )
    )
    ax.text(0.545, 0.732, "计算机视觉引擎", ha="center", va="top", fontsize=8, color="#8b9490", style="italic", zorder=2)

    m1 = rounded_box(ax, (0.34, 0.64), 0.10, 0.075, "人体检测\n模块", fontsize=7.8)
    m2 = rounded_box(ax, (0.47, 0.64), 0.10, 0.075, "人脸特征提取\n512-d 向量", fontsize=7.5)
    m3 = rounded_box(ax, (0.60, 0.64), 0.10, 0.075, "行为分析\n路径 / 热区", fontsize=7.5)
    m4 = rounded_box(ax, (0.40, 0.595), 0.10, 0.075, "步态分析\nPose 估计", fontsize=7.5)

    # Store
    s_face = rounded_box(ax, (0.72, 0.50), 0.10, 0.055, "人脸\n特征库", fontsize=7.8)
    s_beh = rounded_box(ax, (0.86, 0.50), 0.10, 0.055, "行为\n数据库", fontsize=7.8)
    s_req = rounded_box(ax, (0.72, 0.44), 0.10, 0.05, "搜索请求\n姓名 / 手", fontsize=7.5)
    s_res = rounded_box(ax, (0.86, 0.44), 0.10, 0.05, "搜索结果\n患者列表", fontsize=7.5)
    s_pat = rounded_box(ax, (0.72, 0.365), 0.10, 0.055, "患者\n档案库", fontsize=7.8)
    s_visit = rounded_box(ax, (0.86, 0.365), 0.10, 0.055, "就诊\n记录库", fontsize=7.8)

    # Data service
    f_engine = rounded_box(ax, (0.30, 0.305), 0.17, 0.065, "行为画像\n生成引擎", fontsize=8.2)
    f_ws1 = rounded_box(ax, (0.51, 0.305), 0.12, 0.065, "到达通知卡\nWebSocket 推送", fontsize=7.3)
    f_ws2 = rounded_box(ax, (0.66, 0.305), 0.12, 0.065, "行为画像切片\nWebSocket 推送", fontsize=7.3)
    f_fusion = rounded_box(ax, (0.30, 0.18), 0.17, 0.043, "多源数据\n融合处理", fontsize=8)

    # Consultation
    c_start = rounded_box(ax, (0.55, 0.105), 0.12, 0.048, "开始诊疗\nnREST 鉴权/签名", fontsize=7.5)
    c_sess = rounded_box(ax, (0.55, 0.045), 0.12, 0.048, "诊疗会话控制", fontsize=7.5)
    c_voice = rounded_box(ax, (0.72, 0.08), 0.10, 0.044, "实时\n语音引擎", fontsize=7.3)
    c_env = rounded_box(ax, (0.72, 0.03), 0.10, 0.044, "环境\n感知", fontsize=7.3)

    # --- Arrows (z=2 under nodes z=3) ---
    # Cameras
    arrow(ax, (b1[0] + b1[2] / 2, b1[1] + b1[3] * 0.1), (b2[0] - 0.01, b2[1] + b2[3] / 2), "视频流", rad=0.0, z=2)
    # Store camera -> human detect
    arrow(
        ax,
        (b2[0] + b2[2] / 2, b2[1]),
        (m1[0] + m1[2] / 2, m1[1] + m1[3]),
        "视频流",
        rad=0.14,
        z=2,
    )
    # CV
    arrow(ax, (m1[0] + m1[2] / 2, m1[1] + m1[3] * 0.5), (m2[0] - 0.01, m2[1] + m2[3] * 0.5), "人脸区域", rad=0.0, z=2)
    arrow(ax, (m1[0] + m1[2] / 2, m1[1]), (m3[0] + m3[2] / 2, m3[1] + m3[3]), "人体框", rad=-0.12, z=2)
    arrow(ax, (m1[0] + m1[2] / 2, m1[1]), (m4[0] + m4[2] / 2, m4[1] + m4[3]), "关键点", rad=0.12, z=2)
    # To DB
    arrow(ax, (m2[0] + m2[2] / 2, m2[1] + m2[3] * 0.5), (s_face[0], s_face[1] + s_face[3] * 0.5), "特征向量", rad=0.12, z=2)
    # To engine
    arrow(
        ax,
        (s_face[0] + s_face[2] * 0.5, s_face[1]),
        (f_engine[0] + f_engine[2] * 0.4, f_engine[1] + f_engine[3]),
        "匹配\n患者ID",
        rad=0.22,
        z=2,
    )
    arrow(
        ax,
        (m3[0] + m3[2] / 2, m3[1]),
        (f_engine[0] + f_engine[2] * 0.35, f_engine[1] + f_engine[3]),
        "行为轨迹",
        rad=0.18,
        z=2,
    )
    arrow(
        ax,
        (m4[0] + m4[2] / 2, m4[1]),
        (f_engine[0] + f_engine[2] * 0.2, f_engine[1] + f_engine[3]),
        "步态特征",
        rad=0.2,
        z=2,
    )
    # Engine out
    arrow(
        ax,
        (f_engine[0] + f_engine[2], f_engine[1] + f_engine[3] * 0.5),
        (f_ws1[0], f_ws1[1] + f_ws1[3] * 0.45),
        "",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (f_engine[0] + f_engine[2] * 0.9, f_engine[1] + f_engine[3] * 0.25),
        (f_ws2[0] - 0.015, f_ws2[1] + f_ws2[3] * 0.3),
        "JSON",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (f_engine[0] + f_engine[2] * 0.5, f_engine[1]),
        (s_beh[0] + s_beh[2] * 0.5, s_beh[1] + s_beh[3]),
        "行为画像",
        rad=0.0,
        z=2,
    )
    # Up to hardware terminals
    arrow(
        ax,
        (f_engine[0] + f_engine[2] * 0.1, f_engine[1] + f_engine[3] * 0.55),
        (t_clerk[0] + t_clerk[2] * 0.5, t_clerk[1]),
        "WebSocket",
        rad=0.42,
        z=2,
    )
    arrow(
        ax,
        (f_engine[0] + f_engine[2] * 0.25, f_engine[1] + f_engine[3] * 0.5),
        (t_doc[0] + t_doc[2] * 0.5, t_doc[1]),
        "WebSocket",
        rad=0.35,
        z=2,
    )
    # Search: device <-> store
    arrow(
        ax,
        (t_doc[0] + t_doc[2] * 0.5, t_doc[1]),
        (s_req[0] + s_req[2] * 0.5, s_req[1] + s_req[3]),
        "搜索",
        rad=0.2,
        z=2,
    )
    arrow(
        ax,
        (s_res[0] + s_res[2] * 0.5, s_res[1] + s_res[3] * 0.5),
        (t_doc[0] + t_doc[2] * 0.5, t_doc[1] + t_doc[3]),
        "结果",
        rad=0.18,
        z=2,
    )
    arrow(ax, (s_req[0] + s_req[2] * 0.5, s_req[1]), (s_pat[0] + s_pat[2] * 0.5, s_pat[1] + s_pat[3]), "查档案", rad=0.0, z=2)
    arrow(
        ax,
        (s_pat[0] + s_pat[2] * 0.5, s_pat[1]),
        (s_res[0] + s_res[2] * 0.5, s_res[1] + s_res[3] * 0.5),
        "列表",
        rad=0.0,
        z=2,
    )
    # Fusion
    arrow(
        ax,
        (f_fusion[0] + f_fusion[2] * 0.5, f_fusion[1] + f_fusion[3]),
        (c_start[0] + c_start[2] * 0.5, c_start[1] + c_start[3] * 0.5),
        "nREST",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (f_fusion[0] + f_fusion[2], f_fusion[1] + f_fusion[3] * 0.4),
        (s_pat[0], s_pat[1] + s_pat[3] * 0.3),
        "更新档案",
        rad=0.2,
        z=2,
    )
    arrow(
        ax,
        (f_fusion[0] + f_fusion[2] * 0.85, f_fusion[1] + f_fusion[3] * 0.15),
        (s_visit[0], s_visit[1] + s_visit[3] * 0.4),
        "预写\n就诊",
        rad=0.12,
        z=2,
    )
    # Session
    arrow(
        ax,
        (c_start[0] + c_start[2] * 0.5, c_start[1]),
        (c_sess[0] + c_sess[2] * 0.5, c_sess[1] + c_sess[3]),
        "",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (c_sess[0] + c_sess[2], c_sess[1] + c_sess[3] * 0.65),
        (c_voice[0], c_voice[1] + c_voice[3] * 0.35),
        "启动",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (c_sess[0] + c_sess[2], c_sess[1] + c_sess[3] * 0.35),
        (c_env[0], c_env[1] + c_env[3] * 0.4),
        "启动",
        rad=0.0,
        z=2,
    )
    arrow(
        ax,
        (c_voice[0] + c_voice[2] * 0.2, c_voice[1] + c_voice[3] * 0.5),
        (s_visit[0] + s_visit[2] * 0.2, s_visit[1] + s_visit[3] * 0.5),
        "写入",
        rad=0.4,
        z=2,
    )
    # Consultation -> records (entire process)
    ax.annotate(
        "",
        xy=(s_visit[0] + s_visit[2] * 0.5, s_visit[1] + s_visit[3] * 0.9),
        xytext=(c_sess[0] + c_sess[2] * 0.2, c_sess[1] + 0.002),
        textcoords="data",
        arrowprops=dict(
            arrowstyle="-|>", color=ARROW, linewidth=0.9, connectionstyle="arc3,rad=0.3", linestyle="--", alpha=0.75
        ),
        zorder=2,
    )
    ax.text(0.59, 0.31, "诊疗落库", fontsize=6.5, color="#7d8590", ha="center", zorder=5)

    leg = "说明：自上而下为硬件 → AI 视觉 → 存储 → 数据服务 → 会诊；实线主数据/控制，虚线汇总落库关系。"
    ax.text(0.5, 0.006, leg, ha="center", va="bottom", fontsize=7.5, color="#6e7681", zorder=20)

    out_dir = "/workspace/diagrams"
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, "alphaherb_phase0_swimlane.png")
    out_svg = os.path.join(out_dir, "alphaherb_phase0_swimlane.svg")
    fig.savefig(out_png, dpi=220, bbox_inches="tight", facecolor=BG, edgecolor="none", pad_inches=0.28)
    fig.savefig(out_svg, format="svg", bbox_inches="tight", facecolor=BG, edgecolor="none", pad_inches=0.28)
    plt.close()
    print("Wrote", out_png)
    print("Wrote", out_svg, "(Visio: 插入 → 可导入此 SVG 为可编辑形状)")


if __name__ == "__main__":
    main()
