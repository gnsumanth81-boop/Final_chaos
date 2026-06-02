import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

user_html = """
<!-- TAB 1: INTEL ROOM -->
<section id="view-terminal" class="spa-view active space-y-6">
  <!-- Top Headline HUD Grid -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-center border-b border-zinc-800 pb-4">
    <!-- Restored Interactive SVG Gauge -->
    <div class="bg-zinc-950 border border-zinc-800 p-4 flex flex-col items-center justify-center relative">
      <span class="absolute top-1 left-2 font-mono text-[9px] text-zinc-400 font-bold">FEAR GAUGE</span>
      <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" stroke="#111" stroke-width="8" fill="transparent" />
        <circle id="gauge-progress" cx="50" cy="50" r="40" stroke="#ff003c" stroke-width="8" fill="transparent" stroke-dasharray="251.2" stroke-dashoffset="251.2" class="transition-all duration-700" />
      </svg>
      <div class="absolute text-center mt-2">
        <span id="gauge-value" class="text-2xl font-black font-mono text-white">--</span>
        <span id="gauge-label" class="block text-[8px] font-mono font-bold text-zinc-400 uppercase tracking-tighter">FEAR</span>
      </div>
    </div>
    <!-- Headline Section -->
    <div class="md:col-span-3 space-y-2">
      <div id="vibe-pill" class="inline-flex font-mono text-[10px] font-bold uppercase px-2 py-0.5 bg-zinc-900 border border-zinc-700 text-white">--</div>
      <h1 id="main-headline" class="font-serif font-black text-2xl sm:text-4xl text-white leading-tight">--</h1>
    </div>
  </div>

  <!-- Intelligence Levels Toggle & Audio Trigger Overlay -->
  <div class="bg-zinc-950 border border-zinc-800 p-4 space-y-3">
    <div class="flex justify-between items-center border-b border-zinc-900 pb-2">
      <span class="font-mono text-[10px] font-bold text-zinc-400">INTELLIGENCE LEVEL COMPILATION</span>
      <div class="flex space-x-2 font-mono text-[10px]" id="intel-level-toggles">
        <button onclick="switchIntelLevel('eli5')" id="btn-eli5" class="px-2 py-0.5 bg-zinc-900 border border-zinc-700 text-white font-bold">ELI5</button>
        <button onclick="switchIntelLevel('analyst')" id="btn-analyst" class="px-2 py-0.5 border border-transparent text-zinc-400">ANALYST</button>
        <button onclick="switchIntelLevel('quant')" id="btn-quant" class="px-2 py-0.5 border border-transparent text-zinc-400">QUANT</button>
      </div>
    </div>
    <p id="intel-narrative-box" class="text-zinc-200 text-sm leading-relaxed font-sans font-normal">--</p>
  </div>

  <!-- Golden Accent Cinematic Quote Block -->
  <div class="relative border-l-4 border-amber-500 bg-amber-950/5 p-5 terminal-glow italic">
    <div class="absolute -top-2.5 left-3 font-mono text-[9px] text-amber-500 font-bold bg-black border border-amber-500/20 px-1.5 uppercase flex items-center gap-2">THE CHAOS LINE <button class="voice-btn text-white" onclick="window.chaosSpeak('metaphor-content', this, 'chaos')">🔊 LISTEN</button></div>
    <p id="metaphor-content" class="text-zinc-100 text-sm md:text-base font-medium font-sans">--</p>
  </div>

  <!-- Agent Consensus & Debate Box -->
  <div class="border border-zinc-800 bg-zinc-950">
    <div class="grid grid-cols-3 border-b border-zinc-800 font-mono text-[11px] text-center" id="agent-tab-headers">
      <button onclick="toggleAgentTab('fundamental')" id="tab-btn-fundamental" class="py-2 bg-zinc-900 text-white border-b-2 border-[#ff003c] font-bold">FUNDAMENTAL</button>
      <button onclick="toggleAgentTab('technical')" id="tab-btn-technical" class="py-2 text-zinc-400 border-b-2 border-transparent">TECHNICAL</button>
      <button onclick="toggleAgentTab('sentiment')" id="tab-btn-sentiment" class="py-2 text-zinc-400 border-b-2 border-transparent">SENTIMENT</button>
    </div>
    <div class="p-4 font-mono text-xs space-y-1" id="agent-tab-contents">
      <div id="agent-body-wrapper" class="space-y-1">
        <div class="text-[9px] text-zinc-500 font-bold uppercase" id="agent-pane-header">AGENT // OUT_STREAM</div>
        <p id="agent-text-content" class="text-zinc-200 font-sans pt-1">--</p>
      </div>
    </div>
  </div>

  <!-- Active Macro Forces Illuminator Chips (9-Grid Matrix) -->
  <div class="space-y-2">
    <div class="font-mono text-[10px] font-bold text-zinc-400 uppercase">ACTIVE MACRO FORCES TRACKER</div>
    <div class="grid grid-cols-3 sm:grid-cols-9 gap-1.5 font-mono text-center text-[10px]" id="macro-forces-chips">
      <div data-force="MONEY" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">💵 MN_</div>
      <div data-force="TECH" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">🧠 AI_</div>
      <div data-force="ENERGY" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">⚡ EN_</div>
      <div data-force="POLITICS" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">🏛️ PL_</div>
      <div data-force="WAR" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">⚔️ WR_</div>
      <div data-force="DEBT" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">📉 DB_</div>
      <div data-force="JOBS" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">👔 JB_</div>
      <div data-force="FOOD" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">🌾 FD_</div>
      <div data-force="PEOPLE" class="py-2 bg-zinc-950 border border-zinc-900 text-zinc-600">👥 PP_</div>
    </div>
  </div>

  <!-- Polymarket Action Stack Execution Plays -->
  <div class="space-y-3">
    <div class="font-mono text-[10px] font-bold text-zinc-300 uppercase tracking-wider border-l border-zinc-500 pl-2">TACTICAL ORDER ROUTING MATRIX</div>
    <div id="execution-plays" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
  </div>

  <!-- Market Trap & Tactical Edge Module -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-xs">
    <div class="bg-zinc-950 border border-[#ff003c]/20 p-4 space-y-1">
      <div class="text-[#ff003c] font-bold uppercase tracking-wider">⚠️ THE MARKET TRAP</div>
      <p id="trap-text" class="text-zinc-300 font-sans">--</p>
    </div>
    <div class="bg-zinc-950 border border-[#00ff66]/20 p-4 space-y-1">
      <div class="text-[#00ff66] font-bold uppercase tracking-wider">💎 THE ALPHA EDGE</div>
      <p id="edge-text" class="text-zinc-300 font-sans">--</p>
    </div>
  </div>
</section>
<!-- TAB 2: VERIFICATION LEDGER -->
<section id="view-ledger" class="spa-view space-y-6">
  <div class="border-b border-zinc-800 pb-4">
    <h2 class="font-serif font-black text-2xl text-white uppercase">Audit Verification Ledger</h2>
    <p class="text-xs text-zinc-400 font-mono mt-1">Cryptographic hashes validate past engine positioning metrics.</p>
  </div>
  <!-- Progress Tracker Module -->
  <div class="bg-zinc-950 border border-zinc-800 p-4 space-y-2 font-mono text-xs">
    <div class="flex justify-between font-bold">
      <span>TRACK RECORD VALIDATION PROGRESS</span>
      <span id="ledger-progress-pct" class="text-[#00ff66]">--%</span>
    </div>
    <div class="w-full bg-zinc-900 h-2 border border-zinc-800">
      <div id="ledger-progress-bar" class="bg-[#00ff66] h-full transition-all" style="width: 0%"></div>
    </div>
    <div class="text-[10px] text-zinc-400">Track metrics publish globally once 14+ sequential nodes fully resolve.</div>
  </div>
  <!-- Ledger Rows Table Frame -->
  <div class="border border-zinc-800 bg-zinc-950 overflow-hidden font-mono text-xs">
    <div class="grid grid-cols-3 bg-zinc-900 p-3 border-b border-zinc-800 text-zinc-300 font-bold uppercase tracking-wider">
      <div>Timestamp</div><div>Signal Narrative Context</div><div>Status Outcome</div>
    </div>
    <div class="divide-y divide-zinc-900" id="ledger-rows"></div>
  </div>
</section>
<!-- TAB 3: TELEMETRY ALGORITHMIC VITALS -->
<section id="view-vitals" class="spa-view space-y-6">
  <div class="border-b border-zinc-800 pb-4">
    <h2 class="font-serif font-black text-2xl text-white uppercase">Algorithmic Telemetry Matrix</h2>
  </div>
  
  <!-- Macro Dashboard Core Grid Elements -->
  <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 font-mono text-center" id="vitals-matrix-deck"></div>

  <!-- Cross-Market Context Boxes -->
  <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 font-mono text-xs" id="cross-market-context-grid">
    <!-- Custom data containers injected dynamically -->
  </div>

  <!-- Polymarket Betting Probability Line -->
  <div class="bg-zinc-950 border border-zinc-800 p-4 space-y-2 font-mono text-xs">
    <div class="flex justify-between font-bold">
      <span>TOP PREDICTION MARKET PROBABILITY MATRIX</span>
      <span id="poly-odds-pct" class="text-sky-400">--%</span>
    </div>
    <div class="w-full bg-zinc-900 h-2 border border-zinc-800">
      <div id="poly-odds-bar" class="bg-sky-500 h-full transition-all" style="width: 0%"></div>
    </div>
  </div>

  <!-- News Wires Feed Scroller -->
  <div class="border border-zinc-800 bg-zinc-950 p-4 space-y-2 font-mono">
    <div class="text-[10px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-900 pb-1">⚡ INTEL WIRES INTELLIGENCE LOGS</div>
    <div class="h-32 overflow-y-auto space-y-2 text-[11px]" id="intel-wires-feed"></div>
  </div>
</section>
"""

