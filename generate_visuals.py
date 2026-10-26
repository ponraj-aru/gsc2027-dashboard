import json
import re
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json as _j
_DS = _j.load(open('parsed_dataset.json', encoding='utf-8'))
TOTAL_N = len(_DS)
NATIONS_N = len({d['primary_country'] for d in _DS if d.get('primary_country')})


# Load dataset
with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

os.makedirs('visuals', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Custom Stopwords & Word Clouds
# -----------------------------------------------------------------------------
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
    'important', 'specific', 'various', 'show', 'potential', 'role', 'roles'
])

def generate_wordcloud(texts, filename, colormap='teal', title=''):
    combined = " ".join(texts).lower()
    combined = re.sub(r'[^a-z\s-]', ' ', combined)
    
    wc = WordCloud(
        width=1200, height=650,
        background_color='#0B132B',
        colormap=colormap,
        stopwords=custom_stopwords,
        max_words=100,
        contour_width=0,
        collocations=False,
        prefer_horizontal=0.85,
        random_state=42
    ).generate(combined)
    
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=200)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    if title:
        plt.title(title, fontsize=16, color='white', pad=15, weight='bold')
    plt.tight_layout(pad=0)
    plt.savefig(f'visuals/{filename}', facecolor='#0B132B', edgecolor='none')
    plt.close()

# Generate word clouds for all themes
theme_cmaps = {
    1: 'autumn',
    2: 'summer',
    3: 'plasma',    # Theme 3 vibrant
    4: 'cool',
    5: 'spring'
}

for tnum in range(1, 6):
    t_texts = [d['abstract'] + " " + (d['keywords'] or '') for d in dataset if d['theme_num'] == tnum]
    generate_wordcloud(t_texts, f'wordcloud_theme{tnum}.png', colormap=theme_cmaps[tnum])

# Overall word cloud
all_texts = [d['abstract'] + " " + (d['keywords'] or '') for d in dataset]
generate_wordcloud(all_texts, 'wordcloud_overall.png', colormap='viridis')
print("Generated all word clouds successfully!")

# -----------------------------------------------------------------------------
# 2. Matplotlib Theme Distribution Chart
# -----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

themes_data = [
    ('Theme 2: Resilience Across Systems', 76, '#059669'),
    ('Theme 3: Climate Change–Development Nexus', 75, '#2563EB'),
    ('Theme 1: Lessons from SDGs Beyond 2030', 60, '#D97706'),
    ('Theme 4: Health & Well-being Foundations', 45, '#7C3AED'),
    ('Theme 5: AI, Big Data & Digitalization', 45, '#0284C7')
]

labels = [x[0] for x in themes_data]
counts = [x[1] for x in themes_data]
colors = [x[2] for x in themes_data]

bars = ax.barh(labels[::-1], counts[::-1], color=colors[::-1], height=0.6, edgecolor='none')
ax.set_xlabel('Number of Abstract Submissions', fontsize=12, fontweight='bold', color='#1E293B', labelpad=10)
ax.set_title(f'Abstract Submissions by Theme (Total: {TOTAL_N} Submissions)', fontsize=14, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.grid(axis='y', visible=False)

for bar in bars:
    w = bar.get_width()
    pct = w / TOTAL_N * 100
    ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f'{int(w)} ({pct:.1f}%)', 
            va='center', ha='left', fontsize=11, fontweight='bold', color='#1E293B')

ax.set_xlim(0, 90)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#94A3B8')
ax.spines['bottom'].set_color('#94A3B8')
ax.tick_params(axis='both', colors='#334155', labelsize=10.5)
plt.tight_layout()
plt.savefig('visuals/chart_themes.png', facecolor='#FFFFFF', dpi=200)
plt.close()
print("Generated chart_themes.png successfully!")

# -----------------------------------------------------------------------------
# 3. Matplotlib Theme 3 Subtopics Breakdown Chart
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=200)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

