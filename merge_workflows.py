import json
import re

def main():
    # 1. Read transcript to get the full v5 JSON
    transcript_path = r'C:\Users\sumanth\.gemini\antigravity-ide\brain\bfadf122-a10e-48dd-a262-36b514cef2da\.system_generated\logs\transcript.jsonl'
    v5_json_str = None
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in reversed(lines):
        try:
            step = json.loads(line)
            if step.get('type') == 'USER_INPUT' and 'here is my old one - {' in step.get('content', ''):
                content = step['content']
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                v5_json_str = content[start_idx:end_idx]
                break
        except Exception:
            pass

    if not v5_json_str:
        print("Could not find the v5 workflow in transcript.")
        return

    # Parse v5 workflow
    try:
        v5_workflow = json.loads(v5_json_str)
    except Exception as e:
        print("Failed to parse v5 workflow JSON:", e)
        return

    # 2. Read new brains
    try:
        with open('chaos_v7_brains.json', 'r', encoding='utf-8') as f:
            v7_brains = json.load(f)
    except Exception as e:
        print("Failed to read chaos_v7_brains.json:", e)
        return

    # 3. Merge
    v5_workflow['name'] = 'Chaos Intelligence Bot v7 (Complete Edition)'
    
    # Append the new nodes
    new_nodes = v7_brains.get('nodes', [])
    v5_workflow['nodes'].extend(new_nodes)
    
    # Append the internal connections of the new brains
    if 'connections' not in v5_workflow:
        v5_workflow['connections'] = {}
        
    new_connections = v7_brains.get('connections', {})
    for src_node, target_data in new_connections.items():
        if src_node not in v5_workflow['connections']:
            v5_workflow['connections'][src_node] = target_data
        else:
            # Merge if node already has connections
            if 'main' in target_data:
                if 'main' not in v5_workflow['connections'][src_node]:
                    v5_workflow['connections'][src_node]['main'] = target_data['main']
                else:
                    v5_workflow['connections'][src_node]['main'][0].extend(target_data['main'][0])

    # 4. Automagically wire up the main v5 nodes to the new brains
    # ContextNews -> Geopolitical Wires Prompt
    if 'ContextNews' in v5_workflow['connections']:
        v5_workflow['connections']['ContextNews']['main'][0].append({
            "node": "📝 Geopolitical Wires Prompt",
            "type": "main",
            "index": 0
        })
    else:
        v5_workflow['connections']['ContextNews'] = {
            "main": [[{"node": "📝 Geopolitical Wires Prompt", "type": "main", "index": 0}]]
        }

    # Chaos Pre-Processor v5 -> Autopsy Prompt (since Pre-processor holds current market data)
    if 'Chaos Pre-Processor v5' in v5_workflow['connections']:
        v5_workflow['connections']['Chaos Pre-Processor v5']['main'][0].append({
            "node": "📝 Autopsy Prompt",
            "type": "main",
            "index": 0
        })
    else:
        v5_workflow['connections']['Chaos Pre-Processor v5'] = {
            "main": [[{"node": "📝 Autopsy Prompt", "type": "main", "index": 0}]]
        }
        
    # We won't wire the outputs of OpenRouter to HTML Builder directly because HTML builder needs its code updated to parse the new outputs.
    # The user can just see them connected on the canvas!

    # Save
    with open('chaos_v7_complete.json', 'w', encoding='utf-8') as f:
        json.dump(v5_workflow, f, indent=2)

    print("Successfully generated chaos_v7_complete.json!")

main()
