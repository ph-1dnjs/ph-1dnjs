"""Tiny bitmap-font + pixel-art engine that renders straight to SVG paths.

Everything is geometry, so the posters look identical on every OS and inside
GitHub's image proxy (no web fonts, no JavaScript).
"""
import html

GLYPHS = {
    'A': ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'B': ['####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.'],
    'C': ['.###.', '#...#', '#....', '#....', '#....', '#...#', '.###.'],
    'D': ['####.', '#...#', '#...#', '#...#', '#...#', '#...#', '####.'],
    'E': ['#####', '#....', '#....', '####.', '#....', '#....', '#####'],
    'F': ['#####', '#....', '#....', '####.', '#....', '#....', '#....'],
    'G': ['.###.', '#...#', '#....', '#.###', '#...#', '#...#', '.####'],
    'H': ['#...#', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'I': ['###', '.#.', '.#.', '.#.', '.#.', '.#.', '###'],
    'J': ['..###', '...#.', '...#.', '...#.', '#..#.', '#..#.', '.##..'],
    'K': ['#...#', '#..#.', '#.#..', '##...', '#.#..', '#..#.', '#...#'],
    'L': ['#....', '#....', '#....', '#....', '#....', '#....', '#####'],
    'M': ['#...#', '##.##', '#.#.#', '#.#.#', '#...#', '#...#', '#...#'],
    'N': ['#...#', '#...#', '##..#', '#.#.#', '#..##', '#...#', '#...#'],
    'O': ['.###.', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'P': ['####.', '#...#', '#...#', '####.', '#....', '#....', '#....'],
    'Q': ['.###.', '#...#', '#...#', '#...#', '#.#.#', '#..#.', '.##.#'],
    'R': ['####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#'],
    'S': ['.####', '#....', '#....', '.###.', '....#', '....#', '####.'],
    'T': ['#####', '..#..', '..#..', '..#..', '..#..', '..#..', '..#..'],
    'U': ['#...#', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'V': ['#...#', '#...#', '#...#', '#...#', '#...#', '.#.#.', '..#..'],
    'W': ['#...#', '#...#', '#...#', '#.#.#', '#.#.#', '#.#.#', '.#.#.'],
    'X': ['#...#', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '#...#'],
    'Y': ['#...#', '#...#', '.#.#.', '..#..', '..#..', '..#..', '..#..'],
    'Z': ['#####', '....#', '...#.', '..#..', '.#...', '#....', '#####'],
    '0': ['.###.', '#...#', '#..##', '#.#.#', '##..#', '#...#', '.###.'],
    '1': ['.#.', '##.', '.#.', '.#.', '.#.', '.#.', '###'],
    '2': ['.###.', '#...#', '....#', '...#.', '..#..', '.#...', '#####'],
    '3': ['####.', '....#', '....#', '.###.', '....#', '....#', '####.'],
    '4': ['...#.', '..##.', '.#.#.', '#..#.', '#####', '...#.', '...#.'],
    '5': ['#####', '#....', '####.', '....#', '....#', '#...#', '.###.'],
    '6': ['.###.', '#....', '#....', '####.', '#...#', '#...#', '.###.'],
    '7': ['#####', '....#', '...#.', '..#..', '.#...', '.#...', '.#...'],
    '8': ['.###.', '#...#', '#...#', '.###.', '#...#', '#...#', '.###.'],
    '9': ['.###.', '#...#', '#...#', '.####', '....#', '....#', '.###.'],
    ' ': ['...', '...', '...', '...', '...', '...', '...'],
    '.': ['..', '..', '..', '..', '..', '##', '##'],
    ',': ['..', '..', '..', '..', '..', '.#', '#.'],
    '!': ['#', '#', '#', '#', '#', '.', '#'],
    '?': ['.###.', '#...#', '....#', '...#.', '..#..', '.....', '..#..'],
    "'": ['#', '#', '.', '.', '.', '.', '.'],
    ':': ['.', '#', '.', '.', '.', '#', '.'],
    '-': ['....', '....', '....', '####', '....', '....', '....'],
    '_': ['.....', '.....', '.....', '.....', '.....', '.....', '#####'],
    '+': ['.....', '..#..', '..#..', '#####', '..#..', '..#..', '.....'],
    '/': ['....#', '...#.', '...#.', '..#..', '.#...', '.#...', '#....'],
    '%': ['##..#', '##..#', '...#.', '..#..', '.#...', '#..##', '#..##'],
    '&': ['.##..', '#..#.', '#.#..', '.#...', '#.#.#', '#..#.', '.##.#'],
    '#': ['.#.#.', '#####', '.#.#.', '.#.#.', '.#.#.', '#####', '.#.#.'],
    '>': ['#....', '.#...', '..#..', '...#.', '..#..', '.#...', '#....'],
    '<': ['....#', '...#.', '..#..', '.#...', '..#..', '...#.', '....#'],
    '(': ['.#', '#.', '#.', '#.', '#.', '#.', '.#'],
    ')': ['#.', '.#', '.#', '.#', '.#', '.#', '#.'],
    '*': ['.....', '#.#.#', '.###.', '#####', '.###.', '#.#.#', '.....'],
    '@': ['.###.', '#...#', '#.###', '#.#.#', '#.###', '#....', '.####'],
}

ICONS = {
    'heart': ['.##...##.', '####.####', '#########', '#########', '.#######.', '..#####..', '...###...', '....#....'],
    'star': ['....#....', '....#....', '...###...', '..#####..', '#########', '..#####..', '...###...', '....#....', '....#....'],
    'x': ['##.....##', '###...###', '.###.###.', '..#####..', '...###...', '..#####..', '.###.###.', '###...###', '##.....##'],
    'smile': ['..#####..', '.#.....#.', '#..#.#..#', '#..#.#..#', '#.......#', '#.#...#.#', '#..###..#', '.#.....#.', '..#####..'],
}

INK = '#ececec'
DIM = '#5c5c5c'
BG = '#0c0c0c'
LINE = '#2b2b2b'
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono','Apple SD Gothic Neo','Malgun Gothic',monospace"


def esc(value):
    return html.escape(str(value), quote=True)


def n(value):
    """Compact number formatting for SVG attributes."""
    return f'{value:.2f}'.rstrip('0').rstrip('.') if isinstance(value, float) else str(value)


def text_bitmap(text):
    rows = [''] * 7
    for index, char in enumerate(text.upper()):
        glyph = GLYPHS.get(char, GLYPHS[' '])
        for r in range(7):
            rows[r] += glyph[r] + ('.' if index < len(text) - 1 else '')
    return rows


def bitmap_width(rows):
    return max((len(r) for r in rows), default=0)


def text_width(text, px):
    return bitmap_width(text_bitmap(text)) * px


def fill_path(rows, x, y, px):
    """Filled pixels, merged into horizontal runs to keep the path short."""
    parts = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == '#':
                start = c
                while c < len(row) and row[c] == '#':
                    c += 1
                parts.append(f'M{n(x + start * px)} {n(y + r * px)}h{n((c - start) * px)}v{n(px)}h{n(-(c - start) * px)}z')
            else:
                c += 1
    return ''.join(parts)


def outline_path(rows, x, y, px):
    """Only the outer contour of the pixel shapes: the hollow 'PIXEL PARTY' look."""
    h, w = len(rows), bitmap_width(rows)

    def on(r, c):
        return 0 <= r < h and 0 <= c < len(rows[r]) and rows[r][c] == '#'

    parts = []
    for r in range(h + 1):  # horizontal edges on boundary r
        c = 0
        while c < w:
            if on(r - 1, c) != on(r, c):
                start = c
                while c < w and on(r - 1, c) != on(r, c):
                    c += 1
                parts.append(f'M{n(x + start * px)} {n(y + r * px)}h{n((c - start) * px)}')
            else:
                c += 1
    for c in range(w + 1):  # vertical edges on boundary c
        r = 0
        while r < h:
            if on(r, c - 1) != on(r, c):
                start = r
                while r < h and on(r, c - 1) != on(r, c):
                    r += 1
                parts.append(f'M{n(x + c * px)} {n(y + start * px)}v{n((r - start) * px)}')
            else:
                r += 1
    return ''.join(parts)


def pixel_text(text, x, y, px, mode='fill', anchor='start', color=INK, extra=''):
    rows = text_bitmap(text)
    width = bitmap_width(rows) * px
    if anchor == 'middle':
        x -= width / 2
    elif anchor == 'end':
        x -= width
    if mode == 'outline':
        sw = max(1.0, px * 0.3)
        d = outline_path(rows, x, y, px)
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(sw)}" stroke-linecap="square"{extra}/>'
    return f'<path d="{fill_path(rows, x, y, px)}" fill="{color}"{extra}/>'


def icon(name, x, y, px, color=INK, extra=''):
    return f'<path d="{fill_path(ICONS[name], x, y, px)}" fill="{color}"{extra}/>'


def sparkle(cx, cy, r, color=INK, extra=''):
    k = r * 0.12
    d = (f'M{n(cx)} {n(cy - r)}C{n(cx + k)} {n(cy - k)} {n(cx + k)} {n(cy - k)} {n(cx + r)} {n(cy)}'
         f'C{n(cx + k)} {n(cy + k)} {n(cx + k)} {n(cy + k)} {n(cx)} {n(cy + r)}'
         f'C{n(cx - k)} {n(cy + k)} {n(cx - k)} {n(cy + k)} {n(cx - r)} {n(cy)}'
         f'C{n(cx - k)} {n(cy - k)} {n(cx - k)} {n(cy - k)} {n(cx)} {n(cy - r)}Z')
    return f'<path d="{d}" fill="{color}"{extra}/>'


def arrow(x1, y, x2, color=INK, sw=2, extra=''):
    head = 12 if x2 > x1 else -12
    return (f'<g{extra} fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="square">'
            f'<path d="M{n(x1)} {n(y)}H{n(x2)}M{n(x2 - head)} {n(y - abs(head))}L{n(x2)} {n(y)}L{n(x2 - head)} {n(y + abs(head))}"/></g>')


def visual_len(text):
    return sum(1.0 if ord(ch) > 0x2E7F else 0.6 for ch in text)


def wrap(text, max_em, max_lines):
    """Wrap by visual width (CJK glyphs are wider than latin in monospace)."""
    words, lines, cur = str(text).split(), [], ''
    for word in words:
        trial = f'{cur} {word}'.strip()
        if visual_len(trial) <= max_em:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        cur = word
        while visual_len(cur) > max_em:  # hard-break very long tokens
            cut = len(cur)
            while visual_len(cur[:cut]) > max_em:
                cut -= 1
            lines.append(cur[:cut])
            cur = cur[cut:]
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while visual_len(last + '…') > max_em and last:
            last = last[:-1]
        lines[-1] = last.rstrip() + '…'
    return lines


def mono_lines(lines, x, y, size, lh, color=INK, opacity=1, anchor='start', weight=400):
    out = []
    for i, line in enumerate(lines):
        out.append(f'<text x="{n(x)}" y="{n(y + i * lh)}" font-size="{size}" fill="{color}" fill-opacity="{opacity}" '
                   f'text-anchor="{anchor}" font-weight="{weight}" font-family="{MONO}">{esc(line)}</text>')
    return ''.join(out)


BASE_CSS = '''
.tw{transform-box:fill-box;transform-origin:center;animation:tw 2.8s ease-in-out infinite}
@keyframes tw{0%,100%{transform:scale(1) rotate(0)}50%{transform:scale(.35) rotate(90deg)}}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.nudge{animation:nudge 1.6s steps(4) infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
.scan{animation:scan 5.5s linear infinite}
@keyframes scan{from{transform:translateY(-60px)}to{transform:translateY(var(--h))}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
'''


def svg(width, height, label, body, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{esc(label)}"><style>{BASE_CSS}{css}</style>'
            f'<defs><pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="1.2" height="1.2" fill="{INK}" fill-opacity=".09"/></pattern></defs>'
            f'<rect width="{width}" height="{height}" rx="6" fill="{BG}"/>'
            f'<rect width="{width}" height="{height}" rx="6" fill="url(#dots)"/>'
            f'{body}'
            f'<rect x="10.5" y="10.5" width="{width - 21}" height="{height - 21}" fill="none" stroke="{INK}" stroke-opacity=".18"/>'
            f'<g class="scan" style="--h:{height + 60}px"><rect x="0" y="0" width="{width}" height="60" fill="{INK}" fill-opacity=".025"/>'
            f'<rect x="0" y="59" width="{width}" height="1" fill="{INK}" fill-opacity=".12"/></g>'
            f'</svg>')


def ticker(y, width, text, height=30, speed=18):
    """An endless marquee band. The text is repeated so the loop is seamless."""
    unit = f'{text}  ///  '
    unit_w = visual_len(unit) * 11
    reps = int(width / unit_w) + 2
    line = esc(unit * reps)
    return (f'<g><rect x="10" y="{y}" width="{width - 20}" height="{height}" fill="{INK}"/>'
            f'<clipPath id="tk{y}"><rect x="10" y="{y}" width="{width - 20}" height="{height}"/></clipPath>'
            f'<g clip-path="url(#tk{y})"><text x="10" y="{y + height / 2 + 4}" font-size="11" font-weight="700" textLength="{n(unit_w * reps)}" lengthAdjust="spacing" '
            f'fill="{BG}" font-family="{MONO}" style="animation:mq{y} {speed}s linear infinite">{line}</text></g>'
            f'<style>@keyframes mq{y}{{to{{transform:translateX(-{n(unit_w)}px)}}}}</style></g>')


def code(tokens, x, y, size=10, anchor='start'):
    """One line of 'syntax highlighted' monochrome code.

    tokens: list of (text, opacity) or (text, opacity, weight).
    """
    spans = []
    for token in tokens:
        text, opacity = token[0], token[1]
        weight = token[2] if len(token) > 2 else 400
        spans.append(f'<tspan fill-opacity="{opacity}" font-weight="{weight}">{esc(text)}</tspan>')
    return (f'<text x="{n(x)}" y="{n(y)}" font-size="{size}" fill="{INK}" text-anchor="{anchor}" '
            f'font-family="{MONO}" xml:space="preserve">{"".join(spans)}</text>')
