import json
from collections import Counter, defaultdict

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

with open('word_clusters_data.json', 'r', encoding='utf-8') as f:
    word_clusters = json.load(f)

REGION_MAP = {
    'Netherlands': 'Europe', 'India': 'Asia', 'China': 'Asia', 'Germany': 'Europe',
    'Indonesia': 'Asia', 'Nepal': 'Asia', 'United Kingdom': 'Europe', 'Ghana': 'Africa',
    'South Africa': 'Africa', 'United States': 'Americas', 'Nigeria': 'Africa',
    'Bangladesh': 'Asia', 'Belgium': 'Europe', 'Pakistan': 'Asia', 'Morocco': 'Africa',
    'Thailand': 'Asia', 'Italy': 'Europe', 'Kenya': 'Africa', 'Malaysia': 'Asia',
    'Spain': 'Europe', 'Ecuador': 'Americas', 'Japan': 'Asia', 'Uganda': 'Africa',
    'Sri Lanka': 'Asia', 'Tanzania': 'Africa', 'Finland': 'Europe', 'Brazil': 'Americas',
    'Poland': 'Europe', 'Mozambique': 'Africa', 'New Zealand': 'Oceania', 'Malawi': 'Africa',
    'Ireland': 'Europe', 'Canada': 'Americas', 'Cameroon': 'Africa', 'Egypt': 'Africa',
    'Czech Republic': 'Europe', 'Lebanon': 'Asia', 'Mexico': 'Americas', 'Sweden': 'Europe',
    'France': 'Europe', 'Palestine': 'Asia', 'Philippines': 'Asia', 'DR Congo': 'Africa',
    'The Gambia': 'Africa', 'Colombia': 'Americas', 'Venezuela': 'Americas', 'Romania': 'Europe',
    'United Arab Emirates': 'Asia', 'Australia': 'Oceania', 'Yemen': 'Asia', 'Benin': 'Africa',
    'Zambia': 'Africa', 'Zimbabwe': 'Africa', 'Austria': 'Europe', 'Denmark': 'Europe',
    'Norway': 'Europe', 'Switzerland': 'Europe', 'Turkey': 'Europe/Asia', 'Portugal': 'Europe',
    'Greece': 'Europe', 'Hungary': 'Europe', 'Iran': 'Asia', 'Iraq': 'Asia', 'Jordan': 'Asia',
    'Vietnam': 'Asia', 'Ivory Coast': 'Africa'
}

# 1. Countries aggregation
country_stats = defaultdict(lambda: {
    'total': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0,
    'oral': 0, 'poster': 0, 'special': 0, 'titles': []
})

for d in dataset:
    c = d['primary_country']
    tnum = d['theme_num']
    fmt = d['format']
    
    country_stats[c]['total'] += 1
    if tnum in [1, 2, 3, 4, 5]:
        country_stats[c][f't{tnum}'] += 1
    if fmt == 'Oral Presentation':
        country_stats[c]['oral'] += 1
    elif fmt == 'Poster Presentation':
        country_stats[c]['poster'] += 1
    else:
        country_stats[c]['special'] += 1
    if len(country_stats[c]['titles']) < 5:
        country_stats[c]['titles'].append(d['title'])

country_data_list = []
for c, s in country_stats.items():
    country_data_list.append({
        'country': c,
        'region': REGION_MAP.get(c, 'Other'),
        'total': s['total'],
        't1': s['t1'],
        't2': s['t2'],
        't3': s['t3'],
        't4': s['t4'],
        't5': s['t5'],
        'oral': s['oral'],
        'poster': s['poster'],
        'special': s['special'],
        'titles': s['titles']
    })

country_data_list.sort(key=lambda x: x['total'], reverse=True)
for i, item in enumerate(country_data_list, 1):
    item['rank'] = i

# 2. Dynamic Charts Data per Theme (0 to 5)
theme_details = {}

for t in range(0, 6):
    papers = dataset if t == 0 else [d for d in dataset if d['theme_num'] == t]
    tot = len(papers)
    
    # Subtopics (if t == 0, show Themes 1 to 5; if t > 0, show subtopics under that theme)
    if t == 0:
        sub_list = [
            {'label': 'Theme 1: SDGs Post-2030', 'short': 'Theme 1', 'count': 60, 'pct': round(60/tot*100, 1)},
            {'label': 'Theme 2: Resilience Across Systems', 'short': 'Theme 2', 'count': 76, 'pct': round(76/tot*100, 1)},
            {'label': 'Theme 3: Climate Nexus', 'short': 'Theme 3', 'count': 75, 'pct': round(75/tot*100, 1)},
            {'label': 'Theme 4: Health & Well-being', 'short': 'Theme 4', 'count': 45, 'pct': round(45/tot*100, 1)},
            {'label': 'Theme 5: AI & Digitalization', 'short': 'Theme 5', 'count': 45, 'pct': round(45/tot*100, 1)}
        ]
        sub_title = "Overall Thematic Distribution (Themes 1 to 5)"
    else:
        # Get subtopics under this theme
        counts = Counter([f"{d['topic_code']}: {d['topic_title']}" for d in papers])
        # Sort by topic code ascending (e.g. 1.1, 1.2, 1.3...)
        sub_list = []
        for code_title, cnt in sorted(counts.items(), key=lambda x: x[0]):
            code = code_title.split(':')[0].strip()
            title = code_title.split(':')[1].strip()
            # Clean short title for outside pie label
            short_label = f"Topic {code}"
            sub_list.append({
                'label': f"{code} {title}",
                'short': short_label,
                'count': cnt,
                'pct': round(cnt / tot * 100, 1)
            })
        sub_title = f"Theme {t} Subtopics Distribution"

    # Formats Breakdown
    fmt_counts = Counter([d['format'] for d in papers])
    # Preferred order: Oral, Poster, Innovative, Full Panel
    ordered_fmts = ['Oral Presentation', 'Poster Presentation', 'Innovative Session', 'Full Panel Session']
    fmt_list = []
    for f in ordered_fmts:
        if fmt_counts[f] > 0:
            short_f = f.replace(' Presentation', '').replace(' Session', '')
            fmt_list.append({
                'label': f,
                'short': short_f,
                'count': fmt_counts[f],
                'pct': round(fmt_counts[f] / tot * 100, 1)
            })

    # Regions Breakdown
    reg_counts = Counter([REGION_MAP.get(d['primary_country'], 'Other') for d in papers])
    ordered_regs = ['Asia', 'Europe', 'Africa', 'Americas', 'Oceania']
    reg_list = []
    for r in ordered_regs:
        if reg_counts[r] > 0:
            reg_list.append({
                'region': r,
                'count': reg_counts[r],
                'pct': round(reg_counts[r] / tot * 100, 1)
            })

    theme_details[str(t)] = {
        'theme_num': t,
        'total_papers': tot,
        'subtopics_title': sub_title,
        'subtopics': sub_list,
        'formats': fmt_list,
        'regions': reg_list
    }

advanced_data = {
    'countries': country_data_list,
    'theme_details': theme_details,
    'word_clusters': word_clusters
}

with open('advanced_dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(advanced_data, f, ensure_ascii=False, indent=2)

print("advanced_dashboard_data.json successfully created!")
for t in range(0, 6):
    td = theme_details[str(t)]
    print(f"Theme {t}: {td['total_papers']} papers | Subtopics: {len(td['subtopics'])} | Formats: {[f['short']+': '+str(f['count']) for f in td['formats']]}")
