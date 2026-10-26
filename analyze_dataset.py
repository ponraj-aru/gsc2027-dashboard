from source_config import SOURCE_DOC
import sys
import codecs
from bs4 import BeautifulSoup
import re
import json
import os
from collections import Counter, defaultdict

try:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except Exception:
    pass

COUNTRY_PATTERNS = [
    (r'\b(afghanistan)\b', 'Afghanistan'),
    (r'\b(albania)\b', 'Albania'),
    (r'\b(algeria)\b', 'Algeria'),
    (r'\b(argentina)\b', 'Argentina'),
    (r'\b(armenia)\b', 'Armenia'),
    (r'\b(australia|anu|australian national university|melbourne|sydney|unsw|monash|queensland|curtin)\b', 'Australia'),
    (r'\b(austria|boku|vienna|innsbruck|graz)\b', 'Austria'),
    (r'\b(azerbaijan)\b', 'Azerbaijan'),
    (r'\b(bangladesh|people\'s republic of bangladesh|dhaka)\b', 'Bangladesh'),
    (r'\b(belgium|vub|ku leuven|gent university|ghent university|antwerp|uclouvain|liege)\b', 'Belgium'),
    (r'\b(benin)\b', 'Benin'),
    (r'\b(bhutan)\b', 'Bhutan'),
    (r'\b(bolivia)\b', 'Bolivia'),
    (r'\b(botswana)\b', 'Botswana'),
    (r'\b(brazil|brasil|unisantos|faap|brasilia|usp|unicamp|ufrj)\b', 'Brazil'),
    (r'\b(bulgaria|sofia university)\b', 'Bulgaria'),
    (r'\b(burkina faso)\b', 'Burkina Faso'),
    (r'\b(burundi)\b', 'Burundi'),
    (r'\b(cambodia)\b', 'Cambodia'),
    (r'\b(cameroon)\b', 'Cameroon'),
    (r'\b(canada|brocku|brock university|mcgill|toronto|ubc|waterloo)\b', 'Canada'),
    (r'\b(chile|chilean)\b', 'Chile'),
    (r'\b(china|peking university|tsinghua|chinese academy of sciences|nanjing|chongqing|guangdong|huazhong|zhejiang|hubei|wuhan|fudan|tongji|shanghai|tianjin|xi\'an|xian|163\.com)\b', 'China'),
    (r'\b(colombia)\b', 'Colombia'),
    (r'\b(costa rica)\b', 'Costa Rica'),
    (r'\b(croatia)\b', 'Croatia'),
    (r'\b(cyprus)\b', 'Cyprus'),
    (r'\b(czech republic|czechia|charles university)\b', 'Czech Republic'),
    (r'\b(denmark|copenhagen|aarhus|dtu)\b', 'Denmark'),
    (r'\b(congo|dr congo|democratic republic of the congo|d\.r\. congo|bukavu)\b', 'DR Congo'),
    (r'\b(ecuador|universidad de cuenca|escuela politécnica nacional|escuela politecnica nacional|ucuenca)\b', 'Ecuador'),
    (r'\b(egypt|cairo|alexandria)\b', 'Egypt'),
    (r'\b(estonia|tartu)\b', 'Estonia'),
    (r'\b(ethiopia|addis ababa)\b', 'Ethiopia'),
    (r'\b(fiji)\b', 'Fiji'),
    (r'\b(finland|helsinki|aalto)\b', 'Finland'),
    (r'\b(france|montpellier|sorbonne|paris|essca|cnrs|inrae)\b', 'France'),
    (r'\b(gambia|the gambia)\b', 'The Gambia'),
    (r'\b(georgia)\b', 'Georgia'),
    (r'\b(germany|deutschland|max planck|dresden|helmholtz|lausitz|potsdam|pik|hereon|animoconsulting|bauhaus|berlin|munich|hamburg|bonn|heidelberg)\b', 'Germany'),
    (r'\b(ghana|ucc|cape coast|knust|accra)\b', 'Ghana'),
    (r'\b(greece|athens|thessaloniki)\b', 'Greece'),
    (r'\b(guatemala)\b', 'Guatemala'),
    (r'\b(hungary|budapest)\b', 'Hungary'),
    (r'\b(iceland)\b', 'Iceland'),
    (r'\b(india|bharat|iit|iim|delhi|mumbai|bengaluru|bangalore|kolkata|chennai|hyderabad|pune|ahmedabad|kerala|tamil nadu|uttar pradesh|maharashtra|rajasthan|gujarat|madhya pradesh|bihar|odisha|punjab|haryana|assam|jharkhand|karnataka|andhra pradesh|telangana|goa|chhattisgarh|jammu|kashmir|himachal|uttarakhand|chandigarh|nalanda|purulia|sidho-kanho-birsha|south asian university|roorkee|gitam)\b', 'India'),
    (r'\b(indonesia|indonesian|jakarta|gadjah mada|ugm|bandung|itb|bogor|ipb|airlangga|diponegoro|padjadjaran|brawijaya|komnas ham|universitas terbuka)\b', 'Indonesia'),
    (r'\b(iran|tehran)\b', 'Iran'),
    (r'\b(iraq|baghdad)\b', 'Iraq'),
    (r'\b(ireland|trinity college dublin|ucd|university college cork|galway|dublin)\b', 'Ireland'),
    (r'\b(israel|hebrew university|tel aviv|technion)\b', 'Israel'),
    (r'\b(italy|italia|bologna|sapienza|milano|padova|firenze|turin|torino)\b', 'Italy'),
    (r'\b(ivory coast|côte d\'ivoire|cote d\'ivoire)\b', 'Ivory Coast'),
    (r'\b(japan|tokyo|kyoto|osaka|tohoku|nagoya)\b', 'Japan'),
    (r'\b(jordan|amman)\b', 'Jordan'),
    (r'\b(kazakhstan|almaty|astana)\b', 'Kazakhstan'),
    (r'\b(kenya|nairobi|kenyatta|strathmore)\b', 'Kenya'),
    (r'\b(kuwait)\b', 'Kuwait'),
    (r'\b(kyrgyzstan)\b', 'Kyrgyzstan'),
    (r'\b(latvia|riga)\b', 'Latvia'),
    (r'\b(lebanon|beirut|aub)\b', 'Lebanon'),
    (r'\b(luxembourg)\b', 'Luxembourg'),
    (r'\b(madagascar)\b', 'Madagascar'),
    (r'\b(malawi)\b', 'Malawi'),
    (r'\b(malaysia|kuala lumpur|universiti malaya|ukm|usm|upm|utm)\b', 'Malaysia'),
    (r'\b(maldives)\b', 'Maldives'),
    (r'\b(mexico|méxico|unam|tecnológico de monterrey|cinvestav|guadalajara)\b', 'Mexico'),
    (r'\b(moldova|chisinau)\b', 'Moldova'),
    (r'\b(mongolia|ulaanbaatar)\b', 'Mongolia'),
    (r'\b(morocco|maroc|rabat|casablanca|marrakech)\b', 'Morocco'),
    (r'\b(mozambique|maputo)\b', 'Mozambique'),
    (r'\b(myanmar)\b', 'Myanmar'),
    (r'\b(namibia|windhoek)\b', 'Namibia'),
    (r'\b(nepal|kathmandu|tribhuvan|pokhara)\b', 'Nepal'),
    (r'\b(netherlands|the netherlands|holland|groningen|rug|utrecht|amsterdam|leiden|rotterdam|delft|wageningen|wur|eindhoven|twente|maastricht|radboud|vu amsterdam|uva|frisius|ihe delft|world benchmarking alliance|wba|genmab|lozano nasi)\b', 'Netherlands'),
    (r'\b(new zealand|auckland|otago|canterbury|victoria university of wellington)\b', 'New Zealand'),
    (r'\b(nigeria|lagos|ibadan|abuja|benin|covenant|nigerian|obafemi awolowo|oauife)\b', 'Nigeria'),
    (r'\b(norway|oslo|bergen|ntnu|tromsø)\b', 'Norway'),
    (r'\b(oman|muscat)\b', 'Oman'),
    (r'\b(pakistan|islamabad|lahore|karachi|quaid-i-azam|nust|lums|aga khan)\b', 'Pakistan'),
    (r'\b(palestine|palestinian|birzeit|an-najah|al-quds)\b', 'Palestine'),
    (r'\b(peru|perú|pontificia universidad católica del perú|san marcos)\b', 'Peru'),
    (r'\b(philippines|manila|up diliman|ateneo|de la salle)\b', 'Philippines'),
    (r'\b(poland|polska|warsaw|krakow|jagiellonian|adam mickiewicz)\b', 'Poland'),
    (r'\b(portugal|lisbon|porto|coimbra)\b', 'Portugal'),
    (r'\b(qatar|doha)\b', 'Qatar'),
    (r'\b(romania|bucharest|cluj|iasi)\b', 'Romania'),
    (r'\b(russia|russian federation|moscow|saint petersburg|hse)\b', 'Russia'),
    (r'\b(rwanda|kigali)\b', 'Rwanda'),
    (r'\b(saudi arabia|kaust|kfupm|ksu|riyadh)\b', 'Saudi Arabia'),
    (r'\b(senegal|dakar)\b', 'Senegal'),
    (r'\b(serbia|belgrade|novi sad)\b', 'Serbia'),
    (r'\b(singapore|nus|ntu|smu)\b', 'Singapore'),
    (r'\b(slovakia|bratislava)\b', 'Slovakia'),
    (r'\b(slovenia|ljubljana)\b', 'Slovenia'),
    (r'\b(south africa|cape town|witwatersrand|stellenbosch|pretoria|kwazulu-natal|johannesburg|rhodes|ukzn)\b', 'South Africa'),
    (r'\b(south korea|korea|seoul|kaist|yonsei|korea university|postech)\b', 'South Korea'),
    (r'\b(spain|españa|barcelona|madrid|valencia|sevilla|autònoma de barcelona)\b', 'Spain'),
    (r'\b(sri lanka|colombo|peradeniya|moratuwa)\b', 'Sri Lanka'),
    (r'\b(sudan|khartoum)\b', 'Sudan'),
    (r'\b(sweden|stockholm|uppsala|lund|kth|chalmers|gothenburg)\b', 'Sweden'),
    (r'\b(switzerland|eth zurich|epfl|geneva|basel|bern|zurich)\b', 'Switzerland'),
    (r'\b(taiwan|national taiwan university|ntu|taipei)\b', 'Taiwan'),
    (r'\b(tanzania|dar es salaam|sokoine)\b', 'Tanzania'),
    (r'\b(thailand|chulalongkorn|srinakharinwirot|ait|asian institute of technology|bangkok|naresuan)\b', 'Thailand'),
    (r'\b(tunisia|tunis)\b', 'Tunisia'),
    (r'\b(turkey|türkiye|istanbul|ankara|boğaziçi|bogazici)\b', 'Turkey'),
    (r'\b(uganda|soroti|makerere|kampala)\b', 'Uganda'),
    (r'\b(ukraine|kyiv)\b', 'Ukraine'),
    (r'\b(united arab emirates|uae|abu dhabi|dubai|mbzuai)\b', 'United Arab Emirates'),
    (r'\b(united kingdom|uk|great britain|england|scotland|wales|oxford|cambridge|imperial college|sheffield|uofsussex|sussex|brunel|essex|liverpool|london|manchester|nature portfolio)\b', 'United Kingdom'),
    (r'\b(united states|unites states|usa|united states of america|clemson|uta|maryland|harvard|stanford|columbia university|mit|berkeley|arizona state|asu)\b', 'United States'),
    (r'\b(uruguay|montevideo)\b', 'Uruguay'),
    (r'\b(uzbekistan|tashkent)\b', 'Uzbekistan'),
    (r'\b(venezuela|caracas)\b', 'Venezuela'),
    (r'\b(vietnam|viet nam|hanoi|ho chi minh)\b', 'Vietnam'),
    (r'\b(yemen|sanaa)\b', 'Yemen'),
    (r'\b(zambia|lusaka)\b', 'Zambia'),
    (r'\b(zimbabwe|harare)\b', 'Zimbabwe')
]

