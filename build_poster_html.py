"""
Builds the interactive marketing poster and pamphlet for GSC 2027.
Generates poster.html and docs/poster.html.
"""
import os
import json
import base64
from generate_maps import REGION_MAP

_HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_HERE, 'parsed_dataset.json'), 'r', encoding='utf-8') as f:
    ds = json.load(f)

with open(os.path.join(_HERE, 'rug_logo.svg'), 'r', encoding='utf-8') as f:
    rug_svg = f.read()

# Filter valid countries
countries_set = sorted(list({d['primary_country'] for d in ds if d.get('primary_country') and d.get('primary_country') != 'Unknown'}))
total_nations = len(countries_set)

# Country theme mapping
country_data = {}
for c in countries_set:
    reg = REGION_MAP.get(c, 'Other')
    if reg in ['Other', 'Europe/Asia']:
        if c in ['Turkey', 'Cyprus', 'Azerbaijan']: reg = 'Europe'
        elif c in ['Burkina Faso', 'Benin']: reg = 'Africa'
        elif c in ['Saudi Arabia', 'Kuwait', 'Oman', 'UAE', 'Yemen', 'Lebanon', 'Israel', 'Palestine', 'Iran', 'Afghanistan']: reg = 'Asia / Middle East'
        else: reg = 'Other'
    elif reg == 'Asia':
        reg = 'Asia'
    
    country_data[c] = {
        'country': c,
        'region': reg,
        'themes': set()
    }

for d in ds:
    c = d.get('primary_country')
    t = d.get('theme_num')
    if c in country_data and t in [1, 2, 3, 4, 5]:
        country_data[c]['themes'].add(t)

# Serialize sets to sorted lists
for c in country_data:
    country_data[c]['themes'] = sorted(list(country_data[c]['themes']))

# Theme country counts
theme_countries = {
    t: [c for c, val in country_data.items() if t in val['themes']]
    for t in range(1, 6)
}

# Regional counts
region_counts = {}
for c, val in country_data.items():
    r = val['region']
    region_counts[r] = region_counts.get(r, 0) + 1

