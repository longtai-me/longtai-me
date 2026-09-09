"""產生個人網頁改版設計稿（SVG）。

從 public/json/*.json 讀取真實資料，輸出 design/redesign-2026.svg。
設計稿包含三個 artboard：桌機版全頁、手機版、設計 token 一覽。

用法：python3 scripts/generate_design_svg.py
"""

import json
import os

OUTPUT = 'design/redesign-2026.svg'
DATA_DIR = 'public/json'

# --- 設計 token ---------------------------------------------------------

C = {
    'canvas': '#0d1117',
    'bg': '#1b212c',
    'bg2': '#161c25',
    'surface': '#212936',
    'surface2': '#28323f',
    'line': '#2f3846',
    'line2': '#3b4656',
    'primary': '#00a8f0',
    'primary_dark': '#0b7fb8',
    'cyan': '#7ee0ff',
    'text': '#ffffff',
    'muted': '#b0b7c3',
    'dim': '#7f8a9c',
}

FONT = "Inter, 'Segoe UI', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"

# artboard 尺寸
D_W = 1440          # 桌機版寬度
D_PAD = 160         # 桌機版左右留白
D_COL = D_W - D_PAD * 2  # 內容欄寬 1120
M_W = 390           # 手機版寬度
M_PAD = 24
T_W = 640           # token 面板寬度
GUTTER = 80


# --- 小工具 -------------------------------------------------------------

def esc(s):
    """XML 逃脫。"""
    return (str(s)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def char_width(ch, size):
    """粗略估算字元寬度，供手動換行用（SVG 沒有自動換行）。"""
    code = ord(ch)
    if code == 32:
        return size * 0.28
    # CJK 與全形標點視為全形
    if 0x2E80 <= code <= 0x9FFF or 0xFF00 <= code <= 0xFF60 or 0x3000 <= code <= 0x303F:
        return size * 1.0
    if ch in 'MW@':
        return size * 0.87
    if ch in 'mw':
        return size * 0.82
    if ch in "iljtfrI.,;:'|!()[]{}/\\-":
        return size * 0.32
    if ch.isupper() or ch.isdigit():
        return size * 0.60
    return size * 0.54


def text_width(s, size):
    return sum(char_width(ch, size) for ch in s)


def wrap(s, max_px, size, max_lines=None):
    """依估算寬度手動斷行；CJK 可任意斷，拉丁文字盡量以空白斷。"""
    lines, cur, cur_w = [], '', 0.0
    for ch in s:
        w = char_width(ch, size)
        if cur_w + w > max_px and cur:
            # 拉丁單字盡量不切斷
            if ch != ' ' and ord(ch) < 0x2E80 and ' ' in cur.strip():
                head, _, tail = cur.rstrip().rpartition(' ')
                if head and text_width(tail, size) < max_px * 0.5:
                    lines.append(head)
                    cur, cur_w = tail + ch, text_width(tail + ch, size)
                    continue
            lines.append(cur.rstrip())
            cur, cur_w = ch.lstrip(), char_width(ch, size) if ch != ' ' else 0.0
        else:
            cur += ch
            cur_w += w
    if cur.strip():
        lines.append(cur.rstrip())
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:-1] + '…'
    return lines


def text(x, y, s, size=16, fill=C['text'], weight=400, anchor='start',
         mono=False, opacity=None, spacing=None):
    """單行文字；y 為基線。"""
    attrs = [
        'x="%s"' % fmt(x), 'y="%s"' % fmt(y),
        'font-family="%s"' % (MONO if mono else FONT),
        'font-size="%s"' % fmt(size),
        'fill="%s"' % fill,
    ]
    if weight != 400:
        attrs.append('font-weight="%d"' % weight)
    if anchor != 'start':
        attrs.append('text-anchor="%s"' % anchor)
    if opacity is not None:
        attrs.append('opacity="%s"' % fmt(opacity))
    if spacing is not None:
        attrs.append('letter-spacing="%s"' % fmt(spacing))
    return '<text %s>%s</text>' % (' '.join(attrs), esc(s))


def paragraph(x, y, lines, size=16, line_height=1.65, **kw):
    """多行文字；y 為第一行基線。"""
    lh = size * line_height
    return '\n'.join(text(x, y + i * lh, ln, size=size, **kw) for i, ln in enumerate(lines))


def rect(x, y, w, h, fill='none', rx=0, stroke=None, sw=1, opacity=None):
    attrs = ['x="%s"' % fmt(x), 'y="%s"' % fmt(y),
             'width="%s"' % fmt(w), 'height="%s"' % fmt(h), 'fill="%s"' % fill]
    if rx:
        attrs.append('rx="%s"' % fmt(rx))
    if stroke:
        attrs += ['stroke="%s"' % stroke, 'stroke-width="%s"' % fmt(sw)]
    if opacity is not None:
        attrs.append('opacity="%s"' % fmt(opacity))
    return '<rect %s/>' % ' '.join(attrs)


def line(x1, y1, x2, y2, stroke=C['line'], sw=1, opacity=None):
    attrs = ['x1="%s"' % fmt(x1), 'y1="%s"' % fmt(y1),
             'x2="%s"' % fmt(x2), 'y2="%s"' % fmt(y2),
             'stroke="%s"' % stroke, 'stroke-width="%s"' % fmt(sw)]
    if opacity is not None:
        attrs.append('opacity="%s"' % fmt(opacity))
    return '<line %s/>' % ' '.join(attrs)


def circle(cx, cy, r, fill='none', stroke=None, sw=1, opacity=None):
    attrs = ['cx="%s"' % fmt(cx), 'cy="%s"' % fmt(cy), 'r="%s"' % fmt(r), 'fill="%s"' % fill]
    if stroke:
        attrs += ['stroke="%s"' % stroke, 'stroke-width="%s"' % fmt(sw)]
    if opacity is not None:
        attrs.append('opacity="%s"' % fmt(opacity))
    return '<circle %s/>' % ' '.join(attrs)


def fmt(v):
    """數字轉字串，去掉多餘小數。"""
    if isinstance(v, float):
        return ('%.2f' % v).rstrip('0').rstrip('.')
    return str(v)


