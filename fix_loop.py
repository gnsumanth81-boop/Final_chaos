import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Nodes that need to run once for all items (to stop the 12x loop)
nodes_to_fix = [
    'Chaos Pre-Processor v5',
    'Merge All Brains'
]

for n in wf['nodes']:
    if n['name'] in nodes_to_fix:
        # In n8n Code nodes, setting mode to 'runOnceForAllItems' prevents it 
        # from looping 12 times when it receives 12 items from parallel inputs.
        n['parameters']['mode'] = 'runOnceForAllItems'

with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("Fixed the loop! The nodes will now run exactly ONE time.")
