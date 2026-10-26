from source_config import SOURCE_DOC
import sys
import codecs
from bs4 import BeautifulSoup
import re
import json

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open(SOURCE_DOC, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

# Known countries list (standard names)
standard_countries = {
    'afghanistan': 'Afghanistan', 'albania': 'Albania', 'algeria': 'Algeria', 'andorra': 'Andorra',
    'angola': 'Angola', 'argentina': 'Argentina', 'armenia': 'Armenia', 'australia': 'Australia',
    'austria': 'Austria', 'azerbaijan': 'Azerbaijan', 'bahamas': 'Bahamas', 'bahrain': 'Bahrain',
    'bangladesh': 'Bangladesh', "people's republic of bangladesh": 'Bangladesh', 'barbados': 'Barbados',
    'belarus': 'Belarus', 'belgium': 'Belgium', 'belize': 'Belize', 'benin': 'Benin', 'bhutan': 'Bhutan',
    'bolivia': 'Bolivia', 'bosnia and herzegovina': 'Bosnia and Herzegovina', 'botswana': 'Botswana',
    'brazil': 'Brazil', 'bulgaria': 'Bulgaria', 'burkina faso': 'Burkina Faso', 'burundi': 'Burundi',
    'cambodia': 'Cambodia', 'cameroon': 'Cameroon', 'canada': 'Canada', 'chile': 'Chile', 'china': 'China',
    'colombia': 'Colombia', 'costa rica': 'Costa Rica', 'croatia': 'Croatia', 'cuba': 'Cuba',
    'cyprus': 'Cyprus', 'czech republic': 'Czech Republic', 'czechia': 'Czech Republic',
    'denmark': 'Denmark', 'dr congo': 'DR Congo', 'democratic republic of the congo': 'DR Congo',
    'ecuador': 'Ecuador', 'egypt': 'Egypt', 'estonia': 'Estonia', 'eswatini': 'Eswatini', 'ethiopia': 'Ethiopia',
    'fiji': 'Fiji', 'finland': 'Finland', 'france': 'France', 'gambia': 'The Gambia', 'the gambia': 'The Gambia',
    'georgia': 'Georgia', 'germany': 'Germany', 'ghana': 'Ghana', 'greece': 'Greece', 'guatemala': 'Guatemala',
    'guinea': 'Guinea', 'guyana': 'Guyana', 'haiti': 'Haiti', 'honduras': 'Honduras', 'hungary': 'Hungary',
    'iceland': 'Iceland', 'india': 'India', 'indonesia': 'Indonesia', 'iran': 'Iran', 'iraq': 'Iraq',
    'ireland': 'Ireland', 'israel': 'Israel', 'italy': 'Italy', 'ivory coast': 'Ivory Coast',
    'cote d\'ivoire': 'Ivory Coast', 'jamaica': 'Jamaica', 'japan': 'Japan', 'jordan': 'Jordan',
    'kazakhstan': 'Kazakhstan', 'kenya': 'Kenya', 'kuwait': 'Kuwait', 'kyrgyzstan': 'Kyrgyzstan',
    'laos': 'Laos', 'latvia': 'Latvia', 'lebanon': 'Lebanon', 'lebanese republic': 'Lebanon',
    'lesotho': 'Lesotho', 'liberia': 'Liberia', 'libya': 'Libya', 'lithuania': 'Lithuania',
    'luxembourg': 'Luxembourg', 'madagascar': 'Madagascar', 'malawi': 'Malawi', 'malaysia': 'Malaysia',
    'maldives': 'Maldives', 'mali': 'Mali', 'malta': 'Malta', 'mexico': 'Mexico', 'moldova': 'Moldova',
    'mongolia': 'Mongolia', 'montenegro': 'Montenegro', 'morocco': 'Morocco', 'mozambique': 'Mozambique',
    'myanmar': 'Myanmar', 'namibia': 'Namibia', 'nepal': 'Nepal', 'netherlands': 'Netherlands',
    'netherlands, the': 'Netherlands', 'the netherlands': 'Netherlands', 'new zealand': 'New Zealand',
    'nicaragua': 'Nicaragua', 'niger': 'Niger', 'nigeria': 'Nigeria', 'north macedonia': 'North Macedonia',
    'norway': 'Norway', 'oman': 'Oman', 'pakistan': 'Pakistan', 'palestine': 'Palestine', 'panama': 'Panama',
    'papua new guinea': 'Papua New Guinea', 'paraguay': 'Paraguay', 'peru': 'Peru', 'philippines': 'Philippines',
    'poland': 'Poland', 'portugal': 'Portugal', 'qatar': 'Qatar', 'romania': 'Romania', 'russia': 'Russia',
    'russian federation': 'Russia', 'rwanda': 'Rwanda', 'saudi arabia': 'Saudi Arabia', 'senegal': 'Senegal',
    'serbia': 'Serbia', 'sierra leone': 'Sierra Leone', 'singapore': 'Singapore', 'slovakia': 'Slovakia',
    'slovenia': 'Slovenia', 'somalia': 'Somalia', 'south africa': 'South Africa', 'south korea': 'South Korea',
    'korea, republic of': 'South Korea', 'republic of korea': 'South Korea', 'korea': 'South Korea',
    'spain': 'Spain', 'sri lanka': 'Sri Lanka', 'sudan': 'Sudan', 'sweden': 'Sweden', 'switzerland': 'Switzerland',
    'syria': 'Syria', 'taiwan': 'Taiwan', 'tajikistan': 'Tajikistan', 'tanzania': 'Tanzania',
    'thailand': 'Thailand', 'togo': 'Togo', 'trinidad and tobago': 'Trinidad and Tobago', 'tunisia': 'Tunisia',
    'turkey': 'Turkey', 'türkiye': 'Turkey', 'uganda': 'Uganda', 'ukraine': 'Ukraine',
    'united arab emirates': 'United Arab Emirates', 'uae': 'United Arab Emirates',
    'united kingdom': 'United Kingdom', 'uk': 'United Kingdom', 'great britain': 'United Kingdom',
    'united states': 'United States', 'unites states': 'United States', 'usa': 'United States', 'united states of america': 'United States',
    'uruguay': 'Uruguay', 'uzbekistan': 'Uzbekistan', 'vietnam': 'Vietnam', 'viet nam': 'Vietnam',
    'yemen': 'Yemen', 'zambia': 'Zambia', 'zimbabwe': 'Zimbabwe'
}

papers = []
unmatched = []

for p in paper_divs:
    pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
    theme = p.find('span', class_='paper_type').get_text(strip=True) if p.find('span', class_='paper_type') else ''
    pformat = p.find('span', class_='paper_format').get_text(strip=True) if p.find('span', class_='paper_format') else ''
    topics = p.find('span', class_='paper_topics').get_text(strip=True) if p.find('span', class_='paper_topics') else ''
    keywords = p.find('span', class_='paper_keywords').get_text(strip=True) if p.find('span', class_='paper_keywords') else ''
    title = p.find('p', class_='paper_title').get_text(strip=True) if p.find('p', class_='paper_title') else ''
    authors = p.find('p', class_='paper_author').get_text(strip=True) if p.find('p', class_='paper_author') else ''
    
    porg_tags = p.find_all('p', class_='paper_organisation')
    org_str = " | ".join([o.get_text(" ", strip=True) for o in porg_tags if o.get_text(strip=True)])
    
    pabstract_tags = p.find_all('p', class_='paper_abstract')
    abstract_text = "\n".join([a.get_text(strip=True) for a in pabstract_tags if a.get_text(strip=True)])
    
    # Try finding country from organisations
    found_countries = set()
    # Check lowercase words / phrases
    clean_org = org_str.lower()
    for alias, std in standard_countries.items():
        # Word boundary match
        pattern = r'\b' + re.escape(alias) + r'\b'
        if re.search(pattern, clean_org):
            found_countries.add(std)
            
    if not found_countries:
        unmatched.append({
            'id': pid,
            'title': title,
            'authors': authors,
            'org': org_str,
            'abstract': abstract_text[:200]
        })
    else:
        papers.append({
            'id': pid,
            'title': title,
            'countries': list(found_countries)
        })

print(f"Matched countries: {len(papers)}")
print(f"Unmatched countries: {len(unmatched)}")
if unmatched:
    print("\n--- UNMATCHED DETAILS ---")
    for u in unmatched:
        print(f"ID {u['id']}: Org: {u['org']!r} | Authors: {u['authors']!r} | Title: {u['title']!r}")
