# Chaos Intelligence 14x

This is a secure production starter kit for turning the current Chaos Intelligence n8n workflow into a real market intelligence product.

It contains:

- A static dashboard in `public/index.html`
- Local JSON API outputs in `public/api/`
- Core market, signal, validation, and Telegram helpers in `src/`
- Runner scripts in `scripts/`
- Supabase ledger schema in `supabase/schema.sql`
- n8n paste-in code nodes in `n8n/code/`
- The final DPR and launch runbook in `docs/`

## Critical First Step

The workflow you pasted had real secrets in it. Rotate every exposed key before running any production workflow:

- AI providers
- News/FRED keys
- Telegram bot token
- GitHub token/credential if it had broad write access

Do not paste real keys into Code nodes. Use n8n Credentials, GitHub Secrets, or environment variables.

## Quick Local Smoke Test

```powershell
npm test
node scripts/run-brief.js
```

`run-brief.js` will try live public data where possible and falls back safely if network/API credentials are missing.

Open:

```text
public/index.html
```

For best browser behavior, serve the folder with any static server.

## Production Flow

Recommended flow:

1. n8n collects data and calls OpenRouter agents.
2. Parse + Validate normalizes the final JSON.
3. Signal Ledger Logger writes every signal to Supabase.
4. HTML/dashboard reads latest JSON and ledger stats.
5. Telegram Free sends teaser.
6. Telegram Pro sends full plays and alerts.
7. Resolver workflow marks signals win/loss after the selected window.

## What Makes This 14/10

The upgrade is not more decoration. It is trust architecture:

- No secrets in exports
- No fake track record
- Every signal stored
- Every signal resolved
- Multi-agent disagreement visible
- Safe fallback when AI/data fails
- Free tier gives real value
- Pro tier unlocks faster, deeper intelligence

