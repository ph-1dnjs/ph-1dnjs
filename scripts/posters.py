"""Poster builders. Each function returns a complete animated SVG string."""
from datetime import datetime, timezone

from pixel import (BG, DIM, ICONS, INK, LINE, arrow, esc, icon, mono_lines, n, pixel_text, sparkle, svg,
                   text_width, ticker, wrap)

STAMPS = ('heart', 'star', 'x', 'smile')


def header(width, left, right, y=34):
    return (mono_lines([left], 28, y, 9.5, 0, INK, .9, weight=700)
            + mono_lines([right], width - 28, y, 9.5, 0, INK, .55, 'end')
            + f'<rect x="28" y="{y + 9}" width="{width - 56}" height="1" fill="{INK}" fill-opacity=".25"/>')


# ───────────────────────────────────────────── HERO ──
def hero(name, tagline_ko, ticker_text):
    W, H = 800, 440
    body = []
    body.append(header(W, '✦ PROFILE / VOL.' + datetime.now(timezone.utc).strftime('%y'),
                       'GITHUB.COM/PH-1DNJS', 34))
    body.append(mono_lines([
        'HELLO, WORLD. THIS IS UNA - A FRONTEND ENGINEER WHO',
        'TURNS IDEAS INTO REAL THINGS AND SHOWS THEM TO THE',
        'WORLD. DON\'T MISS OUT ON THE NEXT RELEASE.',
    ], 28, 68, 9, 13, INK, .62))
    body.append(mono_lines([tagline_ko], 28, 114, 11, 0, INK, .9))

    # Title with a glitch layer that only fires for a split second each cycle.
    t1 = pixel_text('HELLO,', 28, 146, 9, 'outline')
    t2 = pixel_text(f"I'M {name}", 28, 226, 12, 'fill')
    w2 = text_width(f"I'M {name}", 12)
    body.append(t1)
    body.append(f'<g class="gl1" opacity=".55">{pixel_text(f"I M {name}", 28, 226, 12, "outline")}</g>')
    body.append(f'<g class="gl2">{t2}</g>')
    body.append(f'<rect class="blink" x="{28 + w2 + 14}" y="226" width="22" height="84" fill="{INK}"/>')

    # Right: pixel X that ripples outward from a spinning diamond star.
    cx, cy, cell, size = 640, 198, 17, 11
    ox, oy = cx - size * cell / 2, cy - size * cell / 2
    for i in range(size):
        for j in (i, size - 1 - i):
            if i == size // 2 and j != i:
                continue
            d = abs(i - size // 2)
            if d < 2:
                continue
            body.append(f'<rect class="rip" style="animation-delay:{d * .12:.2f}s" x="{n(ox + j * cell + 2)}" '
                        f'y="{n(oy + i * cell + 2)}" width="{cell - 4}" height="{cell - 4}" fill="{INK}"/>')
    body.append(f'<rect x="{cx - 26}" y="{cy - 26}" width="52" height="52" fill="none" stroke="{INK}" stroke-width="1.5" '
                f'transform="rotate(45 {cx} {cy})"/>')
    body.append(f'<g class="spin">{sparkle(cx, cy, 24)}</g>')
    body.append(f'<ellipse cx="{cx + 80}" cy="{cy}" rx="24" ry="9" fill="none" stroke="{INK}" stroke-width="1.2" '
                f'transform="rotate(-24 {cx + 80} {cy})"/>')
    body.append(f'<g class="orbit" style="transform-origin:{cx + 80}px {cy}px"><circle cx="{cx + 104}" cy="{cy}" r="3.5" fill="{INK}"/></g>')
    body.append(f'<circle cx="{cx - 80}" cy="{cy}" r="10" fill="none" stroke="{INK}" stroke-width="1.5"/>')

    # Sparkles + arrow + smiley
    for sx, sy, r, delay in ((520, 82, 9, 0), (760, 300, 7, .7), (470, 300, 6, 1.3), (744, 86, 5, 2.0)):
        body.append(f'<g class="tw" style="animation-delay:{delay}s">{sparkle(sx, sy, r)}</g>')
    body.append(arrow(560, 60, 750, extra=' class="nudge"'))
    body.append(f'<g class="smile">{icon("smile", 28, 334, 3.4)}</g>')
    body.append(mono_lines(['BUILD · LEARN · KEEP MOVING', 'SEOUL, KR  —  OPEN TO NEW IDEAS'], 72, 344, 9.5, 14, INK, .7))
    fw = text_width('FUTURE FLASHBACK', 1.6)
    body.append(''.join(f'<rect x="{n(W - 28 - fw - 46 + i * 9)}" y="336" width="6" height="11.2" fill="{INK}"/>' for i in range(4)))
    body.append(pixel_text('FUTURE FLASHBACK', W - 28, 336, 1.6, anchor='end'))
    body.append(ticker(388, W, ticker_text))

    css = '''
.gl1{animation:g1 4s steps(1) infinite}
@keyframes g1{0%,88%,100%{transform:translate(0,0);opacity:0}89%{transform:translate(-6px,2px);opacity:.6}92%{transform:translate(5px,-3px);opacity:.6}95%{transform:translate(-2px,0);opacity:.6}}
.gl2{animation:g2 4s steps(1) infinite}
@keyframes g2{0%,88%,100%{transform:none}90%{transform:translateX(4px)}93%{transform:translateX(-3px)}}
.rip{animation:rip 2.2s steps(2) infinite}
@keyframes rip{0%,100%{opacity:1}50%{opacity:.15}}
.orbit{animation:spin 3.2s linear infinite}
.smile{animation:sm 3s steps(1) infinite}
@keyframes sm{0%,100%{transform:none}50%{transform:translateY(-3px)}}
'''
    return svg(W, H, f"Hi, I'm {name}. {tagline_ko}", ''.join(body), css)


# ───────────────────────────────────────── PROJECTS ──
def _motif_checker(x, y, w, h):
    cell = 20
    cols, rows = int(w // cell), int(h // cell)
    out = []
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2:
                continue
            delay = (c + r) * .09
            out.append(f'<rect class="flip" style="animation-delay:{delay:.2f}s" x="{x + c * cell}" y="{y + r * cell}" '
                       f'width="{cell}" height="{cell}" fill="{INK}"/>')
    out.append(f'<rect x="{x + w / 2 - 34}" y="{y + h / 2 - 34}" width="68" height="68" fill="{BG}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<g class="tw">{sparkle(x + w / 2, y + h / 2, 22)}</g>')
    return ''.join(out)


def _motif_cross(x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    out, cell, size = [], 14, 11
    ox, oy = cx - size * cell / 2, cy - size * cell / 2
    for i in range(size):
        for j in {i, size - 1 - i}:
            d = abs(i - size // 2)
            if d < 2:
                continue
            out.append(f'<rect class="rip" style="animation-delay:{d * .14:.2f}s" x="{n(ox + j * cell + 2)}" y="{n(oy + i * cell + 2)}" '
                       f'width="{cell - 4}" height="{cell - 4}" fill="{INK}"/>')
    for k in range(4):
        out.append(f'<path d="M{cx} {cy - 44}V{cy - 68}" stroke="{INK}" stroke-width="1.2" transform="rotate({k * 90 + 45} {cx} {cy})"/>')
    out.append(f'<rect x="{cx - 24}" y="{cy - 24}" width="48" height="48" fill="{BG}" stroke="{INK}" stroke-width="1.5" transform="rotate(45 {cx} {cy})"/>')
    out.append(f'<g class="spin">{sparkle(cx, cy, 20)}</g>')
    out.append(f'<circle cx="{x + w - 16}" cy="{y + 14}" r="9" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    return ''.join(out)


def _motif_eyes(x, y, w, h):
    cy = y + h / 2
    out = []
    for k, ex in enumerate((x + w / 2 - 50, x + w / 2 + 50)):
        out.append(f'<g class="lid" style="transform-origin:{n(ex)}px {n(cy)}px">'
                   f'<ellipse cx="{n(ex)}" cy="{n(cy)}" rx="44" ry="66" fill="{BG}" stroke="{INK}" stroke-width="2"/>'
                   f'<ellipse cx="{n(ex)}" cy="{n(cy)}" rx="30" ry="50" fill="none" stroke="{INK}" stroke-width="1" stroke-opacity=".5"/>'
                   f'<g class="look"><ellipse cx="{n(ex)}" cy="{n(cy)}" rx="15" ry="24" fill="{INK}"/>'
                   f'<rect x="{n(ex - 7)}" y="{n(cy - 14)}" width="6" height="6" fill="{BG}"/></g></g>')
    out.append(f'<g class="tw">{sparkle(x + 14, y + 16, 9)}</g>')
    out.append(f'<g class="tw" style="animation-delay:1.2s">{sparkle(x + w - 14, y + h - 14, 7)}</g>')
    return ''.join(out)


MOTIFS = (_motif_checker, _motif_cross, _motif_eyes)

PROJECT_CSS = '''
.flip{animation:flip 3s steps(1) infinite}
@keyframes flip{0%,49%,64%,100%{opacity:1}50%,63%{opacity:0}}
.rip{animation:rip 2.2s steps(2) infinite}
@keyframes rip{0%,100%{opacity:1}50%{opacity:.15}}
.look{animation:look 6s steps(1) infinite}
@keyframes look{0%,100%{transform:none}20%{transform:translate(12px,-6px)}45%{transform:translate(-12px,4px)}70%{transform:translate(0,16px)}}
.lid{animation:lid 6s ease-in-out infinite}
@keyframes lid{0%,46%,52%,100%{transform:scaleY(1)}49%{transform:scaleY(.06)}}
.go{animation:nudge 1.4s steps(3) infinite}
.fresh{transform-origin:left;animation:fresh 2.4s cubic-bezier(.2,.8,.2,1) both}
@keyframes fresh{from{transform:scaleX(0)}}
'''


def project(repo, index, total):
    W, H = 260, 460
    name = repo['name']
    pushed = repo.get('pushed_at') or ''
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(pushed.replace('Z', '+00:00'))).days
    except ValueError:
        age = 999
    body = [header(W, 'PROJECT ↗', f'{index:02d} / {total:02d}', 32)]
    desc = repo.get('description') or 'A NEW EXPERIMENT IN PROGRESS.'
    body.append(mono_lines(wrap(desc, 21, 3), 28, 62, 9.5, 13.5, INK, .7))

    body.append(MOTIFS[(index - 1) % len(MOTIFS)](30, 112, 200, 160))

    px = min(6.0, 204 / max(text_width(name, 1), 1))
    body.append(pixel_text(name, 28, 296, px, 'outline'))
    ny = 296 + 7 * px + 18
    lang = (repo.get('language') or 'MIXED').upper()
    body.append(f'<rect x="28" y="{n(ny - 10)}" width="{W - 56}" height="1" fill="{INK}" fill-opacity=".25"/>')
    body.append(mono_lines([f'LANG   {lang}', f'STAR   {repo.get("stargazers_count", 0):<4} FORK  {repo.get("forks_count", 0)}',
                            f'PUSH   {pushed[:10].replace("-", ".")}'], 28, ny + 6, 9.5, 14, INK, .8))
    # "freshness" meter: full when pushed today, empty after ~90 days.
    fresh = max(.04, 1 - min(age, 90) / 90)
    by = ny + 50
    body.append(f'<rect x="28" y="{n(by)}" width="{W - 56}" height="8" fill="none" stroke="{INK}" stroke-opacity=".45"/>')
    body.append(f'<rect class="fresh" x="30" y="{n(by + 2)}" width="{n((W - 60) * fresh)}" height="4" fill="{INK}"/>')
    body.append(f'<rect x="20" y="{H - 46}" width="{W - 40}" height="24" fill="{INK}"/>')
    body.append(mono_lines(['VIEW REPOSITORY'], 28, H - 30, 9.5, 0, BG, 1, weight=700))
    body.append(f'<g class="go">{arrow(W - 70, H - 34, W - 34, BG, 2)}</g>')
    return svg(W, H, f'{name} — {desc}', ''.join(body), PROJECT_CSS)


# ─────────────────────────────────────────── INUNA ──
def inuna():
    W, H = 800, 250
    body = [header(W, '✦ COMING SOON / PRODUCT', 'STATUS: IN REVIEW', 34)]
    body.append(pixel_text('INUNA', 28, 72, 13, 'outline'))
    body.append(mono_lines(['현재 출시 심사 중입니다.', '프로젝트 소개와 서비스 화면을 준비하고 있습니다.'], 28, 190, 11.5, 18, INK, .8))
    # looping pixel loading bar
    bx, by, blocks = 470, 92, 16
    for i in range(blocks):
        body.append(f'<rect class="load" style="animation-delay:{i * .18:.2f}s" x="{bx + i * 16}" y="{by}" width="12" height="22" fill="{INK}"/>')
    body.append(f'<rect x="{bx - 5}" y="{by - 5}" width="{blocks * 16 + 6}" height="32" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    body.append(f'<circle class="blink" cx="{bx + 4}" cy="146" r="4" fill="{INK}"/>')
    body.append(mono_lines(['REVIEW IN PROGRESS', 'LAUNCHING SOON — STAY TUNED'], bx + 16, 150, 9.5, 15, INK, .75))
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                body.append(f'<rect x="{676 + c * 24}" y="{170 + r * 18 - 6}" width="24" height="18" fill="{INK}" fill-opacity=".85"/>')
    css = '''.load{animation:load 2.88s steps(1) infinite}
@keyframes load{0%{opacity:.08}6%,80%{opacity:1}81%,100%{opacity:.08}}'''
    return svg(W, H, 'Inuna — 현재 출시 심사 중입니다.', ''.join(body), css)


# ─────────────────────────────────────── LANGUAGES ──
def languages(counter):
    items = counter.most_common()
    top = items[:6]
    if len(items) > 6:
        top[-1] = ('OTHERS', sum(v for _, v in items[5:]))
    total = sum(counter.values()) or 1
    W = 800
    H = 120 + len(top) * 34
    body = [header(W, '✦ SIGNAL / LANGUAGES', 'PUBLIC ORIGINAL REPOSITORIES · BY BYTES', 34)]
    body.append(pixel_text('DIGITAL DREAMSCAPE', 28, 62, 2.4))
    blocks, bx = 36, 228
    for row, (lang, amount) in enumerate(top):
        y = 104 + row * 34
        pct = amount / total * 100
        filled = max(1, round(pct / 100 * blocks))
        body.append(mono_lines([lang.upper()], 28, y + 12, 11, 0, INK, .9, weight=700))
        for b in range(blocks):
            x = bx + b * 13
            if b < filled:
                cls = 'bk last' if b == filled - 1 else 'bk'
                body.append(f'<rect class="{cls}" style="animation-delay:{row * .12 + b * .035:.2f}s" x="{x}" y="{y}" width="10" height="14" fill="{INK}"/>')
            else:
                body.append(f'<rect x="{x + .5}" y="{y + .5}" width="9" height="13" fill="none" stroke="{INK}" stroke-opacity=".18"/>')
        body.append(pixel_text(f'{pct:.1f}%', W - 28, y + 1, 1.8, anchor='end'))
    css = '''.bk{animation:bk .4s steps(1) both}
@keyframes bk{from{opacity:0}}
.last{animation:bk .4s steps(1) both,blink 1.1s steps(1) 2.5s infinite}'''
    label = ', '.join(f'{k} {v / total * 100:.1f}%' for k, v in top)
    return svg(W, H, f'언어별 코드 비율: {label}', ''.join(body), css)


# ──────────────────────────────────────── ACTIVITY ──
LEVELS = {'NONE': 0, 'FIRST_QUARTILE': 1, 'SECOND_QUARTILE': 2, 'THIRD_QUARTILE': 3, 'FOURTH_QUARTILE': 4}


def activity(public_count, contributions, weeks):
    W = 800
    H = 300 if weeks else 150
    body = [header(W, '✦ HOW I BUILD / LOG', 'LAST 365 DAYS', 34)]
    stats = ((f'{public_count}', 'PUBLIC REPOSITORIES', '포크 포함 공개 저장소'),
             (f'{contributions}', 'CONTRIBUTIONS / 1Y', '커밋 · 이슈 · PR · 리뷰 합계'))
    for k, (value, en, ko) in enumerate(stats):
        x = 28 + k * 384
        body.append(f'<g class="pop" style="animation-delay:{k * .25}s">{pixel_text(value.replace("—", "--"), x, 66, 9)}</g>')
        vx = x + text_width(value.replace('—', '--'), 9) + 18
        body.append(mono_lines([en], vx, 86, 10, 0, INK, .95, weight=700))
        body.append(mono_lines([ko], vx, 104, 10.5, 0, INK, .6))
        body.append(f'<g class="tw" style="animation-delay:{k}s">{sparkle(vx + 6, 76 - 10, 5)}</g>')
    if weeks:
        cell, gap = 11, 3
        weeks = weeks[-53:]
        gx = (W - len(weeks) * (cell + gap) + gap) / 2
        gy = 172
        body.append(mono_lines(['CONTRIBUTION CALENDAR'], 28, gy - 18, 9.5, 0, INK, .55))
        cells = []
        for wi, week in enumerate(weeks):
            for day in week:
                d = datetime.fromisoformat(day['date']).weekday()
                row = (d + 1) % 7
                lv = LEVELS.get(day.get('contributionLevel'), 0)
                x, y = gx + wi * (cell + gap), gy + row * (cell + gap)
                if lv:
                    cells.append(f'<rect x="{n(x)}" y="{y}" width="{cell}" height="{cell}" fill="{INK}" fill-opacity="{(.22, .48, .74, 1)[lv - 1]}"/>')
                else:
                    cells.append(f'<rect x="{n(x + .5)}" y="{y + .5}" width="{cell - 1}" height="{cell - 1}" fill="none" stroke="{INK}" stroke-opacity=".14"/>')
        body.append(''.join(cells))
        span = len(weeks) * (cell + gap)
        body.append(f'<rect class="sweep" style="--w:{n(span)}px" x="{n(gx - 4)}" y="{gy - 6}" width="{cell + 8}" height="{7 * (cell + gap) + 8}" '
                    f'fill="none" stroke="{INK}" stroke-width="1.5"/>')
    css = '''.pop{animation:pop .9s steps(5) both}
@keyframes pop{from{opacity:0;transform:translateY(8px)}}
.sweep{animation:sweep 9s steps(53) infinite}
@keyframes sweep{to{transform:translateX(var(--w))}}'''
    return svg(W, H, f'공개 저장소 {public_count}개, 최근 1년간 활동 {contributions}건', ''.join(body), css)


# ────────────────────────────────────────── STAMPS ──
def stamp_wall(data):
    W, H = 800, 300
    recent = data.get('recent', [])[-24:][::-1]
    counts = data.get('counts', {})
    total = sum(counts.values())
    body = [header(W, '✦ GUESTBOOK / INTERACTIVE', f'{total} SIGNALS RECEIVED', 34)]
    body.append(pixel_text('PIXEL PARTY', 28, 60, 5, 'outline'))
    body.append(mono_lines(['아래 버튼으로 스탬프를 남겨주세요 → 이슈 Submit 한 번이면', 'GitHub Actions가 이 벽을 실시간으로 다시 그립니다.'],
                           360, 72, 10.5, 16, INK, .7))
    tile, gap, cols = 52, 8, 12
    gx = (W - cols * (tile + gap) + gap) / 2
    for i in range(24):
        r, c = divmod(i, cols)
        x, y = gx + c * (tile + gap), 120 + r * (tile + gap)
        if i < len(recent):
            kind = recent[i]['stamp']
            cls = ' class="new"' if i == 0 else ''
            body.append(f'<g{cls}><rect x="{n(x)}" y="{y}" width="{tile}" height="{tile}" fill="{INK}" fill-opacity="{1 if i == 0 else .08}" stroke="{INK}" stroke-opacity=".35"/>'
                        f'{icon(kind, x + (tile - len(ICONS[kind][0]) * 4) / 2, y + (tile - len(ICONS[kind]) * 4) / 2, 4, BG if i == 0 else INK)}</g>')
        else:
            body.append(f'<rect x="{n(x + .5)}" y="{y + .5}" width="{tile - 1}" height="{tile - 1}" fill="none" stroke="{INK}" stroke-opacity=".15" stroke-dasharray="3 3"/>'
                        f'<path d="M{n(x + tile / 2 - 4)} {y + tile / 2}h8M{n(x + tile / 2)} {y + tile / 2 - 4}v8" stroke="{INK}" stroke-opacity=".25"/>')
    fy = 262
    for k, kind in enumerate(STAMPS):
        x = 28 + k * 120
        body.append(icon(kind, x, fy - 2, 2))
        body.append(pixel_text(str(counts.get(kind, 0)), x + 26, fy, 2.2))
    if recent:
        body.append(mono_lines([f'LAST SIGNAL FROM @{recent[0]["login"]}'], W - 28, fy + 12, 10, 0, INK, .85, 'end', 700))
    css = '''.new{animation:blink 1.1s steps(1) infinite}'''
    return svg(W, H, f'Pixel Party 방명록: 총 {total}개의 스탬프', ''.join(body), css)


def stamp_button(kind):
    W, H = 190, 74
    body = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="{INK}" stroke-width="2"/>',
            f'<g class="hop">{icon(kind, 22, 21, 3.4)}</g>',
            pixel_text(kind.upper(), 66, 24, 2.6),
            mono_lines(['CLICK TO STAMP ↗'], 66, 55, 9, 0, INK, .6)]
    css = '''.hop{animation:hop 1.2s steps(2) infinite}
@keyframes hop{50%{transform:translateY(-3px)}}'''
    return svg(W, H, f'{kind} 스탬프 남기기', ''.join(body), css).replace(
        f'<rect x="10.5" y="10.5" width="{W - 21}" height="{H - 21}" fill="none" stroke="{INK}" stroke-opacity=".18"/>', '')


def footer(text):
    W, H = 800, 64
    return svg(W, H, text, ticker(17, W, text), '')
