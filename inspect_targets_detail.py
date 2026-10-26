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

# Let's inspect the 25 papers specifically
target_ids = ['103', '109', '131', '161', '165', '189', '198', '229', '233', '238', 
              '241', '251', '271', '277', '297', '311', '328', '336', '340', '367', 
              '376', '384', '385', '386', '391']

for p in paper_divs:
    pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
    if pid in target_ids:
        print(f"\n================ ID {pid} ================")
        print("Title:", p.find('p', class_='paper_title').get_text(strip=True) if p.find('p', class_='paper_title') else '')
        print("Format:", p.find('span', class_='paper_format').get_text(strip=True) if p.find('span', class_='paper_format') else '')
        print("Authors:", [a.get_text(strip=True) for a in p.find_all('p', class_='paper_author')])
        print("Symposium Authors:", [s.get_text(" ", strip=True) for s in p.find_all('p', class_='paper_symposium_authors')])
        print("Orgs:", [o.get_text(" ", strip=True) for o in p.find_all('p', class_='paper_organisation')])
