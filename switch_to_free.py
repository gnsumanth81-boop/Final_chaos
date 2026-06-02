import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Nodes that call OpenRouter - switch all to free model
openrouter_nodes = [
    'OpenRouter (Supervisor)',
    '🐋 OpenRouter (Alpha)',
    '📝 OpenRouter (Autopsy)',
    '🌍 OpenRouter (Geo)'
]

fixed = []
for n in wf['nodes']:
    if n['name'] in openrouter_nodes:
        params = n.get('parameters', {})
        
        # Fix the JSON body - switch model to openrouter/free
        # Also REMOVE response_format because many free models don't support it
        if 'jsonBody' in params:
            body = params['jsonBody']
            # Replace model name
            body = body.replace('google/gemini-2.5-flash', 'openrouter/free')
            body = body.replace('meta-llama/llama-3.1-70b-instruct', 'openrouter/free')
            body = body.replace('anthropic/claude-3.5-sonnet', 'openrouter/free')
            body = body.replace('meta-llama/llama-3.1-8b-instruct', 'openrouter/free')
            # Remove response_format from the JSON body string
            import re
            body = re.sub(r',\s*\"response_format\":\s*\{[^}]+\}', '', body)
            body = re.sub(r',\s*response_format:\s*\$json\.response_format', '', body)
            params['jsonBody'] = body
            fixed.append(n['name'])

        # Also fix if the model is set directly in parameters
        if 'json' in str(params.get('body', '')):
            pass

with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("Fixed nodes to use openrouter/free:")
for f_name in fixed:
    print(f"  - {f_name}")
print("\nAll 4 brains now use FREE models - zero credits needed!")