TLD_MAP = {
    'nl': 'Netherlands', 'de': 'Germany', 'uk': 'United Kingdom', 'np': 'Nepal',
    'in': 'India', 'za': 'South Africa', 'ng': 'Nigeria', 'ec': 'Ecuador',
    'br': 'Brazil', 'be': 'Belgium', 'es': 'Spain', 'fr': 'France',
    'it': 'Italy', 'ro': 'Romania', 'se': 'Sweden', 'jp': 'Japan',
    'cn': 'China', 'id': 'Indonesia', 'bd': 'Bangladesh', 'th': 'Thailand',
    'md': 'Moldova', 'ca': 'Canada', 'pk': 'Pakistan', 'us': 'United States',
    'edu': 'United States', 'ch': 'Switzerland', 'at': 'Austria', 'au': 'Australia',
    'eg': 'Egypt', 'ke': 'Kenya', 'my': 'Malaysia', 'ph': 'Philippines',
    'gh': 'Ghana', 'tz': 'Tanzania', 'ug': 'Uganda', 'mx': 'Mexico', 'co': 'Colombia',
    'fi': 'Finland', 'no': 'Norway', 'dk': 'Denmark', 'pt': 'Portugal', 'pl': 'Poland',
    'gr': 'Greece', 'ie': 'Ireland', 'cz': 'Czech Republic', 'nz': 'New Zealand',
    'cl': 'Chile', 'ar': 'Argentina', 'vn': 'Vietnam', 'kr': 'South Korea', 'tr': 'Turkey',
    'hu': 'Hungary', 'sg': 'Singapore', 'ae': 'United Arab Emirates', 'il': 'Israel',
    'bg': 'Bulgaria'
}

