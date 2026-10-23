import json
import pandas as pd
from collections import Counter, defaultdict
import plotly.express as px
import plotly.graph_objects as go
import os

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

os.makedirs('visuals', exist_ok=True)

# -----------------------------------------------------------------------------
# Country to Continent / Region Mapping
# -----------------------------------------------------------------------------
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
    title='<b>GSC 2027: Global Distribution of Abstract Submissions</b><br><sup>Total: 301 Submissions across 66 Primary Countries</sup>',
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
ax.set_title('Submissions by Continental Region (Total: 301)', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.grid(axis='x', visible=False)

for bar in bars:
    h = bar.get_height()
    pct = h / 301 * 100
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

# -----------------------------------------------------------------------------
# 4. Interactive HTML Dashboard with Dropdown for Themes
# -----------------------------------------------------------------------------
# Create rich interactive figure with traces for All, Theme 1, Theme 2, Theme 3, Theme 4, Theme 5

fig_interactive = go.Figure()

# Custom hover template
def make_hovertemplate(metric_name):
    return (
        "<b>%{customdata[0]}</b> (%{customdata[1]})<br>" +
        "━━━━━━━━━━━━━━━━━━━━━━━<br>" +
        f"<b>{metric_name}: %{{z}}</b><br>" +
        "Oral: %{customdata[2]} | Poster: %{customdata[3]} | Panels: %{customdata[4]}<br>" +
        "──────── Thematic Breakdown ────────<br>" +
        "T1 (SDGs): %{customdata[5]} | T2 (Resilience): %{customdata[6]}<br>" +
        "T3 (Climate): %{customdata[7]} | T4 (Health): %{customdata[8]}<br>" +
        "T5 (AI & Digital): %{customdata[9]}<br>" +
        "<extra></extra>"
    )

custom_data_matrix = df_countries[[
    'Country', 'Region', 'Oral', 'Poster', 'Special_Sessions',
    'Theme_1', 'Theme_2', 'Theme_3', 'Theme_4', 'Theme_5'
]].values

# Trace 0: All Themes
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Total_Submissions'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Total Submissions"),
    colorscale='Teal',
    colorbar=dict(title=dict(text="<b>Total Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="All Themes",
    visible=True
))

# Trace 1: Theme 3 (Spotlight)
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Theme_3'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Theme 3 Submissions"),
    colorscale='Plasma',
    colorbar=dict(title=dict(text="<b>Theme 3 Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="Theme 3: Climate Nexus",
    visible=False
))

# Trace 2: Theme 1
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Theme_1'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Theme 1 Submissions"),
    colorscale='YlOrRd',
    colorbar=dict(title=dict(text="<b>Theme 1 Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="Theme 1: SDGs Beyond 2030",
    visible=False
))

# Trace 3: Theme 2
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Theme_2'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Theme 2 Submissions"),
    colorscale='Greens',
    colorbar=dict(title=dict(text="<b>Theme 2 Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="Theme 2: Resilience & WEF Nexus",
    visible=False
))

# Trace 4: Theme 4
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Theme_4'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Theme 4 Submissions"),
    colorscale='Purples',
    colorbar=dict(title=dict(text="<b>Theme 4 Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="Theme 4: Health & Well-being",
    visible=False
))

# Trace 5: Theme 5
fig_interactive.add_trace(go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z=df_countries['Theme_5'],
    text=df_countries['Country'],
    customdata=custom_data_matrix,
    hovertemplate=make_hovertemplate("Theme 5 Submissions"),
    colorscale='Blues',
    colorbar=dict(title=dict(text="<b>Theme 5 Papers</b>", side="top"), thickness=18, len=0.6, y=0.5),
    name="Theme 5: AI & Digitalization",
    visible=False
))

