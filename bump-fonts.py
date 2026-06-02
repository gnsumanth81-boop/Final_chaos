import re
import sys

def bump_font_sizes(content):
    def repl(match):
        val = float(match.group(1))
        if val < 0.8:
            new_val = val + 0.35
            return f"font-size:{new_val:.2f}rem"
        return match.group(0)
    
    # Also fix some specific buttons to make them pop more
    content = content.replace("background:var(--s2)", "background:var(--s3)") # More contrast for ghost buttons
    content = content.replace(".s-btn.ghost{", ".s-btn.ghost{padding:10px 18px;") 
    content = content.replace(".voice-btn{", ".voice-btn{padding:4px 16px;height:auto;") 
    
    return re.sub(r'font-size:\.?(\d+(?:\.\d+)?)rem', repl, content)

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_html = bump_font_sizes(html)

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Font sizes bumped!")
