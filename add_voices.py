import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update The Chaos Line header to include the LISTEN button
old_chaos_line = """<div class="absolute -top-3 left-4 font-mono text-[10px] text-amber-500 font-bold bg-black border border-amber-500/30 px-2 py-0.5 uppercase tracking-widest">
            THE CHAOS LINE
          </div>"""
new_chaos_line = """<div class="absolute -top-3 left-4 font-mono text-[10px] text-amber-500 font-bold bg-black border border-amber-500/30 px-2 py-0.5 uppercase tracking-widest flex items-center gap-2">
            THE CHAOS LINE
            <button class="voice-btn hover:text-white transition-colors border-l border-amber-500/30 pl-2" onclick="window.chaosSpeak('metaphor-content', this, 'chaos')">🔊 LISTEN</button>
          </div>"""

html = html.replace(old_chaos_line, new_chaos_line)

# 2. Insert the Intelligence Levels section below the Agent Consensus section
intel_section = """
        <!-- INTELLIGENCE LEVEL TABS -->
        <div class="border border-zinc-800 bg-zinc-950/40 backdrop-blur-sm mt-6">
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

agent_section_end = '</div>\\n        </div>\\n\\n        <!-- QUANT LIVE GRID BOXES -->'
html = html.replace(agent_section_end, '</div>\\n        </div>\\n' + intel_section + '\\n        <!-- QUANT LIVE GRID BOXES -->')


# 3. Inject JS: toggleIntelTab, voice functions, and update loadTerminalPayload
js_inject = """
    window.toggleIntelTab = function(tabId) {
      document.querySelectorAll('.intel-pane').forEach(el => el.className = 'intel-pane hidden space-y-2');
      const targetPane = document.getElementById(`tab-content-${tabId}`);
      if (targetPane) targetPane.className = 'intel-pane block space-y-2';
      
      document.querySelectorAll('#intel-tab-headers button').forEach(btn => {
        btn.className = "py-2.5 font-bold uppercase tracking-wider text-zinc-400 hover:text-white hover:bg-zinc-900/30 border-b-transparent";
      });
      
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if (activeBtn) activeBtn.className = "py-2.5 font-bold uppercase tracking-wider bg-zinc-900 text-white border-b-2 border-[#ff003c] border-r border-zinc-800";
    };

    window.findVoice = function(patterns) {
      const vs = speechSynthesis.getVoices();
      for (const p of patterns) {
        const v = vs.find(x => p.test(x.name));
        if (v) return v;
      }
      return vs.find(x => /en-(US|GB)/i.test(x.lang)) || vs[0];
    };

    window.chaosSpeak = function(id, btn, type) {
      if (!window.speechSynthesis) return alert('Speech synthesis not supported in this browser.');
      
      const el = document.getElementById(id);
      if (!el) return;
      let text = el.innerText;
      
      if (btn.classList.contains('playing')) {
        speechSynthesis.cancel();
        btn.classList.remove('playing');
        btn.innerHTML = '🔊 LISTEN';
        return;
      }

      document.querySelectorAll('.voice-btn').forEach(b => {
        b.classList.remove('playing');
        b.innerHTML = '🔊 LISTEN';
      });
      speechSynthesis.cancel();

      const u = new SpeechSynthesisUtterance(text);
      switch(type) {
        case 'eli5':
          u.rate = 1.0; u.pitch = 1.2; u.volume = 1;
          u.voice = window.findVoice([/Samantha/i, /Victoria/i, /Google US English/i, /Zira/i]);
          break;
        case 'analyst':
          u.rate = 1.1; u.pitch = 1.0; u.volume = 1;
          u.voice = window.findVoice([/Daniel/i, /Oliver/i, /Arthur/i, /Google UK/i]);
          break;
        case 'quant':
          u.rate = 1.25; u.pitch = 0.9; u.volume = 1;
          u.voice = window.findVoice([/Fred/i, /Ralph/i, /Albert/i, /Microsoft Mark/i, /Richard/i, /Google UK/i]);
          break;
        default: // chaos line
          u.rate = 0.85; u.pitch = 0.8; u.volume = 1;
          u.voice = window.findVoice([/Moira/i, /Fiona/i, /Rishi/i, /Microsoft Zira/i]);
      }
      
      btn.classList.add('playing');
      btn.innerHTML = '⏹ STOP';
      
      u.onend = () => {
        btn.classList.remove('playing');
        btn.innerHTML = '🔊 LISTEN';
      };
      u.onerror = () => {
        btn.classList.remove('playing');
        btn.innerHTML = '🔊 LISTEN';
      };
      
      speechSynthesis.speak(u);
    };

    if ('speechSynthesis' in window) {
      speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
    }
"""

html = html.replace("window.toggleAgentTab = function(tabId) {", js_inject + "\\n    window.toggleAgentTab = function(tabId) {")

load_payload_inject = """
        // Inject Intel Text
        if (rawJson.brief) {
          document.getElementById('intel-text-eli5').innerText = rawJson.brief.eli5 || "--";
          document.getElementById('intel-text-analyst').innerText = rawJson.brief.analyst || "--";
          document.getElementById('intel-text-quant').innerText = rawJson.brief.quant || "--";
        }
"""
html = html.replace("const a = rawJson.agents || {};", load_payload_inject + "\\n        const a = rawJson.agents || {};")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Index.html upgraded with Intel tabs and voice features.")
