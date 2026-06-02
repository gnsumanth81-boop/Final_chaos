import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Find the Supervisor Prompt node and verify the model change
# Also check the Chaos Pre-Processor to confirm prompt includes JSON instruction
for n in wf['nodes']:
    if n['name'] == 'OpenRouter (Supervisor)':
        print("OpenRouter Supervisor body:")
        body = n['parameters'].get('jsonBody', '')
        print(body[:300])
        print("...")
        
    if n['name'] == 'Supervisor Prompt':
        code = n['parameters'].get('jsCode', '')
        # Check if we have the json instruction
        print("\nSupervisor Prompt last 300 chars:")
        print(code[-300:])
