import sqlite3
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\sumanth\.n8n\database.sqlite"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, nodes FROM workflow_entity WHERE name LIKE '%Chaos Intelligence Bot v5%' ORDER BY updatedAt DESC LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("Could not find Chaos Intelligence Bot v5 in the n8n database.")
        sys.exit(1)
        
    wf_name, nodes_json = row
    print(f"Found workflow: {wf_name}")
    
    nodes = json.loads(nodes_json)
    
    # Look for the Parse + Validate Output node (which contains the HTML)
    target_node = None
    for n in nodes:
        if n.get('name') == 'Parse + Validate Output' or 'html=`<!DOCTYPE html>' in n.get('parameters', {}).get('jsCode', ''):
            target_node = n
            break
            
    if not target_node:
        print("Could not find the HTML builder node inside the workflow.")
        sys.exit(1)
        
    # Read the new v7 complete workflow
    with open('chaos_v7_complete.json', 'r', encoding='utf-8') as f:
        v7_wf = json.load(f)
        
    # Find the HTML Builder v7 node and replace its code with the V5 one
    original_code = target_node['parameters']['jsCode']
    
    found = False
    for n in v7_wf['nodes']:
        if n.get('name') == 'HTML Builder v7':
            n['parameters']['jsCode'] = original_code
            found = True
            break
            
    if not found:
        print("Could not find HTML Builder v7 in the new workflow.")
        sys.exit(1)
        
    # Save the updated workflow
    with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
        json.dump(v7_wf, f, indent=2, ensure_ascii=False)
        
    print("\nSUCCESS! Extracted the original massive HTML UI from n8n's database!")
    print("Saved the PERFECT workflow as: chaos_v7_complete_UI.json")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
