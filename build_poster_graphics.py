"""
Generates a polished, publication-grade marketing poster image (PNG)
for Groningen Sustainability Conference 2027 (GSC 2027).
Adheres strictly to: 73 Nations, 5 Themes, ZERO mention of abstract counts.
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))

# Data
with open(os.path.join(_HERE, 'parsed_dataset.json'), 'r', encoding='utf-8') as f:
    ds = json.load(f)

all_countries = sorted(list({d['primary_country'] for d in ds if d.get('primary_country') and d.get('primary_country') != 'Unknown'}))
total_nations = len(all_countries)

theme_countries = {
    1: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 1 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    2: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 2 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    3: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 3 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    4: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 4 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    5: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 5 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
}

themes_info = [
    {
        'num': 1,
        'title': 'SDGs Beyond 2030',
        'subtitle': 'Governance, Multilevel Targets & Institutional Frameworks',
        'nations': len(theme_countries[1]),
        'color': '#0D9488',
        'sample': 'Netherlands, India, China, Germany, Indonesia, South Africa, USA, Brazil, Nigeria, UK, Switzerland'
    },
    {
        'num': 2,
        'title': 'Resilience Across Systems',
        'subtitle': 'Food-Water-Energy Nexus & Nature-Based Solutions',
        'nations': len(theme_countries[2]),
        'color': '#0284C7',
        'sample': 'China, Netherlands, Germany, India, Egypt, France, Kenya, Singapore, South Africa, USA, Philippines'
    },
    {
        'num': 3,
        'title': 'Climate–Development Nexus',
        'subtitle': 'Just Transitions, Adaptation & Climate Equity',
        'nations': len(theme_countries[3]),
        'color': '#BA1C24',
        'sample': 'India, Netherlands, Germany, Ghana, Indonesia, Canada, Nigeria, Sweden, New Zealand, UK, Tanzania'
    },
    {
        'num': 4,
        'title': 'Health & Well-being Foundations',
        'subtitle': 'Planetary Health, Health Equity & Social Drivers',
        'nations': len(theme_countries[4]),
        'color': '#7C3AED',
        'sample': 'India, Netherlands, China, Germany, Indonesia, Japan, Malaysia, Morocco, Spain, USA, Zimbabwe'
    },
    {
        'num': 5,
        'title': 'AI, Big Data & Digitalization',
        'subtitle': 'Digital Twins, Frontier Tech & Ethical Transformation',
        'nations': len(theme_countries[5]),
        'color': '#D97706',
        'sample': 'Netherlands, China, Germany, India, Indonesia, Australia, UAE, Mexico, Kenya, UK, Uruguay'
    }
]

def generate_poster():
    # 12 x 18 inches at 300 DPI = 3600 x 5400 px
    fig = plt.figure(figsize=(12, 18), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 180)
    ax.axis('off')

    # Background
    ax.add_patch(patches.Rectangle((0, 0), 120, 180, facecolor='#F8FAFC', edgecolor='none'))

    # Top University of Groningen Red Brand Line
    ax.add_patch(patches.Rectangle((0, 177.5), 120, 2.5, facecolor='#BA1C24', edgecolor='none'))

    # HEADER CARD (Dark Navy)
    h_card = patches.FancyBboxPatch((5, 148), 110, 27, boxstyle="round,pad=0.5,rounding_size=2.0",
                                   facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5)
    ax.add_patch(h_card)

    ax.text(9, 171.5, "RIJKSUNIVERSITEIT GRONINGEN  •  UNIVERSITY OF GRONINGEN", 
            fontsize=10.5, weight='bold', color='#BA1C24', family='sans-serif')
    
    ax.text(9, 163, "GRONINGEN SUSTAINABILITY CONFERENCE 2027", 
            fontsize=19, weight='black', color='#FFFFFF', family='sans-serif')
    
    ax.text(9, 157.5, "Lessons from the SDGs for the Post-2030 Agenda", 
            fontsize=12, weight='semibold', color='#38BDF8', family='sans-serif')

    ax.text(9, 152, "APRIL 05 – 10, 2027   |   ZERNIKE CAMPUS, GRONINGEN, THE NETHERLANDS", 
            fontsize=9, weight='bold', color='#94A3B8', family='sans-serif')

    # HERO NATIONS CALLOUT
    hero_card = patches.FancyBboxPatch((5, 124), 110, 21, boxstyle="round,pad=0.5,rounding_size=2.0",
                                      facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.5)
    ax.add_patch(hero_card)

    ax.text(10, 134.5, "73", fontsize=48, weight='black', color='#BA1C24', family='sans-serif')
    ax.text(28, 139, "NATIONS REPRESENTED WORLDWIDE", fontsize=16, weight='black', color='#0F172A', family='sans-serif')
    ax.text(28, 134, "A truly global gathering uniting leading researchers, policymakers, and innovators across 6 continents.", 
            fontsize=10, color='#475569', family='sans-serif')
    
    # Continent Badges
    continents = [
        ("Europe", "18 Nations", "#BA1C24"),
        ("Asia", "17 Nations", "#D97706"),
        ("Africa", "16 Nations", "#0D9488"),
        ("Americas", "8 Nations", "#2563EB"),
        ("Oceania", "2 Nations", "#0284C7"),
        ("Middle East", "10 Nations", "#7C3AED")
    ]
    cx = 10
    for cname, ccount, ccol in continents:
        badge = patches.FancyBboxPatch((cx, 126.5), 15.5, 4.2, boxstyle="round,pad=0.2,rounding_size=0.8", 
                                       facecolor='#F1F5F9', edgecolor=ccol, linewidth=1.2)
        ax.add_patch(badge)
        ax.text(cx + 7.75, 128.6, f"{cname}\n{ccount}", fontsize=7.2, weight='bold', color='#0F172A', 
                ha='center', va='center', family='sans-serif', linespacing=1.1)
        cx += 18

    # WORLD MAP EMBED
    map_card = patches.FancyBboxPatch((5, 96), 110, 25.5, boxstyle="round,pad=0.5,rounding_size=2.0",
                                     facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.5)
    ax.add_patch(map_card)

    map_img_path = os.path.join(_HERE, 'visuals', 'poster_regional_world_map.png')
    if os.path.exists(map_img_path):
        m_img = mpimg.imread(map_img_path)
        ax.imshow(m_img, extent=[7, 113, 97.5, 120], aspect='auto', zorder=3)

    # THEMES SECTION TITLE
    ax.text(6, 91.5, "GLOBAL THEMATIC PILLARS & NATION INTEREST", fontsize=13, weight='black', color='#0F172A', family='sans-serif')
    ax.text(6, 88.8, "Explore how 73 participating nations are distributing their research focus and priorities", fontsize=9.2, color='#64748B', family='sans-serif')

    # 5 THEME CARDS
    card_y = 74
    for t in themes_info:
        card = patches.FancyBboxPatch((5, card_y), 110, 12.8, boxstyle="round,pad=0.4,rounding_size=1.5",
                                      facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.2)
        ax.add_patch(card)

        # Left Color Accent
        strip = patches.Rectangle((5, card_y), 2.2, 12.8, facecolor=t['color'], edgecolor='none')
        ax.add_patch(strip)

        # Theme Pill
        tpill = patches.FancyBboxPatch((9, card_y + 8.6), 16, 2.8, boxstyle="round,pad=0.2,rounding_size=0.7", facecolor=t['color'], edgecolor='none')
        ax.add_patch(tpill)
        ax.text(17, card_y + 10, f"THEME 0{t['num']}", fontsize=7.5, weight='bold', color='#FFFFFF', ha='center', va='center', family='sans-serif')

        # Title
        ax.text(27, card_y + 9.5, t['title'], fontsize=12.5, weight='bold', color='#0F172A', family='sans-serif')

        # Subtitle
        ax.text(9, card_y + 5.5, t['subtitle'], fontsize=9, color='#475569', family='sans-serif')

        # Sample Nations
        ax.text(9, card_y + 2.0, f"Representative Nations: {t['sample']}", fontsize=7.6, color='#64748B', family='sans-serif')

        # Nation Count Badge on Right
        nbadge = patches.FancyBboxPatch((93, card_y + 1.8), 20, 9.2, boxstyle="round,pad=0.3,rounding_size=1.2",
                                        facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1)
        ax.add_patch(nbadge)
        ax.text(103, card_y + 7.2, f"{t['nations']}", fontsize=20, weight='black', color=t['color'], ha='center', va='center', family='sans-serif')
        ax.text(103, card_y + 3.8, "NATIONS", fontsize=7.5, weight='bold', color='#64748B', ha='center', va='center', family='sans-serif')

        card_y -= 14.2

    # FOOTER BAR
    f_bar = patches.Rectangle((0, 0), 120, 9, facecolor='#0F172A', edgecolor='none')
    ax.add_patch(f_bar)

    ax.text(6, 5.2, "“ SDGs have shown us what is possible; now we need to design what comes next. ”", 
            fontsize=9.5, weight='semibold', color='#38BDF8', style='italic', family='sans-serif')
    ax.text(6, 2.5, "Join 73+ nations in Groningen • Call for Panels, Workshops & Collaborative Dialogues", 
            fontsize=8, color='#94A3B8', family='sans-serif')
    
    ax.text(114, 4.5, "rug.nl/sustainability-conference-2027", fontsize=10, weight='bold', color='#FFFFFF', ha='right', family='sans-serif')

    out_file = os.path.join(_HERE, 'visuals', 'GSC2027_Poster_Marketing_Final.png')
    plt.savefig(out_file, dpi=300, facecolor='#F8FAFC')
    plt.close()
    print(f"Generated {out_file} successfully!")

if __name__ == '__main__':
    generate_poster()