def chip(x, y, label, size=12, fg=None, bg=None, stroke=None, h=26, pad=12, mono=False):
    """膠囊標籤；回傳 (svg, 寬度)。y 為頂端。"""
    fg = fg or C['muted']
    w = text_width(label, size) + pad * 2
    out = [rect(x, y, w, h, fill=bg or 'none', rx=h / 2,
                stroke=stroke or (None if bg else C['line']))]
    out.append(text(x + w / 2, y + h / 2 + size * 0.36, label,
                    size=size, fill=fg, anchor='middle', mono=mono))
    return '\n'.join(out), w


def chip_row(x, y, labels, gap=8, **kw):
    """一列膠囊標籤；回傳 (svg, 總寬度)。"""
    out, cx = [], x
    for label in labels:
        svg, w = chip(cx, y, label, **kw)
        out.append(svg)
        cx += w + gap
    return '\n'.join(out), cx - x - gap


def button(x, y, label, w=None, h=52, primary=True, size=16):
    """主要／次要按鈕。y 為頂端。回傳 (svg, 寬度)。"""
    w = w or text_width(label, size) + 56
    out = [rect(x, y, w, h, fill=C['primary'] if primary else 'none', rx=h / 2,
                stroke=None if primary else C['line2'])]
    out.append(text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, weight=700,
                    fill=C['bg'] if primary else C['text'], anchor='middle'))
    return '\n'.join(out), w


def section_head(x, y, index, label_en, title, meta=None, meta_x=None):
    """區塊標題：編號 + 英文標籤 + 中文大標，右側可放註記。"""
    out = [
        text(x, y, '%s — %s' % (index, label_en), size=12, fill=C['primary'],
             mono=True, weight=700, spacing=1.6),
        text(x, y + 44, title, size=34, fill=C['text'], weight=700),
    ]
    if meta:
        out.append(text(meta_x, y + 40, meta, size=13, fill=C['dim'],
                        anchor='end', mono=True))
    return '\n'.join(out)


AVATAR_CLIPS = []


def avatar(cx, cy, r, ring=True):
    """向量頭像佔位圖：漸層底 + 剪影（真實照片會放在這個位置）。"""
    clip_id = 'avatarClip%d' % len(AVATAR_CLIPS)
    AVATAR_CLIPS.append('<clipPath id="%s">%s</clipPath>'
                        % (clip_id, circle(cx, cy, r, fill='#fff')))
    out = []
    if ring:
        out.append(circle(cx, cy, r + 14, stroke=C['primary'], sw=1.5, opacity=0.35))
    out.append(circle(cx, cy, r, fill='url(#avatarGrad)'))
    out.append('<g clip-path="url(#%s)" opacity="0.5">' % clip_id)
    out.append(circle(cx, cy - r * 0.24, r * 0.33, fill=C['bg']))
    out.append('<path d="M %s %s a %s %s 0 0 1 %s 0 Z" fill="%s"/>' % (
        fmt(cx - r * 0.66), fmt(cy + r * 1.02), fmt(r * 0.66), fmt(r * 0.66),
        fmt(r * 1.32), C['bg']))
    out.append('</g>')
    out.append(circle(cx, cy, r, stroke=C['line2'], sw=1))
    return '\n'.join(out)


# --- 讀資料 -------------------------------------------------------------

