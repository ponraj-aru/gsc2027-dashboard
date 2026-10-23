import sys
import codecs
from bs4 import BeautifulSoup
import re
import json
import glob
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
    (r'\b(australia)\b', 'Australia'),
    (r'\b(austria)\b', 'Austria'),
    (r'\b(azerbaijan)\b', 'Azerbaijan'),
    (r'\b(bangladesh|people\'s republic of bangladesh)\b', 'Bangladesh'),
    (r'\b(belgium|vub|ku leuven|gent university|ghent university|antwerp)\b', 'Belgium'),
    (r'\b(benin)\b', 'Benin'),
    (r'\b(bhutan)\b', 'Bhutan'),
    (r'\b(bolivia)\b', 'Bolivia'),
    (r'\b(botswana)\b', 'Botswana'),
    (r'\b(brazil|brasil|unisantos|faap)\b', 'Brazil'),
    (r'\b(bulgaria)\b', 'Bulgaria'),
    (r'\b(burkina faso)\b', 'Burkina Faso'),
    (r'\b(burundi)\b', 'Burundi'),
    (r'\b(cambodia)\b', 'Cambodia'),
    (r'\b(cameroon)\b', 'Cameroon'),
    (r'\b(canada|brocku|brock university)\b', 'Canada'),
    (r'\b(chile)\b', 'Chile'),
    (r'\b(china|peking university|tsinghua|chinese academy of sciences|nanjing|chongqing|guangdong|huazhong)\b', 'China'),
    (r'\b(colombia)\b', 'Colombia'),
    (r'\b(costa rica)\b', 'Costa Rica'),
    (r'\b(croatia)\b', 'Croatia'),
    (r'\b(cyprus)\b', 'Cyprus'),
    (r'\b(czech republic|czechia)\b', 'Czech Republic'),
    (r'\b(denmark)\b', 'Denmark'),
    (r'\b(congo|dr congo|democratic republic of the congo|d\.r\. congo|bukavu)\b', 'DR Congo'),
    (r'\b(ecuador|universidad de cuenca|escuela politécnica nacional|escuela politecnica nacional)\b', 'Ecuador'),
    (r'\b(egypt)\b', 'Egypt'),
    (r'\b(estonia)\b', 'Estonia'),
    (r'\b(ethiopia)\b', 'Ethiopia'),
    (r'\b(fiji)\b', 'Fiji'),
    (r'\b(finland|helsinki)\b', 'Finland'),
    (r'\b(france|montpellier|sorbonne|paris)\b', 'France'),
    (r'\b(gambia|the gambia)\b', 'The Gambia'),
    (r'\b(georgia)\b', 'Georgia'),
    (r'\b(germany|deutschland|max planck|dresden|helmholtz|lausitz)\b', 'Germany'),
    (r'\b(ghana)\b', 'Ghana'),
    (r'\b(greece)\b', 'Greece'),
    (r'\b(guatemala)\b', 'Guatemala'),
    (r'\b(hungary)\b', 'Hungary'),
    (r'\b(iceland)\b', 'Iceland'),
    (r'\b(india|iisc|iit|iim kolkata|delhi university|bhopal|nidm)\b', 'India'),
    (r'\b(indonesia|yogyakarta|komnas ham|sebelas maret|warmadewa)\b', 'Indonesia'),
    (r'\b(iran)\b', 'Iran'),
    (r'\b(iraq)\b', 'Iraq'),
    (r'\b(ireland)\b', 'Ireland'),
    (r'\b(israel)\b', 'Israel'),
    (r'\b(italy|italia|udine|bologna|rome|milan)\b', 'Italy'),
    (r'\b(ivory coast|côte d\'ivoire|cote d\'ivoire)\b', 'Ivory Coast'),
    (r'\b(japan|tokyo|kyoto|hayama)\b', 'Japan'),
    (r'\b(jordan)\b', 'Jordan'),
    (r'\b(kazakhstan)\b', 'Kazakhstan'),
    (r'\b(kenya|nairobi)\b', 'Kenya'),
    (r'\b(kuwait)\b', 'Kuwait'),
    (r'\b(kyrgyzstan)\b', 'Kyrgyzstan'),
    (r'\b(latvia)\b', 'Latvia'),
    (r'\b(lebanon|lebanese republic)\b', 'Lebanon'),
    (r'\b(luxembourg)\b', 'Luxembourg'),
    (r'\b(madagascar)\b', 'Madagascar'),
    (r'\b(malawi)\b', 'Malawi'),
    (r'\b(malaysia)\b', 'Malaysia'),
    (r'\b(maldives)\b', 'Maldives'),
    (r'\b(mexico)\b', 'Mexico'),
    (r'\b(moldova)\b', 'Moldova'),
    (r'\b(mongolia)\b', 'Mongolia'),
    (r'\b(morocco)\b', 'Morocco'),
    (r'\b(mozambique)\b', 'Mozambique'),
    (r'\b(myanmar)\b', 'Myanmar'),
    (r'\b(namibia)\b', 'Namibia'),
    (r'\b(nepal|kathmandu|tribhuvan|chitwan|fncsi)\b', 'Nepal'),
    (r'\b(netherlands|netherlands, the|the netherlands|holland|groningen|rotterdam|utrecht|amsterdam|vu amsterdam|thuas|rug|erasmus|fse|fss|esrig|wageningen|leiden|delft|twente)\b', 'Netherlands'),
    (r'\b(new zealand|auckland)\b', 'New Zealand'),
    (r'\b(nigeria|uniosun|osun|adebisi|ilorin|ibadan)\b', 'Nigeria'),
    (r'\b(norway|oslo)\b', 'Norway'),
    (r'\b(oman)\b', 'Oman'),
    (r'\b(pakistan|multan|rawalpindi)\b', 'Pakistan'),
    (r'\b(palestine|aaup)\b', 'Palestine'),
    (r'\b(peru)\b', 'Peru'),
    (r'\b(philippines|davao del norte)\b', 'Philippines'),
    (r'\b(poland|polska|jagiellonian|warsaw|krakow)\b', 'Poland'),
    (r'\b(portugal|lisbon|porto)\b', 'Portugal'),
    (r'\b(qatar)\b', 'Qatar'),
    (r'\b(romania|ploiesti)\b', 'Romania'),
    (r'\b(russia|russian federation)\b', 'Russia'),
    (r'\b(rwanda)\b', 'Rwanda'),
    (r'\b(saudi arabia)\b', 'Saudi Arabia'),
    (r'\b(senegal)\b', 'Senegal'),
    (r'\b(serbia)\b', 'Serbia'),
    (r'\b(singapore)\b', 'Singapore'),
    (r'\b(slovakia)\b', 'Slovakia'),
    (r'\b(slovenia)\b', 'Slovenia'),
    (r'\b(south africa|kwazulu-natal|ukzn|cape town|johannesburg|pretoria|stellenbosch)\b', 'South Africa'),
    (r'\b(south korea|korea, republic of|republic of korea|korea)\b', 'South Korea'),
    (r'\b(spain|españa|zaragoza|valladolid|madrid|barcelona)\b', 'Spain'),
    (r'\b(sri lanka|colombo)\b', 'Sri Lanka'),
    (r'\b(sudan)\b', 'Sudan'),
    (r'\b(sweden|sverige|stockholm|uppsala|södertörn|sodertorn|lund)\b', 'Sweden'),
    (r'\b(switzerland|geneva|zurich|eth zurich)\b', 'Switzerland'),
    (r'\b(taiwan)\b', 'Taiwan'),
    (r'\b(tanzania)\b', 'Tanzania'),
    (r'\b(thailand|chulalongkorn|srinakharinwirot|ait|asian institute of technology|bangkok)\b', 'Thailand'),
    (r'\b(tunisia)\b', 'Tunisia'),
    (r'\b(turkey|türkiye)\b', 'Turkey'),
    (r'\b(uganda)\b', 'Uganda'),
    (r'\b(ukraine)\b', 'Ukraine'),
    (r'\b(united arab emirates|uae|abu dhabi|dubai|mbzuai)\b', 'United Arab Emirates'),
    (r'\b(united kingdom|uk|great britain|england|scotland|wales|oxford|cambridge|imperial college|sheffield|uofsussex|sussex|brunel|essex|liverpool|london|nature portfolio)\b', 'United Kingdom'),
    (r'\b(united states|unites states|usa|united states of america|clemson|uta|maryland|harvard|stanford|columbia university|mit)\b', 'United States'),
    (r'\b(uruguay)\b', 'Uruguay'),
    (r'\b(uzbekistan)\b', 'Uzbekistan'),
    (r'\b(venezuela)\b', 'Venezuela'),
    (r'\b(vietnam|viet nam)\b', 'Vietnam'),
    (r'\b(yemen)\b', 'Yemen'),
    (r'\b(zambia)\b', 'Zambia'),
    (r'\b(zimbabwe)\b', 'Zimbabwe')
]

