import re
import datetime

def execute_phase2():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. SEO META TAGS
    current_desc = '<meta name="description" content="Chaos Intelligence live macro war-room brief. AI-powered market intelligence terminal.">'
    new_meta = """<meta name="description" content="Chaos Intelligence live macro war-room brief.">
  <meta name="keywords" content="market intelligence, fear greed index, macro trading, btc, spx, quantitative analysis, prediction markets, orderbook telemetry">
  <link rel="canonical" href="https://chaos.sumanthworks.com/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://chaos.sumanthworks.com/">
  <meta property="og:title" id="og-title" content="CHAOS. | Live Brief">
  <meta property="og:description" id="og-desc" content="Chaos Intelligence live macro war-room brief.">
  <meta property="og:image" content="https://chaos.sumanthworks.com/og-image.jpg">
  <meta property="og:site_name" content="Chaos Intelligence Terminal">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://chaos.sumanthworks.com/">
  <meta name="twitter:title" id="tw-title" content="CHAOS. | Live Brief">
  <meta name="twitter:description" id="tw-desc" content="Chaos Intelligence live macro war-room brief.">
  <meta name="twitter:image" content="https://chaos.sumanthworks.com/og-image.jpg">"""
    if current_desc in html:
        html = html.replace(current_desc, new_meta)

    # Add dynamic update logic in render()
    js_update = """
      const hd = b.headline || 'Live Brief';
      const cl = b.chaos_line || 'Chaos Intelligence live macro war-room brief.';
      if(document.getElementById('og-title')) document.getElementById('og-title').content = `CHAOS. | ${hd}`;
      if(document.getElementById('tw-title')) document.getElementById('tw-title').content = `CHAOS. | ${hd}`;
      if(document.getElementById('og-desc')) document.getElementById('og-desc').content = cl;
      if(document.getElementById('tw-desc')) document.getElementById('tw-desc').content = cl;
"""
    if "document.getElementById('date-line').textContent =" in html and "document.getElementById('og-title')" not in html:
        html = html.replace("document.getElementById('date-line').textContent =", js_update + "\n      document.getElementById('date-line').textContent =")

    # 2. THE TRUST FOOTER
    old_footer_match = re.search(r'<footer.*?</footer>', html, re.DOTALL)
    if old_footer_match:
        old_footer = old_footer_match.group(0)
        current_year = datetime.datetime.now().year
        new_footer = f"""<footer class="ftr wrap">
  <div class="ftr-content">
    <div class="ftr-brand">CHAOS<em>.</em></div>
    <div class="ftr-links">
      <a href="https://sumanth664.gumroad.com/l/hlpqa" class="ftr-link" target="_blank" rel="noopener">PRO Access</a>
      <a href="https://chaos.sumanthworks.com" class="ftr-link">Live Terminal</a>
      <a href="mailto:rgnsumanth81@gmail.com" class="ftr-link">Support & Inquiries</a>
    </div>
  </div>
  <div class="ftr-disc">
    <strong>CONFIDENTIALITY & DISCLAIMER:</strong> This terminal and its outputs are for informational and educational purposes only. Chaos Intelligence is an automated data synthesis tool, not a registered investment advisor. The intelligence provided, including "Plays" and "Alpha Telemetry," does not constitute financial, investment, or trading advice. Trading cryptocurrencies, equities, and derivatives involves substantial risk of loss. Past performance of the signal ledger is not indicative of future results. Information is gathered from public APIs and is not guaranteed to be accurate or timely.
    <br><br>
    &copy; {current_year} Chaos Intelligence by Sumanth. All rights reserved.
  </div>
</footer>"""
        html = html.replace(old_footer, new_footer)

    # 3. CSS POLISH
    css_injection = """
/* Institutional Footer Styling */
.ftr {
  border-top: 1px solid var(--s3);
  padding: 48px 24px 80px;
  margin-top: 64px;
}
.ftr-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}
.ftr-brand {
  font-family: var(--font-big);
  font-size: 2.2rem;
  letter-spacing: 6px;
  color: var(--muted);
  margin-bottom: 20px;
  opacity: 0.6;
}
.ftr-brand em {
  color: var(--red);
  font-style: normal;
}
.ftr-links {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  justify-content: center;
}
.ftr-link {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--ink2);
  text-decoration: none;
  letter-spacing: 2px;
  text-transform: uppercase;
  transition: all 0.25s ease;
}
.ftr-link:hover {
  color: var(--gold);
  transform: translateY(-1px);
}
.ftr-disc {
  font-family: var(--font-mono);
  font-size: 0.45rem;
  color: var(--muted);
  line-height: 1.9;
  text-align: justify;
  text-align-last: center;
  max-width: 850px;
  margin: 0 auto;
  letter-spacing: 0.8px;
  padding: 24px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--s2);
  border-radius: 6px;
}
.ftr-disc strong {
  color: var(--ink2);
}
"""
    if '/* Institutional Footer Styling */' not in html:
        html = html.replace('</style>', css_injection + '\n  </style>')

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully injected Phase 2 SEO, Footer, and CSS!")

execute_phase2()
