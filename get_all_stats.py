import json
from collections import Counter

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

print("="*60)
print(f"TOTAL ABSTRACTS ANALYZED: {len(dataset)}")
print("="*60)

for tnum in range(1, 6):
    t_papers = [d for d in dataset if d['theme_num'] == tnum]
    tname = t_papers[0]['theme_title'] if t_papers else ''
    pct = len(t_papers) / len(dataset) * 100
    print(f"\nTHEME {tnum}: {tname}")
    print(f"Total Submissions: {len(t_papers)} ({pct:.1f}%)")
    
    # Subtopics
    topics = Counter([f"{d['topic_code']}: {d['topic_title']}" for d in t_papers])
    print("Subtopics:")
    for top, c in sorted(topics.items(), key=lambda x: x[0]):
        print(f"   * {top}: {c} ({c/len(t_papers)*100:.1f}%)")
        
    # Formats
    fmts = Counter([d['format'] for d in t_papers])
    print("Formats: " + ", ".join([f"{k}: {v}" for k, v in fmts.items()]))
    
    # Top 5 Countries
    cntrs = Counter([d['primary_country'] for d in t_papers])
    print("Top Countries: " + ", ".join([f"{k} ({v})" for k, v in cntrs.most_common(5)]))