t3_subtopics = [
    ('3.2 Actions for Climate Adaptation & Resilience', 23, '#2563EB'),
    ('3.5 Climate Governance, Finance & Negotiation', 22, '#3B82F6'),
    ('3.3 Mitigation & Net-Zero Just Transition Pathways', 16, '#60A5FA'),
    ('3.4 Climate Actions for Human Security', 9, '#93C5FD'),
    ('3.1 Earth System Modeling & Climate Impacts', 5, '#BFDBFE')
]

t3_labels = [x[0] for x in t3_subtopics]
t3_counts = [x[1] for x in t3_subtopics]
t3_colors = [x[2] for x in t3_subtopics]

bars = ax.barh(t3_labels[::-1], t3_counts[::-1], color=t3_colors[::-1], height=0.58)
ax.set_xlabel('Number of Submissions in Theme 3', fontsize=12, fontweight='bold', color='#1E293B', labelpad=10)
ax.set_title('Theme 3 Subtopics Breakdown (Total: 75 Submissions, 24.9% of Conference)', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.grid(axis='y', visible=False)

for bar in bars:
    w = bar.get_width()
    pct = w / 75 * 100
    ax.text(w + 0.4, bar.get_y() + bar.get_height()/2, f'{int(w)} ({pct:.1f}%)', 
            va='center', ha='left', fontsize=11, fontweight='bold', color='#1E293B')

ax.set_xlim(0, 27)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#94A3B8')
ax.spines['bottom'].set_color('#94A3B8')
ax.tick_params(axis='both', colors='#334155', labelsize=10.5)
plt.tight_layout()
plt.savefig('visuals/chart_theme3_subtopics.png', facecolor='#FFFFFF', dpi=200)
plt.close()
print("Generated chart_theme3_subtopics.png successfully!")

# -----------------------------------------------------------------------------
# 4. Top 15 Submitting Countries Chart
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6), dpi=200)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

country_counts = Counter([d['primary_country'] for d in dataset])
top15 = country_counts.most_common(15)

c_names = [x[0] for x in top15]
c_vals = [x[1] for x in top15]

bars = ax.barh(c_names[::-1], c_vals[::-1], color='#0D9488', height=0.6)
ax.set_xlabel('Number of Submissions (Primary Country)', fontsize=12, fontweight='bold', color='#1E293B', labelpad=10)
ax.set_title('Top 15 Submitting Countries (Representing 66 Total Participating Nations)', fontsize=13, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.grid(axis='y', visible=False)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.4, bar.get_y() + bar.get_height()/2, f'{int(w)}', 
            va='center', ha='left', fontsize=10.5, fontweight='bold', color='#1E293B')

ax.set_xlim(0, 30)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#94A3B8')
ax.spines['bottom'].set_color('#94A3B8')
ax.tick_params(axis='both', colors='#334155', labelsize=10)
plt.tight_layout()
plt.savefig('visuals/chart_top_countries.png', facecolor='#FFFFFF', dpi=200)
plt.close()
print("Generated chart_top_countries.png successfully!")

# -----------------------------------------------------------------------------
# 5. Presentation Formats Donut Chart
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.2), dpi=200)
fig.patch.set_facecolor('#FFFFFF')
fmt_counts = Counter([d['format'] for d in dataset])
f_labels = list(fmt_counts.keys())
f_vals = list(fmt_counts.values())
f_colors = ['#2563EB', '#059669', '#D97706', '#7C3AED']

wedges, texts, autotexts = ax.pie(
    f_vals, labels=None, autopct='%1.1f%%', startangle=140,
    pctdistance=0.75, colors=f_colors,
    textprops=dict(color="white", weight="bold", fontsize=11),
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
)

legend_labels = [f"{l}: {v} ({v/TOTAL_N*100:.1f}%)" for l, v in zip(f_labels, f_vals)]
ax.legend(wedges, legend_labels, title="Session Format", loc="center left", bbox_to_anchor=(0.95, 0.5), frameon=False, fontsize=10.5)
ax.set_title(f"Abstracts by Presentation Format (Total: {TOTAL_N})", fontsize=13, fontweight='bold', color='#0F172A', pad=10)
plt.tight_layout()
plt.savefig('visuals/chart_formats.png', facecolor='#FFFFFF', dpi=200)
plt.close()
print("Generated chart_formats.png successfully!")
