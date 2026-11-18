import html
import json
import os
import urllib.request
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

OWNER = 'ph-1dnjs'
TOKEN = os.environ.get('GITHUB_TOKEN', '')
PRIVATE_TOKEN = os.environ.get('PROFILE_PRIVATE_TOKEN', '')
ROOT = Path(__file__).resolve().parent.parent

def request(url, token=TOKEN, data=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Una-profile'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if data is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as response:
        return json.load(response)

def get_repositories():
    repos = []
    for page in range(1, 100):
        result = request(f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(result)
        if len(result) < 100:
            return repos
    raise RuntimeError('Repository pagination limit reached')

def contributions(token):
    query = '''query($login:String!) { user(login:$login) { contributionsCollection { totalCommitContributions totalIssueContributions totalPullRequestContributions totalPullRequestReviewContributions } } }'''
    data = request('https://api.github.com/graphql', token, {'query': query, 'variables': {'login': OWNER}})
    if data.get('errors'):
        raise RuntimeError('Contribution query failed')
    return sum(data['data']['user']['contributionsCollection'].values())

def escape(value):
    return html.escape(str(value), quote=True)

def make_chart(languages):
    colors = ['#353535', '#595959', '#777777', '#969696', '#b3b3b3', '#d0d0d0']
    items = languages.most_common()
    top = items[:5]
    if len(items) > 5:
        top.append(('기타', sum(n for _, n in items[5:])))
    total = sum(languages.values())
    if not total:
        raise RuntimeError('No language data available')
    bars = []
    labels = []
    x = 34.0
    for i, (name, amount) in enumerate(top):
        width = 732 * amount / total
        bars.append(f'<rect x="{x:.2f}" y="30" width="{width:.2f}" height="14" fill="{colors[i]}"/>')
        x += width
        col, row = i % 3, i // 3
        lx, ly = 34 + col * 244, 83 + row * 38
        labels.append(f'<circle cx="{lx+5}" cy="{ly-5}" r="5" fill="{colors[i]}"/><text x="{lx+18}" y="{ly}" font-size="15" fill="#555">{escape(name)}</text><text x="{lx+225}" y="{ly}" text-anchor="end" font-size="15" font-weight="600" fill="#333">{amount / total * 100:.1f}%</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="150" viewBox="0 0 800 150" role="img" aria-label="언어별 코드 비율"><rect x="1" y="1" width="798" height="148" rx="20" fill="#fafafa" stroke="#e5e5e5"/><defs><clipPath id="bar"><rect x="34" y="30" width="732" height="14" rx="7"/></clipPath></defs><g clip-path="url(#bar)">{''.join(bars)}</g><g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">{''.join(labels)}</g></svg>'''

def main():
    repos = get_repositories()
    public = [r for r in repos if not r['private']]
    originals = [r for r in public if not r['fork'] and not r['archived']]
    by_name = {r['name']: r for r in originals}
    featured = [by_name[n] for n in ('checkly', 'doxen', 'auto-qa', 'interacta') if n in by_name][:3]
    languages = Counter()
    for repo in originals:
        languages.update(request(repo['languages_url']))
    (ROOT / 'assets/languages.svg').write_text(make_chart(languages), encoding='utf-8')
    project_rows = []
    for r in featured:
        name = escape(r['name'])
        url = escape(r['html_url'])
        date = escape(r['pushed_at'][:10])
        project_rows.append(f'<td width="33%"><a href="{url}"><strong>{name} ↗</strong></a><br /><br /><sub>최근 코드 업데이트 {date}<br />★ {r["stargazers_count"]} · ⑂ {r["forks_count"]}</sub></td>')
    project_table = '<table><tr>' + ''.join(project_rows) + '</tr></table>' if project_rows else '표시할 공개 프로젝트가 없습니다.'
    activity = '—'
    if PRIVATE_TOKEN:
        activity = str(contributions(PRIVATE_TOKEN))
    readme = f'''<div align="center">

<img src="assets/hero.svg" alt="Hi, I'm Una. 생각을 현실로 만들고, 그 결과를 세상에 보여주는 것을 좋아합니다." width="100%" />

</div>

## Featured Projects

{project_table}

## Languages in My Repositories

제 저장소의 코드가 어떤 언어로 이루어져 있는지 보여드립니다.

<img src="assets/languages.svg" alt="공개 원본 저장소의 언어별 코드 비율" width="100%" />

## How I Build

활동을 바탕으로 한 작업 기록입니다.

<table><tr><td width="50%"><strong>{len(public)}</strong><br /><sub>포크를 포함한 공개 저장소입니다.</sub></td><td width="50%"><strong>{activity}</strong><br /><sub>올해 공개 및 비공개 커밋·이슈·PR·리뷰 활동 합계입니다.</sub></td></tr></table>

<div align="center"><sub>Designed to build, learn &amp; keep moving ✦</sub></div>
'''
    (ROOT / 'README.md').write_text(readme, encoding='utf-8')

if __name__ == '__main__':
    main()
