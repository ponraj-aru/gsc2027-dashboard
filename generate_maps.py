from source_config import SOURCE_DOC
import json
import pandas as pd
from collections import Counter, defaultdict
import plotly.express as px
import plotly.graph_objects as go
import os
import json as _j
_DS = _j.load(open('parsed_dataset.json', encoding='utf-8'))
TOTAL_N = len(_DS)
NATIONS_N = len({d['primary_country'] for d in _DS if d.get('primary_country')})


with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

os.makedirs('visuals', exist_ok=True)

# -----------------------------------------------------------------------------
# Country to Continent / Region Mapping
# -----------------------------------------------------------------------------
from prepare_advanced_dashboard_data import REGION_MAP

# Aggregate data by country
country_stats = defaultdict(lambda: {
    'total': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0,
    'oral': 0, 'poster': 0, 'symp': 0, 'titles': []
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
        country_stats[c]['symp'] += 1
    if len(country_stats[c]['titles']) < 4:
        country_stats[c]['titles'].append(d['title'])

country_rows = []
for c, s in country_stats.items():
    region = REGION_MAP.get(c, 'Other')
    top_titles_str = "<br>• ".join([t[:60] + ("..." if len(t) > 60 else "") for t in s['titles']])
    country_rows.append({
        'Country': c,
        'Region': region,
        'Total_Submissions': s['total'],
        'Theme_1': s['t1'],
        'Theme_2': s['t2'],
        'Theme_3': s['t3'],
        'Theme_4': s['t4'],
        'Theme_5': s['t5'],
        'Oral': s['oral'],
        'Poster': s['poster'],
        'Special_Sessions': s['symp'],
        'Sample_Papers': "• " + top_titles_str if top_titles_str else ""
    })

df_countries = pd.DataFrame(country_rows)
df_countries = df_countries.sort_values(by='Total_Submissions', ascending=False)
df_countries.to_csv('country_submissions_summary.csv', index=False)

# -----------------------------------------------------------------------------
# 1. Global Static Choropleth Map for PPTX
# -----------------------------------------------------------------------------
fig_global = px.choropleth(
    df_countries,
    locations='Country',
    locationmode='country names',
    color='Total_Submissions',
    color_continuous_scale=[[0, '#E0F2FE'], [0.15, '#7DD3FC'], [0.35, '#0284C7'], [0.7, '#0369A1'], [1.0, '#0C4A6E']],
    range_color=(1, 28),
    title=f'<b>GSC 2027: Global Distribution of Abstract Submissions</b><br><sup>Total: {TOTAL_N} Submissions across {NATIONS_N} Primary Countries</sup>',
    projection='natural earth'
)

fig_global.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    paper_bgcolor='#FFFFFF',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='#CBD5E1',
        showcountries=True,
        countrycolor='#E2E8F0',
        landcolor='#F8FAFC',
        lakecolor='#FFFFFF',
        bgcolor='#FFFFFF'
    ),
    font=dict(family='Arial, sans-serif', size=13, color='#0F172A'),
    coloraxis_colorbar=dict(
        title='<b>Abstracts</b>',
        thickness=16,
        len=0.6,
        y=0.5,
        tickfont=dict(size=11, color='#1E293B')
    )
)

fig_global.write_image('visuals/map_global.png', width=1600, height=850, scale=2)
print("Generated map_global.png successfully!")

# -----------------------------------------------------------------------------
# 2. Theme 3 Static Choropleth Map for PPTX
# -----------------------------------------------------------------------------
df_t3 = df_countries[df_countries['Theme_3'] > 0].copy()
fig_t3 = px.choropleth(
    df_t3,
    locations='Country',
    locationmode='country names',
    color='Theme_3',
    color_continuous_scale=[[0, '#EDE9FE'], [0.25, '#C4B5FD'], [0.5, '#8B5CF6'], [0.75, '#6D28D9'], [1.0, '#4C1D95']],
    range_color=(1, 10),
    title='<b>Theme 3 Global Participation: Climate Change–Development Nexus</b><br><sup>Total: 75 Submissions across 28 Contributing Countries</sup>',
    projection='natural earth'
)

fig_t3.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    paper_bgcolor='#FFFFFF',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='#CBD5E1',
        showcountries=True,
        countrycolor='#E2E8F0',
        landcolor='#F8FAFC',
        lakecolor='#FFFFFF',
        bgcolor='#FFFFFF'
    ),
    font=dict(family='Arial, sans-serif', size=13, color='#0F172A'),
    coloraxis_colorbar=dict(
        title='<b>Theme 3 Papers</b>',
        thickness=16,
        len=0.6,
        y=0.5,
        tickfont=dict(size=11, color='#1E293B')
    )
)

fig_t3.write_image('visuals/map_theme3.png', width=1600, height=850, scale=2)
print("Generated map_theme3.png successfully!")

# -----------------------------------------------------------------------------
# 3. Regional Distribution Donut / Bar Chart
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8.5, 5), dpi=200)
fig.patch.set_facecolor('#FFFFFF')

region_counts = Counter()
for d in dataset:
    c = d['primary_country']
    reg = REGION_MAP.get(c, 'Other')
    region_counts[reg] += 1

r_labels = ['Asia', 'Europe', 'Africa', 'Americas', 'Oceania']
r_vals = [region_counts[r] for r in r_labels]
r_colors = ['#0D9488', '#2563EB', '#D97706', '#7C3AED', '#EC4899']

bars = ax.bar(r_labels, r_vals, color=r_colors, width=0.55)
ax.set_ylabel('Number of Submissions', fontsize=12, fontweight='bold', color='#1E293B')
ax.set_title(f'Submissions by Continental Region (Total: {TOTAL_N})', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.grid(axis='x', visible=False)

for bar in bars:
    h = bar.get_height()
    pct = h / TOTAL_N * 100
    ax.text(bar.get_x() + bar.get_width()/2, h + 2, f'{int(h)}\n({pct:.1f}%)', 
            ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#1E293B')

ax.set_ylim(0, 115)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#94A3B8')
ax.spines['bottom'].set_color('#94A3B8')
ax.tick_params(axis='both', colors='#334155', labelsize=11)
plt.tight_layout()
plt.savefig('visuals/chart_regional.png', facecolor='#FFFFFF', dpi=200)
plt.close()
print("Generated chart_regional.png successfully!")
