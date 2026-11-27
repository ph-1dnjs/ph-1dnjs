"""Poster builders. Each function returns a complete animated SVG string.

Visual language: monochrome Y2K techno posters, crossed with a developer's
workspace: terminal prompts, code comments, object literals and git logs.
"""
from datetime import datetime, timezone

from pixel import BG, INK, arrow, code, mono_lines, n, pixel_text, sparkle, svg, text_width, ticker, wrap

# Code token opacities: keyword / punctuation / value / comment
KW, PUN, VAL, COM = 1, .45, .85, .5


def header(width, left, right, y=34):
    return (mono_lines([left], 28, y, 9.5, 0, INK, .9, weight=700)
            + mono_lines([right], width - 28, y, 9.5, 0, INK, .55, 'end')
            + f'<rect x="28" y="{y + 9}" width="{width - 56}" height="1" fill="{INK}" fill-opacity=".25"/>')


def typed(x, y, prompt, command, size=10.5, delay=0, chars_per_sec=14):
    """A terminal line whose command types itself out, then a blinking caret."""
    cw = size * .6
    px_prompt = len(prompt) * cw
    width = len(command) * cw
    dur = max(.4, len(command) / chars_per_sec)
    cid = f'ty{int(x)}x{int(y)}'
    return (code([(prompt, COM)], x, y, size)
            + f'<clipPath id="{cid}"><rect class="type" style="--d:{dur:.2f}s;--n:{len(command)};animation-delay:{delay}s" '
              f'x="{n(x + px_prompt)}" y="{n(y - size)}" width="{n(width + 2)}" height="{n(size * 1.4)}"/></clipPath>'
            + f'<g clip-path="url(#{cid})">{code([(command, KW, 700)], x + px_prompt, y, size)}</g>'
            + f'<rect class="blink" x="{n(x + px_prompt + width + 3)}" y="{n(y - size + 1)}" width="{n(cw)}" height="{n(size)}" fill="{INK}"/>')


TYPE_CSS = '''
.type{transform-box:fill-box;transform-origin:left;animation:type var(--d) steps(var(--n)) both}
@keyframes type{from{transform:scaleX(0)}}
'''