TLD_MAP = {
    'nl': 'Netherlands', 'de': 'Germany', 'uk': 'United Kingdom', 'np': 'Nepal',
    'in': 'India', 'za': 'South Africa', 'ng': 'Nigeria', 'ec': 'Ecuador',
    'br': 'Brazil', 'be': 'Belgium', 'es': 'Spain', 'fr': 'France',
    'it': 'Italy', 'ro': 'Romania', 'se': 'Sweden', 'jp': 'Japan',
    'cn': 'China', 'id': 'Indonesia', 'bd': 'Bangladesh', 'th': 'Thailand',
    'md': 'Moldova', 'ca': 'Canada', 'pk': 'Pakistan', 'us': 'United States',
    'edu': 'United States', 'ch': 'Switzerland', 'at': 'Austria', 'au': 'Australia',
    'eg': 'Egypt', 'ke': 'Kenya', 'my': 'Malaysia', 'ph': 'Philippines'
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

def get_latest_doc_file():
    doc_files = sorted(glob.glob('adminPapersBrowse_*.doc'))
    if not doc_files:
        raise FileNotFoundError("No adminPapersBrowse_*.doc file found in the workspace.")
    return doc_files[-1]

def parse_and_process(doc_path=None):
    if not doc_path:
        doc_path = get_latest_doc_file()
    print(f"Reading dataset from: {doc_path}")

    with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    main = soup.find('main')
    paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

    dataset = []

    for p in paper_divs:
        pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
        theme_raw = p.find('span', class_='paper_type').get_text(strip=True) if p.find('span', class_='paper_type') else ''
        pformat = p.find('span', class_='paper_format').get_text(strip=True) if p.find('span', class_='paper_format') else ''
        topics = p.find('span', class_='paper_topics').get_text(strip=True) if p.find('span', class_='paper_topics') else ''
        keywords = p.find('span', class_='paper_keywords').get_text(strip=True) if p.find('span', class_='paper_keywords') else ''
        title = p.find('p', class_='paper_title').get_text(strip=True) if p.find('p', class_='paper_title') else ''
        
        # Theme short name & number
        m = re.search(r'Theme\s+(\d+):\s*(.*)', theme_raw)
        theme_num = int(m.group(1)) if m else 0
        theme_title = m.group(2).strip() if m else theme_raw
        
        # Subtopic code & title
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
        
        # Affiliation text
        affil_text = " ; ".join(orgs + symp_authors)
        countries = extract_countries(affil_text)
        
        if not countries:
            emails = re.findall(r'[\w\.-]+@([\w\.-]+)', affil_text + " " + " ".join(authors))
            for em in emails:
                parts = em.split('.')
                tld = parts[-1].lower()
                if tld in TLD_MAP and TLD_MAP[tld] not in countries:
                    countries.append(TLD_MAP[tld])
                if len(parts) >= 2 and parts[-2].lower() in ['ac', 'co', 'gov', 'org']:
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

    print(f"Total processed: {len(dataset)}")

    # Overall theme stats
    print("\n" + "="*50)
    print("THEME BREAKDOWN:")
    theme_counts = Counter([d['theme_num'] for d in dataset])
    for tnum in sorted(theme_counts.keys()):
        t_papers = [d for d in dataset if d['theme_num'] == tnum]
        t_name = t_papers[0]['theme_title'] if t_papers else 'Unknown'
        print(f"Theme {tnum}: {len(t_papers)} abstracts ({len(t_papers)/len(dataset)*100:.1f}%) | {t_name}")

    # Country stats
    print("\n" + "="*50)
    print("COUNTRY STATS (Primary Country):")
    country_primary_counts = Counter([d['primary_country'] for d in dataset])
    print(f"Total Unique Primary Countries: {len(country_primary_counts)}")
    for c, cnt in country_primary_counts.most_common(20):
        print(f"  {c}: {cnt}")

    # Save full parsed dataset as JSON for subsequent processing
    with open('parsed_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"\nSaved parsed_dataset.json successfully with {len(dataset)} records!")
    return dataset

if __name__ == '__main__':
    parse_and_process()
