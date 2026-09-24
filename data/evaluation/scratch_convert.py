import json
import os

source_path = 'data/evaluation/golden_questions.json'
dest_dir = 'data/evaluation'
dest_path = os.path.join(dest_dir, 'golden_dataset.json')

os.makedirs(dest_dir, exist_ok=True)

with open(source_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []
for item in data:
    expected_sources = item.get('expected_sources', [])
    
    new_item = {
        'id': item.get('id', ''),
        'question': item.get('question', ''),
        'relevant_chunks': expected_sources
    }
    if 'expected_answer' in item:
        new_item['expected_answer'] = item['expected_answer']
    
    new_data.append(new_item)

with open(dest_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2)

print('Converted golden_questions.json to golden_dataset.json')