# Dropdown buttons
buttons = [
    dict(label="🌍 All Themes (301 Abstracts)", method="update",
         args=[{"visible": [True, False, False, False, False, False]},
               {"title": "<b>GSC 2027 Global Abstract Submissions (All 301 Papers)</b><br><sup>66 Primary Countries Represented Across 5 Themes</sup>"}]),
    dict(label="🔥 Theme 3: Climate Change–Development Nexus (75 Abstracts)", method="update",
         args=[{"visible": [False, True, False, False, False, False]},
               {"title": "<b>Theme 3: Climate Change–Development Nexus (75 Papers across 28 Countries)</b><br><sup>Top: India (9), Netherlands (7), Germany (7), Nepal (5), UK (5), Bangladesh (5), South Africa (5)</sup>"}]),
    dict(label="🌱 Theme 2: Building Resilience across Systems (76 Abstracts)", method="update",
         args=[{"visible": [False, False, False, True, False, False]},
               {"title": "<b>Theme 2: Resilience Across Natural and Human Systems (76 Papers)</b><br><sup>Largest Theme (25.2%) — High concentration on Food-Water-Energy Nexus & Circularity</sup>"}]),
    dict(label="🎯 Theme 1: Lessons from SDGs Beyond 2030 (60 Abstracts)", method="update",
         args=[{"visible": [False, False, True, False, False, False]},
               {"title": "<b>Theme 1: Lessons from the SDGs Beyond 2030 (60 Papers)</b><br><sup>SDG Localization, Governance, Policy Reforms & Post-2030 Agendas</sup>"}]),
    dict(label="🏥 Theme 4: Health & Well-being Foundations (45 Abstracts)", method="update",
         args=[{"visible": [False, False, False, False, True, False]},
               {"title": "<b>Theme 4: Health, Well-being & Societal Foundations (45 Papers)</b><br><sup>Health Equity, Environmental Exposure, One Health & Societal Drivers</sup>"}]),
    dict(label="🤖 Theme 5: AI, Big Data & Digitalization (45 Abstracts)", method="update",
         args=[{"visible": [False, False, False, False, False, True]},
               {"title": "<b>Theme 5: AI, Big Data & Digitalization for Sustainability (45 Papers)</b><br><sup>Twin Transition, AI Governance, Earth Observation & Big Data Analytics</sup>"}])
]

fig_interactive.update_layout(
    updatemenus=[dict(
        type="buttons",
        direction="right",
        x=0.5,
        y=1.15,
        xanchor="center",
        yanchor="top",
        bgcolor="#F1F5F9",
        bordercolor="#CBD5E1",
        borderwidth=1,
        font=dict(size=11.5, color="#0F172A", family="Arial, sans-serif"),
        buttons=buttons
    )],
    title=dict(
        text="<b>GSC 2027 Global Abstract Submissions (All 301 Papers)</b><br><sup>66 Primary Countries Represented Across 5 Themes</sup>",
        x=0.03,
        y=0.96,
        font=dict(size=18, family="Arial, sans-serif", color="#0F172A")
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='#94A3B8',
        showcountries=True,
        countrycolor='#CBD5E1',
        landcolor='#F8FAFC',
        lakecolor='#E0F2FE',
        bgcolor='#F8FAFC',
        projection_type='natural earth'
    ),
    margin=dict(l=20, r=20, t=110, b=20),
    paper_bgcolor='#FFFFFF',
    font=dict(family="Arial, sans-serif")
)