# ───────────────────────────────────────────── HERO ──
def hero(name, tagline_ko, ticker_text):
    W, H = 800, 440
    X0 = 58  # content starts right of the line-number gutter
    body = [header(W, '✦ README.MD / VOL.' + datetime.now(timezone.utc).strftime('%y'), 'GITHUB.COM/PH-1DNJS', 34)]

    # Editor gutter with line numbers + a "current line" marker that hops down.
    for i in range(18):
        body.append(mono_lines([f'{i + 1:02d}'], 28, 70 + i * 16, 8.5, 0, INK, .28))
    body.append(f'<rect class="cur" x="44" y="61" width="2" height="12" fill="{INK}"/>')

    body.append(typed(X0, 70, '~/una $ ', 'whoami --verbose'))
    body.append(code([('/** ', COM), ('A frontend engineer who turns ideas into real things', COM)], X0, 90, 9.5))
    body.append(code([(' *  ', COM), ('and ships them to the world. create / build / improve.', COM), (' */', COM)], X0, 104, 9.5))
    body.append(code([('// ', COM), (tagline_ko, .9)], X0, 124, 11))

    # Title with a glitch layer that only fires for a split second each cycle.
    title = f"I'M {name}"
    body.append(pixel_text('HELLO,', X0, 146, 9, 'outline'))
    body.append(f'<g class="gl1" opacity=".55">{pixel_text(title, X0, 226, 12, "outline")}</g>')
    body.append(f'<g class="gl2">{pixel_text(title, X0, 226, 12)}</g>')
    body.append(f'<rect class="blink" x="{X0 + text_width(title, 12) + 14}" y="226" width="22" height="84" fill="{INK}"/>')

    body.append(code([('const ', KW, 700), ('una', VAL), (' = { ', PUN), ('role', VAL), (': ', PUN), ('"frontend"', KW),
                      (', ', PUN), ('loves', VAL), (': [', PUN), ('"interaction"', KW), (', ', PUN), ('"ux"', KW),
                      ('], ', PUN), ('status', VAL), (': ', PUN), ('"shipping"', KW), (' };', PUN)], X0, 336, 10))

    # Right: pixel X that ripples outward from a spinning diamond star.
    cx, cy, cell, size = 650, 198, 17, 11
    ox, oy = cx - size * cell / 2, cy - size * cell / 2
    for i in range(size):
        for j in {i, size - 1 - i}:
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
    body.append(pixel_text('</>', cx - 80, cy - 7, 2, anchor='middle'))
    for sx, sy, r, delay in ((530, 82, 9, 0), (764, 300, 7, .7), (480, 300, 6, 1.3), (754, 86, 5, 2.0)):
        body.append(f'<g class="tw" style="animation-delay:{delay}s">{sparkle(sx, sy, r)}</g>')
    body.append(arrow(570, 60, 760, extra=' class="nudge"'))

    # Status bar, like the bottom of an editor.
    body.append(code([('● ', KW), ('main', VAL, 700), ('   ✓ build passing   ', COM), ('UTF-8   TSX   LF', COM)], X0, 362, 9))
    fw = text_width('FRONTEND ENGINEER', 1.6)
    body.append(''.join(f'<rect x="{n(W - 28 - fw - 46 + i * 9)}" y="353" width="6" height="11.2" fill="{INK}"/>' for i in range(4)))
    body.append(pixel_text('FRONTEND ENGINEER', W - 28, 353, 1.6, anchor='end'))
    body.append(ticker(388, W, ticker_text))

    css = TYPE_CSS + '''
.gl1{animation:g1 4s steps(1) infinite}
@keyframes g1{0%,88%,100%{transform:translate(0,0);opacity:0}89%{transform:translate(-6px,2px);opacity:.6}92%{transform:translate(5px,-3px);opacity:.6}95%{transform:translate(-2px,0);opacity:.6}}
.gl2{animation:g2 4s steps(1) infinite}
@keyframes g2{0%,88%,100%{transform:none}90%{transform:translateX(4px)}93%{transform:translateX(-3px)}}
.rip{animation:rip 2.2s steps(2) infinite}
@keyframes rip{0%,100%{opacity:1}50%{opacity:.15}}
.orbit{animation:spin 3.2s linear infinite}
.cur{animation:cur 7.2s steps(1) infinite}
@keyframes cur{0%{transform:translateY(0)}12%{transform:translateY(16px)}24%{transform:translateY(32px)}36%{transform:translateY(48px)}50%{transform:translateY(80px)}70%{transform:translateY(160px)}86%{transform:translateY(272px)}}
'''
    return svg(W, H, f"Hi, I'm {name}. {tagline_ko}", ''.join(body), css)


