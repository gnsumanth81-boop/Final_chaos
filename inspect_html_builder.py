import sqlite3
import json

db_path = r"C:\Users\sumanth\.n8n\database.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT nodes FROM workflow_entity WHERE name LIKE '%Chaos Intelligence Bot v5%' ORDER BY updatedAt DESC LIMIT 1")
row = cursor.fetchone()
nodes = json.loads(row[0])

target_node = next((n for n in nodes if n.get('name') == 'HTML Builder v5'), None)
if target_node:
    code = target_node['parameters']['jsCode']
    print("Found HTML Builder v5! Contains 'alpha_telemetry'? ", 'alpha_telemetry' in code)
    print("Contains 'autopsy'? ", 'autopsy' in code)
    print("Contains 'telemetry'? ", 'telemetry' in code)
    print("Contains 'ledger'? ", 'ledger' in code)
    print("\nFIRST 500 CHARS:\n", code[:500])
    print("\nLAST 500 CHARS:\n", code[-500:])
else:
    print("Not found.")