# Embed inside a complete HTML page with rich dashboard styling
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GSC 2027 - Interactive Global Abstract Submissions Map</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0B132B;
            color: #F8FAFC;
            min-height: 100vh;
            padding: 24px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #1E293B;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .header-title h1 {{
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8, #818CF8, #C084FC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }}
        .header-title p {{
            font-size: 14px;
            color: #94A3B8;
        }}
        .badge {{
            background: #1E293B;
            color: #38BDF8;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid #334155;
            display: inline-block;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: #16203B;
            border: 1px solid #233157;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: #38BDF8;
        }}
        .stat-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94A3B8;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        .stat-value {{
            font-size: 30px;
            font-weight: 800;
            color: #FFFFFF;
        }}
        .stat-sub {{
            font-size: 12px;
            color: #38BDF8;
            margin-top: 4px;
        }}
        .map-container {{
            background: #FFFFFF;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            margin-bottom: 24px;
            border: 1px solid #334155;
        }}
        .leaderboard {{
            background: #16203B;
            border: 1px solid #233157;
            border-radius: 16px;
            padding: 20px;
            margin-top: 24px;
        }}
        .leaderboard h2 {{
            font-size: 18px;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .table-responsive {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            color: #CBD5E1;
        }}
        th {{
            background: #0F172A;
            text-align: left;
            padding: 12px 14px;
            font-weight: 600;
            color: #94A3B8;
            border-bottom: 2px solid #334155;
        }}
        td {{
            padding: 12px 14px;
            border-bottom: 1px solid #1E293B;
        }}
        tr:hover td {{
            background: #1E293B;
            color: #FFFFFF;
        }}
        .pill {{
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            display: inline-block;
        }}
        .pill-theme3 {{ background: rgba(139, 92, 246, 0.2); color: #C4B5FD; }}
        .pill-theme2 {{ background: rgba(5, 150, 105, 0.2); color: #6EE7B7; }}
        .pill-theme1 {{ background: rgba(217, 119, 6, 0.2); color: #FCD34D; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #64748B;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            <h1>Groningen Sustainability Conference 2027 (GSC 2027)</h1>
            <p>Interactive Global Geographic & Thematic Landscape of Abstract Submissions</p>
        </div>
        <div class="badge">Official Analysis Dashboard • 301 Abstracts Processed</div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Total Submissions</div>
            <div class="stat-value">301</div>
            <div class="stat-sub">Across 5 Master Themes</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Primary Countries</div>
            <div class="stat-value">66</div>
            <div class="stat-sub">75 Participating Nations</div>
        </div>
        <div class="stat-card" style="border-color: #8B5CF6;">
            <div class="stat-label">Theme 3: Climate Nexus</div>
            <div class="stat-value" style="color: #A78BFA;">75</div>
            <div class="stat-sub">24.9% • 28 Contributing Nations</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Theme 2: Resilience</div>
            <div class="stat-value" style="color: #34D399;">76</div>
            <div class="stat-sub">25.2% • Largest Track</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Oral Presentations</div>
            <div class="stat-value">246</div>
            <div class="stat-sub">81.7% of Submissions</div>
        </div>
    </div>

    <div class="map-container">
        <div id="plotlyMap" style="width: 100%; height: 680px;"></div>
    </div>

    <div class="leaderboard">
        <h2>🏆 Top Contributing Nations Leaderboard</h2>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Country</th>
                        <th>Region</th>
                        <th>Total Papers</th>
                        <th>Theme 3 (Climate)</th>
                        <th>Theme 2 (Resilience)</th>
                        <th>Theme 1 (SDGs)</th>
                        <th>Theme 4 (Health)</th>
                        <th>Theme 5 (AI)</th>
                        <th>Oral / Poster</th>
                    </tr>
                </thead>
                <tbody>
"""

for rank, row in enumerate(df_countries.head(20).to_dict(orient='records'), 1):
    html_content += f"""
                    <tr>
                        <td><b>#{rank}</b></td>
                        <td><b>{row['Country']}</b></td>
                        <td>{row['Region']}</td>
                        <td><b style="color:#38BDF8;">{row['Total_Submissions']}</b></td>
                        <td><span class="pill pill-theme3">{row['Theme_3']}</span></td>
                        <td><span class="pill pill-theme2">{row['Theme_2']}</span></td>
                        <td><span class="pill pill-theme1">{row['Theme_1']}</span></td>
                        <td>{row['Theme_4']}</td>
                        <td>{row['Theme_5']}</td>
                        <td>{row['Oral']} / {row['Poster']}</td>
                    </tr>
    """

html_content += f"""
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        Generated for Groningen Sustainability Conference 2027 (GSC 2027) • Data source: adminPapersBrowse_2026-10-19_09-37-14.doc
    </div>

    <script>
        var figData = {fig_interactive.to_json()};
        Plotly.newPlot('plotlyMap', figData.data, figData.layout, {{responsive: true, displayModeBar: true}});
    </script>
</body>
</html>
"""

with open('gsc2027_interactive_world_map.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated gsc2027_interactive_world_map.html successfully!")
