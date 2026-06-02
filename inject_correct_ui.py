import sqlite3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
db_path = r"C:\Users\sumanth\.n8n\database.sqlite"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nodes FROM workflow_entity WHERE name LIKE '%Chaos Intelligence Bot v5%' ORDER BY updatedAt DESC LIMIT 1")
    row = cursor.fetchone()
    
    nodes = json.loads(row[0])
    target_node = next((n for n in nodes if n.get('name') == 'HTML Builder v5'), None)
    
    if not target_node:
        print("Could not find HTML Builder v5 in database!")
        sys.exit(1)
        
    original_html_code = target_node['parameters']['jsCode']
    
    with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
        v7_wf = json.load(f)
        
    for n in v7_wf['nodes']:
        if n['name'] == 'HTML Builder v7':
            n['parameters']['jsCode'] = original_html_code
            
    with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
        json.dump(v7_wf, f, indent=2, ensure_ascii=False)
        
    print("Successfully injected the 73,000-character HTML Builder v5 code into the V7 workflow!")

except Exception as e:
    print(f"Error: {e}")
