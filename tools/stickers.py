"""Draws the cartoon stickers for the GitHub profile README as self-contained SVGs.

Fonts (ZCOOL KuaiLe for Chinese, Fredoka for English; both SIL OFL) are subset to the glyphs each
image uses and embedded as WOFF2, so the stickers look the same on every machine.
"""
import base64
import io
import pathlib
import sys

# Usage: python tools/stickers.py assets
# Needs fonttools + brotli, and the two fonts in tools/fonts/ (not committed, 1.5 MB):
#   ZCOOLKuaiLe.ttf  https://github.com/google/fonts/tree/main/ofl/zcoolkuaile
#   Fredoka.ttf      https://github.com/google/fonts/tree/main/ofl/fredoka  (Fredoka[wdth,wght].ttf)
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE / "pylib"))
from fontTools import subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.varLib import instancer  # noqa: E402

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

INK = "#2d2a45"
TEXT = "#4a4668"
SOFT = "#6e6a8c"
PINK = "#ff8fab"
HOT = "#ff6f91"
MINT = "#7ee0c3"
LAV = "#c3bbff"
SUN = "#ffd166"


def woff2(path, text, wght=None):
    f = TTFont(path)
    if wght is not None:
        f = instancer.instantiateVariableFont(f, {"wght": wght, "wdth": 100})
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text + " ")
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def doc(w, h, body, cn="", en="", css=""):
    faces = ""
    if cn:
        faces += "@font-face{font-family:'Kuaile';src:url(data:font/woff2;base64,%s) format('woff2')}" % woff2(
            HERE / "fonts/ZCOOLKuaiLe.ttf", cn
        )
    if en:
        faces += "@font-face{font-family:'Fredoka';src:url(data:font/woff2;base64,%s) format('woff2')}" % woff2(
            HERE / "fonts/Fredoka.ttf", en, wght=600
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
{faces}
.cn{{font-family:'Kuaile','Microsoft YaHei','PingFang SC',sans-serif}}
.en{{font-family:'Fredoka','Segoe UI',sans-serif;font-weight:600}}
.ink{{stroke:{INK};stroke-linejoin:round;stroke-linecap:round}}
.bounce{{transform-box:fill-box;transform-origin:50% 100%;animation:bounce 1.6s ease-in-out infinite}}
@keyframes bounce{{0%,100%{{transform:translateY(0) scale(1.08,.92)}}30%{{transform:translateY(-16px) scale(.94,1.06)}}55%{{transform:translateY(-20px) scale(.97,1.03)}}80%{{transform:translateY(0) scale(1.1,.9)}}}}
.shadow{{transform-box:fill-box;transform-origin:50% 50%;animation:shadow 1.6s ease-in-out infinite}}
@keyframes shadow{{0%,100%{{transform:scaleX(1.05)}}45%{{transform:scaleX(.7);opacity:.5}}}}
.blink{{transform-box:fill-box;transform-origin:50% 50%;animation:blink 4s infinite}}
@keyframes blink{{0%,90%,100%{{transform:scaleY(1)}}94%{{transform:scaleY(.1)}}}}
.twinkle{{transform-box:fill-box;transform-origin:50% 50%;animation:twinkle 2.2s ease-in-out infinite}}
@keyframes twinkle{{0%,100%{{transform:scale(1) rotate(0)}}50%{{transform:scale(.55) rotate(45deg);opacity:.6}}}}
.drift{{animation:drift 9s ease-in-out infinite alternate}}
@keyframes drift{{from{{transform:translateX(-14px)}}to{{transform:translateX(14px)}}}}
{css}
</style>
{body}
</svg>
"""


def slime(x, y, s, color=MINT, mouth="smile", eyes="open", cls="bounce"):
    """A slime 160 wide, 130 tall at scale 1, bottom-left at (x, y + 130*s)."""
    if eyes == "open":
        eye = f"""<g class="blink"><ellipse cx="60" cy="78" rx="7" ry="10" fill="{INK}"/><ellipse cx="100" cy="78" rx="7" ry="10" fill="{INK}"/>
<circle cx="62.5" cy="73" r="2.6" fill="#fff"/><circle cx="102.5" cy="73" r="2.6" fill="#fff"/></g>"""
    else:
        eye = '<path class="ink" d="M52 80 Q60 86 68 80 M92 80 Q100 86 108 80" fill="none" stroke-width="3.5"/>'
    if mouth == "smile":
        m = '<path class="ink" d="M73 95 Q80 103 87 95" fill="none" stroke-width="3.5"/>'
    elif mouth == "open":
        m = f'<ellipse class="chomp" cx="80" cy="99" rx="13" ry="10" fill="{INK}"/><ellipse cx="80" cy="104" rx="6" ry="3" fill="{PINK}"/>'
    else:
        m = '<path class="ink" d="M76 97 Q80 99 84 97" fill="none" stroke-width="3"/>'
    return f"""<g transform="translate({x} {y}) scale({s})">
<ellipse class="shadow" cx="80" cy="131" rx="58" ry="7" fill="{INK}" opacity=".16"/>
<g class="{cls}">
<path class="ink" d="M18 128 C6 128 4 108 10 92 C20 52 48 18 80 18 C112 18 140 52 150 92 C156 108 154 128 142 128 Z" fill="{color}" stroke-width="4"/>
<ellipse cx="50" cy="48" rx="15" ry="8" fill="#fff" opacity=".75" transform="rotate(-32 50 48)"/>
<circle cx="37" cy="64" r="4" fill="#fff" opacity=".75"/>
{eye}
<ellipse cx="42" cy="95" rx="10" ry="5" fill="{PINK}" opacity=".55"/><ellipse cx="118" cy="95" rx="10" ry="5" fill="{PINK}" opacity=".55"/>
{m}
</g></g>"""


def sparkle(x, y, s=1, color=SUN, delay=0):
    return f"""<g transform="translate({x} {y}) scale({s})"><path class="ink twinkle" style="animation-delay:{delay}s"
d="M0 -13 Q2.5 -2.5 13 0 Q2.5 2.5 0 13 Q-2.5 2.5 -13 0 Q-2.5 -2.5 0 -13 Z" fill="{color}" stroke-width="2.5"/></g>"""


def cloud(x, y, s=1, delay=0):
    return f"""<g transform="translate({x} {y}) scale({s})"><g class="drift" style="animation-delay:{delay}s">
<path class="ink" d="M30 52 Q8 52 12 36 Q14 22 32 24 Q38 6 60 10 Q78 0 90 18 Q110 16 110 34 Q116 52 96 52 Z" fill="#fff" stroke-width="3"/></g></g>"""


# ---------------------------------------------------------------- header

def header():
    w, h = 900, 290
    cn = "你好呀，我是喜欢做让电脑更顺手的小工具最近在用写桌面应用 RustTauri+"
    en = "cjxhaaa"
    body = f"""<defs>
<linearGradient id="sky" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d7ecff"/><stop offset="1" stop-color="#ffe1ef"/></linearGradient>
<clipPath id="frame"><rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30"/></clipPath>
</defs>
<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30" fill="url(#sky)"/>
<g clip-path="url(#frame)">
{cloud(560, 196, .55, 1)}{cloud(40, 26, .8)}{cloud(720, 14, .7, 3)}
<path class="ink" d="M-10 238 Q150 186 330 226 T660 214 T910 206 L910 300 L-10 300 Z" fill="#c8f5d8" stroke-width="4"/>
<path class="ink" d="M-10 262 Q200 226 420 254 T910 244 L910 300 L-10 300 Z" fill="#9fe8bf" stroke-width="4"/>
<g fill="{PINK}" class="ink" stroke-width="2"><circle cx="604" cy="246" r="5"/><circle cx="640" cy="252" r="4"/><circle cx="760" cy="236" r="5"/></g>
</g>
<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30" fill="none" class="ink" stroke-width="4"/>
{slime(70, 112, 1.08)}
<path class="ink" d="M318 176 L250 206 L352 176" fill="#fff" stroke-width="4"/>
<rect class="ink" x="300" y="34" width="566" height="150" rx="32" fill="#fff" stroke-width="4"/>
<rect x="322" y="170" width="28" height="9" fill="#fff"/>
<text class="cn" x="330" y="96" font-size="30" fill="{TEXT}">你好呀，我是</text>
<text class="en" x="514" y="100" font-size="56" fill="{HOT}" stroke="{INK}" stroke-width="2.4" paint-order="stroke" letter-spacing="1">cjxhaaa</text>
<text class="cn" x="330" y="140" font-size="25" fill="{TEXT}">喜欢做让电脑更顺手的小工具</text>
<text class="cn" x="330" y="168" font-size="19" fill="{SOFT}">最近在用 Rust + Tauri 写桌面应用</text>
{sparkle(266, 56, 1.1)}{sparkle(842, 66, .8, PINK, .7)}{sparkle(820, 238, 1, SUN, 1.3)}{sparkle(470, 228, .7, "#fff", .4)}
"""
    return doc(w, h, body, cn, en)


# ---------------------------------------------------------------- project cards

def pills(tags, x, y, colors):
    out, cx = "", x
    for t, c in zip(tags, colors):
        tw = len(t) * 8.6 + 26
        out += f"""<rect class="ink" x="{cx}" y="{y}" width="{tw}" height="30" rx="15" fill="{c}" stroke-width="2.5"/>
<text class="en" x="{cx + tw / 2}" y="{y + 20.5}" font-size="15" fill="{INK}" text-anchor="middle">{t}</text>"""
        cx += tw + 10
    return out


def card(name, bg, ring, art, tagline, lines, tags, tag_colors, accent):
    w, h = 440, 300
    cn = "".join(tagline) + "".join(lines)
    en = name + "".join(tags)
    body = f"""<rect x="10" y="10" width="{w - 14}" height="{h - 14}" rx="28" fill="{INK}"/>
<rect class="ink" x="4" y="4" width="{w - 14}" height="{h - 14}" rx="28" fill="{bg}" stroke-width="4"/>
<circle cx="84" cy="84" r="60" fill="{ring}"/>
{art}
<text class="en" x="164" y="72" font-size="40" fill="{INK}">{name}</text>
<text class="cn" x="166" y="106" font-size="21" fill="{accent}">{tagline[0]}</text>
<text class="cn" x="166" y="132" font-size="21" fill="{accent}">{tagline[1]}</text>
""" + "".join(
        f'<text class="cn" x="28" y="{178 + i * 26}" font-size="17" fill="{TEXT}">{t}</text>' for i, t in enumerate(lines)
    ) + pills(tags, 28, 244, tag_colors)
    css = """.wiggle{transform-box:fill-box;transform-origin:50% 100%;animation:wiggle 1.4s ease-in-out infinite}
@keyframes wiggle{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.sweep{transform-box:fill-box;transform-origin:30% 0%;animation:sweep .7s ease-in-out infinite alternate}
@keyframes sweep{from{transform:rotate(-12deg)}to{transform:rotate(12deg)}}
.puff{animation:puff 1.4s ease-out infinite}
@keyframes puff{0%{opacity:0;transform:translate(0,0) scale(.6)}30%{opacity:1}100%{opacity:0;transform:translate(-14px,-10px) scale(1.2)}}
.gulp{transform-box:fill-box;transform-origin:50% 100%;animation:gulp 2.4s ease-in infinite}
@keyframes gulp{0%,15%{transform:translateY(-6px) rotate(-8deg) scale(1)}70%{transform:translateY(26px) rotate(4deg) scale(.45);opacity:1}72%,100%{transform:translateY(26px) scale(.4);opacity:0}}
.chomp{transform-box:fill-box;transform-origin:50% 50%;animation:chomp .6s ease-in-out infinite alternate}
@keyframes chomp{from{transform:scaleY(1)}to{transform:scaleY(.45)}}
.ring{transform-box:fill-box;transform-origin:50% 0%;animation:ring .25s ease-in-out infinite alternate}
@keyframes ring{from{transform:rotate(-10deg)}to{transform:rotate(10deg)}}"""
    return doc(w, h, body, cn, en, css)


def disk_art():
    return f"""<g transform="translate(24 26)">
<g class="puff" fill="#ece9fb"><circle class="ink" cx="14" cy="104" r="7" stroke-width="2"/><circle class="ink" cx="4" cy="94" r="4" stroke-width="2"/></g>
<g class="wiggle">
<rect class="ink" x="20" y="10" width="78" height="96" rx="18" fill="{LAV}" stroke-width="4"/>
<rect class="ink" x="36" y="21" width="46" height="9" rx="4.5" fill="#8f84ff" stroke-width="2.5"/>
<circle class="ink" cx="59" cy="66" r="25" fill="#fff" stroke-width="3.5"/>
<g class="blink"><ellipse cx="51" cy="62" rx="3.6" ry="5.2" fill="{INK}"/><ellipse cx="67" cy="62" rx="3.6" ry="5.2" fill="{INK}"/></g>
<ellipse cx="44" cy="73" rx="5" ry="3" fill="{PINK}" opacity=".6"/><ellipse cx="74" cy="73" rx="5" ry="3" fill="{PINK}" opacity=".6"/>
<path class="ink" d="M52 74 Q59 81 66 74" fill="none" stroke-width="3"/>
</g>
<g class="sweep">
<path d="M92 34 L106 96" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
<path d="M92 34 L106 96" stroke="#c98a5a" stroke-width="5.5" stroke-linecap="round"/>
<path class="ink" d="M96 92 L118 88 L124 110 L94 114 Z" fill="{SUN}" stroke-width="3"/>
<path class="ink" d="M103 92 L106 112 M110 91 L114 111" stroke-width="2" fill="none"/>
</g>
<path class="ink" d="M96 58 Q104 56 99 64" fill="none" stroke-width="3.5"/>
</g>"""


def slime_art():
    return f"""<g transform="translate(26 22)">
<g transform="translate(70 0)"><g class="ring">
<circle class="ink" cx="22" cy="20" r="15" fill="#fff" stroke-width="3"/>
<path class="ink" d="M22 11 L22 20 L29 24" fill="none" stroke-width="3"/>
<path class="ink" d="M9 7 Q12 2 17 5 M35 7 Q32 2 27 5" fill="{HOT}" stroke-width="3"/></g></g>
<g class="gulp" transform="translate(14 14)">
<rect class="ink" x="0" y="0" width="54" height="40" rx="7" fill="#fff" stroke-width="3"/>
<path class="ink" d="M0 14 L54 14" stroke-width="3"/>
<rect x="1.5" y="1.5" width="51" height="11" rx="6" fill="{PINK}"/>
<path class="ink" d="M43 4 L49 10 M49 4 L43 10" stroke-width="2.5"/>
<path class="ink" d="M8 23 L34 23 M8 31 L26 31" stroke-width="2.5" stroke="#c9c4e8"/>
</g>
{slime(0, 28, .74, MINT, mouth="open", cls="")}
</g>"""


def cards():
    disk = card(
        "DiskMate", "#f4f1ff", "#e4defe", disk_art(),
        ["看清 C 盘都去哪了，", "放心地腾出空间"],
        ["每一项都写清删了有什么影响，", "大文件夹一键搬到 D 盘也不用改设置，", "还能管应用、开机启动和性能。"],
        ["Rust", "Tauri 2", "React"], ["#ffd6a5", "#bde0fe", "#c3f0ff"], "#7a62ff",
    )
    goo = card(
        "slime", "#ebfbf4", "#d2f5e6", slime_art(),
        ["住在屏幕上的", "史莱姆桌宠"],
        ["身体是软体物理模拟，没有一张贴图。", "放到窗口上，它会把窗口吞掉关闭，", "开会前还会着急地提醒你。"],
        ["TypeScript", "Tauri 2"], ["#bde0fe", "#ffc8dd"], "#1fa88a",
    )
    return disk, goo


# ---------------------------------------------------------------- section stickers

def sticker(text, fill, icon_color):
    tw = len(text) * 27
    w = int(24 + 26 + 12 + tw + 26 + 8)
    h = 66
    body = f"""<rect x="8" y="8" width="{w - 10}" height="{h - 10}" rx="29" fill="{INK}"/>
<rect class="ink" x="3" y="3" width="{w - 10}" height="{h - 10}" rx="29" fill="{fill}" stroke-width="4"/>
{sparkle(36, 31, 1.05, icon_color)}
<text class="cn" x="60" y="41" font-size="27" fill="{INK}">{text}</text>"""
    return doc(w, h, body, cn=text)


# ---------------------------------------------------------------- footer

def footer():
    w, h = 900, 190
    cn = "谢谢你来玩～下次见！"
    en = "Zz"
    css = """.zz{animation:zz 3s ease-out infinite;opacity:0}
@keyframes zz{0%{opacity:0;transform:translate(0,0)}20%{opacity:1}100%{opacity:0;transform:translate(16px,-34px)}}
.breathe{transform-box:fill-box;transform-origin:50% 100%;animation:breathe 3s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1.04,.96)}50%{transform:scale(.98,1.03)}}"""
    body = f"""<defs><clipPath id="f"><rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30"/></clipPath></defs>
<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30" fill="#fff4e3"/>
<g clip-path="url(#f)">
<path class="ink" d="M-10 150 Q220 104 450 140 T910 128 L910 200 L-10 200 Z" fill="#c8f5d8" stroke-width="4"/>
<g class="ink" stroke-width="2"><circle cx="150" cy="138" r="6" fill="{SUN}"/><circle cx="182" cy="132" r="5" fill="{PINK}"/><circle cx="700" cy="130" r="6" fill="{PINK}"/><circle cx="736" cy="136" r="5" fill="{SUN}"/></g>
</g>
<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="30" fill="none" class="ink" stroke-width="4"/>
{slime(250, 34, .74, "#a8d8ff", mouth="sleep", eyes="closed", cls="breathe")}
<text class="en zz" x="372" y="52" font-size="22" fill="{SOFT}">Z</text>
<text class="en zz" x="386" y="42" font-size="16" fill="{SOFT}" style="animation-delay:1s">z</text>
<text class="en zz" x="396" y="34" font-size="13" fill="{SOFT}" style="animation-delay:2s">z</text>
<text class="cn" x="450" y="92" font-size="30" fill="{TEXT}">谢谢你来玩～下次见！</text>
{sparkle(430, 52, .8, SUN, .3)}{sparkle(780, 64, 1, PINK, 1.1)}"""
    return doc(w, h, body, cn, en, css)


files = {
    "header.svg": header(),
    "footer.svg": footer(),
    "title-projects.svg": sticker("最近在做的小东西", "#ffe08a", PINK),
    "title-tools.svg": sticker("常用的工具", "#ffc8dd", SUN),
    "title-snake.svg": sticker("贡献小蛇在吃格子", "#c8f5d8", HOT),
}
files["card-diskmate.svg"], files["card-slime.svg"] = cards()
for name, svg in files.items():
    (OUT / name).write_text(svg, encoding="utf-8", newline="\n")
    print(f"{name}: {len(svg.encode()) // 1024} KB")
