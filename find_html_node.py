import sqlite3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\sumanth\.n8n\database.sqlite"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, nodes FROM workflow_entity WHERE name LIKE '%Chaos Intelligence Bot v5%' ORDER BY updatedAt DESC LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("No V5 workflow found.")
        sys.exit(1)
        
    wf_name, nodes_json = row
    nodes = json.loads(nodes_json)
    
    print(f"Workflow: {wf_name}")
    print("Nodes available:")
    html_found = False
    
    for n in nodes:
        name = n.get('name', 'Unknown')
        print(f" - {name}")
        code = n.get('parameters', {}).get('jsCode', '')
        if 'html' in code.lower() or '<!DOCTYPE html>' in code:
            print(f"   >>> THIS NODE CONTAINS HTML! ({len(code)} characters)")
            html_found = True
            
    if not html_found:
        print("\nNone of the nodes contained the HTML string!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
