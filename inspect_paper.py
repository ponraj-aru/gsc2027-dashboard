import sys
import codecs
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

doc_path = r'adminPapersBrowse_2026-10-19_09-37-14.doc'

with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

papers = soup.find_all('div', class_='paper')
print(f'Total paper divs found: {len(papers)}')

first_paper = papers[0]
print("--- FIRST PAPER HTML ---")
print(first_paper.prettify()[:4000])

print("\n--- SECOND PAPER HTML ---")
print(papers[1].prettify()[:4000])