user_js = """
// Local store variable caching for multi-layer intelligence views
let intelligenceLevelsCache = { eli5: "", analyst: "", quant: "" };
let agentConsensusCache = {};
async function loadTerminalPayload() {
  try {
    const response = await fetch('./api/latest.json', {cache:'no-store'});
    if(!response.ok) throw new Error(`Outage: ${response.status}`);
    const data = await response.json();

    // 1. Core Header and Global Variables Config
    document.getElementById('terminal-session').innerText = data.session || "LIVE DATA FEED";
    document.querySelectorAll('.last-updated-stamp').forEach(el => el.innerText = `UPDATED: ${data.timestamp || '--:--'}`);
    document.getElementById('side-conf').innerText = `${data.brief?.confidence || data.confidence || '66'}%`;

    // 2. SVG Gauge Dynamic Math Execution
    const tension = parseInt(data.market?.fearIndex) || 22;
    document.getElementById('gauge-value').innerText = tension;
    const progressCircle = document.getElementById('gauge-progress');
    if (progressCircle) {
      const circ = 2 * Math.PI * 40; // radius 40
      progressCircle.style.strokeDasharray = `${circ} ${circ}`;
      progressCircle.style.strokeDashoffset = circ - (tension / 100) * circ;
      progressCircle.setAttribute('stroke', String(data.brief?.signal).includes('BEARISH') ? '#ff003c' : '#00ff66');
      document.getElementById('gauge-label').innerText = String(data.brief?.signal).includes('BEARISH') ? "EXTREME FEAR" : "BULLISH EDGE";
    }

    // 3. Top Master Headline Box Mapping
    document.getElementById('main-headline').innerText = data.brief?.headline || "Terminal Online";
    document.getElementById('metaphor-content').innerText = data.brief?.chaos_line || "--";

    // 4. Intelligence Levels Text Layer Cache
    intelligenceLevelsCache.eli5 = data.brief?.eli5 || "Summary frame.";
    intelligenceLevelsCache.analyst = data.brief?.analyst || "Intermediate analysis frame.";
    intelligenceLevelsCache.quant = data.brief?.quant || "Advanced mathematical indicators.";
    
    // Refresh text frame container values
    const activeLevelButton = document.querySelector('#intel-level-toggles .bg-zinc-900')?.id?.split('-')[1] || 'eli5';
    switchIntelLevel(activeLevelButton);

    // 5. Agent Debate Array Configurations
    const a = data.agents || {};
    agentConsensusCache = {
      fundamental: { score: `${a.fundamental?.bias || 'NEUTRAL'} / ${a.fundamental?.confidence || 0}%`, text: a.fundamental?.thesis || "No data." },
      technical: { score: `${a.technical?.bias || 'NEUTRAL'} / ${a.technical?.confidence || 0}%`, text: a.technical?.thesis || "No data." },
      sentiment: { score: `${a.sentiment?.bias || 'NEUTRAL'} / ${a.sentiment?.confidence || 0}%`, text: a.sentiment?.thesis || "No data." }
    };
    const activeAgentTab = document.querySelector('#agent-tab-headers .bg-zinc-900')?.id?.split('tab-btn-')[1] || 'fundamental';
    toggleAgentTab(activeAgentTab);

    // 6. Illuminator Macro Force Chips Matrix Parsing Loop
    const activatedForces = data.brief?.forces || ["MONEY", "TECH", "DEBT"]; 
    document.querySelectorAll('#macro-forces-chips [data-force]').forEach(chip => {
      const forceName = chip.getAttribute('data-force');
      if (activatedForces.includes(forceName)) {
        chip.className = "py-2 bg-[#00ff66]/10 border border-[#00ff66]/40 text-[#00ff66] font-bold tracking-wide shadow-md";
      } else {
        chip.className = "py-2 bg-zinc-950 border border-zinc-900 text-zinc-600 font-normal";
      }
    });

    // 7. Tactical Order Routing Cards Panel Array Generator
    const plays = data.brief?.plays || [];
    document.getElementById('execution-plays').innerHTML = plays.map(p => {
      let variantColor = "border-zinc-800 bg-zinc-950/40 text-white";
      let focusText = "text-zinc-300";
      if (p.type.includes('SQUEEZE') || p.type.includes('CONTRARIAN')) { variantColor = "border-[#00ff66]/30 bg-[#00ff66]/5 text-[#00ff66]"; focusText = "text-[#00ff66]"; }
      if (p.type.includes('HUNT') || p.type.includes('AGGRESSIVE')) { variantColor = "border-[#ff003c]/30 bg-[#ff003c]/5 text-[#ff003c]"; focusText = "text-[#ff003c]"; }
      return `
        <div class="border ${variantColor} p-4 flex flex-col justify-between space-y-3 font-mono">
          <div>
            <div class="text-[9px] uppercase font-bold tracking-widest text-zinc-400 bg-black/50 px-1 w-fit border border-zinc-900">${p.type}</div>
            <h4 class="text-sm font-bold text-white pt-1">${p.thesis}</h4>
            <p class="text-[11px] font-sans text-zinc-300 leading-tight pt-1 font-normal">${p.details}</p>
          </div>
          <div class="border-t border-zinc-900 pt-2 flex items-center justify-between text-[11px]">
            <span class="text-zinc-400 text-[10px] font-bold uppercase tracking-wider">EXECUTE</span>
            <span class="font-bold text-sm ${focusText}">MONITOR</span>
          </div>
        </div>
      `;
    }).join('');

    // 8. Market Trap & Extreme Tactical Edge
    document.getElementById('trap-text').innerText = data.brief?.trap || "Avoid treating extreme index panic parameters as single directions.";
    document.getElementById('edge-text').innerText = data.brief?.edge || "Watch macro volatility indexes closely for confirmations.";

    // 9. Verification Ledger Progress Automation Array Processing
    // Mocked ledger length to 2
    const totalSettledEntriesCount = 2;
    const trackingCompletionRatio = Math.min(Math.round((totalSettledEntriesCount / 14) * 100), 100);
    document.getElementById('ledger-progress-pct').innerText = `${trackingCompletionRatio}%`;
    document.getElementById('ledger-progress-bar').style.width = `${trackingCompletionRatio}%`;
    
    // Inject mock ledger rows or fetched ledger rows
    document.getElementById('sidebar-ledger-count').innerText = `${totalSettledEntriesCount}/14`;
    document.getElementById('ledger-rows').innerHTML = `
        <div class="grid grid-cols-3 p-3 border-b border-zinc-900 bg-zinc-950/20 font-mono text-[11px] items-center">
          <div class="text-zinc-400">2026-05-28</div>
          <div class="text-zinc-200 font-sans tracking-wide truncate pr-4">Fear Rises, Vol Stays Contained</div>
          <div class="font-bold text-[#ff003c]">BEARISH / OPEN</div>
        </div>
    `;

    // 10. Telemetry Vitals & Cross Market Context
    const m = data.market || {};
    const macroVitals = [
        { label: "BTC/USD", value: m.btcPrice || 'N/A', change: `${m.btcChange || '0'}%`, state: parseFloat(m.btcChange || 0) >= 0 ? "BULLISH" : "BEARISH" },
        { label: "VIX INDEX", value: m.vixVal || 'N/A', change: "CALM", state: "STABLE" },
        { label: "DXY DOLLAR", value: m.dxyVal || 'N/A', change: "N/A", state: "NEUTRAL" },
        { label: "10Y YIELD", value: `${m.yieldVal || 'N/A'}%`, change: `${m.yieldPrev || 'N/A'}% PREV`, state: "CONSTRAINED" }
    ];

    document.getElementById('vitals-matrix-deck').innerHTML = macroVitals.map(v => `
      <div class="bg-zinc-950 border border-zinc-800 p-3">
        <div class="text-[9px] text-zinc-400 font-bold uppercase tracking-wider">${v.label}</div>
        <div class="text-lg font-black text-white mt-1">${v.value}</div>
        <div class="text-[10px] ${v.change.includes('-') ? 'text-[#ff003c]' : 'text-[#00ff66]'} font-bold mt-1">${v.change}</div>
      </div>
    `).join('');

    // Polymarket Prediction Odd Tracking Module UI Updates
    const computedPolyOdds = parseInt(m.marketOdds) || 50;
    document.getElementById('poly-odds-pct').innerText = `${computedPolyOdds}% ODDS`;
    document.getElementById('poly-odds-bar').style.width = `${computedPolyOdds}%`;

    // Intel Wire scrolling news block compiler injection
    const fallBackNewsWires = [m.newsText || "Bond metrics flag caution parameters on duration tracking loops."];
    document.getElementById('intel-wires-feed').innerHTML = fallBackNewsWires.map(wire => `
      <div class="p-2 bg-zinc-950 border border-zinc-900 text-zinc-300 font-mono tracking-tight leading-normal border-l-2 border-zinc-600">
        <span class="text-zinc-500 font-bold">// WIRE_IN:</span> ${wire}
      </div>
    `).join('');

  } catch(e) { console.error("🎚️ [REBIND INTEGRITY EXCEPTION]:", e.message); }
}

// Sub-interface control execution handlers
window.switchIntelLevel = function(lvl) {
  document.querySelectorAll('#intel-level-toggles button').forEach(b => b.className = "px-2 py-0.5 border border-transparent text-zinc-400");
  const btn = document.getElementById(`btn-${lvl}`);
  if(btn) btn.className = "px-2 py-0.5 bg-zinc-900 border border-zinc-700 text-white font-bold";
  document.getElementById('intel-narrative-box').innerText = intelligenceLevelsCache[lvl] || "--";
};
window.toggleAgentTab = function(tabId) {
  document.querySelectorAll('#agent-tab-headers button').forEach(b => b.className = "py-2 text-zinc-400 border-b-2 border-transparent");
  const btn = document.getElementById(`tab-btn-${tabId}`);
  if(btn) btn.className = "py-2 bg-zinc-900 text-white border-b-2 border-[#ff003c] font-bold";
  
  const selectedAgentData = agentConsensusCache[tabId] || { score: "N/A", text: "No active matrix output logs found." };
  document.getElementById('agent-pane-header').innerText = `AGENT_OUTPUT // ${tabId.toUpperCase()} — RATIO: ${selectedAgentData.score}`;
  document.getElementById('agent-text-content').innerText = selectedAgentData.text;
};

"""

