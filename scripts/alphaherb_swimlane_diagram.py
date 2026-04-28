#!/usr/bin/env python3
"""
Visio-style cross-functional (swimlane) flowchart — AlphaHerb Phase 0.
Renders a high-DPI PNG for use in documentation or Visio as reference.
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

mpl.rcParams["font.family"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "sans-serif"]
mpl.rcParams["axes.unicode_minus"] = False


def box(
    ax,
    xy,
    w,
    h,
    text,
    facecolor,
    edgecolor="#404040",
    fs=7,
    ewidth=0.7,
    tc="#111",
):
    x, y = xy
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.25", linewidth=ewidth, edgecolor=edgecolor, facecolor=facecolor, zorder=2
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3)
    return p


def seg_arrow(
    ax,
    x0,
    y0,
    x1,
    y1,
    label=None,
    l_off=(0, 0),
    color="#1e3a5f",
    rad=0,
    end_arrow=True,
):
    style = f"arc3,rad={rad}" if rad else "arc3,rad=0"
    astyle = "Simple,tail_width=0.15,head_width=4.5,head_length=5" if end_arrow else "-"
    arr = FancyArrowPatch(
        (x0, y0),
        (x1, y1),
        arrowstyle=astyle,
        color=color,
        linewidth=0.85,
        zorder=1.5,
        connectionstyle=style,
    )
    ax.add_patch(arr)
    if label:
        mid = ((x0 + x1) / 2 + l_off[0], (y0 + y1) / 2 + l_off[1])
        ax.text(
            mid[0], mid[1], label, ha="center", va="center", fontsize=6, color="#0d1f33", zorder=4,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#ccc", alpha=0.95),
        )


def arrow_elbow(
    ax,
    x0,
    y0,
    x1,
    y1,
    x2,
    y2,
    label=None,
    l_off=(0, 0),
    color="#1e3a5f",
    label_on=(1, 2),
    l_off2=None,
):
    """(x0,y0)->(x1,y1)->(x2,y2); no arrow on first segment, arrow on last."""
    l2 = l_off2 if l_off2 is not None else l_off
    if label_on == (0, 1):
        seg_arrow(ax, x0, y0, x1, y1, label=label, l_off=l_off, color=color, end_arrow=False)
        seg_arrow(ax, x1, y1, x2, y2, color=color, end_arrow=True)
    elif label_on == (1, 2):
        seg_arrow(ax, x0, y0, x1, y1, l_off=(0, 0), color=color, end_arrow=False)
        seg_arrow(ax, x1, y1, x2, y2, label=label, l_off=l2, color=color, end_arrow=True)
    else:
        seg_arrow(ax, x0, y0, x1, y1, l_off=(0, 0), color=color, end_arrow=False)
        seg_arrow(ax, x1, y1, x2, y2, l_off=(0, 0), color=color, end_arrow=True)


def swimlane_h(ax, y, h, w, x0, title, bg, text_color="#0d47a1", title_fs=8.2):
    """Horizontal swimlane band."""
    ax.add_patch(mpatches.Rectangle((x0, y), w, h, facecolor=bg, edgecolor="#6b6b6b", linewidth=0.55, zorder=0))
    ax.text(x0 + 0.35, y + h * 0.5, title, ha="left", va="center", rotation=90, fontsize=title_fs, fontweight="600", color=text_color)


def main():
    out_dir = Path(__file__).resolve().parent.parent / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "AlphaHerb_Phase0_Swimlane_Flowchart.png"

    # Canvas
    W, H = 100, 100
    fig, ax = plt.subplots(figsize=(16, 22), dpi=160, facecolor="white")
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")

    x0, lane_w = 2.0, 96.0
    left = x0 + 5.5  # after vertical title strip in main bands

    # ---- Colors
    c_cloud = "#9EC9EF"
    c_hw = "#F0D4B0"
    c_aiframe = "#E0D0EC"
    c_cv_inner = "#4F4F4F"
    c_cv_sub = "#6E6E6E"
    c_light_txt = "#F8F8F8"
    c_fusion = "#A8D9A0"
    c_session = "#FFD9A3"
    c_user = "#B0D0F0"

    # === Title
    ax.text(50, H - 0.3, "AlphaHerb Phase 0 — 系统流程及数据流转图（Visio 风格 / 跨职能泳道）", ha="center", va="top", fontsize=10.5, fontweight="600", color="#111")

    # === Lane 1: Cloud (y 81–98)
    y1, h1 = 81, 16.5
    swimlane_h(ax, y1, h1, lane_w, x0, "AlphaHerb 云", "#C8E0F8", "#0d47a1")
    ax.text(left, y1 + h1 - 1, "长周期：特征匹配、档案与行为持久化", ha="left", va="top", fontsize=6.8, color="#0d3d82", style="italic")
    # Top search strip
    ax.text(left, y1 + h1 - 2.8, "搜索请求(姓名/手机号)", fontsize=6, color="#1565c0")
    seg_arrow(ax, left + 11, y1 + h1 - 2.1, left + 22, y1 + h1 - 2.1)
    ax.text(left + 25, y1 + h1 - 2.8, "→ 患者队列", fontsize=6, color="#1565c0")
    seg_arrow(ax, left + 32, y1 + h1 - 2.1, left + 40, y1 + h1 - 2.1, label=None)
    box(ax, (left, y1 + h1 - 4.2), 10, 2.2, "患者档案库", "#7EB8E8", fs=6.5)
    box(ax, (left + 12, y1 + h1 - 4.2), 10, 2.2, "就诊记录库", "#7EB8E8", fs=6.5)
    # Main cloud row: face lib | match | behavior db
    bx, by = left, y1 + 1.2
    box(ax, (bx, by + 3.5), 9.2, 3, "人脸特征库", c_cloud, edgecolor="#1565c0", fs=6.5)
    box(ax, (bx + 10.2, by + 3.5), 9.2, 3, "匹配结果\n患者ID/未匹配", "#7EB0E0", edgecolor="#1565c0", fs=5.8)
    box(ax, (bx, by), 9.2, 2.8, "行为数据库", c_cloud, edgecolor="#1565c0", fs=6.5)
    # Match links face lib to match
    seg_arrow(ax, bx + 9.2, by + 4.3, bx + 10.2, by + 4.3, label="检索", l_off=(0, 0.4))

    # === Lane 2: Hardware (y 64–80)
    y2, h2 = 64, 16
    swimlane_h(ax, y2, h2, lane_w, x0, "硬件端", c_hw, "#5d3d1a")
    box(ax, (left, y2 + 9.5), 7.2, 3, "门口摄像头", "#E0A86A", edgecolor="#a36a2a", fs=6.5)
    box(ax, (left, y2 + 4.2), 7.2, 3.2, "店内摄像头\n(多角度)", "#E0A86A", edgecolor="#a36a2a", fs=6.2)

    # === Large AI frame (dashed) — y 8–63, covers CV + fusion + part of session
    ai_x, ai_w = left, 80
    frame = mpatches.FancyBboxPatch(
        (ai_x, 6), ai_w, 58, boxstyle="round,pad=0,rounding_size=0.2", facecolor="#EEE5F0", edgecolor="#6A1B9A", linewidth=1.0, linestyle=(0, (4, 3)), zorder=0
    )
    ax.add_patch(frame)
    ax.text(ai_x + 0.3, 63, "AlphaHerb AI Core", ha="left", va="top", fontsize=8.4, fontweight="700", color="#4A148C")

    # CV engine region (y ~ 47–60)
    cv_y, cv_h = 45.5, 12.0
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (ai_x + 0.3, cv_y - 0.2), 42, cv_h + 0.4, boxstyle="round,pad=0,rounding_size=0.15", facecolor="#2a2a2a", edgecolor="#111", linewidth=0.6, zorder=0.5, alpha=0.92
        )
    )
    ax.text(ai_x + 0.4, cv_y + cv_h + 0.1, "计算机视觉引擎", ha="left", va="bottom", fontsize=7, fontweight="600", color=c_light_txt, zorder=1)

    det_w, det_h = 30, 2.6
    d_x, d_y = ai_x + 1, cv_y + cv_h - 2.8
    box(ax, (d_x, d_y), det_w, det_h, "人体检测模块 (视频输入融合)", c_cv_inner, edgecolor="#888", fs=6.2, tc=c_light_txt)
    # Sub boxes
    f_x, f_y = ai_x + 0.6, cv_y
    box(ax, (f_x, f_y), 9, 3.5, "人脸特征提取\nFace Embedding", c_cv_sub, edgecolor="#999", fs=5.2, tc=c_light_txt)
    b_x = f_x + 10
    box(ax, (b_x, f_y), 10.2, 3.5, "行为分析 路径+热区", c_cv_sub, edgecolor="#999", fs=5, tc=c_light_txt)
    g_x = b_x + 10.5
    box(ax, (g_x, f_y), 4.2, 3.5, "步态", c_cv_sub, edgecolor="#999", fs=5, tc=c_light_txt)

    # HD to subs
    seg_arrow(ax, d_x + 9, d_y, f_x + 4.5, f_y + 3.5, label="人脸区域", l_off=(-0.2, 0.35), rad=0, color="#a8d0ff")
    seg_arrow(ax, d_x + 15, d_y, b_x + 5, f_y + 3.5, color="#a8d0ff")
    seg_arrow(ax, d_x + 22, d_y, g_x + 1.5, f_y + 3.5, label="人体", l_off=(0, 0.3), color="#a8d0ff")

    # Cameras to CV
    seg_arrow(ax, left + 3.6, y2 + 11, ai_x + 1.5, d_y + 1, label="视频流", l_off=(-0.3, 0.5), color="#2e7d32", rad=0.08)
    seg_arrow(ax, left + 3.6, y2 + 5, ai_x + 7, d_y, label="视频流", l_off=(-0.1, 0.3), color="#2e7d32", rad=0.05)

    # Fusion area (x ~ 56–72, y 47–60)
    fus_x, fus_y, fus_w, fus_h = 55.0, 47.0, 18.0, 10.0
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (fus_x, fus_y), fus_w, fus_h, boxstyle="round,pad=0,rounding_size=0.1", facecolor="#c0e0b5", edgecolor="#2E7B2E", linewidth=0.9, zorder=0.2, alpha=0.5
        )
    )
    ax.text(fus_x + fus_w / 2, fus_y + fus_h, "数据融合层", ha="center", va="bottom", fontsize=7, fontweight="600", color="#1b4d1b")
    box(
        ax,
        (fus_x + 0.4, fus_y + 0.3),
        fus_w - 0.8,
        3.2,
        "行为画像\n生成引擎",
        c_fusion,
        edgecolor="#2E7B2E",
        fs=6.3,
    )

    # 512 to cloud (orthogonal to reduce overlap)
    y_mid_face = y1 + 1.0
    arrow_elbow(
        ax,
        f_x + 1.2, f_y + 3.5, f_x + 1.2, y_mid_face, bx + 0.2, y_mid_face,
        label="512 维特征向量", l_off=(0.2, 0.25), l_off2=(0.1, 0.25), color="#1565c0", label_on=(1, 2),
    )

    # Match back to fusion
    seg_arrow(
        ax, bx + 10.2 + 9.2 * 0.5, y1 + 3.0, fus_x + 7, fus_y + 3.0,
        label="回传", l_off=(-0.2, 0.6), color="#1565c0", rad=0.18,
    )

    # Trajectory + multimodal to fusion
    seg_arrow(
        ax, b_x + 4, f_y, fus_x, fus_y + 2, label="行为轨迹(路径/停留)", l_off=(0, 0.2), color="#1b4d1b", rad=0.05,
    )
    seg_arrow(
        ax, g_x + 2, f_y, fus_x + 8, fus_y + 1, label="步态/姿态/步幅", l_off=(0.1, 0.3), color="#1b4d1b", rad=0.08,
    )

    # Fusion -> behavior JSON to cloud
    y_json = by + 0.8
    arrow_elbow(
        ax,
        fus_x + 0.25, fus_y, fus_x + 0.25, y_json, bx + 0.5, y_json,
        label="行为画像切片 JSON", l_off=(-0.1, 0.35), l_off2=(-0.1, 0.35), color="#0d3d0d", label_on=(1, 2),
    )

    # User terminals
    u_x, u_y = 75.0, 47.0
    box(ax, (u_x, u_y + 5.5), 6.2, 3.2, "店员终端\nPC/平板", c_user, edgecolor="#0d47a1", fs=5.2)
    box(ax, (u_x + 7, u_y + 5.5), 6.8, 3.2, "中医师\n手持", c_user, edgecolor="#0d47a1", fs=5.0)
    ax.text(u_x + 7, u_y + 4.2, "用户终端", ha="center", va="top", fontsize=6.4, color="#0d47a1", fontweight="600")
    box(ax, (u_x, u_y), 14, 3.0, "多源数据 融合处理\n(REST 查询/提交)", "#9ec5ec", edgecolor="#1565c0", fs=5.2)

    # WebSocket to terminals
    seg_arrow(ax, fus_x + 14, fus_y + 1.0, u_x, u_y + 1.0, label="WebSocket: 到诊/画像切片", l_off=(0, 0.8), color="#0d4f8a", rad=0.0)

    # Multi-source to cloud
    seg_arrow(
        ax, u_x + 1.0, u_y + 0.0, left + 1, y1 + 0.0,
        label="更新档案",
        l_off=(-0.1, 0.7), color="#0d47a1", rad=-0.2,
    )
    seg_arrow(
        ax, u_x + 12, u_y + 0.0, left + 20, y1 - 0.0,
        label="写入就诊记录", l_off=(-0.0, 0.7), color="#0d47a1", rad=0.15,
    )
    # REST from terminals to fusion
    seg_arrow(
        ax, u_x + 7, u_y + 3, fus_x + 4, fus_y, label="REST 查询/关联", l_off=(-0.1, 0.5), color="#0d3d0d", rad=0.02,
    )

    # === Session (bottom left of frame)
    sess_x, sess_y, sess_w, sess_h = ai_x + 0.3, 9.0, 35, 14.0
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (sess_x, sess_y), sess_w, sess_h, boxstyle="round,pad=0,rounding_size=0.1", facecolor="#FFF3E0", edgecolor="#E65100", linewidth=1, zorder=0.1
        )
    )
    ax.text(sess_x + sess_w / 2, sess_y + sess_h, "会话管理控制", ha="center", va="bottom", fontsize=6.8, color="#E65100", fontweight="600")
    box(ax, (sess_x + 0.4, sess_y + 0.3), 6, 2.2, "开始诊疗\nREST", c_session, edgecolor="#E65100", fs=4.8)
    box(ax, (sess_x + 8, sess_y + 0.4), 8, 2.0, "诊疗会话控制", c_session, edgecolor="#E65100", fs=5.5)
    box(ax, (sess_x + 20, sess_y + 0.2), 5, 2.0, "实时\n语音", "#FFD4A0", edgecolor="#E65100", fs=4.8)
    box(ax, (sess_x + 20, sess_y + 2.4), 5, 1.6, "环境\n感知", "#FFD4A0", edgecolor="#E65100", fs=4.5)
    seg_arrow(ax, sess_x + 6.4, sess_y + 1, sess_x + 8, sess_y + 1, label=None, color="#e65100")
    # 诊疗会话控制 -> 实时语音 / 环境感知
    vox_cx, vox_cy = sess_x + 22.5, sess_y + 1.2
    env_cx, env_cy = sess_x + 22.5, sess_y + 3.2
    seg_arrow(ax, sess_x + 16, sess_y + 1.1, vox_cx, vox_cy, label="启动", l_off=(-0.1, 0.2), color="#e65100", rad=0.02)
    seg_arrow(ax, sess_x + 16, sess_y + 0.9, env_cx, env_cy, label="启动", l_off=(-0.1, -0.2), color="#e65100", rad=-0.02)
    ax.text(
        sess_x + 4, sess_y + 3.5, "↘ 会话元数据",
        ha="left", va="top", fontsize=5.5, color="#5d4037", zorder=5, style="italic", )

    fig.tight_layout()
    fig.savefig(out_png, dpi=200, bbox_inches="tight", facecolor="white", pad_inches=0.3)
    plt.close(fig)
    print(f"Wrote: {out_png}")


if __name__ == "__main__":
    main()