def extract_countries(text):
    if not text:
        return []
    text_low = text.lower()
    matched = []
    for pattern, std_name in COUNTRY_PATTERNS:
        if re.search(pattern, text_low):
            if std_name not in matched:
                matched.append(std_name)
    return matched

# Load existing dataset if available to carry over abstract text and keywords
prev_dataset = {}
for prev_file in ['parsed_dataset-ponraj_ws.json', 'parsed_dataset.json']:
    if os.path.exists(prev_file):
        try:
            with open(prev_file, 'r', encoding='utf-8') as pf:
                for item in json.load(pf):
                    if item.get('id') and item['id'] not in prev_dataset:
                        prev_dataset[item['id']] = item
        except Exception:
            pass

print(f"Reading dataset from: {SOURCE_DOC}")
with open(SOURCE_DOC, 'r', encoding='utf-8', errors='ignore') as f:
    raw_html = f.read()
    soup = BeautifulSoup(raw_html, 'html.parser')

main = soup.find('main')
paper_divs = []
if main:
    paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

dataset = []

if paper_divs:
    # Format 1: Rich Overview with <div class="paper">
    for p in paper_divs:
        pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
        theme_raw = p.find('span', class_='paper_type').get_text(strip=True) if p.find('span', class_='paper_type') else ''
        pformat = p.find('span', class_='paper_format').get_text(strip=True) if p.find('span', class_='paper_format') else ''
        topics = p.find('span', class_='paper_topics').get_text(strip=True) if p.find('span', class_='paper_topics') else ''
        keywords = p.find('span', class_='paper_keywords').get_text(strip=True) if p.find('span', class_='paper_keywords') else ''
        title = p.find('p', class_='paper_title').get_text(strip=True) if p.find('p', class_='paper_title') else ''
        
        m = re.search(r'Theme\s+(\d+):\s*(.*)', theme_raw)
        theme_num = int(m.group(1)) if m else 0
        theme_title = m.group(2).strip() if m else theme_raw
        
        m_top = re.search(r'(\d+\.\d+)\s*(.*)', topics)
        topic_code = m_top.group(1) if m_top else topics[:3]
        topic_title = m_top.group(2).strip() if m_top else topics
        
        authors = []
        presenter = None
        auth_tags = p.find_all('p', class_='paper_author')
        for a in auth_tags:
            authors.append(a.get_text(strip=True))
            if a.find('u'):
                presenter = a.find('u').get_text(strip=True)
                
        symp_authors = []
        symp_tags = p.find_all('p', class_='paper_symposium_authors')
        for s in symp_tags:
            symp_authors.append(s.get_text(" ", strip=True))
            
        org_tags = p.find_all('p', class_='paper_organisation')
        orgs = [o.get_text(" ", strip=True) for o in org_tags if o.get_text(strip=True)]
        
        pabstract_tags = p.find_all('p', class_='paper_abstract')
        abstract_text = "\n".join([a.get_text(strip=True) for a in pabstract_tags if a.get_text(strip=True)])
        
        affil_text = " ; ".join(orgs + symp_authors)
        countries = extract_countries(affil_text)
        
        if not countries:
            emails = re.findall(r'[\w\.-]+@([\w\.-]+)', affil_text + " " + " ".join(authors))
            for em in emails:
                parts = em.split('.')
                tld = parts[-1].lower()
                if tld in TLD_MAP and TLD_MAP[tld] not in countries:
                    countries.append(TLD_MAP[tld])
                if len(parts) >= 2 and parts[-2].lower() in ['ac', 'co', 'gov', 'org', 'edu']:
                    tld2 = parts[-1].lower()
                    if tld2 in TLD_MAP and TLD_MAP[tld2] not in countries:
                        countries.append(TLD_MAP[tld2])
                    
        if not countries and 'adebisi' in ' '.join(authors).lower():
            countries.append('Nigeria')

        if not countries:
            countries = ['Unknown']
            
        primary_country = countries[0]
        
        dataset.append({
            'id': pid,
            'theme_num': theme_num,
            'theme_title': theme_title,
            'format': pformat,
            'topic_code': topic_code,
            'topic_title': topic_title,
            'keywords': keywords,
            'title': title,
            'authors': authors,
            'presenter': presenter,
            'symp_authors': symp_authors,
            'orgs': orgs,
            'countries': countries,
            'primary_country': primary_country,
            'abstract': abstract_text,
            'abstract_word_count': len(abstract_text.split())
        })

