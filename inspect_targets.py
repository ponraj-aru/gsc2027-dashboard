import sys
import codecs
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open('adminPapersBrowse_2026-10-19_09-37-14.doc', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
paper_divs = [c for c in main.children if c.name == 'div' and 'paper' in c.get('class', [])]

target_ids = ['131', '189', '238', '241', '251', '271', '277', '297', '311', '336', '376', '384', '385', '386', '391']

for p in paper_divs:
    pid = p.find('span', class_='paper_id').get_text(strip=True).replace('ID:', '').strip()
    if pid in target_ids:
        print(f"=== ID {pid} ===")
        for child in p.find_all(recursive=False):
            print(f"  <{child.name} class='{child.get('class')}'>: {child.get_text(strip=True)[:120]}")
