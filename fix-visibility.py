import re

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix Tab Icons (ELI5, Analyst, Quant)
html = html.replace('width:28px;height:28px', 'width:56px;height:56px;filter:drop-shadow(0 0 10px rgba(255,255,255,0.2))')
html = re.sub(r'\.cx-n\{[^\}]+\}', '.cx-n{display:block;font-family:var(--font-ui);font-size:1.6rem;font-weight:700;letter-spacing:1.5px;color:var(--ink);margin-top:8px;}', html)
html = re.sub(r'\.cx-sub\{[^\}]+\}', '.cx-sub{display:block;font-family:var(--font-mono);font-size:0.9rem;color:var(--ink2);margin-top:4px}', html)

# 2. Fix Vitals (Fear Index, BTC, Signal, Confidence)
html = re.sub(r'\.vital-val\{[^\}]+\}', '.vital-val{font-family:var(--font-mono);font-size:2.2rem;font-weight:700;letter-spacing:-0.5px;line-height:1}', html)
html = re.sub(r'\.vital-lbl\{[^\}]+\}', '.vital-lbl{font-family:var(--font-mono);font-size:1.1rem;font-weight:700;color:var(--ink);letter-spacing:1.5px;margin-top:10px;text-transform:uppercase}', html)
html = re.sub(r'\.vital-sub\{[^\}]+\}', '.vital-sub{font-family:var(--font-mono);font-size:0.9rem;margin-top:5px;color:var(--ink2)}', html)
html = re.sub(r'\.vital-ago\{[^\}]+\}', '.vital-ago{font-family:var(--font-mono);font-size:0.85rem;color:var(--muted);margin-top:6px}', html)

# 3. Fix Section Titles (MACRO DASHBOARD, CROSS-MARKET CONTEXT)
html = re.sub(r'\.sec-title\{[^\}]+\}', '.sec-title{font-family:var(--font-ui);font-size:1.6rem;font-weight:700;color:var(--ink);letter-spacing:3px;margin-bottom:20px;display:flex;align-items:center;gap:12px;text-transform:uppercase}', html)

# 4. Fix Agent Consensus
html = re.sub(r'\.agent-name\{[^\}]+\}', '.agent-name{font-family:var(--font-mono);font-size:1rem;font-weight:700;letter-spacing:1.5px;color:var(--ink);margin-bottom:8px;text-transform:uppercase}', html)
html = re.sub(r'\.agent-bias\{[^\}]+\}', '.agent-bias{font-family:var(--font-mono);font-size:1.2rem;font-weight:700;letter-spacing:1px}', html)
html = re.sub(r'\.agent-thesis\{[^\}]+\}', '.agent-thesis{font-family:var(--font-body);font-size:1.1rem;color:var(--ink2);line-height:1.6;margin-top:10px}', html)

# 5. Fix World Clock / Nav
html = re.sub(r'\.world-clock-bar\{[^\}]+\}', '.world-clock-bar{font-family:var(--font-mono);font-size:0.9rem;color:var(--ink2);letter-spacing:1.5px;padding:12px 0;border-bottom:1px solid var(--s3);display:flex;justify-content:flex-start;align-items:center;gap:16px;flex-wrap:wrap}', html)

# 6. Fix Telegram CTA Button
html = re.sub(r'\.tg-cta\{[^\}]+\}', '.tg-cta{margin-bottom:48px;padding:32px;background:linear-gradient(135deg,rgba(76,201,240,.1),var(--s1) 80%);border:2px solid rgba(76,201,240,.3);border-radius:12px;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;box-shadow:0 10px 30px rgba(76,201,240,0.05)}', html)
html = re.sub(r'\.tg-cta-title\{[^\}]+\}', '.tg-cta-title{font-family:var(--font-body);font-size:1.6rem;font-style:italic;color:var(--ink);font-weight:400;margin-bottom:8px;line-height:1.4}', html)
html = re.sub(r'\.tg-cta-sub\{[^\}]+\}', '.tg-cta-sub{font-family:var(--font-mono);font-size:0.95rem;color:var(--blue);letter-spacing:1px;font-weight:700}', html)
html = re.sub(r'\.tg-btn\{[^\}]+\}', '.tg-btn{display:inline-flex;align-items:center;gap:10px;padding:16px 32px;border-radius:8px;font-family:var(--font-mono);font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,#4cc9f0,#228be6);color:#fff;text-decoration:none;box-shadow:0 8px 25px rgba(76,201,240,.4);transition:all .2s ease;white-space:nowrap;letter-spacing:1px}', html)

# 7. Track Record (Signal Ledger)
html = re.sub(r'\.track-empty-txt\{[^\}]+\}', '.track-empty-txt{font-family:var(--font-mono);font-size:1.1rem;color:var(--ink);letter-spacing:1px;margin-bottom:14px}', html)
html = re.sub(r'\.track-progress-label\{[^\}]+\}', '.track-progress-label{font-family:var(--font-mono);font-size:1rem;font-weight:700;color:var(--ink);margin-top:10px}', html)

# 8. Plays
html = re.sub(r'\.play-type\{[^\}]+\}', '.play-type{font-family:var(--font-mono);font-size:1.1rem;font-weight:700;letter-spacing:2px;margin-bottom:12px}', html)
html = re.sub(r'\.play-thesis\{[^\}]+\}', '.play-thesis{font-family:var(--font-ui);font-size:1.4rem;font-weight:700;color:var(--ink);letter-spacing:0.5px;margin-bottom:12px}', html)

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Visibility massively upgraded!")
