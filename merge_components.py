import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace <section id="view-terminal">
new_view_terminal = """      <section id="view-terminal" class="spa-view active space-y-8">
        
        <!-- SYSTEM STATUS LINE (HIGH CONTRAST) -->
        <div class="flex items-center justify-between border-b border-zinc-800 pb-4">
          <span class="font-mono text-xs text-zinc-200 tracking-widest font-bold uppercase flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-[#ff003c] animate-pulse"></span>
            CORE STATUS // INTEL_STREAM
          </span>
          <span class="font-mono text-xs text-zinc-400 font-bold bg-zinc-950 px-2 py-0.5 border border-zinc-900 last-updated-stamp">LOADING LIVE CORE...</span>
        </div>

        <!-- MULTI-COMPONENT HEADLINE BLOCK -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 items-center border-b border-zinc-900 pb-6">
          
          <!-- 1. THE INTERACTIVE SVG FEAR GAUGE (LEFT) -->
          <div class="flex flex-col items-center justify-center p-4 bg-zinc-950/60 border border-zinc-800 backdrop-blur-sm relative group">
            <div class="absolute top-2 left-2 font-mono text-[9px] text-zinc-400 font-bold uppercase tracking-wider">MARKET FEAR GAUGE</div>
            <div class="relative w-32 h-32 mt-4 flex items-center justify-center">
              <!-- SVG Gauge Track -->
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#18181b" stroke-width="8" fill="transparent" />
                <circle id="gauge-progress" cx="50" cy="50" r="40" stroke="#ff003c" stroke-width="8" fill="transparent" 
                        stroke-dasharray="251.2" stroke-dashoffset="251.2" class="transition-all duration-1000 ease-out" />
              </svg>
              <!-- Center Value HUD -->
              <div class="absolute text-center">
                <span id="gauge-value" class="text-3xl font-black font-mono text-white leading-none">--</span>
                <span class="block text-[9px] font-mono text-zinc-300 uppercase tracking-tighter mt-0.5 font-bold" id="gauge-label">FEAR INDEX</span>
              </div>
            </div>
          </div>

          <!-- 2. AUTHORITATIVE MASTER HEADLINE (RIGHT) -->
          <div class="md:col-span-3 space-y-3">
            <div id="vibe-pill" class="inline-flex items-center font-mono text-[10px] font-bold uppercase px-2 py-1 bg-[#ff003c]/10 border border-[#ff003c]/40 text-[#ff003c] tracking-widest rounded-none">
              --
            </div>
            <h1 id="main-headline" class="font-serif font-black text-3xl sm:text-5xl tracking-tight text-white leading-[1.05]">
              --
            </h1>
          </div>
        </div>

        <!-- 3. THE CINEMATIC QUOTE BLOCK -->
        <div class="relative border-l-4 border-amber-500 bg-gradient-to-r from-amber-950/10 to-transparent p-6 backdrop-blur-sm terminal-glow my-6">
          <div class="absolute -top-3 left-4 font-mono text-[10px] text-amber-500 font-bold bg-black border border-amber-500/30 px-2 py-0.5 uppercase tracking-widest">
            THE CHAOS LINE
          </div>
          <span class="absolute right-4 bottom-2 text-zinc-800 font-serif font-black text-7xl select-none leading-none opacity-40">"</span>
          <p id="metaphor-content" class="text-zinc-200 text-base md:text-xl font-medium font-sans leading-relaxed tracking-wide italic">
            --
          </p>
        </div>

        <!-- 4. AGENT CONSENSUS TABS IMPLEMENTATION -->
        <div class="border border-zinc-800 bg-zinc-950/40 backdrop-blur-sm">
          <!-- Tab Controls -->
          <div class="grid grid-cols-3 border-b border-zinc-800 font-mono text-xs text-center" id="agent-tab-headers">
            <button onclick="window.toggleAgentTab('fundamental')" id="tab-btn-fundamental" class="py-2.5 font-bold uppercase tracking-wider border-r border-zinc-800 bg-zinc-900 text-white border-b-2 border-[#ff003c]">Fundamental</button>
            <button onclick="window.toggleAgentTab('technical')" id="tab-btn-technical" class="py-2.5 font-bold uppercase tracking-wider border-r border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-900/30">Technical</button>
            <button onclick="window.toggleAgentTab('sentiment')" id="tab-btn-sentiment" class="py-2.5 font-bold uppercase tracking-wider text-zinc-400 hover:text-white hover:bg-zinc-900/30">Sentiment</button>
          </div>
          <!-- Tab Content Shells -->
          <div class="p-4 font-mono text-xs leading-relaxed text-zinc-300" id="agent-tab-contents">
            <div id="tab-content-fundamental" class="agent-pane block space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1"><span>AGENT_OUTPUT // FUNDAMENTAL</span><span id="agent-score-fundamental" class="text-white bg-zinc-900 px-1.5 py-0.5">--</span></div>
              <p id="agent-text-fundamental" class="text-zinc-200 text-xs font-sans pt-1">--</p>
            </div>
            <div id="tab-content-technical" class="agent-pane hidden space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1"><span>AGENT_OUTPUT // TECHNICAL</span><span id="agent-score-technical" class="text-white bg-zinc-900 px-1.5 py-0.5">--</span></div>
              <p id="agent-text-technical" class="text-zinc-200 text-xs font-sans pt-1">--</p>
            </div>
            <div id="tab-content-sentiment" class="agent-pane hidden space-y-2">
              <div class="flex justify-between items-center text-zinc-400 text-[10px] uppercase font-bold border-b border-zinc-900 pb-1"><span>AGENT_OUTPUT // SENTIMENT</span><span id="agent-score-sentiment" class="text-white bg-zinc-900 px-1.5 py-0.5">--</span></div>
              <p id="agent-text-sentiment" class="text-zinc-200 text-xs font-sans pt-1">--</p>
            </div>
          </div>
        </div>

        <!-- QUANT LIVE GRID BOXES -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono mt-6" id="macro-grid"></div>

        <!-- TRADING ACTIONS -->
        <div class="space-y-4">
          <div class="flex items-center space-x-3 font-mono text-xs uppercase tracking-wider text-white border-l-2 border-[#ff003c] pl-3 py-0.5 bg-zinc-950/40">
            <span class="font-bold">THE ANTICIPATED BETS</span><span class="text-zinc-500">//</span><span class="text-[#ff003c] animate-pulse">OVERRIDING THE MACHINE</span>
          </div>
          <div id="execution-plays" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
        </div>
      </section>"""

