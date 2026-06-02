import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject the Background CSS Overlay
bg_css = """
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url('backdrop.png');
    background-size: cover;
    background-position: center;
    z-index: -2;
}
body::after {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-color: rgba(0, 0, 0, 0.75); /* Dark cinematic overlay */
    backdrop-filter: blur(8px);
    z-index: -1;
}

/* Fix mobile nav */
.web-menu {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.menu-links {
    display: flex;
    gap: 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.menu-links a {
    color: var(--ink);
    text-decoration: none;
    transition: color 0.2s ease;
}
.menu-links a:hover {
    color: var(--highlight);
}
@media (max-width: 600px) {
    .menu-links { display: none; }
}
"""

html = html.replace('</style>', bg_css + '\n</style>')

# 2. Inject the Burger & Web Menu into the body
nav_html = """
  <nav class="web-menu wrap">
    <div class="menu-brand" style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.2rem; letter-spacing: 2px;">CHAOS<em style="color:var(--highlight);font-style:normal">.</em></div>
    <div class="menu-links">
      <a href="#">Terminal</a>
      <a href="#">Ledger</a>
      <a href="#">Pro Access</a>
      <a href="#">Docs</a>
    </div>
    <div class="burger-menu" style="cursor: pointer; color: var(--highlight);">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </div>
  </nav>
"""

# Insert right after <div class="boot" id="boot-scr">...</div>
html = re.sub(r'(<div class="boot".*?</div>)', r'\1\n' + nav_html, html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Background and Menus added.")
