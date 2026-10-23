import json
import pandas as pd
from collections import Counter, defaultdict

# Load datasets
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

# Aggregate by country
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

# Build clean list of country records
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

# Sort initially by total descending
country_data_list.sort(key=lambda x: x['total'], reverse=True)
for i, item in enumerate(country_data_list, 1):
    item['rank'] = i

print(f"Total countries compiled: {len(country_data_list)}")

# Thematic summary metrics
themes_summary = [
    {
        'num': 1,
        'title': 'Theme 1: Lessons from the SDGs for sustainable development beyond 2030',
        'short': 'Theme 1: SDGs Beyond 2030',
        'count': 60,
        'pct': 19.9,
        'oral': 46,
        'poster': 11,
        'special': 3,
        'top_country': 'Netherlands (9)',
        'top_subtopic': '1.1 National & Local SDG Implementation (25)'
    },
    {
        'num': 2,
        'title': 'Theme 2: Building resilience through integrated sustainable transformation across natural and human systems',
        'short': 'Theme 2: Resilience Across Systems',
        'count': 76,
        'pct': 25.2,
        'oral': 68,
        'poster': 3,
        'special': 5,
        'top_country': 'China (12)',
        'top_subtopic': '2.1 Food-Water-Energy Nexus (31)'
    },
    {
        'num': 3,
        'title': 'Theme 3: Navigating the climate change–development nexus for resilient, just and equitable transformations',
        'short': 'Theme 3: Climate Change–Development Nexus',
        'count': 75,
        'pct': 24.9,
        'oral': 57,
        'poster': 13,
        'special': 5,
        'top_country': 'India (9)',
        'top_subtopic': '3.2 Climate Adaptation Actions (23)'
    },
    {
        'num': 4,
        'title': 'Theme 4: Health, well-being, and societal foundations as key drivers of sustainable development',
        'short': 'Theme 4: Health & Well-being',
        'count': 45,
        'pct': 15.0,
        'oral': 39,
        'poster': 6,
        'special': 0,
        'top_country': 'India (6)',
        'top_subtopic': '4.4 Health Equity & Well-being (21)'
    },
    {
        'num': 5,
        'title': 'Theme 5: Artificial Intelligence, big data, and digitalization as enablers for sustainable development',
        'short': 'Theme 5: AI, Big Data & Digitalization',
        'count': 45,
        'pct': 15.0,
        'oral': 36,
        'poster': 7,
        'special': 2,
        'top_country': 'Netherlands (5)',
        'top_subtopic': '5.5 AI & Digitalization Beyond 2030 (21)'
    }
]

# Regional Summary
regional_summary = [
    {'region': 'Asia', 'count': 107, 'pct': 35.5},
    {'region': 'Europe', 'count': 88, 'pct': 29.2},
    {'region': 'Africa', 'count': 69, 'pct': 22.9},
    {'region': 'Americas', 'count': 33, 'pct': 11.0},
    {'region': 'Oceania', 'count': 4, 'pct': 1.3}
]

# Export JSON for template injection
dashboard_data = {
    'countries': country_data_list,
    'themes': themes_summary,
    'regional': regional_summary,
    'word_clusters': word_clusters
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

print("dashboard_data.json successfully prepared!")
