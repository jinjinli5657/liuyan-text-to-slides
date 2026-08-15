# 流宴图文模板（liuyan-text-to-slides）

> 🌐 **Bilingual / 中英双语**：[在线交互版（点「中文 / English」切换，默认英文）](https://jinjinli5657.github.io/liuyan-text-to-slides/) · 也可直接打开仓库里的 `index.html`。

把一段长文「fit」进小红书主流的 3:4（1080×1440）图文：第 1 张封面（大字标题）+ 后续内页（自动分页），正文用指定配色生成，可直接发小红书。

> WorkBuddy / CodeBuddy 的 Skill：当用户提到某个配色主题名（如「北境清晨」「暮光紫罗兰」）并要求「出图 / 做图文 / 生成小红书笔记 / 用 XX 配色」时，自动用该配色生成一整套 PNG（封面 + 内页）。

## 功能特性

- **28 套精选配色**：提到名字即用，没提配色时默认「深蓝金白」。
- **自动分页**：按内容高度智能分页，不截断句子。
- **结构化标记语法**：章节标题、金句卡片、关键词金色高亮，长文秒变小红书风格。
- **中文字体清晰**：走系统中文矢量字体（Hiragino Sans GB / STHeiti），不糊。
- **配色易扩展**：所有配色集中在 `scripts/palettes.py`，加一项即可新增。

## 28 套可用配色（提到名字即用）

| 分组 | 配色名 |
|---|---|
| 主配色 / 图片取色 | 深蓝金白、秋日暖棕、蓝棕咖啡、治愈紫反转、米杏黑红、北境清晨、秋日信笺、燕麦拿铁、午夜书房、暮光紫罗兰、勃艮第剧场、柔雾玫瑰、留白莓紫 |
| 经典建议 | 小红书经典粉、多巴胺暖橙、莫兰迪低饱和、奶油米白、清新马卡龙、暗黑高级金、知性蓝 |
| 追加经典 | 克莱因蓝、国潮红金、祖母绿翡翠、香芋紫亮版、牛油果薄荷、美拉德焦糖、盐系冷淡灰、番茄活力红 |

每套配色都保证「背景 / 标题重点 / 正文」三者对比度足够，长文字可读（浅底配色正文用深中性色，深底配色正文用浅色）。

## 配色预览（28 套）

每张图都是用对应配色渲染的「小红书封面 + 6 色色卡」；底部色卡从左到右依次为：**背景 / 标题色 / 正文色 / 描边 / 次要文字 / 卡片底**。

| 配色 | 预览 | 配色 | 预览 |
|---|---|---|---|
| 深蓝金白 | ![](previews/01.png) | 多巴胺暖橙 | ![](previews/15.png) |
| 秋日暖棕 | ![](previews/02.png) | 莫兰迪低饱和 | ![](previews/16.png) |
| 蓝棕咖啡 | ![](previews/03.png) | 奶油米白 | ![](previews/17.png) |
| 治愈紫反转 | ![](previews/04.png) | 清新马卡龙 | ![](previews/18.png) |
| 米杏黑红 | ![](previews/05.png) | 暗黑高级金 | ![](previews/19.png) |
| 北境清晨 | ![](previews/06.png) | 知性蓝 | ![](previews/20.png) |
| 秋日信笺 | ![](previews/07.png) | 克莱因蓝 | ![](previews/21.png) |
| 燕麦拿铁 | ![](previews/08.png) | 国潮红金 | ![](previews/22.png) |
| 午夜书房 | ![](previews/09.png) | 祖母绿翡翠 | ![](previews/23.png) |
| 暮光紫罗兰 | ![](previews/10.png) | 香芋紫亮版 | ![](previews/24.png) |
| 勃艮第剧场 | ![](previews/11.png) | 牛油果薄荷 | ![](previews/25.png) |
| 柔雾玫瑰 | ![](previews/12.png) | 美拉德焦糖 | ![](previews/26.png) |
| 留白莓紫 | ![](previews/13.png) | 盐系冷淡灰 | ![](previews/27.png) |
| 小红书经典粉 | ![](previews/14.png) | 番茄活力红 | ![](previews/28.png) |

## 快速开始

依赖 [Pillow](https://pypi.org/project/Pillow/)：

```bash
pip install Pillow
```

生成示例（用「北境清晨」配色 + 一段带标记的文字）：

```bash
python scripts/xhs_template.py \
  --palette 北境清晨 \
  --title "认知公地悲剧" \
  --sub "越用 AI，越没人真正懂行" \
  --tag "流宴图文" \
  --kicker "深度思考" \
  --text-file 你的正文.txt \
  --out ./output
```

> 若你使用 WorkBuddy 的托管隔离 Python（已带 Pillow），可直接用其解释器运行：
> `/Users/robert/.workbuddy/binaries/python/envs/default/bin/python scripts/xhs_template.py ...`

## 命令行参数

| 参数 | 说明 |
|---|---|
| `--palette`（必需） | 配色名，从上方 28 套里选 |
| `--title` | 封面主标题 |
| `--sub` | 封面副标题 |
| `--tag` | 页脚标签 |
| `--kicker` | 栏目小标 |
| `--text` | 直接传正文；或 `--text-file` 读文件（二选一，都不给则用内置示例） |
| `--out` | 输出目录（默认脚本所在目录） |

## 正文标记语法（让长文自动变结构化图文）

```
## 章节标题
这是正文，其中 **关键词** 会被金色高亮。

>> 这是金句卡片（描边框 + 重点色）。
```

- `## ` 开头 → 章节标题（金色 + 方块 bullet）
- `>> ` 开头 → 金句卡片
- 行内 `**词语**` → 该词金色高亮
- 普通行 → 正文

## 输出

`xhs_01_cover.png` + `xhs_02_page.png` + …（封面 1 张 + 内页若干），全部 1080×1440。

## 目录结构

```
liuyan-text-to-slides/
├── SKILL.md              # Skill 元数据与说明（WorkBuddy 加载用）
├── README.md             # 本文件
├── index.html            # 中英双语交互文档（可托管 GitHub Pages）
├── LICENSE               # MIT License
├── gen_previews.py       # 28 套配色预览图生成器（可复现）
├── previews/             # 28 套配色预览图（README 画廊用）
│   ├── 01.png
│   └── ...
└── scripts/
    ├── xhs_template.py   # 主生成脚本
    └── palettes.py       # 28 套配色定义（新增配色改这里）
```

## 技术要点

- 中文字体走 macOS 系统字体（Hiragino Sans GB / STHeiti），中文清晰不糊。
- 配色全部集中在 `scripts/palettes.py`，新增配色只需往 `PALETTES` 里加一项（`bg / gold / text / line / dim / panel` 六值）。
- 与 `jinjin-cover-page` 是同族能力，本 Skill 为整合后的主入口。

## 许可证

[MIT License](./LICENSE) © 2026 jinjinli5657