# Themes definition
themes_def = [
    {
        'num': 1,
        'title': 'SDGs Beyond 2030',
        'full_title': 'Lessons from the SDGs for sustainable development beyond 2030',
        'tagline': 'Evaluating 15 years of SDG implementation & architecting post-2030 global governance',
        'nations_count': len(theme_countries[1]),
        'color': '#0D9488',
        'bg_soft': '#F0FDFA',
        'border': '#99F6E4',
        'focus': ['National & Local SDG Delivery', 'Multi-Level Governance & Synergies', 'Beyond-GDP Metrics', 'Global Development Finance'],
        'sample_nations': ['Netherlands', 'India', 'China', 'Germany', 'Indonesia', 'South Africa', 'Brazil', 'United Kingdom', 'Switzerland']
    },
    {
        'num': 2,
        'title': 'Resilience Across Systems',
        'full_title': 'Building resilience through integrated sustainable transformation across natural and human systems',
        'tagline': 'Integrating food, water, energy and ecological thresholds for systemic transformation',
        'nations_count': len(theme_countries[2]),
        'color': '#0284C7',
        'bg_soft': '#F0F9FF',
        'border': '#BAE6FD',
        'focus': ['Food-Water-Energy Nexus', 'Nature-Based Solutions & Biodiversity', 'Circular Bioeconomy', 'Socio-Ecological Transitions'],
        'sample_nations': ['China', 'Netherlands', 'Germany', 'India', 'Egypt', 'France', 'Kenya', 'Singapore', 'United States']
    },
    {
        'num': 3,
        'title': 'Climate–Development Nexus',
        'full_title': 'Navigating the climate change–development nexus for resilient, just and equitable transformations',
        'tagline': 'Centering equity, climate justice, adaptation finance, and vulnerable communities',
        'nations_count': len(theme_countries[3]),
        'color': '#BA1C24',
        'bg_soft': '#FEF2F2',
        'border': '#FECACA',
        'focus': ['Just Transitions & Decarbonization', 'Loss & Damage Mechanisms', 'Adaptation in Global South', 'Climate-Resilient Infrastructure'],
        'sample_nations': ['India', 'Netherlands', 'Germany', 'Ghana', 'Indonesia', 'Canada', 'Nigeria', 'Sweden', 'New Zealand']
    },
    {
        'num': 4,
        'title': 'Health & Well-being Foundations',
        'full_title': 'Health, well-being, and societal foundations as key drivers of sustainable development',
        'tagline': 'Planetary health, health equity, well-being economics, and thriving communities',
        'nations_count': len(theme_countries[4]),
        'color': '#7C3AED',
        'bg_soft': '#FAF5FF',
        'border': '#E9D5FF',
        'focus': ['Planetary Health Frameworks', 'Health Equity & Social Determinants', 'Well-being Economy Models', 'Resilient Healthcare Infrastructure'],
        'sample_nations': ['India', 'Netherlands', 'China', 'Germany', 'Indonesia', 'Japan', 'Malaysia', 'Morocco', 'Spain']
    },
    {
        'num': 5,
        'title': 'AI, Big Data & Digitalization',
        'full_title': 'Artificial Intelligence, big data, and digitalization as enablers for sustainable development',
        'tagline': 'Harnessing frontier technology, digital public infrastructure, and ethical data science',
        'nations_count': len(theme_countries[5]),
        'color': '#D97706',
        'bg_soft': '#FFFBEB',
        'border': '#FDE68A',
        'focus': ['AI for Sustainability & Earth Observation', 'Digital Public Infrastructure', 'Algorithmic Equity & Ethics', 'Smart Clean Energy Grids'],
        'sample_nations': ['Netherlands', 'China', 'Germany', 'India', 'Indonesia', 'Australia', 'UAE', 'Mexico', 'United Kingdom']
    }
]

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GSC 2027 | Global Outreach Poster & Marketing Pamphlet</title>
  <meta name="description" content="Official marketing poster and conference pamphlet for the Groningen Sustainability Conference 2027 at the University of Groningen. 73 Nations participating across 5 global themes.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --rug-red: #BA1C24;
      --rug-red-dark: #8F141A;
      --rug-red-light: #FEE2E2;
      --navy-dark: #0F172A;
      --navy-card: #1E293B;
      --navy-border: #334155;
      --slate-bg: #F8FAFC;
      --slate-card: #FFFFFF;
      --slate-text: #0F172A;
      --slate-muted: #64748B;
      --slate-border: #E2E8F0;
      
      --t1-teal: #0D9488;
      --t2-blue: #0284C7;
      --t3-red: #BA1C24;
      --t4-purple: #7C3AED;
      --t5-amber: #D97706;
      
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.04);
      --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.05);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      background-color: var(--slate-bg);
      color: var(--slate-text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      padding-bottom: 60px;
    }}

    h1, h2, h3, h4, .font-heading {{
      font-family: 'Outfit', sans-serif;
      letter-spacing: -0.02em;
    }}

    /* Top Brand Bar */
    .brand-stripe {{
      height: 6px;
      background: linear-gradient(90deg, var(--rug-red) 0%, #E11D48 50%, var(--rug-red-dark) 100%);
      width: 100%;
    }}

    /* Control Toolbar (Hidden in print) */
    .toolbar {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      color: #fff;
      padding: 12px 24px;
      position: sticky;
      top: 0;
      z-index: 1000;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: var(--shadow-md);
    }}

    .toolbar-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .toolbar-logo {{
      height: 28px;
      fill: #fff;
    }}

    .toolbar-title {{
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #E2E8F0;
    }}

    .toolbar-nav {{
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.1);
      padding: 4px;
      border-radius: 9999px;
    }}

    .view-btn {{
      background: transparent;
      border: none;
      color: #94A3B8;
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 16px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .view-btn:hover {{
      color: #fff;
    }}

    .view-btn.active {{
      background: var(--rug-red);
      color: #fff;
      box-shadow: 0 2px 8px rgba(186, 28, 36, 0.4);
    }}

    .action-btn {{
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      padding: 7px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
      text-decoration: none;
    }}

    .action-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.35);
    }}

    /* Main Container */
    .container {{
      max-width: 1200px;
      margin: 32px auto;
      padding: 0 24px;
      transition: max-width 0.3s ease;
    }}

    /* POSTER WRAPPER */
    .poster-sheet {{
      background: #FFFFFF;
      border-radius: 24px;
      box-shadow: var(--shadow-xl);
      border: 1px solid var(--slate-border);
      overflow: hidden;
    }}

    /* Poster Header */
    .poster-header {{
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      color: #FFFFFF;
      padding: 40px 48px;
      position: relative;
      border-bottom: 1px solid #334155;
    }}

    .poster-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }}

    .rug-logo-container {{
      width: 220px;
      max-width: 45%;
    }}

    .rug-logo-container svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .conf-badge {{
      background: rgba(186, 28, 36, 0.2);
      border: 1px solid rgba(186, 28, 36, 0.5);
      color: #FECACA;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .poster-title {{
      font-size: 42px;
      font-weight: 900;
      line-height: 1.1;
      margin-bottom: 12px;
      color: #FFFFFF;
    }}

    .poster-subtitle {{
      font-size: 20px;
      font-weight: 500;
      color: #38BDF8;
      margin-bottom: 20px;
    }}

    .poster-meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 24px;
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      font-size: 13.5px;
      color: #CBD5E1;
    }}

    .meta-item {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .meta-item strong {{
      color: #FFFFFF;
    }}

    /* Skyline Architecture Sketch */
    .skyline-strip {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--slate-border);
      padding: 12px 24px 0;
      text-align: center;
      overflow: hidden;
    }}

    .skyline-img {{
      max-width: 100%;
      height: 180px;
      object-fit: contain;
      object-position: bottom center;
      display: block;
      margin: 0 auto;
    }}

    .skyline-caption {{
      padding: 10px 0 14px;
      font-size: 13px;
      font-style: italic;
      color: var(--slate-muted);
      border-top: 1px dashed var(--slate-border);
    }}

    /* HERO NATIONS CALLOUT */
    .hero-nations {{
      background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
      padding: 36px 48px;
      border-bottom: 1px solid var(--slate-border);
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 36px;
      align-items: center;
    }}

    .hero-stat {{
      text-align: center;
      padding-right: 32px;
      border-right: 2px solid var(--slate-border);
    }}

    .hero-num {{
      font-family: 'Outfit', sans-serif;
      font-size: 88px;
      font-weight: 900;
      line-height: 0.9;
      color: var(--rug-red);
      letter-spacing: -0.04em;
    }}

    .hero-label {{
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--navy-dark);
      margin-top: 4px;
    }}

    .hero-sublabel {{
      font-size: 12px;
      font-weight: 600;
      color: var(--slate-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .hero-desc {{
      font-size: 17px;
      font-weight: 500;
      color: #334155;
      margin-bottom: 18px;
      line-height: 1.45;
    }}

    .continent-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .continent-pill {{
      background: #FFFFFF;
      border: 1px solid var(--slate-border);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-sm);
    }}

    .pill-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}

    /* Map Showcase Section */
    .map-section {{
      padding: 36px 48px;
      border-bottom: 1px solid var(--slate-border);
      background: #FFFFFF;
    }}

    .section-title {{
      font-size: 24px;
      font-weight: 800;
      color: var(--navy-dark);
      margin-bottom: 6px;
    }}

    .section-desc {{
      font-size: 14.5px;
      color: var(--slate-muted);
      margin-bottom: 24px;
    }}

    .map-wrapper {{
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--slate-border);
      background: #FFFFFF;
      box-shadow: var(--shadow-sm);
    }}

    .map-wrapper img {{
      width: 100%;
      height: auto;
      display: block;
    }}

    /* Themes Section */
    .themes-section {{
      padding: 40px 48px;
      background: #F8FAFC;
    }}

    .themes-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}

    .theme-card {{
      background: #FFFFFF;
      border-radius: 16px;
      border: 1px solid var(--slate-border);
      padding: 24px 28px;
      display: grid;
      grid-template-columns: 1fr 180px;
      gap: 24px;
      align-items: center;
      transition: all 0.25s ease;
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }}

    .theme-card::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 6px;
      background: var(--theme-color);
    }}

    .theme-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
      border-color: #CBD5E1;
    }}

    .theme-badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #FFFFFF;
      margin-bottom: 8px;
    }}

    .theme-title {{
      font-size: 20px;
      font-weight: 700;
      color: var(--navy-dark);
      margin-bottom: 6px;
    }}

    .theme-tagline {{
      font-size: 13.5px;
      color: #475569;
      margin-bottom: 12px;
    }}

    .theme-focus-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }}

    .focus-tag {{
      background: #F1F5F9;
      color: #334155;
      font-size: 11.5px;
      font-weight: 500;
      padding: 3px 8px;
      border-radius: 4px;
    }}

    .sample-countries {{
      font-size: 12px;
      color: var(--slate-muted);
    }}

    .sample-countries strong {{
      color: #334155;
    }}

    .theme-stat-box {{
      background: var(--theme-bg);
      border: 1px solid var(--theme-border);
      border-radius: 12px;
      padding: 16px;
      text-align: center;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}

    .theme-count {{
      font-family: 'Outfit', sans-serif;
      font-size: 42px;
      font-weight: 900;
      color: var(--theme-color);
      line-height: 1;
    }}

    .theme-count-label {{
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #475569;
      margin-top: 4px;
    }}

    /* Participating Nations Honor Roll */
    .honor-roll-section {{
      padding: 40px 48px;
      background: #FFFFFF;
      border-top: 1px solid var(--slate-border);
    }}

    .search-filter-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}

    .search-input {{
      flex: 1;
      min-width: 260px;
      padding: 10px 16px;
      border-radius: 8px;
      border: 1px solid var(--slate-border);
      font-family: inherit;
      font-size: 14px;
      background: #F8FAFC;
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--rug-red);
      background: #FFFFFF;
      box-shadow: 0 0 0 3px rgba(186, 28, 36, 0.1);
    }}

    .filter-btn {{
      background: #F1F5F9;
      border: 1px solid var(--slate-border);
      color: #334155;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .filter-btn:hover {{
      background: #E2E8F0;
    }}

    .filter-btn.active {{
      background: var(--navy-dark);
      color: #FFFFFF;
      border-color: var(--navy-dark);
    }}

    .country-cloud {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      max-height: 380px;
      overflow-y: auto;
      padding: 16px;
      background: #F8FAFC;
      border-radius: 12px;
      border: 1px solid var(--slate-border);
    }}

    .country-pill {{
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 600;
      color: #1E293B;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .country-pill:hover {{
      border-color: var(--rug-red);
      color: var(--rug-red);
      transform: translateY(-1px);
    }}

    .country-tag-region {{
      font-size: 10px;
      font-weight: 700;
      color: var(--slate-muted);
      background: #F1F5F9;
      padding: 1px 5px;
      border-radius: 3px;
    }}

    /* Poster Footer */
    .poster-footer {{
      background: #0F172A;
      color: #FFFFFF;
      padding: 36px 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 24px;
    }}

    .footer-quote {{
      font-size: 15px;
      font-style: italic;
      color: #38BDF8;
      max-width: 600px;
    }}

    .footer-host {{
      font-size: 13px;
      color: #94A3B8;
      text-align: right;
    }}

    .footer-host strong {{
      color: #FFFFFF;
    }}

    /* PAMPHLET / BROCHURE MODE */
    .pamphlet-mode .poster-sheet {{
      border-radius: 16px;
    }}

    .pamphlet-grid {{
      display: none;
      grid-template-columns: repeat(3, 1fr);
      gap: 0;
      background: #FFFFFF;
    }}

    .pamphlet-panel {{
      padding: 36px 30px;
      border-right: 1px dashed var(--slate-border);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .pamphlet-panel:last-child {{
      border-right: none;
    }}

    .panel-header {{
      border-bottom: 2px solid var(--rug-red);
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}

    .panel-num {{
      font-family: 'Outfit', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: var(--rug-red);
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }}

    .panel-title {{
      font-size: 20px;
      font-weight: 800;
      color: var(--navy-dark);
    }}

    /* Print Optimizations */
    @media print {{
      .brand-stripe, .toolbar, .search-filter-bar, .action-btn {{
        display: none !important;
      }}
      body {{
        background: #FFFFFF;
        padding: 0;
      }}
      .container {{
        max-width: 100%;
        margin: 0;
        padding: 0;
      }}
      .poster-sheet {{
        box-shadow: none;
        border: none;
        border-radius: 0;
      }}
      .poster-header {{
        padding: 24px;
      }}
      .hero-nations, .map-section, .themes-section, .honor-roll-section, .poster-footer {{
        padding: 20px 24px;
      }}
      .theme-card {{
        page-break-inside: avoid;
      }}
    }}

    @media (max-width: 900px) {{
      .hero-nations {{
        grid-template-columns: 1fr;
        text-align: center;
      }}
      .hero-stat {{
        border-right: none;
        border-bottom: 2px solid var(--slate-border);
        padding-right: 0;
        padding-bottom: 20px;
      }}
      .theme-card {{
        grid-template-columns: 1fr;
      }}
      .theme-stat-box {{
        margin-top: 12px;
      }}
      .pamphlet-grid {{
        grid-template-columns: 1fr;
      }}
      .pamphlet-panel {{
        border-right: none;
        border-bottom: 1px dashed var(--slate-border);
      }}
    }}
  </style>
</head>
<body>

  <div class="brand-stripe"></div>

  <!-- CONTROL TOOLBAR -->
  <header class="toolbar">
    <div class="toolbar-left">
      <span class="toolbar-title">University of Groningen • GSC 2027</span>
      <nav class="toolbar-nav">
        <button class="view-btn active" onclick="switchView('poster')">🎯 Poster View</button>
        <button class="view-btn" onclick="switchView('pamphlet')">📑 3-Panel Pamphlet View</button>
      </nav>
    </div>
    <div style="display:flex; gap:10px;">
      <a href="index.html" class="action-btn">📊 Back to Dashboard</a>
      <button class="action-btn" onclick="window.print()">🖨️ Print / Save PDF</button>
    </div>
  </header>

  <main class="container" id="mainContainer">

    <!-- POSTER VIEW -->
    <article class="poster-sheet" id="posterView">
      
      <!-- Top Academic Header -->
      <section class="poster-header">
        <div class="poster-header-top">
          <div class="rug-logo-container">
            {rug_svg}
          </div>
          <div class="conf-badge">Global Sustainability Conference 2027</div>
        </div>

        <h1 class="poster-title">Groningen Sustainability Conference 2027</h1>
        <p class="poster-subtitle">Lessons from the SDGs for the Post-2030 Agenda</p>

        <div class="poster-meta-bar">
          <div class="meta-item">
            <span>📅</span>
            <span><strong>Dates:</strong> April 05 – 10, 2027</span>
          </div>
          <div class="meta-item">
            <span>📍</span>
            <span><strong>Venue:</strong> Zernike Campus, Groningen, The Netherlands</span>
          </div>
          <div class="meta-item">
            <span>🏛️</span>
            <span><strong>Host:</strong> University of Groningen (Rijksuniversiteit Groningen)</span>
          </div>
        </div>
      </section>

      <!-- Architectural Illustration Banner -->
      <section class="skyline-strip">
        <img src="visuals/groningen_skyline_pure.png" alt="University of Groningen Architectural Landmarks" class="skyline-img">
        <p class="skyline-caption">“ SDGs have shown us what is possible; now we need to design what comes next. ” — Groningen Academiegebouw • Forum • Martinitoren • Energy Academy Europe</p>
      </section>

      <!-- HERO STAT: 73 NATIONS -->
      <section class="hero-nations">
        <div class="hero-stat">
          <div class="hero-num">{total_nations}</div>
          <div class="hero-label">Nations</div>
          <div class="hero-sublabel">Represented Worldwide</div>
        </div>
        <div>
          <p class="hero-desc">
            A truly global gathering uniting leading researchers, international policymakers, and community leaders across <strong>6 continents</strong> to co-design the future of sustainability.
          </p>
          <div class="continent-pills">
            <div class="continent-pill">
              <span class="pill-dot" style="background:#BA1C24;"></span>
              <span>Europe: <strong>{region_counts.get('Europe', 18)} Nations</strong></span>
            </div>
            <div class="continent-pill">
              <span class="pill-dot" style="background:#D97706;"></span>
              <span>Asia: <strong>{region_counts.get('Asia', 17)} Nations</strong></span>
            </div>
            <div class="continent-pill">
              <span class="pill-dot" style="background:#0D9488;"></span>
              <span>Africa: <strong>{region_counts.get('Africa', 16)} Nations</strong></span>
            </div>
            <div class="continent-pill">
              <span class="pill-dot" style="background:#2563EB;"></span>
              <span>Americas: <strong>{region_counts.get('Americas', 8)} Nations</strong></span>
            </div>
            <div class="continent-pill">
              <span class="pill-dot" style="background:#0284C7;"></span>
              <span>Oceania: <strong>{region_counts.get('Oceania', 2)} Nations</strong></span>
            </div>
            <div class="continent-pill">
              <span class="pill-dot" style="background:#7C3AED;"></span>
              <span>Middle East & West Asia: <strong>10 Nations</strong></span>
            </div>
          </div>
        </div>
      </section>

      <!-- MAP SECTION -->
      <section class="map-section">
        <h2 class="section-title">Worldwide Participating Nations</h2>
        <p class="section-desc">Global geographical footprint of submitting countries across North America, Latin America, Europe, Africa, Middle East, Asia, and Oceania.</p>
        <div class="map-wrapper">
          <img src="visuals/poster_regional_world_map.png" alt="World Map of Participating Nations">
        </div>
      </section>

      <!-- THEMATIC PILLARS -->
      <section class="themes-section">
        <h2 class="section-title">Global Thematic Pillars & Nation Engagement</h2>
        <p class="section-desc">Discover how 73 nations are channeling their research focus into the 5 core conference themes.</p>

        <div class="themes-grid">
"""

for t in themes_def:
    html_template += f"""
          <div class="theme-card" style="--theme-color:{t['color']}; --theme-bg:{t['bg_soft']}; --theme-border:{t['border']};" onclick="filterByTheme({t['num']})">
            <div>
              <span class="theme-badge" style="background:{t['color']};">Theme 0{t['num']}</span>
              <h3 class="theme-title">{t['title']}</h3>
              <p class="theme-tagline">{t['tagline']}</p>
              <div class="theme-focus-list">
                {''.join(f'<span class="focus-tag">{f}</span>' for f in t['focus'])}
              </div>
              <p class="sample-countries">
                <strong>Leading Participating Nations:</strong> {', '.join(t['sample_nations'])}...
              </p>
            </div>
            <div class="theme-stat-box">
              <div class="theme-count">{t['nations_count']}</div>
              <div class="theme-count-label">Nations Engaged</div>
            </div>
          </div>
    """

html_template += f"""
        </div>
      </section>

      <!-- 73 NATIONS HONOR ROLL -->
      <section class="honor-roll-section">
        <h2 class="section-title">Roll of Participating Nations ({total_nations} Countries)</h2>
        <p class="section-desc">Every participating nation brings crucial local and regional perspectives to the global post-2030 sustainability agenda.</p>
        
        <div class="search-filter-bar">
          <input type="text" id="countrySearch" class="search-input" placeholder="🔍 Search country name (e.g., India, Netherlands, Ghana, Brazil)..." oninput="filterCountries()">
          <button class="filter-btn active" onclick="setContinentFilter('all', this)">All Continents</button>
          <button class="filter-btn" onclick="setContinentFilter('Europe', this)">Europe</button>
          <button class="filter-btn" onclick="setContinentFilter('Asia', this)">Asia</button>
          <button class="filter-btn" onclick="setContinentFilter('Africa', this)">Africa</button>
          <button class="filter-btn" onclick="setContinentFilter('Americas', this)">Americas</button>
          <button class="filter-btn" onclick="setContinentFilter('Oceania', this)">Oceania</button>
        </div>

        <div class="country-cloud" id="countryCloud">
"""

for c, val in sorted(country_data.items(), key=lambda x: x[0]):
    t_str = ','.join(str(t) for t in val['themes'])
    html_template += f"""
          <div class="country-pill" data-country="{c.lower()}" data-region="{val['region']}" data-themes="{t_str}">
            <span>{c}</span>
            <span class="country-tag-region">{val['region']}</span>
          </div>
    """

html_template += f"""
        </div>
      </section>

      <!-- Footer -->
      <footer class="poster-footer">
        <div>
          <p class="footer-quote">“ SDGs have shown us what is possible; now we need to design what comes next. ”</p>
          <p style="font-size:12px; color:#64748B; margin-top:6px;">Groningen Sustainability Conference 2027 • University of Groningen</p>
        </div>
        <div class="footer-host">
          <p><strong>Host:</strong> Rijksuniversiteit Groningen</p>
          <p>Zernike Campus, Groningen, The Netherlands</p>
          <p><a href="https://www.rug.nl" target="_blank" style="color:#38BDF8; text-decoration:none;">www.rug.nl</a></p>
        </div>
      </footer>

    </article>

    <!-- PAMPHLET / TRI-FOLD BROCHURE VIEW -->
    <article class="poster-sheet" id="pamphletView" style="display:none;">
      
      <div class="pamphlet-grid" style="display:grid;">
        
        <!-- PANEL 1: INVITATION & GLOBAL FOOTPRINT -->
        <div class="pamphlet-panel">
          <div>
            <div class="rug-logo-container" style="margin-bottom:16px;">
              {rug_svg}
            </div>
            <div class="panel-header">
              <div class="panel-num">Panel 01 • Invitation</div>
              <h2 class="panel-title">A Truly Global Gathering</h2>
            </div>
            
            <p style="font-size:14px; color:#334155; margin-bottom:16px;">
              The University of Groningen cordially invites global scholars, policy leaders, and practitioners to the <strong>Groningen Sustainability Conference 2027 (GSC 2027)</strong>.
            </p>

            <div style="background:#F1F5F9; border-radius:12px; padding:20px; text-align:center; margin-bottom:20px; border-left:4px solid var(--rug-red);">
              <div style="font-size:54px; font-weight:900; color:var(--rug-red); line-height:1; font-family:'Outfit';">{total_nations}</div>
              <div style="font-size:14px; font-weight:800; color:var(--navy-dark); text-transform:uppercase;">Nations Represented</div>
              <div style="font-size:12px; color:var(--slate-muted);">Spanning 6 Continents</div>
            </div>

            <p style="font-size:13px; color:#475569; line-height:1.6; margin-bottom:16px;">
              Over 70+ nations from Europe, Asia, Africa, the Americas, and Oceania have come together to critically evaluate the SDG framework and construct a sustainable post-2030 paradigm.
            </p>

            <ul style="font-size:12.5px; color:#334155; list-style:none; padding:0; display:grid; gap:8px;">
              <li>🌍 <strong>18 Nations:</strong> Europe</li>
              <li>🌏 <strong>27 Nations:</strong> Asia & Middle East</li>
              <li>🌍 <strong>16 Nations:</strong> Africa</li>
              <li>🌎 <strong>8 Nations:</strong> Americas</li>
              <li>🌏 <strong>2 Nations:</strong> Oceania</li>
            </ul>
          </div>

          <div style="margin-top:24px; border-top:1px solid var(--slate-border); padding-top:16px; font-size:12px; color:var(--slate-muted);">
            📍 <strong>Zernike Campus, Groningen</strong><br>
            📅 <strong>April 05 – 10, 2027</strong>
          </div>
        </div>

        <!-- PANEL 2: THE 5 THEMATIC PILLARS -->
        <div class="pamphlet-panel" style="background:#F8FAFC;">
          <div>
            <div class="panel-header">
              <div class="panel-num">Panel 02 • Core Themes</div>
              <h2 class="panel-title">What Nations Are Exploring</h2>
            </div>

            <div style="display:grid; gap:12px;">
              <div style="background:#FFFFFF; padding:12px; border-radius:8px; border-left:3px solid var(--t1-teal);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:13.5px; color:var(--navy-dark);">Theme 1: SDGs Beyond 2030</strong>
                  <span style="font-size:11px; font-weight:700; color:var(--t1-teal); background:#CCFBF1; padding:2px 6px; border-radius:4px;">41 Nations</span>
                </div>
                <p style="font-size:11.5px; color:#64748B; margin-top:4px;">Governance, beyond-GDP metrics, institutional resilience.</p>
              </div>

              <div style="background:#FFFFFF; padding:12px; border-radius:8px; border-left:3px solid var(--t2-blue);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:13.5px; color:var(--navy-dark);">Theme 2: Resilience Across Systems</strong>
                  <span style="font-size:11px; font-weight:700; color:var(--t2-blue); background:#E0F2FE; padding:2px 6px; border-radius:4px;">32 Nations</span>
                </div>
                <p style="font-size:11.5px; color:#64748B; margin-top:4px;">Food-water-energy nexus, biodiversity, ecological thresholds.</p>
              </div>

              <div style="background:#FFFFFF; padding:12px; border-radius:8px; border-left:3px solid var(--t3-red);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:13.5px; color:var(--navy-dark);">Theme 3: Climate–Development Nexus</strong>
                  <span style="font-size:11px; font-weight:700; color:var(--t3-red); background:#FEE2E2; padding:2px 6px; border-radius:4px;">33 Nations</span>
                </div>
                <p style="font-size:11.5px; color:#64748B; margin-top:4px;">Just transitions, climate finance, vulnerable communities.</p>
              </div>

              <div style="background:#FFFFFF; padding:12px; border-radius:8px; border-left:3px solid var(--t4-purple);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:13.5px; color:var(--navy-dark);">Theme 4: Health & Well-being</strong>
                  <span style="font-size:11px; font-weight:700; color:var(--t4-purple); background:#F3E8FF; padding:2px 6px; border-radius:4px;">21 Nations</span>
                </div>
                <p style="font-size:11.5px; color:#64748B; margin-top:4px;">Planetary health, healthcare equity, well-being economics.</p>
              </div>

              <div style="background:#FFFFFF; padding:12px; border-radius:8px; border-left:3px solid var(--t5-amber);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:13.5px; color:var(--navy-dark);">Theme 5: AI & Digitalization</strong>
                  <span style="font-size:11px; font-weight:700; color:var(--t5-amber); background:#FEF3C7; padding:2px 6px; border-radius:4px;">26 Nations</span>
                </div>
                <p style="font-size:11.5px; color:#64748B; margin-top:4px;">AI for environmental modeling, digital public infrastructure.</p>
              </div>
            </div>
          </div>

          <div style="margin-top:20px; text-align:center;">
            <img src="visuals/groningen_skyline_pure.png" style="max-width:100%; height:90px; object-fit:contain;" alt="Skyline">
          </div>
        </div>

        <!-- PANEL 3: VENUE & CALL TO ACTION -->
        <div class="pamphlet-panel">
          <div>
            <div class="panel-header">
              <div class="panel-num">Panel 03 • Action</div>
              <h2 class="panel-title">Join Us in Groningen</h2>
            </div>

            <p style="font-size:14px; color:#334155; margin-bottom:16px;">
              Founded in 1614, the University of Groningen has a 400-year legacy of academic leadership. GSC 2027 convenes at the vanguard of European sustainability research.
            </p>

            <div style="background:var(--navy-dark); color:#FFFFFF; border-radius:12px; padding:18px; margin-bottom:20px;">
              <h4 style="color:#38BDF8; font-size:14px; margin-bottom:6px;">Highlights of GSC 2027:</h4>
              <ul style="font-size:12px; color:#E2E8F0; padding-left:16px; line-height:1.6;">
                <li>High-level UN & Ministerial Roundtables</li>
                <li>Living Labs at Energy Academy Europe</li>
                <li>Cross-continental Research Consortia</li>
                <li>Young Scholar & Global South Fellowships</li>
              </ul>
            </div>

            <p style="font-size:13px; color:#475569; margin-bottom:12px;">
              Be part of the global roadmap shaping the post-2030 agenda.
            </p>
          </div>

          <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:8px; padding:14px; text-align:center;">
            <p style="font-weight:700; color:var(--rug-red); font-size:14px;">Registration & Panels Open</p>
            <p style="font-size:12px; color:#475569; margin-top:2px;">Visit: <strong>www.rug.nl/gsc2027</strong></p>
            <p style="font-size:11px; color:#64748B; margin-top:4px;">Rijksuniversiteit Groningen</p>
          </div>
        </div>

      </div>

    </article>

  </main>

  <script>
    function switchView(mode) {{
      const poster = document.getElementById('posterView');
      const pamphlet = document.getElementById('pamphletView');
      const btns = document.querySelectorAll('.view-btn');

      if (mode === 'poster') {{
        poster.style.display = 'block';
        pamphlet.style.display = 'none';
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
        document.getElementById('mainContainer').style.maxWidth = '1200px';
      }} else {{
        poster.style.display = 'none';
        pamphlet.style.display = 'block';
        btns[0].classList.remove('active');
        btns[1].classList.add('active');
        document.getElementById('mainContainer').style.maxWidth = '1300px';
      }}
    }}

    let currentContinent = 'all';
    let currentThemeFilter = null;

    function setContinentFilter(continent, btn) {{
      currentContinent = continent;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterCountries();
    }}

    function filterByTheme(themeNum) {{
      currentThemeFilter = (currentThemeFilter === themeNum) ? null : themeNum;
      
      // Update theme cards visual highlight
      document.querySelectorAll('.theme-card').forEach((card, idx) => {{
        if (currentThemeFilter === null) {{
          card.style.opacity = '1';
        }} else if (idx + 1 === currentThemeFilter) {{
          card.style.opacity = '1';
          card.style.boxShadow = '0 0 0 3px var(--rug-red)';
        }} else {{
          card.style.opacity = '0.5';
          card.style.boxShadow = 'none';
        }}
      }});

      filterCountries();
    }}

    function filterCountries() {{
      const query = document.getElementById('countrySearch').value.toLowerCase().trim();
      const pills = document.querySelectorAll('.country-pill');

      pills.forEach(pill => {{
        const cName = pill.getAttribute('data-country');
        const cRegion = pill.getAttribute('data-region');
        const cThemes = pill.getAttribute('data-themes').split(',');

        let matchQuery = !query || cName.includes(query);
        let matchContinent = currentContinent === 'all' || cRegion.includes(currentContinent);
        let matchTheme = currentThemeFilter === null || cThemes.includes(String(currentThemeFilter));

        if (matchQuery && matchContinent && matchTheme) {{
          pill.style.display = 'inline-flex';
        }} else {{
          pill.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""

# Write to GSC2027/poster.html and GSC2027/docs/poster.html
out_local = os.path.join(_HERE, 'poster.html')
out_docs = os.path.join(_HERE, 'docs', 'poster.html')

with open(out_local, 'w', encoding='utf-8') as f:
    f.write(html_template)

with open(out_docs, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Generated {out_local} and {out_docs} successfully!")
