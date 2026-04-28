#!/usr/bin/env python3
"""
Generate AlphaHerb Phase 0 cross-functional swimlane flowchart as PNG.
Visio-style: vertical swimlanes (columns = roles), flow primarily top-to-bottom;
standard process rectangles, database cylinders, labeled connectors.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

# Chinese font (WenQuanYi Micro Hei)
_FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
font_manager.fontManager.addfont(_FONT)
plt.rcParams["font.family"] = ["WenQuanYi Micro Hei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

COL_HW = "#FFE8CC"
COL_AI = "#E8D4F0"
COL_ROUTE = "#D4F0E8"
COL_HERB = "#D4E8F8"
COL_TERM = "#FFF4E0"
COL_CLINIC = "#FFE0D4"


def rounded_rect(ax, x, y, w, h, facecolor, edgecolor="#333333", lw=1.2, radius=0.06):
    box = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.015,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=2,
    )
    ax.add_patch(box)
    return box


def cylinder(ax, cx, cy, w, h, facecolor, edgecolor="#333333"):
    hw = w / 2
    eh = min(h * 0.12, 0.28)
    body = mpatches.Rectangle(
        (cx - hw, cy - h / 2 + eh), w, h - 2 * eh, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.1, zorder=2
    )
    ax.add_patch(body)
    ell_top = mpatches.Ellipse((cx, cy + h / 2 - eh), w, eh * 2, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.1, zorder=2)
    ell_bot = mpatches.Ellipse((cx, cy - h / 2 + eh), w, eh * 2, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.1, zorder=2)
    ax.add_patch(ell_top)
    ax.add_patch(ell_bot)
    ax.plot([cx - hw, cx + hw], [cy + h / 2 - eh, cy + h / 2 - eh], color=edgecolor, linewidth=1.1, zorder=2)


def arrow(ax, x1, y1, x2, y2, text=None, color="#444444", lw=1.4):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=3, shrinkB=3, connectionstyle="arc3,rad=0"),
        zorder=3,
    )
    if text:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.08, my + 0.12, text, ha="center", va="bottom", fontsize=7.5, color="#222", zorder=4)


def vertical_lane(ax, x0, x1, y0, y1, color, title):
    rect = mpatches.Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=color, edgecolor="#888888", linewidth=1.4, zorder=0)
    ax.add_patch(rect)
    xc = (x0 + x1) / 2
    ax.text(xc, y1 - 0.35, title, ha="center", va="top", fontsize=10.5, fontweight="bold", color="#222", zorder=1)


def main():
    fig, ax = plt.subplots(figsize=(26, 15), dpi=150)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 14.5)
    ax.axis("off")
    ax.set_aspect("auto")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    y0, y1 = 0.35, 13.35
    # Left → right: 硬件 | AI | HerbMars | 终端 | 诊疗管理
    lanes = [
        (0.25, 3.85, COL_HW, "硬件层"),
        (3.85, 9.05, COL_AI, "AlphaHerb AI\n视觉引擎 / 数据路由"),
        (9.05, 13.55, COL_HERB, "HerbMars\n后端与数据"),
        (13.55, 17.45, COL_TERM, "终端\n店员 / 医师"),
        (17.45, 21.75, COL_CLINIC, "诊疗管理"),
    ]
    for x0, x1, col, title in lanes:
        vertical_lane(ax, x0, x1, y0, y1, col, title)

    # --- Column centers for placement ---
    xc_hw = 2.05
    xc_ai = 6.45
    xc_herb = 11.3
    xc_term = 15.5
    xc_clinic = 19.6

    # ========== 硬件 ==========
    rounded_rect(ax, xc_hw - 1.35, 1.05, 1.25, 0.55, "#FFFFFF")
    ax.text(xc_hw - 0.73, 1.33, "门口摄像头", ha="center", va="center", fontsize=8.5, zorder=3)
    rounded_rect(ax, xc_hw + 0.15, 1.05, 1.25, 0.55, "#FFFFFF")
    ax.text(xc_hw + 0.78, 1.33, "店内摄像头\n(多角度)", ha="center", va="center", fontsize=8, zorder=3)
    arrow(ax, xc_hw - 0.1, 1.33, xc_hw + 0.12, 1.33)
    ax.text(xc_hw, 0.92, "视频流", ha="center", fontsize=7, color="#555")

    # ========== AI 列：自下而上 输入 → CV → 路由 ==========
    rounded_rect(ax, 4.05, 2.05, 4.35, 2.85, "#FFFFFF")
    ax.text(6.23, 4.85, "计算机视觉引擎", ha="center", fontsize=10, fontweight="bold", zorder=3)
    ax.text(4.25, 4.45, "人体检测 · 人脸 Embedding · 向量512", fontsize=7.5, zorder=3)
    ax.text(4.25, 4.05, "行为：路径 + 热区 → 进店/停留", fontsize=7.5, zorder=3)
    ax.text(4.25, 3.65, "步态：V-Pose → 步频/步幅/姿态", fontsize=7.5, zorder=3)

    rounded_rect(ax, 4.05, 5.15, 4.35, 2.05, COL_ROUTE, lw=1.3)
    ax.text(6.23, 6.85, "数据路由层", ha="center", fontsize=10, fontweight="bold", zorder=3)
    ax.text(4.25, 6.45, "行为画像生成引擎", fontsize=9, zorder=3)
    ax.text(4.25, 6.05, "行为画像切片 JSON", fontsize=8, zorder=3)
    ax.text(4.25, 5.65, "到店通知 / 行为录像 WebSocket", fontsize=8, zorder=3)
    ax.text(4.25, 5.28, "签到·卸载 REST · 多源融合入口", fontsize=7.5, zorder=3)

    arrow(ax, 6.23, 4.95, 6.23, 5.12)
    ax.text(6.65, 5.03, "特征/轨迹", fontsize=7, color="#555")

    # 硬件 → AI：视频流上行
    arrow(ax, xc_hw, 1.65, 4.05, 2.4, "输入")

    # ========== HerbMars：数据库排布 ==========
    cy_db = 7.35
    cylinder(ax, 9.65, cy_db, 1.55, 0.95, "#FFFFFF")
    ax.text(9.65, cy_db, "人脸\n特征库", ha="center", va="center", fontsize=7.5, zorder=3)
    cylinder(ax, 11.35, cy_db, 1.55, 0.95, "#FFFFFF")
    ax.text(11.35, cy_db, "行为\n数据库", ha="center", va="center", fontsize=7.5, zorder=3)
    cylinder(ax, 9.65, 8.95, 1.55, 0.95, "#FFFFFF")
    ax.text(9.65, 8.95, "患者\n档案库", ha="center", va="center", fontsize=7.5, zorder=3)
    cylinder(ax, 11.35, 8.95, 1.55, 0.95, "#FFFFFF")
    ax.text(11.35, 8.95, "就诊\n记录库", ha="center", va="center", fontsize=7.5, zorder=3)

    # AI 路由 → 行为库 / 档案
    arrow(ax, 8.45, 6.2, 9.55, 7.25, "JSON")
    arrow(ax, 8.45, 5.9, 10.9, 8.45, "读写")

    # 特征比对：CV → 人脸库 & 人脸库 → 画像引擎
    ax.annotate(
        "",
        xy=(9.55, 7.55),
        xytext=(5.5, 3.8),
        arrowprops=dict(arrowstyle="-|>", color="#666666", lw=1.2, connectionstyle="arc3,rad=0.12"),
        zorder=3,
    )
    ax.text(7.2, 5.45, "特征比对", fontsize=7, color="#555")
    ax.annotate(
        "",
        xy=(5.6, 6.0),
        xytext=(9.55, 7.85),
        arrowprops=dict(arrowstyle="-|>", color="#0066AA", lw=1.35, connectionstyle="arc3,rad=-0.12"),
        zorder=3,
    )
    ax.text(7.0, 7.15, "匹配结果\n患者ID/未选", fontsize=7, color="#0066AA", ha="center")

    arrow(ax, 8.45, 5.5, 9.4, 7.55)

    # ========== 终端 ==========
    rounded_rect(ax, 13.85, 6.2, 1.55, 1.05, "#FFFFFF")
    ax.text(14.63, 6.73, "店员终端\n(PC/平台)", ha="center", va="center", fontsize=8.5, zorder=3)
    rounded_rect(ax, 15.65, 6.2, 1.55, 1.05, "#FFFFFF")
    ax.text(16.43, 6.73, "中医师设备\n(手机/平台)", ha="center", va="center", fontsize=8.5, zorder=3)

    rounded_rect(ax, 13.75, 8.15, 3.45, 0.65, "#FFFFFF")
    ax.text(15.48, 8.48, "搜索请求/结果  姓名·手机 → 档案列表", ha="center", va="center", fontsize=8, zorder=3)

    # 路由 → 终端 WebSocket
    arrow(ax, 8.45, 6.55, 13.85, 6.85, "WS")
    ax.text(11.0, 6.45, "到店通知·行为录像", fontsize=7, color="#555")

    # 终端 → 库
    arrow(ax, 14.63, 6.75, 10.0, 7.35, "查行为库")
    arrow(ax, 16.43, 6.75, 11.35, 8.45, "档案")
    arrow(ax, 15.48, 8.15, 11.0, 8.95, "查询")

    # ========== 诊疗管理 ==========
    rounded_rect(ax, 17.85, 9.85, 3.55, 1.35, "#FFFFFF")
    ax.text(19.63, 10.78, "开始诊疗 (REST)", ha="center", fontsize=9, zorder=3)
    ax.text(19.63, 10.38, "诊疗会话控制", ha="center", fontsize=9, fontweight="bold", zorder=3)
    ax.text(19.63, 9.98, "会话元数据 · 语音 · 环境感知", ha="center", fontsize=7.5, zorder=3)

    rounded_rect(ax, 18.05, 7.85, 3.15, 1.05, COL_ROUTE, lw=1.2)
    ax.text(19.63, 8.55, "多源数据融合处理", ha="center", fontsize=9, fontweight="bold", zorder=3)
    ax.text(19.63, 8.15, "(路由层)", ha="center", fontsize=8, zorder=3)

    arrow(ax, 19.63, 9.82, 19.63, 8.93)
    ax.text(20.15, 9.35, "诊疗数据", fontsize=7, color="#555")

    # 诊疗融合 → 路由层（进入 AI 列，避免横跨整图）
    arrow(ax, 18.05, 8.35, 8.45, 5.65, "融合输出")
    arrow(ax, 21.45, 8.35, 11.35, 9.05, "更新档案")
    ax.annotate(
        "",
        xy=(11.35, 9.05),
        xytext=(21.15, 10.35),
        arrowprops=dict(arrowstyle="-|>", color="#444444", lw=1.25, connectionstyle="arc3,rad=-0.08"),
        zorder=3,
    )
    ax.text(16.5, 9.85, "会话归档 → 就诊记录", fontsize=7, color="#555", ha="center")

    # Title
    ax.text(11.0, 14.05, "AlphaHerb Phase 0 — 系统流程及数据流转（纵向职能带）", ha="center", fontsize=14, fontweight="bold")
    ax.text(11.0, 13.62, "Vertical swimlanes: columns = organizational roles", ha="center", fontsize=10, style="italic", color="#555")

    # Legend
    ax.text(18.8, 1.05, "图例", fontsize=9, fontweight="bold")
    rounded_rect(ax, 18.6, 0.55, 0.42, 0.2, "#FFFFFF", lw=1)
    ax.text(19.2, 0.65, "流程", fontsize=7, va="center")
    cylinder(ax, 20.0, 0.65, 0.45, 0.18, "#FFFFFF")
    ax.text(20.55, 0.65, "数据库", fontsize=7, va="center")

    plt.tight_layout()
    out = Path(__file__).resolve().parent.parent / "docs" / "alphaherb_phase0_swimlane.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white", edgecolor="none", dpi=200)
    print(f"Written: {out}")
    plt.close()


if __name__ == "__main__":
    main()
