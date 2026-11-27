import json
import os
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import posters
from pixel import esc

OWNER = 'ph-1dnjs'
NAME = 'UNA'
TAGLINE = '생각을 현실로 만들고, 그 결과를 세상에 보여주는 것을 좋아합니다.'
FEATURED = ('checkly', 'doxen', 'auto-qa', 'interacta')
TICKER = '(HEAD -> main) feat: turn ideas into real things  ///  npm run create && npm run build && npm run improve  ///  git push origin future'
FOOTER = 'DESIGNED TO BUILD, LEARN & KEEP MOVING  ///  PROCESS EXITED WITH CODE 0  ///  SEE YOU IN THE NEXT COMMIT'
TOKEN = os.environ.get('GITHUB_TOKEN', '')
PRIVATE_TOKEN = os.environ.get('PROFILE_PRIVATE_TOKEN', '')
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'


def request(url, token=TOKEN, data=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-readme'}
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


def contribution_data():
    """Returns (yearly total or None, calendar weeks or None). Never fails the run."""
    query = '''query($login:String!){user(login:$login){contributionsCollection{
      totalCommitContributions totalIssueContributions totalPullRequestContributions totalPullRequestReviewContributions
      contributionCalendar{totalContributions weeks{contributionDays{date contributionLevel}}}}}}'''
    for token in (PRIVATE_TOKEN, TOKEN):
        if not token:
            continue
        try:
            data = request('https://api.github.com/graphql', token, {'query': query, 'variables': {'login': OWNER}})
            if data.get('errors'):
                continue
            c = data['data']['user']['contributionsCollection']
            calendar = c.pop('contributionCalendar')
            weeks = [w['contributionDays'] for w in calendar['weeks']]
            # With the private token we can count private work too; otherwise use the public calendar total.
            total = sum(c.values()) if token == PRIVATE_TOKEN else calendar['totalContributions']
            return total, weeks
        except Exception as error:  # noqa: BLE001 - metrics are optional
            print(f'contribution query failed: {error}', file=sys.stderr)
    return None, None


def write(name, content):
    (ASSETS / name).write_text(content, encoding='utf-8')


def render_static():
    """Assets that need no network: hero, inuna, footer."""
    ASSETS.mkdir(exist_ok=True)
    write('hero.svg', posters.hero(NAME, TAGLINE, TICKER))
    write('inuna-preview.svg', posters.inuna())
    write('footer.svg', posters.footer(FOOTER))


def readme(featured, public_count, activity_value):
    projects = '\n'.join(
        f'<a href="{esc(r["html_url"])}"><img src="assets/project-{i}.svg" alt="{esc(r["name"])}" width="32%" /></a>'
        for i, r in enumerate(featured, 1)) or '표시할 공개 프로젝트가 없습니다.'
    return f'''<div align="center">

<img src="assets/hero.svg" alt="Hi, I'm Una. {TAGLINE}" width="100%" />

<br /><br />

{projects}

<br /><br />

<details>
<summary><code>&gt; inuna</code> · 출시 심사 중 — 펼쳐서 미리보기</summary>
<br />
<img src="assets/inuna-preview.svg" alt="Inuna는 현재 출시 심사 중입니다. 프로젝트 소개와 서비스 화면을 준비하고 있습니다." width="100%" />
</details>

<br />

<img src="assets/languages.svg" alt="공개 원본 저장소의 언어별 코드 비율" width="100%" />

<br /><br />

<img src="assets/activity.svg" alt="공개 저장소 {public_count}개, 최근 1년간 활동 {activity_value}건" width="100%" />

<br /><br />

<img src="assets/footer.svg" alt="Designed to build, learn &amp; keep moving" width="100%" />

</div>
'''


def main():
    render_static()
    if '--static-only' in sys.argv:
        return
    repos = get_repositories()
    public = [r for r in repos if not r['private']]
    originals = [r for r in public if not r['fork'] and not r['archived']]
    by_name = {r['name']: r for r in originals}
    featured = [by_name[name] for name in FEATURED if name in by_name][:3]

    languages = Counter()
    for repo in originals:
        languages.update(request(repo['languages_url']))
    if not languages:
        raise RuntimeError('No language data available')
    write('languages.svg', posters.languages(languages))

    for index, repo in enumerate(featured, 1):
        write(f'project-{index}.svg', posters.project(repo, index, len(featured)))
    for index in range(len(featured) + 1, 4):
        (ASSETS / f'project-{index}.svg').unlink(missing_ok=True)

    total, weeks = contribution_data()
    activity_value = str(total) if total is not None else '—'
    write('activity.svg', posters.activity(len(public), activity_value, weeks))
    (ROOT / 'README.md').write_text(readme(featured, len(public), activity_value), encoding='utf-8')


if __name__ == '__main__':
    main()
