import json
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Custom domain stopwords to filter out generic academic/conference filler words
custom_stopwords = set(STOPWORDS)
custom_stopwords.update([
    'study', 'paper', 'research', 'results', 'using', 'based', 'used', 'method',
    'methods', 'data', 'analysis', 'findings', 'approach', 'aims', 'examine',
    'examines', 'examined', 'analyzes', 'analyzed', 'shows', 'concludes', 'aim',
    'objective', 'also', 'provide', 'provides', 'providing', 'focuses', 'focused',
    'focus', 'article', 'discuss', 'discusses', 'discussed', 'highlight', 'highlights',
    'well', 'new', 'one', 'two', 'three', 'may', 'can', 'will', 'across', 'including',
    'within', 'among', 'present', 'presents', 'presented', 'towards', 'however',
    'furthermore', 'moreover', 'significant', 'significantly', 'case', 'cases',
    'table', 'figure', 'section', 'author', 'authors', 'et', 'al', 'gsc2027', 'abstract'
])

def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s-]', ' ', text)
    words = text.split()
    return [w for w in words if len(w) > 3 and w not in custom_stopwords and not w.isdigit()]

# Word frequencies per theme
theme_words = {}
for tnum in [1, 2, 3, 4, 5]:
    t_papers = [d for d in dataset if d['theme_num'] == tnum]
    all_words = []
    all_kw = []
    for d in t_papers:
        all_words.extend(clean_and_tokenize(d['abstract']))
        if d['keywords']:
            kws = [k.strip().lower() for k in re.split(r'[,;]\s*', d['keywords']) if k.strip()]
            all_kw.extend([k for k in kws if len(k) > 2])
            
    word_freq = Counter(all_words)
    kw_freq = Counter(all_kw)
    theme_words[tnum] = {
        'top_words': word_freq.most_common(25),
        'top_keywords': kw_freq.most_common(15)
    }

print("=== THEME WORD CLUSTERS ===")
for tnum, data in theme_words.items():
    print(f"\n--- THEME {tnum} Top Words ---")
    print(", ".join([f"{w} ({c})" for w, c in data['top_words'][:15]]))
    print(f"--- THEME {tnum} Top Keywords ---")
    print(", ".join([f"{k} ({c})" for k in data['top_keywords'][:10]]))
