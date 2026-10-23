import sys
import codecs
from bs4 import BeautifulSoup
import re
import json

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open('adminPapersBrowse_2026-10-19_09-37-14.doc', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

print(f"Total papers: {len(paper_divs)}")

# Let's inspect the organisation text for each paper
org_texts = []
for p in paper_divs:
    pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
    porg_tags = p.find_all('p', class_='paper_organisation')
    orgs = " || ".join([o.get_text(" ", strip=True) for o in porg_tags if o.get_text(strip=True)])
    title = p.find('p', class_='paper_title').get_text(strip=True) if p.find('p', class_='paper_title') else ''
    authors = p.find('p', class_='paper_author').get_text(strip=True) if p.find('p', class_='paper_author') else ''
    org_texts.append((pid, authors, title, orgs))

# Let's see what country names or tokens appear after commas or semicolons
print(f"Sample of 50 organisation strings:")
for pid, auth, title, org in org_texts[:50]:
    print(f"[{pid}] {org}")
