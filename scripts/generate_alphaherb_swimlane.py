#!/usr/bin/env python3
"""
Generate AlphaHerb Phase 0 cross-functional (swimlane) flowchart as PNG.
Visio-style: horizontal swimlanes, standard process/database shapes, labeled connectors.
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

# Swimlane colors (light fills, dark borders)
COL_HW = "#FFE8CC"
COL_AI = "#E8D4F0"
COL_ROUTE = "#D4F0E8"
COL_HERB = "#D4E8F8"
COL_TERM = "#FFF4E0"
COL_CLINIC = "#FFE0D4"


def rounded_rect(ax, x, y, w, h, facecolor, edgecolor="#333333", lw=1.2, radius=0.08):
    box = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
    )
    ax.add_patch(box)
    return box


def cylinder(ax, cx, cy, w, h, facecolor, edgecolor="#333333"):
    """Simple DB cylinder: ellipse top + body + ellipse bottom hint."""
    hw = w / 2
    eh = min(h * 0.12, 0.35)
    body = mpatches.Rectangle((cx - hw, cy - h / 2 + eh), w, h - 2 * eh, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.2)
    ax.add_patch(body)
    ell_top = mpatches.Ellipse((cx, cy + h / 2 - eh), w, eh * 2, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.2)
    ell_bot = mpatches.Ellipse((cx, cy - h / 2 + eh), w, eh * 2, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.2)
    ax.add_patch(ell_top)
    ax.add_patch(ell_bot)
    line_top = plt.Line2D([cx - hw, cx + hw], [cy + h / 2 - eh, cy + h / 2 - eh], color=edgecolor, linewidth=1.2)
    ax.add_line(line_top)


def arrow(ax, x1, y1, x2, y2, text=None, color="#444444", lw=1.5):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=2, shrinkB=2, connectionstyle="arc3,rad=0"),
    )
    if text:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.15, text, ha="center", va="bottom", fontsize=8, color="#222")


def swimlane_background(ax, y0, y1, color, title):
    rect = mpatches.Rectangle((0, y0), 18, y1 - y0, facecolor=color, edgecolor="#888888", linewidth=1.5, zorder=0)
    ax.add_patch(rect)
    ax.text(0.35, (y0 + y1) / 2, title, ha="left", va="center", fontsize=11, fontweight="bold", color="#222", rotation=90)


def main():
    fig, ax = plt.subplots(figsize=(22, 16), dpi=150)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 16)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Lane vertical bands (y: bottom to top in matplotlib — use high y at top)
    # Define from bottom: y=0 is bottom of figure content area
    lanes = [
        (0.2, 2.2, COL_HW, "硬件层"),
        (2.2, 7.0, COL_AI, "AlphaHerb AI\n计算机视觉 / 数据路由"),
        (7.0, 10.2, COL_HERB, "HerbMars\n后端与数据"),
        (10.2, 12.5, COL_TERM, "终端\n店员 / 医师"),
        (12.5, 15.5, COL_CLINIC, "诊疗管理"),
    ]
    for y0, y1, col, title in lanes:
        swimlane_background(ax, y0, y1, col, title)

    # --- Hardware (y ~ 1.2-2.0) ---
    rounded_rect(ax, 2.0, 1.35, 2.2, 0.65, "#FFFFFF", lw=1.2)
    ax.text(3.1, 1.68, "门口摄像头", ha="center", va="center", fontsize=9)
    rounded_rect(ax, 5.0, 1.35, 2.4, 0.65, "#FFFFFF", lw=1.2)
    ax.text(6.2, 1.68, "店内摄像头(多角度)", ha="center", va="center", fontsize=9)
    arrow(ax, 4.25, 1.68, 4.95, 1.68)
    ax.text(4.6, 1.95, "视频流", ha="center", fontsize=7, color="#555")
    arrow(ax, 6.2, 2.05, 6.2, 2.55, "输入")

    # --- CV + Routing (merged lane 2.2-7) ---
    # CV box left
    rounded_rect(ax, 2.0, 3.0, 5.5, 3.6, "#FFFFFF", lw=1.2)
    ax.text(4.75, 6.15, "计算机视觉引擎", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(2.3, 5.75, "人体检测", fontsize=8)
    ax.text(2.3, 5.35, "↓ 人脸区域 → Face Embedding → 特征向量 512", fontsize=7.5)
    ax.text(2.3, 4.9, "↓ 行为：路径追踪 + 热区 → 进店/停留", fontsize=7.5)
    ax.text(2.3, 4.45, "↓ 步态：V-Pose → 步频/步幅/姿态", fontsize=7.5)

    # Routing / persona engine right
    rounded_rect(ax, 8.2, 3.3, 4.8, 3.0, COL_ROUTE, lw=1.4)
    ax.text(10.6, 5.85, "数据路由层", ha="center", fontsize=10, fontweight="bold")
    ax.text(8.45, 5.35, "行为画像生成引擎", fontsize=9)
    ax.text(8.45, 4.85, "→ 行为画像切片 JSON", fontsize=8)
    ax.text(8.45, 4.45, "→ 到店感知通知 WebSocket", fontsize=8)
    ax.text(8.45, 4.05, "→ 行为录像切片 WebSocket", fontsize=8)
    ax.text(8.45, 3.65, "签到/卸载 REST · 多源融合", fontsize=8)

    arrow(ax, 7.55, 4.8, 8.15, 4.8)
    ax.text(7.85, 5.05, "向量/轨迹/特征", fontsize=7, ha="center")

    # --- HerbMars ---
    cylinder(ax, 4.0, 8.6, 2.4, 1.1, "#FFFFFF")
    ax.text(4.0, 8.6, "人脸特征库", ha="center", va="center", fontsize=8)
    cylinder(ax, 7.5, 8.6, 2.4, 1.1, "#FFFFFF")
    ax.text(7.5, 8.6, "行为数据库", ha="center", va="center", fontsize=8)
    cylinder(ax, 11.0, 8.6, 2.4, 1.1, "#FFFFFF")
    ax.text(11.0, 8.6, "患者档案库", ha="center", va="center", fontsize=8)
    cylinder(ax, 14.5, 8.6, 2.4, 1.1, "#FFFFFF")
    ax.text(14.5, 8.6, "就诊记录库", ha="center", va="center", fontsize=8)

    # Persona -> 行为库 (画像 JSON)
    arrow(ax, 9.5, 6.35, 7.5, 8.05, "JSON")
    ax.text(8.2, 7.15, "画像写入", fontsize=7, color="#555")

    # Persona -> 患者档案 (画像/档案联动)
    arrow(ax, 11.5, 5.8, 11.0, 8.05, "读写")

    # 人脸特征库 -> 行为画像引擎 (匹配结果回灌)
    ax.annotate(
        "",
        xy=(5.2, 5.9),
        xytext=(4.0, 8.05),
        arrowprops=dict(arrowstyle="-|>", color="#0066AA", lw=1.4, connectionstyle="arc3,rad=0.2"),
    )
    ax.text(4.35, 7.15, "匹配结果\n患者ID/未选", fontsize=7, color="#0066AA", ha="center")

    # 特征向量上传比对 -> 人脸库 (查询)
    ax.annotate(
        "",
        xy=(4.0, 8.05),
        xytext=(4.75, 5.75),
        arrowprops=dict(arrowstyle="-|>", color="#666666", lw=1.2, connectionstyle="arc3,rad=-0.15"),
    )
    ax.text(5.5, 6.75, "特征比对", fontsize=7, color="#555", ha="center")

    # 行为库 <-> 路由融合旁路
    arrow(ax, 8.1, 5.75, 7.9, 8.05)

    # Search flows terminal <-> herb
    rounded_rect(ax, 11.5, 11.0, 3.2, 0.55, "#FFFFFF", lw=1.2)
    ax.text(13.1, 11.28, "搜索请求 / 结果\n姓名·手机 → 档案列表", ha="center", va="center", fontsize=8)

    arrow(ax, 13.1, 10.15, 13.1, 9.15, "查询")

    # Terminals
    rounded_rect(ax, 2.5, 10.8, 2.8, 0.9, "#FFFFFF", lw=1.2)
    ax.text(3.9, 11.25, "店员终端\n(PC/平台)", ha="center", va="center", fontsize=9)
    rounded_rect(ax, 6.0, 10.8, 2.8, 0.9, "#FFFFFF", lw=1.2)
    ax.text(7.4, 11.25, "中医师手持设备\n(手机/平台)", ha="center", va="center", fontsize=9)

    arrow(ax, 10.5, 5.2, 7.4, 11.2, "WS 推送")
    ax.text(9.2, 8.2, "到店通知\n行为录像", fontsize=7, color="#555")

    arrow(ax, 3.9, 10.75, 6.8, 9.15, "查行为库")
    arrow(ax, 7.4, 10.75, 9.5, 9.15)

    # --- Consultation ---
    rounded_rect(ax, 2.0, 13.0, 4.5, 1.8, "#FFFFFF", lw=1.2)
    ax.text(4.25, 14.35, "开始诊疗 (REST)", fontsize=9)
    ax.text(4.25, 13.95, "↓", fontsize=10)
    ax.text(4.25, 13.6, "诊疗会话控制", fontsize=9, fontweight="bold")
    ax.text(4.25, 13.15, "会话元数据 · 实时语音 · 环境感知", fontsize=8)

    rounded_rect(ax, 7.5, 13.2, 3.2, 1.4, COL_ROUTE, lw=1.2)
    ax.text(9.1, 14.0, "多源数据融合处理", ha="center", fontsize=9, fontweight="bold")
    ax.text(9.1, 13.45, "(路由层)", ha="center", fontsize=8)

    arrow(ax, 6.55, 13.9, 7.45, 13.9)
    # 诊疗会话 -> 融合 -> 路由层下游
    arrow(ax, 4.25, 13.0, 9.1, 14.55, "诊疗数据")
    arrow(ax, 9.1, 13.15, 10.8, 7.25, "融合输出")
    arrow(ax, 10.8, 7.25, 11.0, 8.05, "更新档案")
    arrow(ax, 12.5, 13.15, 14.5, 9.15, "会话归档 → 就诊记录")

    # Title
    ax.text(9.0, 15.75, "AlphaHerb Phase 0 — 系统流程及数据流转（跨职能泳道图）", ha="center", fontsize=14, fontweight="bold")
    ax.text(9.0, 15.35, "Cross-functional swimlane flowchart", ha="center", fontsize=10, style="italic", color="#555")

    # Legend
    leg_y = 0.05
    ax.text(14.5, leg_y + 0.35, "图例", fontsize=9, fontweight="bold")
    rounded_rect(ax, 14.2, leg_y, 0.45, 0.22, "#FFFFFF", lw=1)
    ax.text(14.85, leg_y + 0.11, "处理", fontsize=7, va="center")
    cylinder(ax, 15.6, leg_y + 0.11, 0.5, 0.2, "#FFFFFF")
    ax.text(16.25, leg_y + 0.11, "数据库", fontsize=7, va="center")

    plt.tight_layout()
    out = Path(__file__).resolve().parent.parent / "docs" / "alphaherb_phase0_swimlane.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white", edgecolor="none", dpi=200)
    print(f"Written: {out}")
    plt.close()


if __name__ == "__main__":
    main()
