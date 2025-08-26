import create_translations
from bs4 import BeautifulSoup
import csv

paths = create_translations.get_translation_paths()
source_paths = create_translations.find_all_files_recursive('source/', lambda x: x.endswith('.html'))
all_keys = set()
for path in source_paths:
    with open(path, encoding='utf-8') as inputf:
        html_doc = inputf.read() 
        soup = BeautifulSoup(html_doc, 'html.parser')
        text = soup.get_text()
        text_elements = set([t.strip() for t in text.split('\n') if len(t) > 0])
        #print(text_elements)
        all_keys.update(text_elements)

for path in paths:
    existing_mapping = create_translations.load_translation_mapping(path)
    with open(path, "w", encoding="utf-8") as outf:
        writer = csv.writer(outf, delimiter='\t')
        initial_keys = set(existing_mapping)
        for key in sorted(all_keys):
            if key.strip() == "":
                continue
            if key in initial_keys:
                initial_keys.remove(key)
            value = existing_mapping.get(key, "")
            print(key, value)
            writer.writerow([key, value])
        remaining_keys = set()
        for remaining_key in initial_keys:
            if "href" in remaining_key:
                value = existing_mapping.get(remaining_key, "")
                writer.writerow([remaining_key, value])
            else:
                remaining_keys.add(remaining_key)
    with open(path + ".deprecated", "a", encoding="utf-8") as outf:
        writer = csv.writer(outf, delimiter='\t')
        for remaining_key in remaining_keys:
            value = existing_mapping.get(remaining_key, "")
            writer.writerow([remaining_key, value])