# Find the start and end of the existing section
start_idx = html.find('<section id="view-terminal"')
end_idx = html.find('</section>', start_idx) + len('</section>')

html = html[:start_idx] + new_view_terminal + html[end_idx:]

# 2. Inject Javascript for Gauge and Agent Tabs into loadTerminalPayload
js_code_to_inject = """
        // Inject Gauge Update
        const score = data.tensionScore || 22;
        document.getElementById('gauge-value').innerText = score;
        const circle = document.getElementById('gauge-progress');
        if (circle && circle.r) {
          const radius = circle.r.baseVal.value;
          const circumference = 2 * Math.PI * radius;
          const offset = circumference - (score / 100) * circumference;
          circle.style.strokeDasharray = `${circumference} ${circumference}`;
          circle.style.strokeDashoffset = offset;
          if (score <= 30) {
            circle.setAttribute('stroke', '#ff003c'); // Panic Crimson
            document.getElementById('gauge-label').innerText = "EXTREME FEAR";
          } else if (score <= 50) {
            circle.setAttribute('stroke', '#ffaa00'); // Warning Amber
            document.getElementById('gauge-label').innerText = "CAUTION";
          } else {
            circle.setAttribute('stroke', '#00ff66'); // Healthy Green
            document.getElementById('gauge-label').innerText = "GREED";
          }
        }

        // Inject Agent Tabs Binding
        const a = rawJson.agents || {};
        document.getElementById('agent-score-fundamental').innerText = a.fundamental ? `${a.fundamental.bias} / ${a.fundamental.confidence}%` : "NEUTRAL / 64%";
        document.getElementById('agent-text-fundamental').innerText = a.fundamental?.thesis || "Rates remain constraints.";

        document.getElementById('agent-score-technical').innerText = a.technical ? `${a.technical.bias} / ${a.technical.confidence}%` : "BEARISH / 66%";
        document.getElementById('agent-text-technical').innerText = a.technical?.thesis || "BTC trading near local baseline range.";

        document.getElementById('agent-score-sentiment').innerText = a.sentiment ? `${a.sentiment.bias} / ${a.sentiment.confidence}%` : "BULLISH / 64%";
        document.getElementById('agent-text-sentiment').innerText = a.sentiment?.thesis || "Fear reads as contrarian setups.";
"""

# Insert right after `document.getElementById('tension-meter').style.width = `${data.tensionScore}%`;`
# Wait, tension-meter was removed in the new html! Let's insert before vibePill code.
target_line = "const vibePill = document.getElementById('vibe-pill');"
html = html.replace(target_line, js_code_to_inject + "\\n        " + target_line)

# Also remove the old tension-meter line
html = html.replace("document.getElementById('tension-meter').style.width = `${data.tensionScore}%`;", "")

# 3. Inject toggleAgentTab function globally
toggle_func = """
    window.toggleAgentTab = function(tabId) {
      document.querySelectorAll('.agent-pane').forEach(el => el.className = 'agent-pane hidden space-y-2');
      const targetPane = document.getElementById(`tab-content-${tabId}`);
      if (targetPane) targetPane.className = 'agent-pane block space-y-2';
      
      document.querySelectorAll('#agent-tab-headers button').forEach(btn => {
        btn.className = "py-2.5 font-bold uppercase tracking-wider text-zinc-400 hover:text-white hover:bg-zinc-900/30 border-b-transparent";
      });
      
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if (activeBtn) activeBtn.className = "py-2.5 font-bold uppercase tracking-wider bg-zinc-900 text-white border-b-2 border-[#ff003c] border-r border-zinc-800";
    };
"""

html = html.replace("function runClientRouter() {", toggle_func + "\\n    function runClientRouter() {")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Index.html fully upgraded with Gauge and Tabs!")
