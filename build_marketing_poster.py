"""
Generates high-resolution marketing poster and pamphlet graphics for GSC 2027
highlighting global country participation across themes (strictly 0 abstract counts).
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(_HERE, 'visuals'), exist_ok=True)

# Load data
with open(os.path.join(_HERE, 'parsed_dataset.json'), 'r', encoding='utf-8') as f:
    ds = json.load(f)

from prepare_advanced_dashboard_data import REGION_MAP

# Countries computation
all_countries = sorted(list({d['primary_country'] for d in ds if d.get('primary_country') and d.get('primary_country') != 'Unknown'}))
total_nations = len(all_countries)

reg_counts = {}
for c in all_countries:
    r = REGION_MAP.get(c, 'Other')
    if r == 'Europe/Asia':
        r = 'Europe'
    reg_counts[r] = reg_counts.get(r, 0) + 1

theme_countries = {
    1: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 1 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    2: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 2 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    3: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 3 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    4: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 4 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
    5: sorted(list({d['primary_country'] for d in ds if d.get('theme_num') == 5 and d.get('primary_country') and d.get('primary_country') != 'Unknown'})),
}

themes_meta = [
    {
        'num': 1,
        'title': 'SDGs Beyond 2030',
        'subtitle': 'Governance, Multilevel Targets & Accountability',
        'nations': len(theme_countries[1]),
        'color': '#0D9488',
        'sample': 'Netherlands, India, China, Germany, Indonesia, South Africa, USA, Brazil, Nigeria, UK'
    },
    {
        'num': 2,
        'title': 'Resilience Across Systems',
        'subtitle': 'Food-Water-Energy Nexus & Nature-Based Solutions',
        'nations': len(theme_countries[2]),
        'color': '#0284C7',
        'sample': 'China, Netherlands, Germany, India, Egypt, France, Kenya, Singapore, South Africa, USA'
    },
    {
        'num': 3,
        'title': 'Climate–Development Nexus',
        'subtitle': 'Just Transitions, Adaptation & Climate Equity',
        'nations': len(theme_countries[3]),
        'color': '#BA1C24',
        'sample': 'India, Netherlands, Germany, Ghana, Indonesia, Canada, Nigeria, Sweden, New Zealand, UK'
    },
    {
        'num': 4,
        'title': 'Health & Well-being Foundations',
        'subtitle': 'Planetary Health, Health Equity & Social Drivers',
        'nations': len(theme_countries[4]),
        'color': '#7C3AED',
        'sample': 'India, Netherlands, China, Germany, Indonesia, Japan, Malaysia, Morocco, Spain, USA'
    },
    {
        'num': 5,
        'title': 'AI, Big Data & Digitalization',
        'subtitle': 'Digital Twins, Frontier Tech & Ethical Transformation',
        'nations': len(theme_countries[5]),
        'color': '#D97706',
        'sample': 'Netherlands, China, Germany, India, Indonesia, Australia, UAE, Mexico, Kenya, UK'
    }
]

def build_marketing_poster():
    # 2400 x 3600 px (8 x 12 inches at 300 dpi)
    fig = plt.figure(figsize=(10, 15), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 150)
    ax.axis('off')

    # Background
    bg = patches.Rectangle((0, 0), 100, 150, facecolor='#F8FAFC', edgecolor='none')
    ax.add_patch(bg)

    # Top Brand Bar - University of Groningen Red
    top_bar = patches.Rectangle((0, 147.5), 100, 2.5, facecolor='#BA1C24', edgecolor='none')
    ax.add_patch(top_bar)

    # Header Card (Navy Dark)
    header_card = patches.FancyBboxPatch(
        (4, 114), 92, 31,
        boxstyle="round,pad=0.5,rounding_size=2.0",
        facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5
    )
    ax.add_patch(header_card)

    # University Name
    ax.text(8, 140, "RIJKSUNIVERSITEIT GRONINGEN  •  UNIVERSITY OF GRONINGEN", 
            fontsize=10, weight='bold', color='#BA1C24', family='sans-serif')
    
    # Title
    ax.text(8, 131, "GRONINGEN SUSTAINABILITY\nCONFERENCE 2027", 
            fontsize=21, weight='black', color='#FFFFFF', family='sans-serif', linespacing=1.05)
    
    # Subtitle
    ax.text(8, 125, "Lessons from the SDGs for the Post-2030 Agenda", 
            fontsize=11.5, weight='semibold', color='#38BDF8', family='sans-serif')

    # Date & Venue Badge
    date_badge = patches.FancyBboxPatch((8, 116.5), 84, 5.5, boxstyle="round,pad=0.3,rounding_size=1", facecolor='#1E293B', edgecolor='#334155')
    ax.add_patch(date_badge)
    ax.text(10, 118.8, "APRIL 05 – 10, 2027   |   ZERNIKE CAMPUS, GRONINGEN, THE NETHERLANDS", 
            fontsize=8.5, weight='bold', color='#E2E8F0', family='sans-serif')

    # HERO METRIC: 73 NATIONS
    hero_box = patches.FancyBboxPatch(
        (4, 91), 92, 20.5,
        boxstyle="round,pad=0.5,rounding_size=2.0",
        facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.5
    )
    ax.add_patch(hero_box)

    # Left Column: Big Callout
    ax.text(8, 102.5, str(total_nations), fontsize=48, weight='black', color='#BA1C24', family='sans-serif')
    ax.text(25, 106, "NATIONS", fontsize=18, weight='black', color='#0F172A', family='sans-serif')
    ax.text(25, 101.5, "REPRESENTED WORLDWIDE", fontsize=11, weight='bold', color='#64748B', family='sans-serif')
    ax.text(25, 96, "A truly global convergence of researchers, policymakers, and innovators across 6 continents.", 
            fontsize=9.5, color='#334155', family='sans-serif', style='italic')

    # Right Badges: Continent Counts
    continents = [
        ("Europe", f"{reg_counts.get('Europe', 0)} Nations", "#BA1C24"),
        ("Asia", f"{reg_counts.get('Asia', 0)} Nations", "#D97706"),
        ("Africa", f"{reg_counts.get('Africa', 0)} Nations", "#0D9488"),
        ("Americas", f"{reg_counts.get('Americas', 0)} Nations", "#2563EB"),
        ("Oceania", f"{reg_counts.get('Oceania', 0)} Nations", "#0284C7"),
    ]
    cx = 8.5
    for cname, ccount, ccol in continents:
        badge = patches.FancyBboxPatch((cx, 92.5), 17.5, 2.8, boxstyle="round,pad=0.2,rounding_size=0.6", facecolor='#F1F5F9', edgecolor=ccol, linewidth=1.2)
        ax.add_patch(badge)
        ax.text(cx + 8.75, 93.7, f"{cname}: {ccount}", fontsize=7.2, weight='bold', color='#0F172A', ha='center', va='center', family='sans-serif')
        cx += 18.5

    # SECTION HEADER: THEMES OF INTEREST
    ax.text(5, 87, "GLOBAL THEMATIC PILLARS & NATION INTEREST", fontsize=12.5, weight='black', color='#0F172A', family='sans-serif')
    ax.text(5, 84.5, "How participating countries are distributing their expertise and strategic priorities", fontsize=8.5, color='#64748B', family='sans-serif')

    # 5 Theme Cards
    ty = 68.5
    for t in themes_meta:
        card = patches.FancyBboxPatch(
            (4, ty), 92, 14.5,
            boxstyle="round,pad=0.4,rounding_size=1.5",
            facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.2
        )
        ax.add_patch(card)

        # Left Accent Strip
        strip = patches.Rectangle((4, ty), 2, 14.5, facecolor=t['color'], edgecolor='none')
        ax.add_patch(strip)

        # Theme Pill
        tpill = patches.FancyBboxPatch((7.5, ty + 10.2), 17, 3, boxstyle="round,pad=0.2,rounding_size=0.8", facecolor=t['color'], edgecolor='none')
        ax.add_patch(tpill)
        ax.text(16, ty + 11.7, f"THEME 0{t['num']}", fontsize=7.5, weight='bold', color='#FFFFFF', ha='center', va='center', family='sans-serif')

        # Title
        ax.text(26.5, ty + 11.2, t['title'], fontsize=12, weight='bold', color='#0F172A', family='sans-serif')
        
        # Subtitle
        ax.text(7.5, ty + 6.8, t['subtitle'], fontsize=9, color='#475569', family='sans-serif')

        # Sample Nations
        ax.text(7.5, ty + 2.8, f"Key Participating Nations: {t['sample']} ...", fontsize=7.5, color='#64748B', family='sans-serif')

        # Big Nation Count on Right
        badge_right = patches.FancyBboxPatch((76, ty + 2.2), 18, 10.5, boxstyle="round,pad=0.3,rounding_size=1.2", facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1)
        ax.add_patch(badge_right)
        ax.text(85, ty + 8.2, f"{t['nations']}", fontsize=20, weight='black', color=t['color'], ha='center', va='center', family='sans-serif')
        ax.text(85, ty + 4.5, "NATIONS", fontsize=7.5, weight='bold', color='#64748B', ha='center', va='center', family='sans-serif')

        ty -= 16

    # MAP CALLOUT SECTION
    map_box = patches.FancyBboxPatch(
        (4, 9), 92, 18,
        boxstyle="round,pad=0.4,rounding_size=1.5",
        facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.2
    )
    ax.add_patch(map_box)

    ax.text(7, 23.5, "WORLDWIDE GEOGRAPHIC FOOTPRINT", fontsize=11, weight='black', color='#0F172A', family='sans-serif')
    ax.text(7, 20.8, "Active participation spanning North America, Latin America, Europe, Africa, Middle East, Asia, and Oceania.", fontsize=8, color='#64748B', family='sans-serif')
    
    # 73 Country Cloud (Sample list)
    sample_roll = (
        "Afghanistan • Argentina • Australia • Austria • Azerbaijan • Bangladesh • Belgium • Benin • Brazil • Burkina Faso • "
        "Cameroon • Canada • China • Cyprus • Czech Republic • DR Congo • Denmark • Ecuador • Egypt • Estonia • Ethiopia • "
        "Finland • France • Germany • Ghana • India • Indonesia • Iran • Ireland • Israel • Italy • Japan • Kenya • Kuwait • "
        "Lebanon • Malawi • Malaysia • Mexico • Morocco • Mozambique • Nepal • Netherlands • New Zealand • Nigeria • Oman • "
        "Pakistan • Philippines • Poland • Portugal • Romania • Saudi Arabia • Singapore • South Africa • Spain • Sri Lanka • "
        "Sudan • Sweden • Switzerland • Taiwan • Tanzania • Thailand • The Gambia • Turkey • Uganda • UAE • UK • USA • "
        "Uruguay • Venezuela • Vietnam • Yemen • Zimbabwe"
    )
    ax.text(7, 12, sample_roll, fontsize=6.8, color='#475569', family='sans-serif', wrap=True, linespacing=1.35)

    # FOOTER CALL TO ACTION
    footer_box = patches.Rectangle((0, 0), 100, 6.5, facecolor='#0F172A', edgecolor='none')
    ax.add_patch(footer_box)
    ax.text(5, 3.2, "SDGs have shown us what is possible; now we need to design what comes next.", fontsize=8.5, weight='semibold', color='#38BDF8', style='italic', family='sans-serif')
    ax.text(95, 3.2, "rug.nl/sustainability-conference-2027  •  GSC 2027", fontsize=8.5, weight='bold', color='#FFFFFF', ha='right', family='sans-serif')

    out_path = os.path.join(_HERE, 'visuals', 'GSC2027_Marketing_Poster.png')
    plt.savefig(out_path, dpi=300, facecolor='#F8FAFC')
    plt.close()
    print(f"Generated {out_path} successfully!")

if __name__ == '__main__':
    build_marketing_poster()