# Finding injection points
term_start = html.find('<section id="view-terminal"')
alpha_start = html.find('<section id="view-alpha"')

if term_start != -1 and alpha_start != -1:
    # 1. Replace the HTML views
    top_html = html[:term_start]
    alpha_html = html[alpha_start:]
    
    # We need to find where the <script> begins to not overwrite the mobile nav
    mobile_nav_start = html.find('<div class="md:hidden fixed bottom-0 left-0 right-0')
    if mobile_nav_start != -1:
        # Reconstruct HTML
        alpha_html_only = html[alpha_start:mobile_nav_start]
        mobile_nav_html = html[mobile_nav_start:]
        
        # 2. Replace the JS
        # The user_js should replace `async function loadTerminalPayload` to the end of the script
        js_start = mobile_nav_html.find('async function loadTerminalPayload()')
        if js_start != -1:
            js_end = mobile_nav_html.find('</script>', js_start)
            if js_end != -1:
                new_mobile_and_js = mobile_nav_html[:js_start] + user_js + '\\n  ' + mobile_nav_html[js_end:]
                
                final_html = top_html + user_html + '\\n      ' + alpha_html_only + new_mobile_and_js
                
                with open('public/index.html', 'w', encoding='utf-8') as f:
                    f.write(final_html)
                print("Injected user's master blueprint successfully.")
            else:
                print("JS End not found")
        else:
            print("JS Start not found")
    else:
        print("Mobile nav not found")
else:
    print("Section markers not found")

