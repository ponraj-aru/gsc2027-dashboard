"""Single source of truth for all numbers shown in the PPTX report.
Everything is computed from parsed_dataset.json / advanced_dashboard_data.json /
word_clusters_data.json so the deck always matches the dashboard."""
import json
import re
from collections import Counter

from source_config import SOURCE_DOC

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    DS = json.load(f)
with open('advanced_dashboard_data.json', 'r', encoding='utf-8') as f:
    ADV = json.load(f)
with open('word_clusters_data.json', 'r', encoding='utf-8') as f:
    WC = json.load(f)

_m = re.search(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', SOURCE_DOC)
_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December']
UPDATED = f"{int(_m.group(3))} {_MONTHS[int(_m.group(2)) - 1]} {_m.group(1)}, {_m.group(4)}:{_m.group(5)}:{_m.group(6)}"

TOTAL = len(DS)
COUNTRY_SHORT = {'United Kingdom': 'UK', 'United States': 'USA', 'United States of America': 'USA'}


def _papers(t):
    return DS if t == 0 else [d for d in DS if str(d['theme_num']) == str(t)]


def _pct(n, d):
    return f"{(100 * n / d) if d else 0:.1f}%"


def n(t=0):
    return len(_papers(t))


def pct(t):
    return _pct(n(t), TOTAL)


def nations(t=0):
    return len({d['primary_country'] for d in _papers(t) if d.get('primary_country')})


def all_nations():
    s = set()
    for d in DS:
        c = d.get('countries')
        if isinstance(c, str):
            c = re.findall(r"'([^']+)'", c)
        s.update(c or [])
    return len(s)


def fmt(t, label):
    return sum(1 for d in _papers(t) if d.get('format') == label)


def fmt_pct(t, label):
    return _pct(fmt(t, label), n(t))


ORAL, POSTER, INNOV, PANEL = 'Oral Presentation', 'Poster Presentation', 'Innovative Session', 'Full Panel Session'


def format_line(t):
    parts = []
    for lab, word in [(ORAL, 'Oral'), (POSTER, 'Posters'), (PANEL, 'Panels'), (INNOV, 'Innovative Sessions')]:
        c = fmt(t, lab)
        if c:
            parts.append(f"{c} {word}")
    return ', '.join(parts)


def top_countries(t=0, k=5, region=None):
    cnt = Counter(d['primary_country'] for d in _papers(t) if d.get('primary_country'))
    if region:
        allowed = {c['country'] for c in ADV['countries'] if c.get('region') == region}
        cnt = Counter({c: v for c, v in cnt.items() if c in allowed})
    return ', '.join(f"{COUNTRY_SHORT.get(c, c)} ({v})" for c, v in cnt.most_common(k))


def country_count(name):
    return sum(1 for d in DS if d.get('primary_country') == name)


def region(name):
    for r in ADV['theme_details']['0']['regions']:
        if r['region'] == name:
            return r['count'], f"{r['pct']}%"
    return 0, '0.0%'


def sub(code):
    """(count, pct-within-theme) for a subtopic code such as '2.1'."""
    t = code.split('.')[0]
    c = sum(1 for d in _papers(t) if str(d.get('topic_code')) == code)
    return c, _pct(c, n(t))


def top_sub(t):
    cnt = Counter(str(d.get('topic_code')) for d in _papers(t))
    return cnt.most_common(1)[0]


def theme_rank(t):
    order = sorted(range(1, 6), key=lambda x: -n(x))
    return order.index(t) + 1


def largest_theme():
    return max(range(1, 6), key=n)


def words(t, k=10):
    tw = WC[str(t)]['top_words'][:k]
    return ', '.join(f"{w['word']} ({w['count']})" for w in tw)


def keywords(t, k=6):
    cnt = Counter()
    for d in _papers(t):
        for kw in re.split(r'[;,]', d.get('keywords') or ''):
            kw = kw.strip().lower()
            if kw:
                cnt[kw] += 1
    return ', '.join(f"{w} ({c})" for w, c in cnt.most_common(k))


ORDINAL = {1: 'largest', 2: '2nd largest', 3: '3rd largest', 4: '4th largest', 5: 'smallest'}
