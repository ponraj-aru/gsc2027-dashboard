import json
import pandas as pd

with open('parsed_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

rows = []
for d in dataset:
    rows.append({
        'ID': d['id'],
        'Title': d['title'],
        'Theme_Number': d['theme_num'],
        'Theme_Title': d['theme_title'],
        'Topic_Code': d['topic_code'],
        'Topic_Title': d['topic_title'],
        'Presentation_Format': d['format'],
        'Authors': "; ".join(d['authors']) if d['authors'] else "; ".join(d['symp_authors']),
        'Presenter': d['presenter'] or '',
        'Organisations': " | ".join(d['orgs']) if d['orgs'] else "; ".join(d['symp_authors']),
        'Primary_Country': d['primary_country'],
        'All_Countries': ", ".join(d['countries']),
        'Keywords': d['keywords'] or '',
        'Abstract_Word_Count': d['abstract_word_count'],
        'Abstract_Text': d['abstract']
    })

df = pd.DataFrame(rows)
df.to_csv('GSC2027_Abstract_Submissions_Master.csv', index=False, encoding='utf-8-sig')

try:
    df.to_excel('GSC2027_Abstract_Submissions_Master.xlsx', index=False)
    print("Successfully exported GSC2027_Abstract_Submissions_Master.xlsx and .csv")
except Exception as e:
    print("Excel export notice:", e)
