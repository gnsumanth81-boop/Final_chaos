import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Brief Tag (System / Anticonsensus)
# Currently: document.getElementById('brief-tag').textContent = `TODAY'S BRIEFING - ${(b.dateline || 'GLOBAL').toUpperCase()}`;
html = html.replace(
    "document.getElementById('brief-tag').textContent = `TODAY'S BRIEFING - ${(b.dateline || 'GLOBAL').toUpperCase()}`;",
    "document.getElementById('brief-tag').textContent = `SYSTEM // ANTICONSENSUS_v2.0`;"
)

# 2. Update the Context Metaphor title
html = html.replace(
    '<div class="sec-title">INTELLIGENCE LEVEL - PICK YOURS</div>',
    '<div class="sec-title">THE CONTEXT METAPHOR</div>'
)

# 3. Update The Plays title
html = html.replace(
    '<div class="sec-title">THE PLAYS - 3 WAYS TO TRADE THIS</div>',
    '<div class="sec-title">THE ANTICIPATED BETS // OVERRIDING THE MACHINE</div>'
)

# 4. Update the Footer
old_footer = '<div class="ftr-disc">Not financial advice. AI-generated from public data. Public ledger required before performance claims. Chaos Intelligence.</div>'
new_footer = '<div class="ftr-disc" style="text-transform:uppercase;letter-spacing:1px;">RAW SELECTION DATA REWRITTEN VIA OPENROUTER API PROVIDERS<br><br><a href="#" style="color:var(--ink);text-decoration:underline;">VERIFY LEDGER AUTHENTICITY ↗</a></div>'
html = html.replace(old_footer, new_footer)

# 5. Make sure the Vibe Pill / Update text uses the exact "UPDATED: 05:25 UTC" format
# Old: document.getElementById('updated-line').textContent = `${timeStr} - LIVE DATA - ${m.label || ''}`;
html = html.replace(
    "document.getElementById('updated-line').textContent = `${timeStr} - LIVE DATA - ${m.label || ''}`;",
    "document.getElementById('updated-line').textContent = `UPDATED: ${timeStr} - LIVE DATA - ${m.label || ''}`;"
)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Vocabulary updated.")
