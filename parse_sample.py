from source_config import SOURCE_DOC
import sys
import codecs
from bs4 import BeautifulSoup
import re

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open(SOURCE_DOC, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Get top-level paper divs (children of main that are div.paper)
main = soup.find('main')
paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]
print(f"Top-level paper divs in main: {len(paper_divs)}")

for i in range(min(10, len(paper_divs))):
    p = paper_divs[i]
    pid = p.find('span', class_='paper_id')
    ptype = p.find('span', class_='paper_type')
    pformat = p.find('span', class_='paper_format')
    ptopics = p.find('span', class_='paper_topics')
    pkeywords = p.find('span', class_='paper_keywords')
    ptitle = p.find('p', class_='paper_title')
    pauthor = p.find('p', class_='paper_author')
    porg = p.find_all('p', class_='paper_organisation')
    pabstract = p.find_all('p', class_='paper_abstract')
    
    print(f"\n================ PAPER #{i+1} ================")
    print("ID:", pid.get_text(strip=True) if pid else None)
    print("Type/Theme:", ptype.get_text(strip=True) if ptype else None)
    print("Format:", pformat.get_text(strip=True) if pformat else None)
    print("Topics:", ptopics.get_text(strip=True) if ptopics else None)
    print("Keywords:", pkeywords.get_text(strip=True) if pkeywords else None)
    print("Title:", ptitle.get_text(strip=True) if ptitle else None)
    print("Authors:", pauthor.get_text(strip=True) if pauthor else None)
    print("Organisations:", [o.get_text(strip=True) for o in porg])
    abstract_text = "\n".join([a.get_text(strip=True) for a in pabstract if a.get_text(strip=True)])
    print("Abstract (len):", len(abstract_text), "Snippet:", repr(abstract_text[:120]))
