from source_config import SOURCE_DOC
import sys
import codecs
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open(SOURCE_DOC, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

target_ids = ['131', '189', '238', '241', '251', '271', '277', '297', '311', '336', '376', '384', '385', '386', '391']

for p in paper_divs:
    pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
    if pid in target_ids:
        print(f"\n================ ID {pid} ================")
        symp = p.find_all('p', class_='paper_symposium_authors')
        for s in symp:
            print("  Symposium authors tag:", s.get_text(" ", strip=True))
        # check any other author or org tags
        auth = p.find_all('p', class_='paper_author')
        org = p.find_all('p', class_='paper_organisation')
        print("  Standard auth tags:", [a.get_text(strip=True) for a in auth])
        print("  Standard org tags:", [o.get_text(strip=True) for o in org])
