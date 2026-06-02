import re

def execute_phase1():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS with DEFCON classes
    css_injection = """
/* DEFCON Foundations */
body.defcon-chaos {
  --dim: rgba(231, 76, 60, 0.12);
  animation: criticalPulse 3s infinite alternate;
}
body.defcon-stressed {
  --dim: rgba(212, 168, 67, 0.08);
}
body.defcon-calm {
  --dim: rgba(46, 204, 113, 0.04);
}

/* Structural Warning Flags */
body.defcon-chaos .sticky-hdr {
  border-bottom: 1px solid #e74c3c !important;
  box-shadow: 0 4px 20px rgba(231, 76, 60, 0.05);
}

body.defcon-stressed .sticky-hdr {
  border-bottom: 1px solid #d4a843 !important;
}

/* High-End Pulsing Animation for Components */
@keyframes criticalPulse {
  0% { box-shadow: inset 0 0 15px rgba(231, 76, 60, 0.02); }
  100% { box-shadow: inset 0 0 30px rgba(231, 76, 60, 0.06); }
}

/* Monospace constraints for numeric execution values */
.terminal-num {
  font-family: 'JetBrains Mono', monospace !important;
  font-weight: 700;
}
"""
    # Inject CSS just before </style>
    if '/* DEFCON Foundations */' not in html:
        html = html.replace('</style>', css_injection + '\n  </style>')

    # 2. Add Terminal Status Indicator and Decay Timer to HTML header
    # Find sticky-center
    sticky_center = '<div class="sticky-center">\n      <div class="live-b"><span class="live-d"></span>LIVE BRIEF</div>\n    </div>'
    new_sticky_center = """<div class="sticky-center">
      <div class="live-b"><span class="live-d"></span>LIVE BRIEF</div>
      <div id="terminal-status" style="font-family: var(--font-mono); font-size: 0.45rem; color: #fff; letter-spacing: 1px; margin-left: 10px; padding-left: 10px; border-left: 1px solid var(--s3); white-space: nowrap;">LOADING STATUS...</div>
    </div>"""
    html = html.replace(sticky_center, new_sticky_center)

    # 3. Add decay-time-label next to date-line
    dateline = '<div class="dateline"><span id="date-line">LOADING</span><span class="ed-badge" id="session-badge">DAILY BRIEF</span></div>'
    new_dateline = '<div class="dateline"><span id="date-line">LOADING</span><span class="ed-badge" id="session-badge">DAILY BRIEF</span><span id="decay-time-label" style="margin-left:auto; font-family:var(--font-mono); font-size:0.45rem; color:var(--red); font-weight:700;"></span></div>'
    html = html.replace(dateline, new_dateline)

    # 4. Replace Alpha View
    old_alpha = """<!-- ═══════════════════════════════════════════
       VIEW 4: ALPHA (locked)
       ═══════════════════════════════════════════ -->
  <div id="view-alpha" class="spa-view">
    <div class="wrap">
      <div class="alpha-lock">
        <div style="font-size:3rem;margin-bottom:16px">🔒</div>
        <h2>Unlock Whale Orderbook Telemetry</h2>
        <p>Get real-time execution parameters and webhook trade updates pushed direct to your console interface. Unfiltered algorithmic dissent straight from the pool trackers.</p>
        <button class="alpha-btn">UNLOCK ACCESS TIER</button>
      </div>
    </div>
  </div>"""

    new_alpha = """<!-- ═══════════════════════════════════════════
       VIEW 4: ALPHA (WHALE ORDERBOOK TELEMETRY)
       ═══════════════════════════════════════════ -->
  <div id="view-alpha" class="spa-view">
    <div class="wrap" style="padding-top:40px;">
      <div class="page-title">WHALE ORDERBOOK TELEMETRY</div>
      <div class="page-sub">REAL-TIME LIQUIDATION FLOW & INSTITUTIONAL BLOCKS</div>
      
      <!-- Telemetry Coordinates Box -->
      <div class="glass-card rv vis" style="margin-bottom: 24px; border-left: 3px solid #e74c3c; padding: 24px;">
        <div style="font-family: var(--font-mono); font-size: 0.55rem; color: #e74c3c; font-weight: 700; letter-spacing: 2px;">
          ⚠️ ORDERBOOK LIQUIDATION FLOOD DETECTION
        </div>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 8px; color: var(--ink);">
          System identifies <strong class="terminal-num" style="color: #fff;">$142.4M</strong> in cumulative structural leverage clustered heavily within a tight support margin of <span class="terminal-num" style="color: var(--gold);">$72,300</span> to <span class="terminal-num" style="color: var(--gold);">$72,550</span>. A structural wick beneath this threshold triggers a cascade velocity event.
        </p>
      </div>

      <!-- Aggressive Whales Transaction Table -->
      <div class="sec-title" style="margin-top:40px;">INCOMING WHALE BLOCK EXECUTIONS</div>
      <div style="overflow-x: auto; font-family: var(--font-mono); font-size: 0.85rem; border: 1px solid var(--s3); background: rgba(8,8,12,0.5);">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
          <thead>
            <tr style="border-bottom: 2px solid var(--dim); color: var(--muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; background: rgba(255,255,255,0.02);">
              <th style="padding: 16px;">TIMESTAMP (UTC)</th>
              <th style="padding: 16px;">ASSET</th>
              <th style="padding: 16px;">TYPE</th>
              <th style="padding: 16px;">SIZE</th>
              <th style="padding: 16px;">EXECUTION VENUE</th>
            </tr>
          </thead>
          <tbody style="color: var(--ink);">
            <tr style="border-bottom: 1px solid var(--dim);">
              <td style="padding: 16px; color: var(--muted);">16:14:02</td>
              <td style="padding: 16px; font-weight: 700; color: #fff;">BTCUSDT</td>
              <td style="padding: 16px; color: #e74c3c;">SHORT SWEEP</td>
              <td style="padding: 16px;" class="terminal-num">420.50 BTC</td>
              <td style="padding: 16px; font-size: 0.75rem;">BINANCE FUTURES</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--dim);">
              <td style="padding: 16px; color: var(--muted);">16:11:55</td>
              <td style="padding: 16px; font-weight: 700; color: #fff;">ETHUSDT</td>
              <td style="padding: 16px; color: #2ecc71;">LIMIT BID WALL</td>
              <td style="padding: 16px;" class="terminal-num">3,150 ETH</td>
              <td style="padding: 16px; font-size: 0.75rem;">COINBASE PRO</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--dim);">
              <td style="padding: 16px; color: var(--muted);">16:08:11</td>
              <td style="padding: 16px; font-weight: 700; color: #fff;">BTCUSDT</td>
              <td style="padding: 16px; color: #e74c3c;">BLOCK TWAP</td>
              <td style="padding: 16px;" class="terminal-num">185.00 BTC</td>
              <td style="padding: 16px; font-size: 0.75rem;">OKX DERIVATIVES</td>
            </tr>
            <tr>
              <td colspan="5" style="padding: 24px; text-align: center; color: var(--muted); font-size: 0.65rem; letter-spacing: 1px;">
                MORE DATA STREAMING FROM ON-CHAIN NODES...
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>"""
    if '<!-- VIEW 4: ALPHA (locked) -->' in html:
        html = html.replace(old_alpha, new_alpha)

    # 5. Move Plays higher (before the cx-tabs)
    plays_section = r'<section class="rv"><div class="sec-title">THE PLAYS - 3 WAYS TO TRADE THIS</div><div class="plays-grid" id="plays-grid"></div><div style="font-family:var(--font-mono);font-size:.44rem;color:var(--muted);margin-top:10px;letter-spacing:.5px">THESIS ONLY - NOT FINANCIAL ADVICE</div></section>'
    
    # We remove plays_section from its current location
    if plays_section in html:
        html = html.replace(plays_section, "")
        
        # And insert it right after the gauge section
        gauge_section_end = '</section>\n\n        <section class="cx-section rv">'
        new_gauge_section_end = f'</section>\n\n        {plays_section}\n\n        <section class="cx-section rv">'
        html = html.replace(gauge_section_end, new_gauge_section_end)

    # 6. Inject DEFCON and Error Eradication Logic into render() function
    js_inject = """
      // 1. DEFCON LOGIC
      const body = document.body;
      const statusIndicator = document.getElementById('terminal-status');
      body.classList.remove('defcon-calm', 'defcon-stressed', 'defcon-chaos');
      if (fear < 25 || fear > 75) {
        body.classList.add('defcon-chaos');
        if (statusIndicator) statusIndicator.innerHTML = '💀 METRIC DISLOCATION ACTIVE';
      } else if ((fear >= 25 && fear < 45) || (fear > 60 && fear <= 75)) {
        body.classList.add('defcon-stressed');
        if (statusIndicator) statusIndicator.innerHTML = '🟠 ELEVATED VOLATILITY REGIME';
      } else {
        body.classList.add('defcon-calm');
        if (statusIndicator) statusIndicator.innerHTML = '🟢 STABLE LIQUIDITY MATRIX';
      }

      // 2. SIGNAL DECAY TIMER
      const elapsedMinutes = Math.floor((new Date() - generated) / 60000);
      const decayLabel = document.getElementById('decay-time-label');
      if (decayLabel) {
        if(elapsedMinutes >= 0) {
            decayLabel.textContent = `UPDATED ${elapsedMinutes}M AGO`;
        } else {
            decayLabel.textContent = `UPDATED LIVE`;
        }
      }

      // 3. ERROR ERADICATION
      const wiresSection = document.getElementById('wires');
      if (wiresSection && wiresSection.parentElement) {
        if (!m.newsText || m.newsText.includes('not configured') || m.newsText.trim() === '') {
          wiresSection.parentElement.style.display = 'none';
        } else {
          wiresSection.parentElement.style.display = 'block';
        }
      }

      const polySection = document.getElementById('poly-card');
      if (polySection) {
        if (!m.marketTitle || m.marketTitle.includes('unavailable') || m.marketTitle.trim() === '') {
          polySection.style.display = 'none';
        } else {
          polySection.style.display = 'block';
        }
      }
"""
    if 'document.getElementById("gauge-glow").style.background = fearColor;' in html and '// 1. DEFCON LOGIC' not in html:
        html = html.replace('document.getElementById("gauge-glow").style.background = fearColor;', 'document.getElementById("gauge-glow").style.background = fearColor;' + js_inject)

    # ID mapping for poly-card and wires
    # ensure wires section has parentElement that is the section container
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Phase 1 enhancements applied successfully!")

execute_phase1()