def load(name):
    with open(os.path.join(DATA_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)


def build_data():
    experiences = load('experiences.json')
    certificates = load('certificate.json')
    friends = load('friends.json')
    support = load('support.json')
    blogs = load('blogs.json')

    featured_titles = ['衛星軌道設計競賽', '國立台中科技大學', 'HITCON']
    featured, rest = [], []
    picked = set()
    for e in experiences:
        if e['title'] in featured_titles and e['title'] not in picked and e['years'] == '2026':
            picked.add(e['title'])
            featured.append(e)
        else:
            rest.append(e)
    featured.sort(key=lambda e: featured_titles.index(e['title']))

    years = sorted({e['years'] for e in rest}, reverse=True)
    timeline = [(y, [e for e in rest if e['years'] == y]) for y in years]

    pro_certs = [c for c in certificates if 'Professional Certificate' in c['name']]

    return {
        'experiences': experiences,
        'featured': featured,
        'timeline': timeline,
        'certificates': certificates,
        'pro_certs': pro_certs,
        'friends': friends,
        'support': support,
        'blogs': blogs,
    }


# --- 桌機版 artboard ----------------------------------------------------

SEC_TOP = 96
SEC_BOTTOM = 96
D_RIGHT = D_PAD + D_COL


def sec_anchors(y):
    """回傳 (英文標籤基線, 內容起點)；中文大標由 section_head 依標籤位置排版。"""
    return y + SEC_TOP, y + SEC_TOP + 84


def nav(y):
    out = [
        rect(D_PAD, y + 26, 36, 36, fill='url(#logoGrad)', rx=11),
        text(D_PAD + 18, y + 51, 'J', size=19, weight=800, fill=C['bg'], anchor='middle'),
        text(D_PAD + 50, y + 51, 'Jiang', size=20, weight=700, fill=C['text']),
    ]
    btn, bw = button(D_RIGHT - 112, y + 22, '聯絡我', w=112, h=44, size=15)
    out.append(btn)

    links = ['About', 'Experience', 'Certificates', 'Writing', 'Community']
    gap = 30
    widths = [text_width(t, 15) for t in links]
    total = sum(widths) + gap * (len(links) - 1)
    lx = D_RIGHT - 112 - 44 - total
    for t, w in zip(links, widths):
        out.append(text(lx, y + 50, t, size=15, fill=C['muted']))
        lx += w + gap
    # 目前所在頁籤的底線
    out.append(line(D_RIGHT - 112 - 44 - total, y + 58,
                    D_RIGHT - 112 - 44 - total + widths[0], y + 58, C['primary'], 2))
    out.append(line(0, y + 88, D_W, y + 88, C['line'], 1))
    return '\n'.join(out), 88


def hero(y):
    h = 620
    out = [rect(0, y, D_W, h, fill=C['bg'])]
    out.append('<ellipse cx="1105" cy="%s" rx="470" ry="400" fill="url(#heroGlow)"/>'
               % fmt(y + 290))
    for i in range(15):
        gx = D_PAD + i * 80
        out.append(line(gx, y, gx, y + h, C['line'], 1, opacity=0.35))
    out.append(line(0, y + h, D_W, y + h, C['line'], 1))

    # 眉標
    eb = '國立台中科技大學 · 資訊工程科'
    ew = 18 + 8 + 10 + text_width(eb, 13) + 18
    out.append(rect(D_PAD, y + 92, ew, 32, fill=C['surface'], rx=16, stroke=C['line']))
    out.append(circle(D_PAD + 18, y + 108, 3.5, fill=C['primary']))
    out.append(text(D_PAD + 36, y + 113, eb, size=13, fill=C['muted']))

    out.append(text(D_PAD, y + 186, "Hi, I'm", size=40, weight=600, fill='#c8d0dc'))
    out.append(text(D_PAD, y + 272, 'Longtai.', size=76, weight=800, fill='url(#titleGrad)'))
    out.append(text(D_PAD, y + 322, '學生 / 討厭開發的開發者', size=21, fill=C['muted']))

    para = ('平常寫一點 HTML、CSS 與 Python，把時間花在社群、活動與開源上，'
            '也在跑步、單車與各種競賽之間找平衡。')
    out.append(paragraph(D_PAD, y + 372, wrap(para, 520, 16), size=16,
                         line_height=1.75, fill=C['dim']))

    b1, w1 = button(D_PAD, y + 436, '認識我 →', h=52)
    b2, _ = button(D_PAD + w1 + 16, y + 436, 'GitHub', h=52, primary=False)
    out += [b1, b2]

    social, _ = chip_row(D_PAD, y + 518,
                         ['GitHub', 'Telegram', 'Instagram', 'Notion', 'Calendar', 'Gravatar'],
                         gap=8, size=12.5, h=30, pad=13, fg=C['dim'], mono=True)
    out.append(social)

    # 右側：頭像 + 軌道（呼應衛星軌道設計競賽）
    cx, cy = 1105, y + 292
    for rx_, ry_, rot, op in ((196, 74, -18, 0.55), (238, 98, 17, 0.4), (168, 62, 64, 0.3)):
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" '
                   'stroke-width="1" opacity="%s" transform="rotate(%s %s %s)"/>'
                   % (fmt(cx), fmt(cy), rx_, ry_, C['line2'], op, rot, fmt(cx), fmt(cy)))
    out.append(circle(cx + 186, cy - 60, 5, fill=C['primary']))
    out.append(circle(cx - 226, cy + 68, 3.5, fill=C['cyan'], opacity=0.7))
    out.append(avatar(cx, cy, 110))

    tag, tw = chip(0, 0, '資工科科學會 · 資訊部長', size=13, h=34, pad=18,
                   fg=C['text'], bg=C['surface'], stroke=C['line2'])
    out.append('<g transform="translate(%s,%s)">%s</g>'
               % (fmt(cx - tw / 2), fmt(cy + 152), tag))
    return '\n'.join(out), h


def stats(y, d):
    h = 148
    items = [
        (str(len(d['experiences'])), '活動與競賽經歷'),
        (str(len(d['certificates'])), '專業與課程證書'),
        (str(len(d['pro_certs'])), 'Google 專業證書'),
        ('21K', '最長完賽距離'),
    ]
    out = [rect(0, y, D_W, h, fill=C['bg2'])]
    out.append(line(0, y + h, D_W, y + h, C['line'], 1))
    cw = D_COL / len(items)
    for i, (value, label) in enumerate(items):
        cx = D_PAD + cw * i + cw / 2
        out.append(text(cx, y + 72, value, size=38, weight=800, fill=C['text'], anchor='middle'))
        out.append(text(cx, y + 104, label, size=13, fill=C['dim'], anchor='middle'))
        if i:
            out.append(line(D_PAD + cw * i, y + 38, D_PAD + cw * i, y + h - 38, C['line'], 1))
    return '\n'.join(out), h


def about(y):
    lb, top = sec_anchors(y)
    head = section_head(D_PAD, lb, '01', 'ABOUT', '關於我')
    out = [head]

    card_h = 316
    out.append(rect(D_PAD, top, D_COL, card_h, fill=C['surface'], rx=20, stroke=C['line']))
    out.append(line(D_PAD + 700, top + 40, D_PAD + 700, top + card_h - 40, C['line'], 1))

    px, py = D_PAD + 44, top + 44
    p1 = ('我是 LongTai Jiang（龍泰），就讀國立台中科技大學資訊工程科，'
          '目前在資工科科學會擔任資訊部長。')
    p2 = ('活躍於 SCAICT、SITCON、COSCUP、HITCON 等台灣資訊社群，'
          '喜歡把學到的東西寫下來、做成專案，然後拿去現場跟人聊。')
    lines1 = wrap(p1, 588, 17)
    lines2 = wrap(p2, 588, 17)
    out.append(paragraph(px, py + 18, lines1, size=17, line_height=1.85, fill=C['text']))
    y2 = py + 18 + len(lines1) * 17 * 1.85 + 12
    out.append(paragraph(px, y2, lines2, size=17, line_height=1.85, fill=C['muted']))
    chips_y = y2 + len(lines2) * 17 * 1.85 + 16
    row1, _ = chip_row(px, chips_y, ['HTML', 'CSS', 'Python'], size=12.5, h=30, mono=True)
    row2, _ = chip_row(px, chips_y + 38, ['Open Source', 'Web Development', 'Community'],
                       size=12.5, h=30, mono=True)
    out += [row1, row2]

    facts = [
        ('SCHOOL', '國立台中科技大學 資訊工程科'),
        ('ROLE', '資工科科學會 資訊部長'),
        ('COMMUNITY', 'SCAICT / SITCON / COSCUP'),
        ('CONTACT', 'me@longtai.me'),
    ]
    fx, fy = D_PAD + 744, top + 48
    for i, (k, v) in enumerate(facts):
        ry = fy + i * 58
        out.append(text(fx, ry + 12, k, size=10.5, fill=C['primary'], mono=True,
                        weight=700, spacing=1.4))
        out.append(text(fx, ry + 36, v, size=14, fill=C['text']))
        if i < len(facts) - 1:
            out.append(line(fx, ry + 52, D_PAD + D_COL - 44, ry + 52, C['line'], 1))
    return '\n'.join(out), (top + card_h + SEC_BOTTOM) - y


