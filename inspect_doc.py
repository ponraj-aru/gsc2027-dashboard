from source_config import SOURCE_DOC
import os
from bs4 import BeautifulSoup
import re

doc_path = SOURCE_DOC

with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
children = [c for c in main.children if c.name]
print(f'Total children of main: {len(children)}')

for i in range(min(15, len(children))):
    c = children[i]
    print(f"Child {i}: <{c.name} class='{c.get('class')}'> text: {c.get_text()[:150].strip()!r}")
