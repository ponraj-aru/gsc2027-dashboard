import json
from collections import Counter, defaultdict

REGION_MAP = {
    # Europe
    'Netherlands': 'Europe', 'Germany': 'Europe', 'United Kingdom': 'Europe',
    'Belgium': 'Europe', 'Italy': 'Europe', 'Spain': 'Europe', 'Finland': 'Europe',
    'Poland': 'Europe', 'Ireland': 'Europe', 'Czech Republic': 'Europe',
    'Sweden': 'Europe', 'France': 'Europe', 'Romania': 'Europe', 'Austria': 'Europe',
    'Denmark': 'Europe', 'Norway': 'Europe', 'Switzerland': 'Europe', 'Portugal': 'Europe',
    'Greece': 'Europe', 'Hungary': 'Europe', 'Moldova': 'Europe', 'Estonia': 'Europe',
    'Serbia': 'Europe', 'Cyprus': 'Europe', 'Albania': 'Europe', 'Bulgaria': 'Europe',
    'Croatia': 'Europe', 'Iceland': 'Europe', 'Latvia': 'Europe', 'Luxembourg': 'Europe',
    'Russia': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Ukraine': 'Europe',
    
    # Asia
    'India': 'Asia', 'China': 'Asia', 'Indonesia': 'Asia', 'Nepal': 'Asia',
    'Bangladesh': 'Asia', 'Pakistan': 'Asia', 'Thailand': 'Asia', 'Malaysia': 'Asia',
    'Japan': 'Asia', 'Sri Lanka': 'Asia', 'Lebanon': 'Asia', 'Palestine': 'Asia',
    'Philippines': 'Asia', 'United Arab Emirates': 'Asia', 'Yemen': 'Asia',
    'Iran': 'Asia', 'Iraq': 'Asia', 'Jordan': 'Asia', 'Vietnam': 'Asia',
    'Kuwait': 'Asia', 'Uzbekistan': 'Asia', 'Azerbaijan': 'Asia', 'Saudi Arabia': 'Asia',
    'Israel': 'Asia', 'Singapore': 'Asia', 'Georgia': 'Asia', 'Taiwan': 'Asia',
    'Oman': 'Asia', 'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Bhutan': 'Asia',
    'Cambodia': 'Asia', 'Kazakhstan': 'Asia', 'Kyrgyzstan': 'Asia', 'Maldives': 'Asia',
    'Mongolia': 'Asia', 'Myanmar': 'Asia', 'Qatar': 'Asia', 'South Korea': 'Asia',
    'Turkey': 'Europe/Asia',
    
    # Africa
    'Ghana': 'Africa', 'South Africa': 'Africa', 'Nigeria': 'Africa', 'Morocco': 'Africa',
    'Kenya': 'Africa', 'Uganda': 'Africa', 'Tanzania': 'Africa', 'Mozambique': 'Africa',
    'Malawi': 'Africa', 'Cameroon': 'Africa', 'Egypt': 'Africa', 'DR Congo': 'Africa',
    'The Gambia': 'Africa', 'Benin': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    'Ivory Coast': 'Africa', 'Burkina Faso': 'Africa', 'Sudan': 'Africa', 'Rwanda': 'Africa',
    'Ethiopia': 'Africa', 'Algeria': 'Africa', 'Botswana': 'Africa', 'Burundi': 'Africa',
    'Madagascar': 'Africa', 'Namibia': 'Africa', 'Senegal': 'Africa', 'Tunisia': 'Africa',
    
    # Americas
    'United States': 'Americas', 'Ecuador': 'Americas', 'Brazil': 'Americas',
    'Canada': 'Americas', 'Mexico': 'Americas', 'Colombia': 'Americas',
    'Venezuela': 'Americas', 'Costa Rica': 'Americas', 'Argentina': 'Americas',
    'Uruguay': 'Americas', 'Bolivia': 'Americas', 'Chile': 'Americas',
    'Guatemala': 'Americas', 'Peru': 'Americas',
    
    # Oceania
    'Australia': 'Oceania', 'New Zealand': 'Oceania', 'Fiji': 'Oceania'
}

def prepare_advanced_data():
    with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    with open('word_clusters_data.json', 'r', encoding='utf-8') as f:
        word_clusters = json.load(f)

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
    theme_meta_names = {
        1: ('Theme 1: SDGs Beyond 2030', 'Theme 1'),
        2: ('Theme 2: Resilience Across Systems', 'Theme 2'),
        3: ('Theme 3: Climate Nexus', 'Theme 3'),
        4: ('Theme 4: Health & Well-being', 'Theme 4'),
        5: ('Theme 5: AI & Digitalization', 'Theme 5')
    }

    theme_overall_counts = Counter([d['theme_num'] for d in dataset])

    for t in range(0, 6):
        papers = dataset if t == 0 else [d for d in dataset if d['theme_num'] == t]
        tot = len(papers)
        
        # Subtopics (if t == 0, show Themes 1 to 5; if t > 0, show subtopics under that theme)
        if t == 0:
            sub_list = []
            for tnum in [1, 2, 3, 4, 5]:
                cnt = theme_overall_counts[tnum]
                full_l, short_l = theme_meta_names[tnum]
                sub_list.append({
                    'label': full_l,
                    'short': short_l,
                    'count': cnt,
                    'pct': round(cnt / tot * 100, 1) if tot > 0 else 0
                })
            sub_title = "Overall Thematic Distribution (Themes 1 to 5)"
        else:
            # Get subtopics under this theme
            counts = Counter([f"{d['topic_code']}: {d['topic_title']}" for d in papers])
            # Sort by topic code ascending (e.g. 1.1, 1.2, 1.3...)
            sub_list = []
            for code_title, cnt in sorted(counts.items(), key=lambda x: x[0]):
                code = code_title.split(':')[0].strip()
                title = code_title.split(':')[1].strip()
                short_label = f"Topic {code}"
                sub_list.append({
                    'label': f"{code} {title}",
                    'short': short_label,
                    'count': cnt,
                    'pct': round(cnt / tot * 100, 1) if tot > 0 else 0
                })
            sub_title = f"Theme {t} Subtopics Distribution"

        # Formats Breakdown
        fmt_counts = Counter([d['format'] for d in papers])
        ordered_fmts = ['Oral Presentation', 'Poster Presentation', 'Innovative Session', 'Full Panel Session']
        fmt_list = []
        for f in ordered_fmts:
            if fmt_counts[f] > 0:
                short_f = f.replace(' Presentation', '').replace(' Session', '')
                fmt_list.append({
                    'label': f,
                    'short': short_f,
                    'count': fmt_counts[f],
                    'pct': round(fmt_counts[f] / tot * 100, 1) if tot > 0 else 0
                })

        # Regions Breakdown
        reg_counts = Counter([REGION_MAP.get(d['primary_country'], 'Other') for d in papers])
        ordered_regs = ['Asia', 'Europe', 'Africa', 'Americas', 'Oceania', 'Europe/Asia', 'Other']
        reg_list = []
        for r in ordered_regs:
            if reg_counts[r] > 0:
                reg_list.append({
                    'region': r,
                    'count': reg_counts[r],
                    'pct': round(reg_counts[r] / tot * 100, 1) if tot > 0 else 0
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
    return advanced_data

if __name__ == '__main__':
    prepare_advanced_data()
