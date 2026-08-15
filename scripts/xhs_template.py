import os
import re
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont

# ====== 配色：运行时按 --palette 从 palettes 取 ======
from palettes import get_palette

# ====== 输出目录：默认脚本所在目录，可用 --out 覆盖 ======
DEFAULT_OUT = os.path.dirname(os.path.abspath(__file__))

# ====== 画布与边距 ======
W, H = 1080, 1440          # 小红书主流 3:4 比例
ML, MR = 110, 110
CW = W - ML - MR            # 内容宽度

# ====== 字号 ======
F_TITLE = 144     # 封面主标题；行高需同步 → LH_TITLE
F_KICKER = 34     # 栏目小标
F_SUB = 38        # 封面副标题
F_HEAD = 42       # 章节标题
F_BODY = 42       # 正文
F_CALL = 40       # 金句
F_FOOT = 28       # 页脚
LH_TITLE = 186    # 封面标题行高（≈ F_TITLE × 1.29）

# ====== 中文字体（macOS 系统字体）======
SANS = "/System/Library/Fonts/Hiragino Sans GB.ttc"
BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

def lf(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.truetype(SANS, size, index=0)


def build_flags(text, phrases):
    flags = [False] * len(text)
    for p in phrases:
        if not p:
            continue
        start = 0
        while True:
            i = text.find(p, start)
            if i < 0:
                break
            for k in range(i, i + len(p)):
                flags[k] = True
            start = i + len(p)
    return flags


def mkline(chars, fr, fb, base, gold, lh):
    return {"chars": chars, "fr": fr, "fb": fb, "base": base, "gold": gold, "lh": lh}


def wrap(text, flags, fr, fb, max_w, line_h, base, gold):
    lines = []
    cur = []
    cur_w = 0
    i = 0
    while i < len(text):
        ch = text[i]
        is_asc = ch.isascii() and ch.isalnum()
        f = fb if flags[i] else fr
        w = f.getlength(ch)
        if cur and cur_w + w > max_w:
            # Don't break inside an ASCII word; move the word to next line
            if is_asc and cur[-1][0].isascii() and cur[-1][0].isalnum():
                j = len(cur) - 1
                while j >= 0 and cur[j][0].isascii() and cur[j][0].isalnum():
                    j -= 1
                if j >= 0:  # word doesn't start at line beginning
                    move = cur[j + 1:]
                    cur = cur[:j + 1]
                    cur_w = sum((fb if ig else fr).getlength(c) for c, ig in cur)
                    lines.append(mkline(cur, fr, fb, base, gold, line_h))
                    cur = list(move)
                    cur_w = sum((fb if ig else fr).getlength(c) for c, ig in cur)
                    continue
            lines.append(mkline(cur, fr, fb, base, gold, line_h))
            cur = []
            cur_w = 0
            if ch == " ":
                i += 1
                continue
        cur.append((ch, flags[i]))
        cur_w += (fb if flags[i] else fr).getlength(ch)
        i += 1
    if cur:
        lines.append(mkline(cur, fr, fb, base, gold, line_h))
    return lines


def para_lines(p, GOLD, TEXT):
    t = p["t"]
    hl = p.get("hl", [])
    if p.get("heading"):
        fl = build_flags(t, hl)
        return {"lines": wrap(t, fl, f_head, f_head, CW, 84, GOLD, GOLD),
                "callout": False, "heading": True}
    if p.get("callout"):
        fl = build_flags(t, hl)
        return {"lines": wrap(t, fl, f_call, f_call, CW - 80, 72, GOLD, GOLD),
                "callout": True, "heading": False}
    fl = build_flags(t, hl)
    return {"lines": wrap(t, fl, f_body, f_body_b, CW, 66, TEXT, GOLD),
            "callout": False, "heading": False}


def block_height(blk):
    bh = sum(ln["lh"] for ln in blk["lines"])
    if blk["callout"]:
        return bh + 40 + 30
    return bh + 20


def draw_line(d, line, x, y):
    x0 = x
    for ch, ig in line["chars"]:
        f = line["fb"] if ig else line["fr"]
        col = line["gold"] if ig else line["base"]
        d.text((x0, y), ch, font=f, fill=col)
        x0 += f.getlength(ch)


def draw_footer(d, idx, N, tag, LINE, DIM, GOLD):
    fy = H - 90
    d.line([(ML, fy - 30), (W - MR, fy - 30)], fill=LINE, width=2)
    d.text((ML, fy), tag, font=f_foot, fill=DIM)
    txt = f"{idx:02d} / {N:02d}"
    w = f_foot.getlength(txt)
    d.text((W - MR - w, fy), txt, font=f_foot, fill=GOLD)


def draw_cover(d, N, GOLD, TEXT, LINE, COVER_KICKER, COVER_TITLE, COVER_SUB, FOOTER_TAG):
    d.rectangle([0, 0, W, 10], fill=GOLD)
    d.text((ML, 200), COVER_KICKER, font=f_kicker, fill=GOLD)
    title = COVER_TITLE
    tfl = [True] * len(title)
    tlines = wrap(title, tfl, f_title, f_title, CW, LH_TITLE, GOLD, GOLD)
    y = 300
    for ln in tlines:
        draw_line(d, ln, ML, y)
        y += ln["lh"]
    d.rectangle([ML, y + 14, ML + 180, y + 22], fill=GOLD)
    y += 70
    sub = COVER_SUB
    sfl = [False] * len(sub)
    slines = wrap(sub, sfl, f_sub, f_sub, CW, 58, TEXT, TEXT)
    for ln in slines:
        draw_line(d, ln, ML, y)
        y += ln["lh"]
    draw_footer(d, 1, N, FOOTER_TAG, LINE, TEXT, GOLD)


def draw_content(d, blocks_slice, idx, N, GOLD, TEXT, LINE, DIM, PANEL, CONTENT_KICKER):
    d.rectangle([0, 0, W, 10], fill=GOLD)
    d.text((ML, 130), CONTENT_KICKER, font=f_kicker, fill=GOLD)
    y = 210
    y_end = H - 120
    for blk in blocks_slice:
        if blk["callout"]:
            bh = sum(ln["lh"] for ln in blk["lines"]) + 40
            d.rounded_rectangle([ML, y, W - MR, y + bh], radius=24,
                                outline=GOLD, width=3, fill=PANEL)
            cy = y + 20
            for ln in blk["lines"]:
                draw_line(d, ln, ML + 40, cy)
                cy += ln["lh"]
            y += bh + 30
        else:
            for ln in blk["lines"]:
                if blk.get("heading"):
                    d.rectangle([ML, y + 16, ML + 18, y + 38], fill=GOLD)
                    draw_line(d, ln, ML + 34, y)
                else:
                    draw_line(d, ln, ML, y)
                y += ln["lh"]
            y += 20


def parse_text(text):
    """把带轻量标记的长文解析成 paras 结构。
    语法：
      ## 行   → 章节标题（heading）
      >> 行   → 金句卡片（callout）
      普通行  → 正文
      行内 **关键词** → 该词金色高亮
    """
    paras = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        kind = None
        if line.startswith("## "):
            line = line[3:].strip()
            kind = "heading"
        elif line.startswith(">> "):
            line = line[3:].strip()
            kind = "callout"
        hl = re.findall(r"\*\*(.+?)\*\*", line)
        clean = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
        d = {"t": clean, "hl": hl}
        if kind == "heading":
            d["heading"] = True
        elif kind == "callout":
            d["callout"] = True
        paras.append(d)
    return paras


# ====== 内置示例长文（未传 --text 时演示用）======
SAMPLE = """## 认知公地悲剧
越用 AI，越没人真正懂行。

AI 把很多练手的活儿接走了，长期看，整个行业可能慢慢没人真正懂行。

>> 大家越依赖 AI，自己的真功夫越退化；而真功夫退化后，反而越看不出 AI 在哪里出错。

**验证纽带**：你指挥 AI 的能力，归根到底得靠你自己的专业经验撑着。"""


def main():
    ap = argparse.ArgumentParser(description="流宴图文模板 · 小红书长文字图文生成器")
    ap.add_argument("--palette", required=True, help="配色名（如 北境清晨 / 深蓝金白 / 暮光紫罗兰 等 28 套之一）")
    ap.add_argument("--title", default="认知公地悲剧", help="封面主标题")
    ap.add_argument("--sub", default="越用 AI，越没人真正懂行", help="封面副标题")
    ap.add_argument("--tag", default="流宴图文", help="页脚标签")
    ap.add_argument("--kicker", default="深度思考", help="封面栏目小标")
    ap.add_argument("--text", default=None, help="正文长文（支持 ## 标题 / >> 金句 / **关键词** 标记）")
    ap.add_argument("--text-file", default=None, help="从文件读取正文长文")
    ap.add_argument("--out", default=DEFAULT_OUT, help="输出目录（默认脚本所在目录）")
    args = ap.parse_args()

    BG, GOLD, TEXT, LINE, DIM, PANEL = get_palette(args.palette)

    # 字体（按当前配色不需要重建，但保持与模块加载时一致）
    global f_title, f_kicker, f_sub, f_head, f_body, f_body_b, f_call, f_foot
    f_title = lf(BOLD, F_TITLE)
    f_kicker = lf(BOLD, F_KICKER)
    f_sub = lf(SANS, F_SUB)
    f_head = lf(BOLD, F_HEAD)
    f_body = lf(SANS, F_BODY)
    f_body_b = lf(BOLD, F_BODY)
    f_call = lf(BOLD, F_CALL)
    f_foot = lf(SANS, F_FOOT)

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8") as fh:
            body = fh.read()
    elif args.text:
        body = args.text
    else:
        body = SAMPLE

    paras = parse_text(body)
    blocks = [para_lines(p, GOLD, TEXT) for p in paras]

    # ====== 自动分页 ======
    pages = []
    cur = []
    y = 210
    y_end = H - 120
    for blk in blocks:
        bh = block_height(blk)
        if y + bh > y_end and cur:
            pages.append(cur)
            cur = []
            y = 210
        cur.append(blk)
        y += bh
    if cur:
        pages.append(cur)
    N = 1 + len(pages)

    os.makedirs(args.out, exist_ok=True)

    # ====== 渲染 ======
    img = Image.new("RGB", (W, H), BG)
    draw_cover(ImageDraw.Draw(img), N, GOLD, TEXT, LINE,
               args.kicker, args.title, args.sub, args.tag)
    img.save(os.path.join(args.out, "xhs_01_cover.png"))

    for i, pblk in enumerate(pages):
        img = Image.new("RGB", (W, H), BG)
        draw_content(ImageDraw.Draw(img), pblk, i + 2, N,
                     GOLD, TEXT, LINE, DIM, PANEL, args.kicker)
        img.save(os.path.join(args.out, f"xhs_{i+2:02d}_page.png"))

    print("palette:", args.palette)
    print("pages:", N)
    print("files:", sorted(os.listdir(args.out)))


if __name__ == "__main__":
    main()
