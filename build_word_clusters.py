import json
import re
from collections import Counter
from wordcloud import STOPWORDS
import pandas as pd

def build_clusters():
    with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)

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
        'table', 'figure', 'section', 'author', 'authors', 'et', 'al', 'gsc2027', 'abstract',
        'first', 'second', 'need', 'needs', 'different', 'order', 'many', 'key', 'main',
        'important', 'specific', 'various', 'show', 'potential', 'role', 'roles', 'number',
        'due', 'well', 'high', 'level', 'levels', 'process', 'processes', 'context'
    ])

    def clean_and_tokenize(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s-]', ' ', text)
        words = text.split()
        return [w for w in words if len(w) > 3 and w not in custom_stopwords and not w.isdigit()]

    word_clusters = {}

    # Process Overall and Themes 1 to 5
    themes_to_process = [
        (0, f"All Themes ({len(dataset)} Abstracts)"),
        (1, "Theme 1: Lessons from the SDGs beyond 2030"),
        (2, "Theme 2: Building resilience across natural and human systems"),
        (3, "Theme 3: Navigating the climate change–development nexus"),
        (4, "Theme 4: Health, well-being, and societal foundations"),
        (5, "Theme 5: AI, big data, and digitalization as enablers")
    ]

    for tnum, ttitle in themes_to_process:
        if tnum == 0:
            papers = dataset
        else:
            papers = [d for d in dataset if d['theme_num'] == tnum]
            
        all_words = []
        all_kw = []
        for d in papers:
            all_words.extend(clean_and_tokenize(d['abstract']))
            if d['keywords']:
                kws = [k.strip().lower() for k in re.split(r'[,;]\s*', d['keywords']) if k.strip()]
                all_kw.extend([k for k in kws if len(k) > 2])
                
        word_freq = Counter(all_words)
        kw_freq = Counter(all_kw)
        
        total_words = len(all_words)
        top_words = [{'word': w, 'count': c, 'pct': round(c / total_words * 100, 2) if total_words > 0 else 0} for w, c in word_freq.most_common(35)]
        top_keywords = [{'keyword': k, 'count': c} for k, c in kw_freq.most_common(15)]
        
        word_clusters[str(tnum)] = {
            'theme_num': tnum,
            'theme_title': ttitle,
            'papers_count': len(papers),
            'total_words': total_words,
            'top_words': top_words,
            'top_keywords': top_keywords
        }

    with open('word_clusters_data.json', 'w', encoding='utf-8') as f:
        json.dump(word_clusters, f, ensure_ascii=False, indent=2)

    print("word_clusters_data.json successfully generated!")
    print(f"Sample Theme 1 top words: {[w['word'] for w in word_clusters['1']['top_words'][:10]]}")
    print(f"Sample Theme 3 top words: {[w['word'] for w in word_clusters['3']['top_words'][:10]]}")
    return word_clusters

if __name__ == '__main__':
    build_clusters()