# ───────────────────────────────────────── PROJECTS ──
def _motif_checker(x, y, w, h):
    cell = 20
    out = []
    for r in range(int(h // cell)):
        for c in range(int(w // cell)):
            if (r + c) % 2:
                continue
            out.append(f'<rect class="flip" style="animation-delay:{(c + r) * .09:.2f}s" x="{x + c * cell}" y="{y + r * cell}" '
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
    for ex in (x + w / 2 - 50, x + w / 2 + 50):
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
    body = [header(W, f'{name.upper()}/', f'{index:02d} / {total:02d}', 32)]
    desc = repo.get('description') or 'A new experiment in progress.'
    for i, line in enumerate(wrap(desc, 19, 3)):
        body.append(code([('// ' if i == 0 else '   ', COM), (line, .75)], 28, 62 + i * 13.5, 9.5))

    body.append(MOTIFS[(index - 1) % len(MOTIFS)](30, 112, 200, 150))

    px = min(5.5, 204 / max(text_width(name, 1), 1))
    body.append(pixel_text(name, 28, 280, px, 'outline'))
    ny = 280 + 7 * px + 22
    lang = repo.get('language') or 'Mixed'
    stars, forks = repo.get('stargazers_count', 0), repo.get('forks_count', 0)
    body.append(code([('{ ', PUN), ('lang', VAL), (': ', PUN), (f'"{lang}"', KW, 700), (',', PUN)], 28, ny, 9.5))
    body.append(code([('  stars', VAL), (': ', PUN), (str(stars), KW, 700), (', ', PUN), ('forks', VAL), (': ', PUN),
                      (str(forks), KW, 700), (',', PUN)], 28, ny + 14, 9.5))
    body.append(code([('  pushed', VAL), (': ', PUN), (f'"{pushed[:10].replace("-", ".")}"', KW, 700), (' }', PUN)], 28, ny + 28, 9.5))
    # Freshness meter: full when pushed today, empty after ~90 days.
    fresh = max(.04, 1 - min(age, 90) / 90)
    by = ny + 40
    body.append(f'<rect x="28" y="{n(by)}" width="{W - 56}" height="8" fill="none" stroke="{INK}" stroke-opacity=".45"/>')
    body.append(f'<rect class="fresh" x="30" y="{n(by + 2)}" width="{n((W - 60) * fresh)}" height="4" fill="{INK}"/>')
    body.append(f'<rect x="20" y="{H - 46}" width="{W - 40}" height="24" fill="{INK}"/>')
    body.append(mono_lines([f'$ cd {name}'], 28, H - 30, 9.5, 0, BG, 1, weight=700))
    body.append(f'<g class="go">{arrow(W - 70, H - 34, W - 34, BG, 2)}</g>')
    return svg(W, H, f'{name} — {desc}', ''.join(body), PROJECT_CSS)


# ─────────────────────────────────────────── INUNA ──
def inuna():
    W, H = 800, 250
    body = [header(W, '✦ COMING SOON / PRODUCT', 'HTTP 202 ACCEPTED', 34)]
    body.append(pixel_text('INUNA', 28, 72, 13, 'outline'))
    body.append(code([('// ', COM), ('현재 출시 심사 중입니다.', .85)], 28, 190, 11.5))
    body.append(code([('// ', COM), ('프로젝트 소개와 서비스 화면을 준비하고 있습니다.', .85)], 28, 208, 11.5))
    bx, by, blocks = 470, 92, 16
    body.append(typed(bx - 5, 72, '> ', 'await store.review("inuna")', 10, chars_per_sec=18))
    for i in range(blocks):
        body.append(f'<rect class="load" style="animation-delay:{i * .18:.2f}s" x="{bx + i * 16}" y="{by}" width="12" height="22" fill="{INK}"/>')
    body.append(f'<rect x="{bx - 5}" y="{by - 5}" width="{blocks * 16 + 6}" height="32" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    body.append(f'<circle class="blink" cx="{bx + 4}" cy="146" r="4" fill="{INK}"/>')
    body.append(code([('status', VAL), (': ', PUN), ('"in_review"', KW, 700)], bx + 16, 150, 9.5))
    body.append(code([('eta', VAL), (': ', PUN), ('"soon"', KW, 700), ('  // stay tuned', COM)], bx + 16, 165, 9.5))
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                body.append(f'<rect x="{676 + c * 24}" y="{176 + r * 18 - 6}" width="24" height="18" fill="{INK}" fill-opacity=".85"/>')
    css = TYPE_CSS + '''.load{animation:load 2.88s steps(1) infinite}
@keyframes load{0%{opacity:.08}6%,80%{opacity:1}81%,100%{opacity:.08}}'''
    return svg(W, H, 'Inuna — 현재 출시 심사 중입니다.', ''.join(body), css)


# ─────────────────────────────────────── LANGUAGES ──
EXT = {'TypeScript': '.ts', 'JavaScript': '.js', 'Python': '.py', 'CSS': '.css', 'SCSS': '.scss', 'HTML': '.html',
       'Java': '.java', 'C#': '.cs', 'Kotlin': '.kt', 'Swift': '.swift', 'Shell': '.sh', 'Dart': '.dart', 'Go': '.go',
       'Rust': '.rs', 'C': '.c', 'C++': '.cpp', 'Vue': '.vue', 'Svelte': '.svelte', 'MDX': '.mdx', 'Objective-C': '.m',
       'Ruby': '.rb', 'PHP': '.php', 'ShaderLab': '.shader', 'HLSL': '.hlsl'}


def languages(counter):
    items = counter.most_common()
    top = items[:6]
    if len(items) > 6:
        top[-1] = ('Others', sum(v for _, v in items[5:]))
    total = sum(counter.values()) or 1
    W = 800
    H = 120 + len(top) * 34
    body = [header(W, '✦ $ LINGUIST --BREAKDOWN', 'PUBLIC ORIGINAL REPOSITORIES · BY BYTES', 34)]
    body.append(pixel_text('STACK OVERVIEW', 28, 62, 2.4))
    body.append(code([('// ', COM), (f'{total / 1024:,.0f} KB of code, measured nightly', COM)], W - 28, 76, 9.5, 'end'))
    blocks, bx = 36, 228
    for row, (lang, amount) in enumerate(top):
        y = 104 + row * 34
        pct = amount / total * 100
        filled = max(1, round(pct / 100 * blocks))
        body.append(code([(EXT.get(lang, '.*').ljust(7), COM), (lang.upper(), KW, 700)], 28, y + 12, 11))
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
SHADES = (.22, .48, .74, 1)


def activity(public_count, contributions, weeks):
    W = 800
    H = 300 if weeks else 150
    body = [header(W, '✦ $ GIT LOG --SINCE=1.YEAR', 'LAST 365 DAYS', 34)]
    stats = ((f'{public_count}', 'repos.length', '포크 포함 공개 저장소'),
             (f'{contributions}', 'contributions.total', '커밋 · 이슈 · PR · 리뷰 합계'))
    for k, (value, key, ko) in enumerate(stats):
        x = 28 + k * 384
        shown = value.replace('—', '--')
        body.append(f'<g class="pop" style="animation-delay:{k * .25}s">{pixel_text(shown, x, 66, 9)}</g>')
        vx = x + text_width(shown, 9) + 18
        body.append(code([(key, KW, 700)], vx, 86, 10.5))
        body.append(code([('// ', COM), (ko, .6)], vx, 104, 10.5))
        body.append(f'<g class="tw" style="animation-delay:{k}s">{sparkle(vx + 6, 66, 5)}</g>')
    if weeks:
        cell, gap = 11, 3
        weeks = weeks[-53:]
        gx = (W - len(weeks) * (cell + gap) + gap) / 2
        gy = 172
        body.append(code([('contributions', VAL), ('.', PUN), ('heatmap', KW, 700), ('()', PUN)], 28, gy - 18, 9.5))
        lx = W - 28 - 5 * 14 - 30
        body.append(mono_lines(['less'], lx - 6, gy - 18, 9, 0, INK, .5, 'end'))
        for i in range(5):
            if i:
                body.append(f'<rect x="{lx + i * 14}" y="{gy - 27}" width="11" height="11" fill="{INK}" fill-opacity="{SHADES[i - 1]}"/>')
            else:
                body.append(f'<rect x="{lx + .5}" y="{gy - 26.5}" width="10" height="10" fill="none" stroke="{INK}" stroke-opacity=".3"/>')
        body.append(mono_lines(['more'], lx + 5 * 14 + 2, gy - 18, 9, 0, INK, .5))
        cells = []
        for wi, week in enumerate(weeks):
            for day in week:
                row = (datetime.fromisoformat(day['date']).weekday() + 1) % 7
                lv = LEVELS.get(day.get('contributionLevel'), 0)
                x, y = gx + wi * (cell + gap), gy + row * (cell + gap)
                if lv:
                    cells.append(f'<rect x="{n(x)}" y="{y}" width="{cell}" height="{cell}" fill="{INK}" fill-opacity="{SHADES[lv - 1]}"/>')
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


def footer(text):
    W, H = 800, 64
    return svg(W, H, text, ticker(17, W, text), '')
