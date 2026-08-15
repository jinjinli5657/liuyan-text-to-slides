#!/usr/bin/env python3
# 生成 28 套配色的预览图（每张 = 小红书风封面 + 6 色色卡），并输出 README 画廊 Markdown。
# 用法：python gen_previews.py
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "scripts")
OUT = os.path.join(HERE, "previews")

# 复用 palettes 定义
import importlib.util
spec = importlib.util.spec_from_file_location("palettes", os.path.join(SCRIPTS, "palettes.py"))
pal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pal)
PALETTES = pal.PALETTES
hex2rgb = pal.hex2rgb

SANS = "/System/Library/Fonts/Hiragino Sans GB.ttc"
BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.truetype(SANS, size, index=0)


def lum(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def render(name, p, idx):
    bg = hex2rgb(p["bg"]); gold = hex2rgb(p["gold"]); text = hex2rgb(p["text"])
    line = hex2rgb(p["line"]); dim = hex2rgb(p["dim"]); panel = hex2rgb(p["panel"])
    W, Hh = 360, 540
    img = Image.new("RGB", (W, Hh), bg)
    d = ImageDraw.Draw(img)

    # 顶部金色条
    d.rectangle([0, 0, W, 6], fill=gold)
    # 栏目小标
    d.text((24, 22), "流宴图文 · 配色预览", font=font(SANS, 16), fill=gold)
    # 标题 = 配色名（金色，展示强调色）
    d.text((24, 52), name, font=font(BOLD, 40), fill=gold)
    # 金色分隔
    d.rectangle([24, 110, 150, 116], fill=gold)
    # 副标题（正文色）
    d.text((24, 132), "越用 AI，越没人真正懂行", font=font(SANS, 19), fill=text)
    # 正文样例（次要色）
    d.text((24, 168), "自动分页 · 关键词高亮", font=font(SANS, 16), fill=dim)
    # 金句高亮样例
    d.text((24, 200), "重点词高亮", font=font(BOLD, 22), fill=gold)

    # 底部 6 色色卡
    roles = [("背景", bg), ("标题", gold), ("正文", text),
             ("描边", line), ("次要", dim), ("卡片", panel)]
    sw = W // 6
    y0 = Hh - 76
    for i, (label, col) in enumerate(roles):
        x = i * sw
        d.rectangle([x, y0, x + sw, y0 + 76], fill=col,
                    outline=(180, 180, 180), width=1)
        lc = (255, 255, 255) if lum(col) < 150 else (20, 20, 20)
        f = font(SANS, 13)
        tw = f.getlength(label)
        d.text((x + (sw - tw) / 2, y0 + 30), label, font=f, fill=lc)

    path = os.path.join(OUT, f"{idx:02d}.png")
    img.save(path)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    names = list(PALETTES.keys())
    for i, name in enumerate(names, start=1):
        render(name, PALETTES[name], i)
    print(f"generated {len(names)} previews in {OUT}")

    # 输出 README 画廊（2 列配对）
    lines = []
    lines.append("## 配色预览（28 套）")
    lines.append("")
    lines.append("每张图都是用对应配色渲染的「小红书封面 + 6 色色卡」；底部色卡从左到右依次为：**背景 / 标题色 / 正文色 / 描边 / 次要文字 / 卡片底**。")
    lines.append("")
    lines.append("| 配色 | 预览 | 配色 | 预览 |")
    lines.append("|---|---|---|---|")
    half = len(names) // 2
    for i in range(half):
        lname = names[i]
        rname = names[i + half]
        lidx = f"{i+1:02d}"
        ridx = f"{i+half+1:02d}"
        lines.append(f"| {lname} | ![](previews/{lidx}.png) | {rname} | ![](previews/{ridx}.png) |")
    out_md = os.path.join(OUT, "_gallery.md")
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"gallery markdown -> {out_md}")


if __name__ == "__main__":
    main()
