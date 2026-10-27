"""
Generates high-impact, eye-catching LinkedIn marketing poster graphics
specifically tailored for LinkedIn posts (4:5 portrait and 1:1 square).
Designed to tag institutions worldwide: highlights 73 nations, 5 themes, and 0 abstract counts.
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

_HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(_HERE, 'visuals'), exist_ok=True)

# Load data
with open(os.path.join(_HERE, 'parsed_dataset.json'), 'r', encoding='utf-8') as f:
    ds = json.load(f)

from prepare_advanced_dashboard_data import REGION_MAP

all_countries = sorted(list({d['primary_country'] for d in ds if d.get('primary_country') and d.get('primary_country') != 'Unknown'}))
total_nations = len(all_countries)

theme_countries = {
    1: len({d['primary_country'] for d in ds if d.get('theme_num') == 1 and d.get('primary_country') and d.get('primary_country') != 'Unknown'}),
    2: len({d['primary_country'] for d in ds if d.get('theme_num') == 2 and d.get('primary_country') and d.get('primary_country') != 'Unknown'}),
    3: len({d['primary_country'] for d in ds if d.get('theme_num') == 3 and d.get('primary_country') and d.get('primary_country') != 'Unknown'}),
    4: len({d['primary_country'] for d in ds if d.get('theme_num') == 4 and d.get('primary_country') and d.get('primary_country') != 'Unknown'}),
    5: len({d['primary_country'] for d in ds if d.get('theme_num') == 5 and d.get('primary_country') and d.get('primary_country') != 'Unknown'}),
}

reg_counts = {}
for c in all_countries:
    r = REGION_MAP.get(c, 'Other')
    if r == 'Europe/Asia':
        r = 'Europe'
    reg_counts[r] = reg_counts.get(r, 0) + 1

themes_meta = [
    {
        'num': 1,
        'title': 'SDGs Beyond 2030',
        'subtitle': 'Governance, Multilevel Targets & Institutional Delivery',
        'nations': theme_countries[1],
        'color': '#0D9488',
        'badge_bg': '#CCFBF1'
    },
    {
        'num': 2,
        'title': 'Resilience Across Systems',
        'subtitle': 'Food-Water-Energy Nexus & Nature-Based Solutions',
        'nations': theme_countries[2],
        'color': '#0284C7',
        'badge_bg': '#E0F2FE'
    },
    {
        'num': 3,
        'title': 'Climate–Development Nexus',
        'subtitle': 'Just Transitions, Climate Equity & Adaptation Finance',
        'nations': theme_countries[3],
        'color': '#BA1C24',
        'badge_bg': '#FEE2E2'
    },
    {
        'num': 4,
        'title': 'Health & Well-being Foundations',
        'subtitle': 'Planetary Health, Health Equity & Well-being Models',
        'nations': theme_countries[4],
        'color': '#7C3AED',
        'badge_bg': '#F3E8FF'
    },
    {
        'num': 5,
        'title': 'AI, Big Data & Digitalization',
        'subtitle': 'Digital Twins, Frontier Tech & Ethical AI for SDGs',
        'nations': theme_countries[5],
        'color': '#D97706',
        'badge_bg': '#FEF3C7'
    }
]

def make_linkedin_portrait():
    # 8 x 10 inches at 300 DPI = 2400 x 3000 px (4:5 standard LinkedIn Portrait)
    fig = plt.figure(figsize=(8, 10), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 125)
    ax.axis('off')

    # Dark Premium Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 125, facecolor='#0B132B', edgecolor='none'))

    # Top Brand Stripe (University of Groningen Red)
    ax.add_patch(patches.Rectangle((0, 123), 100, 2, facecolor='#BA1C24', edgecolor='none'))

    # HEADER CARD
    h_box = patches.FancyBboxPatch((5, 102), 90, 19, boxstyle="round,pad=0.4,rounding_size=1.5",
                                  facecolor='#1C2541', edgecolor='#3A506B', linewidth=1.2)
    ax.add_patch(h_box)

    ax.text(8, 117.5, "RIJKSUNIVERSITEIT GRONINGEN  •  UNIVERSITY OF GRONINGEN", 
            fontsize=8.5, weight='bold', color='#BA1C24', family='sans-serif')
    ax.text(8, 111.5, "GRONINGEN SUSTAINABILITY CONFERENCE 2027", 
            fontsize=15, weight='black', color='#FFFFFF', family='sans-serif')
    ax.text(8, 107.5, "Lessons from the SDGs for the Post-2030 Agenda", 
            fontsize=9.8, weight='semibold', color='#38BDF8', family='sans-serif')
    ax.text(8, 104, "APRIL 05 – 10, 2027   |   ZERNIKE CAMPUS, GRONINGEN, THE NETHERLANDS", 
            fontsize=7.2, weight='bold', color='#94A3B8', family='sans-serif')

    # HERO STAT: NATIONS CALLOUT
    hero_box = patches.FancyBboxPatch((5, 84), 90, 16.5, boxstyle="round,pad=0.4,rounding_size=1.5",
                                     facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
    ax.add_patch(hero_box)

    ax.text(9, 91.5, str(total_nations), fontsize=38, weight='black', color='#BA1C24', family='sans-serif')
    ax.text(23, 95.5, "NATIONS REPRESENTED WORLDWIDE", fontsize=12.5, weight='black', color='#FFFFFF', family='sans-serif')
    ax.text(23, 91.5, "Across 6 Continents • Connecting Leading Global Research Institutions", fontsize=8.2, color='#94A3B8', family='sans-serif')
    
    # Regional Badges
    conts = [
        ("Europe", f"{reg_counts.get('Europe', 0)} Nations", "#BA1C24"),
        ("Asia", f"{reg_counts.get('Asia', 0)} Nations", "#D97706"),
        ("Africa", f"{reg_counts.get('Africa', 0)} Nations", "#0D9488"),
        ("Americas", f"{reg_counts.get('Americas', 0)} Nations", "#38BDF8"),
        ("Oceania", f"{reg_counts.get('Oceania', 0)} Nations", "#0284C7"),
    ]
    cx = 23
    for cname, cnum, ccol in conts:
        p = patches.FancyBboxPatch((cx, 86), 13.5, 3.8, boxstyle="round,pad=0.15,rounding_size=0.6", facecolor='#0F172A', edgecolor=ccol, linewidth=1)
        ax.add_patch(p)
        ax.text(cx + 6.75, 87.9, f"{cname}\n{cnum}", fontsize=5.8, weight='bold', color='#F8FAFC', ha='center', va='center', family='sans-serif', linespacing=1.05)
        cx += 14.2

    # SECTION TITLE
    ax.text(6, 80, "WHAT PARTICIPATING NATIONS ARE EXPLORING", fontsize=10.5, weight='black', color='#FFFFFF', family='sans-serif')
    ax.text(6, 77.5, "Distribution of global research expertise across the 5 conference themes", fontsize=7.5, color='#94A3B8', family='sans-serif')

    # 5 THEME CARDS
    y = 65.5
    for t in themes_meta:
        card = patches.FancyBboxPatch((5, y), 90, 10.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                                      facecolor='#1E293B', edgecolor='#334155', linewidth=1)
        ax.add_patch(card)

        # Left Strip
        ax.add_patch(patches.Rectangle((5, y), 1.8, 10.5, facecolor=t['color'], edgecolor='none'))

        # Theme Tag
        pill = patches.FancyBboxPatch((8.5, y + 6.8), 14, 2.4, boxstyle="round,pad=0.15,rounding_size=0.5", facecolor=t['color'], edgecolor='none')
        ax.add_patch(pill)
        ax.text(15.5, y + 8, f"THEME 0{t['num']}", fontsize=6.5, weight='bold', color='#FFFFFF', ha='center', va='center', family='sans-serif')

        # Title & Subtitle
        ax.text(24, y + 7.5, t['title'], fontsize=10.5, weight='bold', color='#FFFFFF', family='sans-serif')
        ax.text(8.5, y + 3.2, t['subtitle'], fontsize=7.5, color='#94A3B8', family='sans-serif')

        # Nation Count Right Badge
        nbadge = patches.FancyBboxPatch((76, y + 1.8), 17, 7, boxstyle="round,pad=0.2,rounding_size=0.8", facecolor='#0F172A', edgecolor=t['color'], linewidth=1)
        ax.add_patch(nbadge)
        ax.text(84.5, y + 5.9, f"{t['nations']}", fontsize=15, weight='black', color=t['color'], ha='center', va='center', family='sans-serif')
        ax.text(84.5, y + 3.2, "NATIONS", fontsize=6, weight='bold', color='#94A3B8', ha='center', va='center', family='sans-serif')

        y -= 12.2

    # CALL TO ACTION FOR LINKEDIN (Tagging Institutions)
    cta_box = patches.FancyBboxPatch((5, 4.5), 90, 8.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor='#BA1C24', edgecolor='none')
    ax.add_patch(cta_box)

    ax.text(50, 10.0, "IS YOUR INSTITUTION REPRESENTED? SUBMIT & COLLABORATE TODAY!", 
            fontsize=9.0, weight='black', color='#FFFFFF', ha='center', va='center', family='sans-serif')
    ax.text(50, 6.8, "Panels, Workshops & Research Dialogue  •  rug.nl/sustainability-conference-2027", 
            fontsize=7.2, weight='semibold', color='#FEE2E2', ha='center', va='center', family='sans-serif')

    out_path = os.path.join(_HERE, 'visuals', 'GSC2027_LinkedIn_Poster_Portrait.png')
    plt.savefig(out_path, dpi=300, facecolor='#0B132B')
    plt.close()
    print(f"Generated {out_path} successfully!")

def make_linkedin_square():
    # 8 x 8 inches at 300 DPI = 2400 x 2400 px (1:1 LinkedIn Square)
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Dark Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#0B132B', edgecolor='none'))
    ax.add_patch(patches.Rectangle((0, 98.2), 100, 1.8, facecolor='#BA1C24', edgecolor='none'))

    # HEADER
    ax.text(7, 94.5, "UNIVERSITY OF GRONINGEN  •  GSC 2027", fontsize=8.5, weight='bold', color='#BA1C24', family='sans-serif')
    ax.text(7, 89, "GRONINGEN SUSTAINABILITY CONFERENCE", fontsize=15, weight='black', color='#FFFFFF', family='sans-serif')
    ax.text(7, 85, "Lessons from the SDGs for the Post-2030 Agenda  |  April 05–10, 2027", fontsize=8.5, weight='semibold', color='#38BDF8', family='sans-serif')

    # HERO BOX
    hero_box = patches.FancyBboxPatch((5, 68), 90, 14.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor='#1E293B', edgecolor='#334155', linewidth=1)
    ax.add_patch(hero_box)
    ax.text(9, 74.5, str(total_nations), fontsize=34, weight='black', color='#BA1C24', family='sans-serif')
    ax.text(22, 78, "NATIONS REPRESENTED WORLDWIDE", fontsize=11.5, weight='black', color='#FFFFFF', family='sans-serif')
    reg_summary = f"Europe ({reg_counts.get('Europe', 0)}) • Asia ({reg_counts.get('Asia', 0)}) • Africa ({reg_counts.get('Africa', 0)}) • Americas ({reg_counts.get('Americas', 0)}) • Oceania ({reg_counts.get('Oceania', 0)})"
    ax.text(22, 74.5, reg_summary, fontsize=7.5, color='#94A3B8', family='sans-serif')
    ax.text(22, 71, "Zero abstract limits — A global movement of universities and researchers.", fontsize=7, color='#CBD5E1', style='italic', family='sans-serif')

    # 5 THEMES COMPACT GRID
    y = 57.5
    for t in themes_meta:
        c = patches.FancyBboxPatch((5, y), 90, 8.2, boxstyle="round,pad=0.2,rounding_size=0.8", facecolor='#1E293B', edgecolor='#334155', linewidth=0.8)
        ax.add_patch(c)
        ax.add_patch(patches.Rectangle((5, y), 1.5, 8.2, facecolor=t['color'], edgecolor='none'))
        
        ax.text(8.5, y + 5, f"Theme {t['num']}: {t['title']}", fontsize=9.2, weight='bold', color='#FFFFFF', family='sans-serif')
        ax.text(8.5, y + 1.8, t['subtitle'], fontsize=7, color='#94A3B8', family='sans-serif')

        # Badge
        badge = patches.FancyBboxPatch((78, y + 1.5), 15, 5.2, boxstyle="round,pad=0.15,rounding_size=0.6", facecolor='#0F172A', edgecolor=t['color'], linewidth=0.8)
        ax.add_patch(badge)
        ax.text(85.5, y + 4.5, f"{t['nations']}", fontsize=11, weight='black', color=t['color'], ha='center', va='center', family='sans-serif')
        ax.text(85.5, y + 2.5, "NATIONS", fontsize=5, weight='bold', color='#94A3B8', ha='center', va='center', family='sans-serif')

        y -= 9.4

    # BOTTOM CTA
    cta = patches.FancyBboxPatch((5, 3), 90, 7, boxstyle="round,pad=0.3,rounding_size=1", facecolor='#BA1C24', edgecolor='none')
    ax.add_patch(cta)
    ax.text(50, 7.2, f"TAG YOUR INSTITUTION & JOIN {total_nations}+ NATIONS IN GRONINGEN!", fontsize=8.5, weight='black', color='#FFFFFF', ha='center', va='center', family='sans-serif')
    ax.text(50, 4.8, "rug.nl/sustainability-conference-2027  •  April 05–10, 2027", fontsize=7, color='#FEE2E2', ha='center', va='center', family='sans-serif')

    out_path = os.path.join(_HERE, 'visuals', 'GSC2027_LinkedIn_Poster_Square.png')
    plt.savefig(out_path, dpi=300, facecolor='#0B132B')
    plt.close()
    print(f"Generated {out_path} successfully!")

if __name__ == '__main__':
    make_linkedin_portrait()
    make_linkedin_square()
