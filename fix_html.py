import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the Agent Consensus section with Intelligence Levels section
start_marker = "<!-- 4. AGENT CONSENSUS TABS IMPLEMENTATION -->"
end_marker = "<!-- QUANT LIVE GRID BOXES -->"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    intel_section = """<!-- 4. INTELLIGENCE LEVEL TABS -->
        <div class="border border-zinc-800 bg-zinc-950/40 backdrop-blur-sm mt-6 mb-6">
          <div class="grid grid-cols-3 border-b border-zinc-800 font-mono text-xs text-center" id="intel-tab-headers">
            <button onclick="window.toggleIntelTab('eli5')" id="tab-btn-eli5" class="py-2.5 font-bold uppercase tracking-wider border-r border-zinc-800 bg-zinc-900 text-white border-b-2 border-[#ff003c]">ELI5</button>
            <button onclick="window.toggleIntelTab('analyst')" id="tab-btn-analyst" class="py-2.5 font-bold uppercase tracking-wider border-r border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-900/30">Analyst</button>
            <button onclick="window.toggleIntelTab('quant')" id="tab-btn-quant" class="py-2.5 font-bold uppercase tracking-wider text-zinc-400 hover:text-white hover:bg-zinc-900/30">Quant</button>
          </div>
          <div class="p-4 font-mono text-xs leading-relaxed text-zinc-300" id="intel-tab-contents">
            <div id="tab-content-eli5" class="intel-pane block space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1">
                <span>INTELLIGENCE // ELI5</span>
                <button class="voice-btn bg-zinc-900 text-white px-2 py-0.5 border border-zinc-700 hover:bg-zinc-800 transition-colors" onclick="window.chaosSpeak('intel-text-eli5', this, 'eli5')">🔊 LISTEN</button>
              </div>
              <p id="intel-text-eli5" class="text-zinc-200 text-xs font-sans pt-1">--</p>
            </div>
            <div id="tab-content-analyst" class="intel-pane hidden space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1">
                <span>INTELLIGENCE // ANALYST</span>
                <button class="voice-btn bg-zinc-900 text-white px-2 py-0.5 border border-zinc-700 hover:bg-zinc-800 transition-colors" onclick="window.chaosSpeak('intel-text-analyst', this, 'analyst')">🔊 LISTEN</button>
              </div>
              <p id="intel-text-analyst" class="text-zinc-200 text-xs font-sans pt-1 whitespace-pre-line">--</p>
            </div>
            <div id="tab-content-quant" class="intel-pane hidden space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1">
                <span>INTELLIGENCE // QUANT</span>
                <button class="voice-btn bg-zinc-900 text-white px-2 py-0.5 border border-zinc-700 hover:bg-zinc-800 transition-colors" onclick="window.chaosSpeak('intel-text-quant', this, 'quant')">🔊 LISTEN</button>
              </div>
              <p id="intel-text-quant" class="text-zinc-200 text-xs font-sans pt-1 whitespace-pre-line">--</p>
            </div>
          </div>
        </div>

        """
    html = html[:start_idx] + intel_section + html[end_idx:]

    # Also we need to fix the JS error. The previous JS code bound the old agent text:
    # `document.getElementById('agent-score-fundamental').innerText = ...`
    # Since the old agent html is gone, this will also throw an error!
    # Let's remove the agent mapping code.
    agent_js_start = "document.getElementById('agent-score-fundamental').innerText ="
    agent_js_end = "document.getElementById('agent-text-sentiment').innerText = a.sentiment?.thesis || \"Fear reads as contrarian setups.\";"
    
    a_start_idx = html.find(agent_js_start)
    a_end_idx = html.find(agent_js_end) + len(agent_js_end)
    
    if a_start_idx != -1 and a_end_idx != -1:
        html = html[:a_start_idx] + html[a_end_idx:]

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed HTML injection and removed broken JS bindings.")
else:
    print("Could not find markers.")
