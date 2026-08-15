# ====== 流宴图文模板 · 28 套配色调色板 ======
# 每套含 6 个角色：
#   bg   背景色
#   gold 标题/重点/关键词色（强调色）
#   text 正文字色（已确保与 bg 对比度足够，长文字可读）
#   line 分隔线色
#   dim  页脚/次要文字色
#   panel 金句卡片底色
# 浅底配色正文用深中性色、深底配色正文用浅色，避免「浅底浅字/深底深字」读不清。

PALETTES = {
    # ===== final_schemes（图片取色 + 主配色）=====
    "深蓝金白":     dict(bg="#062062", gold="#DAA520", text="#FFFFFF", line="#375897", dim="#C8D0E1", panel="#0E2A6E"),
    "秋日暖棕":     dict(bg="#5C3A21", gold="#F2B134", text="#FFF8E7", line="#8A5A35", dim="#D4B896", panel="#3A2415"),
    "蓝棕咖啡":     dict(bg="#F5F1EB", gold="#64A9F7", text="#182136", line="#C2C2C7", dim="#6D3E2C", panel="#E8E2D8"),
    "治愈紫反转":   dict(bg="#F4F0E9", gold="#493144", text="#5D4958", line="#7A6474", dim="#7A6474", panel="#E5DEE7"),
    "米杏黑红":     dict(bg="#E7CFA8", gold="#CD2918", text="#020700", line="#B49E78", dim="#5A4C38", panel="#F7F0DE"),
    "北境清晨":     dict(bg="#E7EBF8", gold="#BD5D4F", text="#1B312B", line="#C3CCDD", dim="#7A8AA0", panel="#D6DCEC"),
    "秋日信笺":     dict(bg="#E4DBCC", gold="#615E54", text="#4A463F", line="#C8BEAD", dim="#8A8276", panel="#D8CFBE"),
    "燕麦拿铁":     dict(bg="#DBE1E5", gold="#914935", text="#46291E", line="#AE7254", dim="#6E6157", panel="#CBD2D8"),
    "午夜书房":     dict(bg="#082960", gold="#AEACB7", text="#F8F6F0", line="#3A5AA0", dim="#9DAAC0", panel="#0E2A6E"),
    "暮光紫罗兰":   dict(bg="#5E084E", gold="#AEACB7", text="#F8F6F0", line="#8E3E80", dim="#C9A0C0", panel="#3A0530"),
    "勃艮第剧场":   dict(bg="#8B1331", gold="#AEACB7", text="#F8F6F0", line="#B0405A", dim="#C9A0B0", panel="#5A0C20"),
    "柔雾玫瑰":     dict(bg="#F8CAC4", gold="#9A5A6E", text="#5A363E", line="#E0A9A3", dim="#A86E78", panel="#F2D8D4"),
    "留白莓紫":     dict(bg="#FDFDFD", gold="#763D53", text="#3A2030", line="#E0D5DA", dim="#A890A0", panel="#F2ECF0"),

    # ===== orig_schemes（最初建议的 7 套）=====
    "小红书经典粉": dict(bg="#FFF5F5", gold="#FF2442", text="#3A2E2E", line="#FFD5DB", dim="#B08088", panel="#FFE9EC"),
    "多巴胺暖橙":   dict(bg="#FFF8F0", gold="#FF7A45", text="#3A2E26", line="#FFE0CC", dim="#B5907A", panel="#FFEEDD"),
    "莫兰迪低饱和": dict(bg="#F2EFEA", gold="#B0A8B9", text="#4A4742", line="#DAD6CF", dim="#9A928A", panel="#E8E4DE"),
    "奶油米白":     dict(bg="#FBF7F2", gold="#C9A87C", text="#4A4036", line="#EADFCF", dim="#A89080", panel="#F2EADD"),
    "清新马卡龙":   dict(bg="#F4FBF8", gold="#7EC8B1", text="#2E4A42", line="#C8E8DD", dim="#8FB8A8", panel="#E4F5EF"),
    "暗黑高级金":   dict(bg="#1A1A1A", gold="#E8B04B", text="#EEEEEE", line="#444444", dim="#999999", panel="#2A2A2A"),
    "知性蓝":       dict(bg="#F4F8FC", gold="#4A6FA5", text="#28354A", line="#C8D8EE", dim="#8FAADC", panel="#E6EEF8"),

    # ===== extra_schemes（追加的 8 套经典配色）=====
    "克莱因蓝":     dict(bg="#002FA7", gold="#F5C518", text="#FFFFFF", line="#2A55C8", dim="#9DA8C8", panel="#00257F"),
    "国潮红金":     dict(bg="#E60012", gold="#D4AF37", text="#FFF5E6", line="#B00C0C", dim="#C97A7A", panel="#A00000"),
    "祖母绿翡翠":   dict(bg="#0E5C4A", gold="#C9A227", text="#EAF3EE", line="#1A7A62", dim="#9AC2B0", panel="#0A4234"),
    "香芋紫亮版":   dict(bg="#8B7CC6", gold="#C9BEE8", text="#F4F0FB", line="#A394D2", dim="#B0A0D0", panel="#6B5CA6"),
    "牛油果薄荷":   dict(bg="#F0F4E8", gold="#A8C66C", text="#3E563B", line="#D5E0C0", dim="#7E9A5C", panel="#E2EAD2"),
    "美拉德焦糖":   dict(bg="#3A2418", gold="#D2691E", text="#F3E3D3", line="#5A3A28", dim="#C98A5A", panel="#2A1810"),
    "盐系冷淡灰":   dict(bg="#F2F2F2", gold="#8C8C8C", text="#333333", line="#DADADA", dim="#9C9C9C", panel="#E8E8E8"),
    "番茄活力红":   dict(bg="#FFFFFF", gold="#FF4500", text="#1A1A1A", line="#FFD0C0", dim="#CC4A2A", panel="#FFF0EB"),
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def get_palette(name):
    """按配色名取色，返回 6 个 RGB 元组。找不到时抛出 KeyError。"""
    if name not in PALETTES:
        raise KeyError(f"未知配色：{name}。可用：{', '.join(PALETTES)}")
    p = PALETTES[name]
    return (hex2rgb(p["bg"]), hex2rgb(p["gold"]), hex2rgb(p["text"]),
            hex2rgb(p["line"]), hex2rgb(p["dim"]), hex2rgb(p["panel"]))
