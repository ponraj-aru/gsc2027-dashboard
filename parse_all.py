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
print(f"Total papers: {len(paper_divs)}")

papers_data = []

for p in paper_divs:
    pid_tag = p.find('span', class_='paper_id')
    pid = pid_tag.get_text(strip=True).replace('ID:', '').strip() if pid_tag else None
    
    ptype_tag = p.find('span', class_='paper_type')
    theme = ptype_tag.get_text(strip=True) if ptype_tag else None
    
    pformat_tag = p.find('span', class_='paper_format')
    pformat = pformat_tag.get_text(strip=True) if pformat_tag else None
    
    ptopics_tag = p.find('span', class_='paper_topics')
    topics = ptopics_tag.get_text(strip=True) if ptopics_tag else None
    
    pkeywords_tag = p.find('span', class_='paper_keywords')
    keywords = pkeywords_tag.get_text(strip=True) if pkeywords_tag else None
    
    ptitle_tag = p.find('p', class_='paper_title')
    title = ptitle_tag.get_text(strip=True) if ptitle_tag else None
    
    pauthor_tag = p.find('p', class_='paper_author')
    authors_text = pauthor_tag.get_text(strip=True) if pauthor_tag else None
    
    # Presenting author usually in <u>...</u>
    presenter = None
    if pauthor_tag and pauthor_tag.find('u'):
        presenter = pauthor_tag.find('u').get_text(strip=True)
        
    porg_tags = p.find_all('p', class_='paper_organisation')
    orgs = [o.get_text(" ", strip=True) for o in porg_tags if o.get_text(strip=True)]
    
    pabstract_tags = p.find_all('p', class_='paper_abstract')
    abstract_text = "\n".join([a.get_text(strip=True) for a in pabstract_tags if a.get_text(strip=True)])
    
    papers_data.append({
        'id': pid,
        'theme': theme,
        'format': pformat,
        'topics': topics,
        'keywords': keywords,
        'title': title,
        'authors': authors_text,
        'presenter': presenter,
        'organisations': orgs,
        'abstract': abstract_text
    })

print(f"Parsed {len(papers_data)} records.")

# Themes breakdown
from collections import Counter
themes = Counter([p['theme'] for p in papers_data])
print("\n--- THEMES BREAKDOWN ---")
for t, count in themes.most_common():
    print(f"{t}: {count}")

# Formats breakdown
formats = Counter([p['format'] for p in papers_data])
print("\n--- FORMATS BREAKDOWN ---")
for fmt, count in formats.most_common():
    print(f"{fmt}: {count}")

# Topics breakdown
topics = Counter([p['topics'] for p in papers_data])
print(f"\n--- UNIQUE TOPICS COUNT: {len(topics)} ---")
for top, count in topics.most_common(15):
    print(f"  {top}: {count}")

# Sample organizations to see country patterns
print("\n--- SAMPLE ORGANISATIONS (first 25) ---")
for p in papers_data[:25]:
    print(f"ID {p['id']}: {p['organisations']}")