else:
    # Format 2: ConfTool Table View <table ...>
    table = soup.find('table')
    rows = table.find_all('tr') if table else []
    
    for r in rows:
        cells = r.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        c0 = cells[0].get_text(strip=True)
        if not c0.isdigit():
            continue
        pid = c0
        
        col1 = cells[1]
        title_a = col1.find('a', href=lambda h: h and 'adminPapersDetails' in h)
        title = title_a.get_text(strip=True) if title_a else ""
        if not title:
            # Fallback to bold text
            b_tag = col1.find('span', class_='fontbold')
            title = b_tag.get_text(strip=True) if b_tag else ""
            
        em = col1.find('em')
        pformat = em.get_text(strip=True) if em else "Oral Presentation"
        
        col1_text = col1.get_text(" ", strip=True)
        m_theme = re.search(r'Theme\s+(\d+):\s*([^\.·]+)', col1_text)
        theme_num = int(m_theme.group(1)) if m_theme else 0
        theme_title = m_theme.group(2).strip() if m_theme else ""
        
        m_top = re.search(r'(\d+\.\d+)\s*([^·]+)', col1_text)
        topic_code = m_top.group(1) if m_top else ""
        topic_title = m_top.group(2).strip() if m_top else ""
        
        col2 = cells[2]
        u = col2.find('u')
        presenter = u.get_text(strip=True) if u else None
        
        bold_span = col2.find('span', class_='fontbold')
        authors_text = bold_span.get_text(strip=True) if bold_span else ""
        authors = [a.strip() for a in authors_text.split(';') if a.strip()]
        
        email_a = col2.find('a', href=lambda h: h and h.startswith('mailto:'))
        email = email_a['href'].replace('mailto:', '').strip() if email_a else ""
        
        lines = [line.strip() for line in col2.stripped_strings]
        org_candidates = [l for l in lines if l not in authors_text and '@' not in l and 'Send E-Mail' not in l]
        orgs = [l for l in org_candidates if l]
        
        # Check if we already have this paper in previous dataset
        prev_item = prev_dataset.get(pid, {})
        abstract_text = prev_item.get('abstract', '')
        keywords = prev_item.get('keywords', '')
        
        if not abstract_text:
            # Use title and topic title as abstract representation
            abstract_text = f"{title}. {topic_title}."
            
        # Country resolution
        countries = []
        if prev_item.get('primary_country') and prev_item['primary_country'] != 'Unknown':
            countries = prev_item.get('countries', [prev_item['primary_country']])
        else:
            affil_text = " ; ".join(orgs + lines + authors)
            countries = extract_countries(affil_text)
            if not countries and email:
                parts = email.split('.')
                tld = parts[-1].lower()
                if tld in TLD_MAP:
                    countries.append(TLD_MAP[tld])
                elif len(parts) >= 2 and parts[-2].lower() in ['ac', 'co', 'gov', 'org', 'edu']:
                    tld2 = parts[-1].lower()
                    if tld2 in TLD_MAP:
                        countries.append(TLD_MAP[tld2])
            if not countries and 'adebisi' in ' '.join(lines).lower():
                countries.append('Nigeria')
                
        if not countries:
            countries = ['Unknown']
            
        primary_country = countries[0]
        
        dataset.append({
            'id': pid,
            'theme_num': theme_num,
            'theme_title': theme_title,
            'format': pformat,
            'topic_code': topic_code,
            'topic_title': topic_title,
            'keywords': keywords,
            'title': title,
            'authors': authors,
            'presenter': presenter,
            'symp_authors': [],
            'orgs': orgs,
            'countries': countries,
            'primary_country': primary_country,
            'abstract': abstract_text,
            'abstract_word_count': len(abstract_text.split())
        })

