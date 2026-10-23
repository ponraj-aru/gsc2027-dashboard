import json
import pandas as pd
from collections import Counter, defaultdict
from prepare_advanced_dashboard_data import REGION_MAP

def prepare_data():
    # Load datasets
    with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    with open('word_clusters_data.json', 'r', encoding='utf-8') as f:
        word_clusters = json.load(f)

    tot_papers = len(dataset)

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

    country_data_list.sort(key=lambda x: x['total'], reverse=True)
    for i, item in enumerate(country_data_list, 1):
        item['rank'] = i

    print(f"Total countries compiled: {len(country_data_list)}")

    theme_meta = {
        1: {
            'title': 'Theme 1: Lessons from the SDGs for sustainable development beyond 2030',
            'short': 'Theme 1: SDGs Beyond 2030'
        },
        2: {
            'title': 'Theme 2: Building resilience through integrated sustainable transformation across natural and human systems',
            'short': 'Theme 2: Resilience Across Systems'
        },
        3: {
            'title': 'Theme 3: Navigating the climate change–development nexus for resilient, just and equitable transformations',
            'short': 'Theme 3: Climate Change–Development Nexus'
        },
        4: {
            'title': 'Theme 4: Health, well-being, and societal foundations as key drivers of sustainable development',
            'short': 'Theme 4: Health & Well-being'
        },
        5: {
            'title': 'Theme 5: Artificial Intelligence, big data, and digitalization as enablers for sustainable development',
            'short': 'Theme 5: AI, Big Data & Digitalization'
        }
    }

    themes_summary = []
    for tnum in [1, 2, 3, 4, 5]:
        t_papers = [d for d in dataset if d['theme_num'] == tnum]
        cnt = len(t_papers)
        oral_cnt = sum(1 for d in t_papers if d['format'] == 'Oral Presentation')
        poster_cnt = sum(1 for d in t_papers if d['format'] == 'Poster Presentation')
        special_cnt = cnt - oral_cnt - poster_cnt
        
        c_counts = Counter([d['primary_country'] for d in t_papers])
        top_c, top_c_cnt = c_counts.most_common(1)[0] if c_counts else ('None', 0)
        
        sub_counts = Counter([f"{d['topic_code']} {d['topic_title']}" for d in t_papers])
        top_sub, top_sub_cnt = sub_counts.most_common(1)[0] if sub_counts else ('None', 0)
        
        themes_summary.append({
            'num': tnum,
            'title': theme_meta[tnum]['title'],
            'short': theme_meta[tnum]['short'],
            'count': cnt,
            'pct': round(cnt / tot_papers * 100, 1) if tot_papers > 0 else 0,
            'oral': oral_cnt,
            'poster': poster_cnt,
            'special': special_cnt,
            'top_country': f"{top_c} ({top_c_cnt})",
            'top_subtopic': f"{top_sub} ({top_sub_cnt})"
        })

    reg_counts = Counter([REGION_MAP.get(d['primary_country'], 'Other') for d in dataset])
    regional_summary = []
    for r in ['Asia', 'Europe', 'Africa', 'Americas', 'Oceania', 'Europe/Asia', 'Other']:
        if reg_counts[r] > 0:
            regional_summary.append({
                'region': r,
                'count': reg_counts[r],
                'pct': round(reg_counts[r] / tot_papers * 100, 1) if tot_papers > 0 else 0
            })

    dashboard_data = {
        'countries': country_data_list,
        'themes': themes_summary,
        'regional': regional_summary,
        'word_clusters': word_clusters
    }

    with open('dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

    print("dashboard_data.json successfully prepared!")
    return dashboard_data

if __name__ == '__main__':
    prepare_data()
