import re

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "r", encoding="utf-8") as f:
    html = f.read()

def bump_size(match):
    val_str = match.group(1)
    # Handle cases like .5rem vs 0.5rem
    if val_str.startswith('.'):
        val = float('0' + val_str)
    else:
        val = float(val_str)
        
    if val < 0.9:
        new_val = val + 0.55
        return f"font-size:{new_val:.2f}rem"
    return match.group(0)

html = re.sub(r'font-size:\s*([0-9]*\.?[0-9]+)rem', bump_size, html)

# Extra fixes to ensure no other tiny fonts remain
# specifically for "THESIS ONLY" which might not be using a class I hit, or maybe it's in a style tag inline?
# Let's just catch all font-size declarations.

with open(r"C:\Users\sumanth\Documents\Codex\2026-05-26\this-was-my-current-system-name\public\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Bumped all tiny fonts by 0.55rem!")