def experience(y, d):
    lb, top = sec_anchors(y)
    head = section_head(D_PAD, lb, '02', 'EXPERIENCE', '經驗與活動',
                           meta='%d items · 2021–2026' % len(d['experiences']),
                           meta_x=D_RIGHT)
    out = [head]

    # 2026 精選卡
    gap, n = 24, 3
    cw = (D_COL - gap * (n - 1)) / n
    ch = 214
    for i, e in enumerate(d['featured'][:n]):
        cx = D_PAD + (cw + gap) * i
        out.append(rect(cx, top, cw, ch, fill=C['surface'], rx=18, stroke=C['line']))
        out.append(rect(cx + 26, top, 56, 3, fill=C['primary'], rx=1.5))
        out.append(text(cx + 26, top + 44, e['years'], size=12, fill=C['primary'],
                        mono=True, weight=700, spacing=1.2))
        for j, ln in enumerate(wrap(e['title'], cw - 52, 20, max_lines=2)):
            out.append(text(cx + 26, top + 78 + j * 27, ln, size=20, weight=700, fill=C['text']))
        for j, ln in enumerate(wrap(e['subtitle'], cw - 52, 13.5, max_lines=2)):
            out.append(text(cx + 26, top + 126 + j * 22, ln, size=13.5, fill=C['dim']))
        role, _ = chip(cx + 26, top + ch - 50, e['role'], size=12, h=26,
                       fg=C['cyan'], bg='rgba(0,168,240,0.10)', stroke=C['primary'])
        out.append(role)

    # 年表
    tl_top = top + ch + 56
    rail_x = D_PAD + 96
    row_x = rail_x + 36
    cur = tl_top
    rows = []
    for year, items in d['timeline']:
        rows.append(('year', year, cur))
        cur += 46
        for e in items:
            rows.append(('row', e, cur))
            cur += 56
        cur += 12
    tl_bottom = cur - 12

    out.append(line(rail_x, tl_top + 8, rail_x, tl_bottom - 8, C['line'], 1))
    for kind, payload, ry in rows:
        if kind == 'year':
            out.append(text(D_PAD, ry + 28, payload, size=15, weight=700,
                            fill=C['primary'], mono=True))
            out.append(line(row_x, ry + 22, D_RIGHT, ry + 22, C['line'], 1, opacity=0.6))
            continue
        e = payload
        mid = ry + 28
        out.append(circle(rail_x, mid, 4.5, fill=C['bg'], stroke=C['line2'], sw=1.5))
        title = wrap(e['title'], 300, 16, max_lines=1)[0]
        out.append(text(row_x, mid + 6, title, size=16, weight=600, fill=C['text']))
        sub = wrap(e['subtitle'], 400, 13.5, max_lines=1)[0]
        out.append(text(row_x + 320, mid + 5, sub, size=13.5, fill=C['dim']))
        out.append(text(D_RIGHT, mid + 5, e['role'], size=12.5, fill=C['muted'], anchor='end'))
        out.append(line(row_x, ry + 56, D_RIGHT, ry + 56, C['line'], 1, opacity=0.45))
    return '\n'.join(out), (tl_bottom + SEC_BOTTOM) - y


