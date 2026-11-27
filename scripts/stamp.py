"""Handles a guestbook issue: validates it, records the stamp, redraws the wall.

Inputs come from environment variables (never interpolated into shell):
  STAMP_TITLE  issue title, expected `stamp:<kind>`
  STAMP_LOGIN  issue author login
Writes `result=accepted|rejected` and `kind=<kind>` to $GITHUB_OUTPUT.
"""
import json
import os
import re
from datetime import datetime, timezone

import posters
import update

MAX_RECENT = 48


def main():
    title = os.environ.get('STAMP_TITLE', '').strip().lower()
    login = os.environ.get('STAMP_LOGIN', '')
    match = re.fullmatch(r'stamp:\s*(heart|star|x|smile)', title)
    valid_login = re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})(?:\[bot\])?', login)
    result, kind = 'rejected', ''
    if match and valid_login and not login.endswith('[bot]'):
        kind = match.group(1)
        data = update.load_stamps()
        data.setdefault('counts', {})
        data['counts'][kind] = data['counts'].get(kind, 0) + 1
        data.setdefault('recent', []).append(
            {'stamp': kind, 'login': login, 'at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})
        data['recent'] = data['recent'][-MAX_RECENT:]
        update.STAMP_DATA.parent.mkdir(exist_ok=True)
        update.STAMP_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        update.write('stamps.svg', posters.stamp_wall(data))
        result = 'accepted'
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a', encoding='utf-8') as fh:
            fh.write(f'result={result}\nkind={kind}\n')
    print(result, kind)


if __name__ == '__main__':
    main()