print(f"Total processed: {len(dataset)}")

# Overall theme stats
print("\n" + "="*50)
print("THEME BREAKDOWN:")
theme_counts = Counter([d['theme_num'] for d in dataset])
for tnum in sorted(theme_counts.keys()):
    t_papers = [d for d in dataset if d['theme_num'] == tnum]
    t_name = t_papers[0]['theme_title'] if t_papers else 'Unknown'
    pct = len(t_papers)/len(dataset)*100 if len(dataset) > 0 else 0
    print(f"Theme {tnum}: {len(t_papers)} abstracts ({pct:.1f}%) | {t_name}")

# Country stats
print("\n" + "="*50)
print("COUNTRY STATS (Primary Country):")
country_primary_counts = Counter([d['primary_country'] for d in dataset])
print(f"Total Unique Primary Countries: {len(country_primary_counts)}")
for c, cnt in country_primary_counts.most_common(20):
    print(f"  {c}: {cnt}")

print("\nCOUNTRY STATS (All Participating Countries in Co-Authorship/Panels):")
all_country_counts = Counter()
for d in dataset:
    for c in set(d['countries']):
        all_country_counts[c] += 1
print(f"Total Unique Participating Countries: {len(all_country_counts)}")
for c, cnt in all_country_counts.most_common(20):
    print(f"  {c}: {cnt}")

# Focus on Theme 3
print("\n" + "="*50)
print("THEME 3 DEEP-DIVE:")
t3 = [d for d in dataset if d['theme_num'] == 3]
print(f"Theme 3 Total Submissions: {len(t3)}")
if t3:
    print(f"Theme 3 Title: {t3[0]['theme_title']}")
    t3_topics = Counter([f"{d['topic_code']} - {d['topic_title']}" for d in t3])
    print("Subtopics in Theme 3:")
    for top, cnt in t3_topics.most_common(5):
        print(f"  [{cnt}] {top}")
    t3_countries = Counter([d['primary_country'] for d in t3])
    print("Countries in Theme 3 (Primary):")
    for c, cnt in t3_countries.most_common(5):
        print(f"  {c}: {cnt}")
    t3_formats = Counter([d['format'] for d in t3])
    print("Formats in Theme 3:")
    for f, cnt in t3_formats.most_common():
        print(f"  {f}: {cnt}")

# Save full parsed dataset as JSON
with open('parsed_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
print(f"\nSaved parsed_dataset.json successfully with {len(dataset)} records!")