def certificates(y, d):
    lb, top = sec_anchors(y)
    others = len(d['certificates']) - len(d['pro_certs'])
    head = section_head(D_PAD, lb, '03', 'CERTIFICATES', '證書',
                           meta='%d 張 · Google via Coursera' % len(d['certificates']),
                           meta_x=D_RIGHT)
    out = [head]

    gap = 24
    cw = (D_COL - gap) / 2
    ch = 138
    for i, c in enumerate(d['pro_certs'][:4]):
        cx = D_PAD + (cw + gap) * (i % 2)
        cy = top + (ch + gap) * (i // 2)
        out.append(rect(cx, cy, cw, ch, fill=C['surface'], rx=16, stroke=C['line']))
        out.append(rect(cx + 26, cy + 26, 34, 34, fill='rgba(0,168,240,0.12)', rx=10))
        out.append(text(cx + 43, cy + 49, '✓', size=17, fill=C['primary'], anchor='middle'))
        for j, ln in enumerate(wrap(c['name'], cw - 240, 16.5, max_lines=2)):
            out.append(text(cx + 76, cy + 42 + j * 24, ln, size=16.5, weight=600, fill=C['text']))
        out.append(text(cx + 76, cy + ch - 30, c['organization'], size=13, fill=C['dim']))
        out.append(text(cx + cw - 26, cy + 40, c['date'], size=12, fill=C['dim'],
                        mono=True, anchor='end'))
        out.append(text(cx + cw - 26, cy + ch - 30, 'Verify ↗', size=13,
                        fill=C['primary'], anchor='end'))

    bar_y = top + (ch + gap) * 2
    out.append(rect(D_PAD, bar_y, D_COL, 62, fill=C['bg2'], rx=14, stroke=C['line']))
    out.append(text(D_PAD + 26, bar_y + 38, '另有 %d 張課程證書' % others,
                    size=15, fill=C['muted']))
    out.append(text(D_RIGHT - 26, bar_y + 38, '查看全部 →', size=14,
                    fill=C['primary'], anchor='end'))
    return '\n'.join(out), (bar_y + 62 + SEC_BOTTOM) - y


def clean_md(s):
    """去掉摘要裡的 Markdown 記號。"""
    for token in ('**', '__', '`', '#', '[', ']'):
        s = s.replace(token, '')
    return ' '.join(s.split())


def writing(y, d):
    lb, top = sec_anchors(y)
    head = section_head(D_PAD, lb, '04', 'WRITING', '部落格',
                           meta='所有文章 →', meta_x=D_RIGHT)
    out = [head]

    gap = 24
    cw = (D_COL - gap) / 2
    posts = []
    for b in d['blogs'][:2]:
        posts.append((wrap(b['title'], cw - 60, 19, max_lines=2),
                      wrap(clean_md(b['index_content']), cw - 60, 13.5, max_lines=3)))

    # 兩張卡等高：以最長的標題與摘要決定版面
    title_rows = max(len(t) for t, _ in posts)
    excerpt_rows = max(len(e) for _, e in posts)
    excerpt_top = 82 + (title_rows - 1) * 30 + 38
    link_y = excerpt_top + (excerpt_rows - 1) * 23 + 44
    ch = link_y + 26

    for i, (title_lines, excerpt_lines) in enumerate(posts):
        cx = D_PAD + (cw + gap) * i
        out.append(rect(cx, top, cw, ch, fill=C['surface'], rx=18, stroke=C['line']))
        out.append(rect(cx + 30, top, 56, 3, fill=C['primary'], rx=1.5))
        out.append(text(cx + 30, top + 44, 'POST', size=11, fill=C['primary'],
                        mono=True, weight=700, spacing=1.6))
        for j, ln in enumerate(title_lines):
            out.append(text(cx + 30, top + 82 + j * 30, ln, size=19, weight=700, fill=C['text']))
        for j, ln in enumerate(excerpt_lines):
            out.append(text(cx + 30, top + excerpt_top + j * 23, ln, size=13.5, fill=C['dim']))
        out.append(text(cx + 30, top + link_y, '閱讀全文 →', size=13.5, fill=C['primary']))
    return '\n'.join(out), (top + ch + SEC_BOTTOM) - y


def community(y, d):
    lb, top = sec_anchors(y)
    head = section_head(D_PAD, lb, '05', 'COMMUNITY', '愛與支援',
                           meta='%d 筆支援紀錄' % len(d['support']), meta_x=D_RIGHT)
    out = [head]

    gap, n = 20, 4
    cw = (D_COL - gap * (n - 1)) / n
    ch = 164
    for i, s in enumerate(d['support'][:n]):
        cx = D_PAD + (cw + gap) * i
        out.append(rect(cx, top, cw, ch, fill=C['surface'], rx=16, stroke=C['line']))
        out.append(text(cx + 24, top + 48, s['title'], size=19, weight=800, fill=C['primary']))
        for j, ln in enumerate(wrap(s['subtitle'], cw - 48, 13.5, max_lines=2)):
            out.append(text(cx + 24, top + 78 + j * 22, ln, size=13.5, fill=C['muted']))
        out.append(line(cx + 24, top + ch - 56, cx + cw - 24, top + ch - 56, C['line'], 1))
        out.append(text(cx + 24, top + ch - 26, s['desc'], size=13, fill=C['dim']))
    return '\n'.join(out), (top + ch + SEC_BOTTOM) - y


def friends(y, d):
    lb, top = sec_anchors(y)
    items = d['friends']
    head = section_head(D_PAD, lb, '06', 'FRIENDS', '大電神們',
                           meta='%d 位' % len(items), meta_x=D_RIGHT)
    out = [head]

    pitch = D_COL / len(items)
    for i, f in enumerate(items):
        cx = D_PAD + pitch * i + pitch / 2
        out.append(circle(cx, top + 36, 32, fill='url(#friendGrad)', stroke=C['line2'], sw=1))
        out.append(text(cx, top + 45, f['name'][0], size=22, weight=700,
                        fill=C['muted'], anchor='middle'))
        name = wrap(f['name'], pitch - 12, 12.5, max_lines=1)[0]
        out.append(text(cx, top + 94, name, size=12.5, fill=C['dim'], anchor='middle'))
    return '\n'.join(out), (top + 110 + SEC_BOTTOM) - y


def contact(y):
    top = y + 24
    h = 250
    out = [rect(D_PAD, top, D_COL, h, fill=C['bg2'], rx=24)]
    out.append(rect(D_PAD, top, D_COL, h, fill='url(#ctaGrad)', rx=24))
    out.append(rect(D_PAD, top, D_COL, h, fill='none', rx=24, stroke=C['primary'],
                    sw=1, opacity=0.35))
    cx = D_W / 2
    out.append(text(cx, top + 52, 'GET IN TOUCH', size=11.5, fill=C['primary'],
                    mono=True, weight=700, anchor='middle', spacing=2))
    out.append(text(cx, top + 106, '要不要聊聊？', size=38, weight=800,
                    fill=C['text'], anchor='middle'))
    out.append(text(cx, top + 142, 'me@longtai.me', size=19, fill=C['cyan'],
                    mono=True, anchor='middle'))

    labels = ['寄信給我', 'Telegram', 'GitHub']
    widths = [text_width(t, 15) + 52 for t in labels]
    total = sum(widths) + 14 * (len(labels) - 1)
    bx = cx - total / 2
    for i, (t, w) in enumerate(zip(labels, widths)):
        b, _ = button(bx, top + 172, t, w=w, h=48, primary=(i == 0), size=15)
        out.append(b)
        bx += w + 14
    return '\n'.join(out), (top + h + SEC_BOTTOM) - y


def footer(y):
    h = 176
    out = [line(0, y, D_W, y, C['line'], 1)]
    out.append(rect(0, y, D_W, h, fill=C['bg2']))
    out.append(line(0, y, D_W, y, C['line'], 1))
    out.append(rect(D_PAD, y + 44, 32, 32, fill='url(#logoGrad)', rx=10))
    out.append(text(D_PAD + 16, y + 67, 'J', size=17, weight=800,
                    fill=C['bg'], anchor='middle'))
    out.append(text(D_PAD + 44, y + 60, 'Jiang', size=17, weight=700, fill=C['text']))
    out.append(text(D_PAD + 44, y + 80, 'longtai.org', size=12.5, fill=C['dim'], mono=True))

    links = ['About', 'Experience', 'Certificates', 'Writing', 'Community', 'Blog']
    widths = [text_width(t, 13.5) for t in links]
    total = sum(widths) + 26 * (len(links) - 1)
    lx = D_RIGHT - total
    for t, w in zip(links, widths):
        out.append(text(lx, y + 60, t, size=13.5, fill=C['muted']))
        lx += w + 26
    out.append(text(D_RIGHT, y + 82, 'Source on GitHub ↗', size=12.5,
                    fill=C['dim'], anchor='end', mono=True))
    out.append(line(D_PAD, y + 116, D_RIGHT, y + 116, C['line'], 1))
    out.append(text(D_PAD, y + 146, '© 2026 LongTai Jiang', size=12.5, fill=C['dim']))
    out.append(text(D_RIGHT, y + 146, 'Designed in SVG · 深色藍延續版', size=12.5,
                    fill=C['dim'], anchor='end'))
    return '\n'.join(out), h


def build_desktop(d):
    body, y = [], 0
    for builder in (
        lambda yy: nav(yy),
        lambda yy: hero(yy),
        lambda yy: stats(yy, d),
        lambda yy: about(yy),
        lambda yy: experience(yy, d),
        lambda yy: certificates(yy, d),
        lambda yy: writing(yy, d),
        lambda yy: community(yy, d),
        lambda yy: friends(yy, d),
        lambda yy: contact(yy),
        lambda yy: footer(yy),
    ):
        svg, height = builder(y)
        body.append(svg)
        y += height
    return rect(0, 0, D_W, y, fill=C['bg']) + '\n' + '\n'.join(body), y


# --- 手機版 artboard ----------------------------------------------------

M_COL = M_W - M_PAD * 2


def build_mobile(d):
    out, y = [], 0

    # 導覽列
    out.append(rect(M_PAD, 22, 28, 28, fill='url(#logoGrad)', rx=9))
    out.append(text(M_PAD + 14, 41, 'J', size=15, weight=800, fill=C['bg'], anchor='middle'))
    out.append(text(M_PAD + 36, 41, 'Jiang', size=16, weight=700, fill=C['text']))
    for i in range(3):
        out.append(line(M_W - M_PAD - 20, 29 + i * 7, M_W - M_PAD, 29 + i * 7, C['muted'], 2))
    out.append(line(0, 72, M_W, 72, C['line'], 1))
    y = 72

    # Hero
    hero_h = 486
    out.append('<ellipse cx="195" cy="%s" rx="230" ry="220" fill="url(#heroGlow)"/>'
               % fmt(y + 120))
    cx = M_W / 2
    out.append(avatar(cx, y + 108, 54))
    eb = '中科大 · 資訊工程科'
    ew = text_width(eb, 12) + 34
    out.append(rect(cx - ew / 2, y + 190, ew, 28, fill=C['surface'], rx=14, stroke=C['line']))
    out.append(circle(cx - ew / 2 + 15, y + 204, 3, fill=C['primary']))
    out.append(text(cx + 8, y + 208, eb, size=12, fill=C['muted'], anchor='middle'))
    out.append(text(cx, y + 252, "Hi, I'm", size=22, weight=600, fill='#c8d0dc', anchor='middle'))
    out.append(text(cx, y + 302, 'Longtai.', size=44, weight=800,
                    fill='url(#titleGrad)', anchor='middle'))
    out.append(text(cx, y + 332, '學生 / 討厭開發的開發者', size=14,
                    fill=C['muted'], anchor='middle'))
    for i, ln in enumerate(['寫一點 HTML、CSS 與 Python，', '時間都花在社群、活動與開源上。']):
        out.append(text(cx, y + 364 + i * 22, ln, size=13, fill=C['dim'], anchor='middle'))
    bw = (M_COL - 12) / 2
    b1, _ = button(M_PAD, y + 412, '認識我 →', w=bw, h=46, size=14)
    b2, _ = button(M_PAD + bw + 12, y + 412, 'GitHub', w=bw, h=46, primary=False, size=14)
    out += [b1, b2]
    y += hero_h
    out.append(line(0, y, M_W, y, C['line'], 1))

    # 數據
    cells = [
        (str(len(d['experiences'])), '活動經歷'),
        (str(len(d['certificates'])), '證書'),
        (str(len(d['pro_certs'])), '專業證書'),
        ('21K', '最長完賽'),
    ]
    out.append(rect(0, y, M_W, 188, fill=C['bg2']))
    for i, (v, label) in enumerate(cells):
        col, row = i % 2, i // 2
        ccx = M_PAD + M_COL / 2 * col + M_COL / 4
        ccy = y + 94 * row
        out.append(text(ccx, ccy + 56, v, size=30, weight=800, fill=C['text'], anchor='middle'))
        out.append(text(ccx, ccy + 78, label, size=12, fill=C['dim'], anchor='middle'))
    out.append(line(M_PAD + M_COL / 2, y + 26, M_PAD + M_COL / 2, y + 162, C['line'], 1))
    out.append(line(M_PAD, y + 94, M_W - M_PAD, y + 94, C['line'], 1))
    y += 188
    out.append(line(0, y, M_W, y, C['line'], 1))

    # 關於我
    out.append(text(M_PAD, y + 54, '01 — ABOUT', size=11, fill=C['primary'],
                    mono=True, weight=700, spacing=1.4))
    out.append(text(M_PAD, y + 88, '關於我', size=25, weight=700, fill=C['text']))
    card_top = y + 112
    lines = wrap('就讀國立台中科技大學資訊工程科，目前在資工科科學會擔任資訊部長。'
                 '活躍於 SCAICT、SITCON、COSCUP 等台灣資訊社群。', M_COL - 44, 14)
    card_h = 44 + len(lines) * 25 + 16 + 30 + 28
    out.append(rect(M_PAD, card_top, M_COL, card_h, fill=C['surface'], rx=16, stroke=C['line']))
    out.append(paragraph(M_PAD + 22, card_top + 42, lines, size=14,
                         line_height=1.78, fill=C['muted']))
    row, _ = chip_row(M_PAD + 22, card_top + 42 + len(lines) * 25 + 4,
                      ['HTML', 'CSS', 'Python'], size=11.5, h=27, pad=11, mono=True)
    out.append(row)
    y = card_top + card_h + 56

    # 經驗（精選 + 年表片段）
    out.append(text(M_PAD, y + 8, '02 — EXPERIENCE', size=11, fill=C['primary'],
                    mono=True, weight=700, spacing=1.4))
    out.append(text(M_PAD, y + 42, '經驗與活動', size=25, weight=700, fill=C['text']))
    fc_top = y + 66
    e = d['featured'][0]
    fc_h = 168
    out.append(rect(M_PAD, fc_top, M_COL, fc_h, fill=C['surface'], rx=16, stroke=C['line']))
    out.append(rect(M_PAD + 22, fc_top, 52, 3, fill=C['primary'], rx=1.5))
    out.append(text(M_PAD + 22, fc_top + 40, e['years'], size=11.5, fill=C['primary'],
                    mono=True, weight=700, spacing=1.2))
    for j, ln in enumerate(wrap(e['title'], M_COL - 44, 19, max_lines=2)):
        out.append(text(M_PAD + 22, fc_top + 72 + j * 25, ln, size=19,
                        weight=700, fill=C['text']))
    for j, ln in enumerate(wrap(e['subtitle'], M_COL - 44, 13, max_lines=2)):
        out.append(text(M_PAD + 22, fc_top + 106 + j * 20, ln, size=13, fill=C['dim']))
    role, _ = chip(M_PAD + 22, fc_top + fc_h - 46, e['role'], size=11.5, h=26,
                   fg=C['cyan'], bg='rgba(0,168,240,0.10)', stroke=C['primary'])
    out.append(role)

    ty = fc_top + fc_h + 28
    out.append(text(M_PAD, ty + 14, '2026', size=13, weight=700, fill=C['primary'], mono=True))
    ty += 30
    for e in d['timeline'][0][1][:3]:
        out.append(line(M_PAD, ty, M_W - M_PAD, ty, C['line'], 1, opacity=0.6))
        out.append(text(M_PAD, ty + 30, wrap(e['title'], 180, 15, max_lines=1)[0],
                        size=15, weight=600, fill=C['text']))
        out.append(text(M_W - M_PAD, ty + 30, e['role'], size=12,
                        fill=C['dim'], anchor='end'))
        out.append(text(M_PAD, ty + 50, wrap(e['subtitle'], 300, 12.5, max_lines=1)[0],
                        size=12.5, fill=C['dim']))
        ty += 66
    out.append(line(M_PAD, ty, M_W - M_PAD, ty, C['line'], 1, opacity=0.6))
    out.append(text(M_PAD, ty + 34, '查看全部 %d 筆 →' % len(d['experiences']),
                    size=13.5, fill=C['primary']))
    y = ty + 76

    # 頁尾
    out.append(rect(0, y, M_W, 128, fill=C['bg2']))
    out.append(line(0, y, M_W, y, C['line'], 1))
    out.append(text(cx, y + 44, 'me@longtai.me', size=15, fill=C['cyan'],
                    mono=True, anchor='middle'))
    srow, sw_ = chip_row(0, y + 62, ['GitHub', 'Telegram', 'Instagram'],
                         gap=8, size=11.5, h=27, pad=12, fg=C['dim'], mono=True)
    out.append('<g transform="translate(%s,0)">%s</g>' % (fmt(cx - sw_ / 2), srow))
    out.append(text(cx, y + 112, '© 2026 LongTai Jiang', size=11.5,
                    fill=C['dim'], anchor='middle'))
    y += 128

    return rect(0, 0, M_W, y, fill=C['bg']) + '\n' + '\n'.join(out), y


# --- Design token 面板 --------------------------------------------------

def build_tokens():
    pad = 28
    col = T_W - pad * 2
    out, y = [], 0

    out.append(text(pad, 46, 'DESIGN TOKENS', size=12, fill=C['primary'],
                    mono=True, weight=700, spacing=2))
    out.append(text(pad, 78, '延續現有深色藍識別', size=22, weight=700, fill=C['text']))
    out.append(line(pad, 104, T_W - pad, 104, C['line'], 1))
    y = 132

    swatches = [
        ('primary', C['primary']), ('cyan', C['cyan']),
        ('text', C['text']), ('muted', C['muted']),
        ('bg', C['bg']), ('bg-2', C['bg2']),
        ('surface', C['surface']), ('line', C['line']),
    ]
    out.append(text(pad, y, 'COLOR', size=10.5, fill=C['dim'], mono=True, spacing=1.6))
    y += 26
    pitch = col / 4
    for i, (name, hexv) in enumerate(swatches):
        sx = pad + pitch * (i % 4)
        sy = y + (i // 4) * 126
        out.append(rect(sx, sy, 64, 64, fill=hexv, rx=14, stroke=C['line2'], sw=1))
        out.append(text(sx, sy + 84, name, size=12, fill=C['text']))
        out.append(text(sx, sy + 100, hexv, size=11, fill=C['dim'], mono=True))
    y += 126 * 2 + 4

    out.append(line(pad, y, T_W - pad, y, C['line'], 1))
    y += 34
    out.append(text(pad, y, 'TYPE SCALE', size=10.5, fill=C['dim'], mono=True, spacing=1.6))
    y += 24
    scale = [
        ('Display', 76, 800, 'Longtai.'),
        ('H1', 40, 700, "Hi, I'm"),
        ('H2', 34, 700, '經驗與活動'),
        ('H3', 20, 700, '衛星軌道設計競賽'),
        ('Body', 17, 400, '就讀國立台中科技大學'),
        ('Small', 13.5, 400, '0 基礎能飛多遠'),
        ('Micro', 11.5, 700, '02 — EXPERIENCE'),
    ]
    for name, size, weight, sample in scale:
        y += size * 1.1
        out.append(text(pad, y, sample, size=size, weight=weight, fill=C['text']))
        out.append(text(T_W - pad, y, '%s / %gpx' % (name, size), size=11,
                        fill=C['dim'], mono=True, anchor='end'))
        y += 14
    y += 16

    out.append(line(pad, y, T_W - pad, y, C['line'], 1))
    y += 34
    out.append(text(pad, y, 'RADIUS & SPACING', size=10.5, fill=C['dim'],
                    mono=True, spacing=1.6))
    y += 20
    for i, r in enumerate((10, 16, 20, 24)):
        sx = pad + i * 96
        out.append(rect(sx, y, 68, 52, fill=C['surface'], rx=r, stroke=C['line']))
        out.append(text(sx + 34, y + 32, str(r), size=14, fill=C['muted'], anchor='middle'))
    y += 74
    out.append(text(pad, y, 'spacing  4 · 8 · 12 · 16 · 24 · 40 · 56 · 96', size=12.5,
                    fill=C['muted'], mono=True))
    y += 34

    out.append(line(pad, y, T_W - pad, y, C['line'], 1))
    y += 34
    out.append(text(pad, y, 'COMPONENTS', size=10.5, fill=C['dim'], mono=True, spacing=1.6))
    y += 20
    b1, w1 = button(pad, y, '主要按鈕', h=48, size=15)
    b2, w2 = button(pad + w1 + 14, y, '次要按鈕', h=48, primary=False, size=15)
    out += [b1, b2]
    y += 66
    row, _ = chip_row(pad, y, ['標籤', 'Python', '資訊部長'], size=12.5, h=30, mono=True)
    out.append(row)
    y += 48
    out.append(rect(pad, y, col, 92, fill=C['surface'], rx=16, stroke=C['line']))
    out.append(rect(pad + 22, y, 52, 3, fill=C['primary'], rx=1.5))
    out.append(text(pad + 22, y + 36, '卡片 Card', size=17, weight=700, fill=C['text']))
    out.append(text(pad + 22, y + 60, '底 surface · 框線 line · 頂端 3px 主色', size=12.5,
                    fill=C['dim']))
    y += 92 + pad

    return rect(0, 0, T_W, y, fill=C['bg'], rx=20, stroke=C['line']) + '\n' + \
        '\n'.join(out), y


# --- 組裝 ---------------------------------------------------------------

def build_defs(desktop_h, mobile_h):
    return '\n'.join([
        '<defs>',
        '<linearGradient id="logoGrad" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="%s"/>' % C['cyan'],
        '<stop offset="1" stop-color="%s"/>' % C['primary'],
        '</linearGradient>',
        '<linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0" stop-color="%s"/>' % C['primary'],
        '<stop offset="1" stop-color="%s"/>' % C['cyan'],
        '</linearGradient>',
        '<linearGradient id="avatarGrad" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="#31404f"/>',
        '<stop offset="1" stop-color="#1e2733"/>',
        '</linearGradient>',
        '<linearGradient id="friendGrad" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="#2b3542"/>',
        '<stop offset="1" stop-color="#212936"/>',
        '</linearGradient>',
        '<linearGradient id="ctaGrad" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="%s" stop-opacity="0.18"/>' % C['primary'],
        '<stop offset="0.55" stop-color="%s" stop-opacity="0.05"/>' % C['primary'],
        '<stop offset="1" stop-color="%s" stop-opacity="0.03"/>' % C['cyan'],
        '</linearGradient>',
        '<radialGradient id="heroGlow" cx="0.5" cy="0.5" r="0.5">',
        '<stop offset="0" stop-color="%s" stop-opacity="0.20"/>' % C['primary'],
        '<stop offset="0.55" stop-color="%s" stop-opacity="0.06"/>' % C['primary'],
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>' % C['primary'],
        '</radialGradient>',
        '<clipPath id="clipDesktop">%s</clipPath>'
        % rect(0, 0, D_W, desktop_h, rx=6),
        '<clipPath id="clipMobile">%s</clipPath>'
        % rect(0, 0, M_W, mobile_h, rx=24),
        '\n'.join(AVATAR_CLIPS),
        '</defs>',
    ])


def artboard_label(x, y, name, meta):
    return '\n'.join([
        text(x, y, name, size=12, fill=C['muted'], mono=True, weight=700, spacing=1.8),
        text(x + text_width(name, 12) + 16, y, meta, size=12, fill='#4d5766', mono=True),
    ])


def build():
    d = build_data()
    desktop, desktop_h = build_desktop(d)
    mobile, mobile_h = build_mobile(d)
    tokens, tokens_h = build_tokens()

    right_x = GUTTER + D_W + GUTTER
    top_y = GUTTER + 36
    tokens_y = top_y + mobile_h + GUTTER + 36
    content_h = max(desktop_h, mobile_h + GUTTER + 36 + tokens_h)
    canvas_w = right_x + T_W + GUTTER
    canvas_h = top_y + content_h + GUTTER

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img" '
        'aria-label="LongTai Jiang 個人網頁改版設計稿">'
        % (canvas_w, int(canvas_h), canvas_w, int(canvas_h)),
        '<title>LongTai Jiang — 個人網頁改版設計稿 2026</title>',
        '<desc>桌機版、手機版與設計 token 三個 artboard，延續 #1b212c / #00a8f0 深色藍識別。</desc>',
        build_defs(desktop_h, mobile_h),
        rect(0, 0, canvas_w, canvas_h, fill=C['canvas']),
        artboard_label(GUTTER, top_y - 16, 'DESKTOP',
                       '1440 × %d' % desktop_h),
        '<g transform="translate(%d,%d)" clip-path="url(#clipDesktop)">%s</g>'
        % (GUTTER, top_y, desktop),
        artboard_label(right_x, top_y - 16, 'MOBILE', '390 × %d' % mobile_h),
        '<g transform="translate(%d,%d)" clip-path="url(#clipMobile)">%s</g>'
        % (right_x, top_y, mobile),
        artboard_label(right_x, tokens_y - 16, 'TOKENS', 'design system'),
        '<g transform="translate(%d,%d)">%s</g>' % (right_x, tokens_y, tokens),
        '</svg>',
    ]
    return '\n'.join(parts)


def main():
    svg = build()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(svg)
        f.write('\n')
    print('Wrote %s (%.1f KB)' % (OUTPUT, len(svg.encode('utf-8')) / 1024))


if __name__ == '__main__':
    main()
