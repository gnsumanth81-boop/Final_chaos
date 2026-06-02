import json
import re
import os

def extract_and_merge():
    # Read transcript to find the LATEST full v5 workflow JSON the user pasted
    transcript_path = r'C:\Users\sumanth\.gemini\antigravity-ide\brain\bfadf122-a10e-48dd-a262-36b514cef2da\.system_generated\logs\transcript.jsonl'
    
    print("Reading transcript...")
    
    best_json = None
    best_len = 0
    
    with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
        for line_num, line in enumerate(f):
            try:
                step = json.loads(line)
                content = step.get('content', '')
                if not content:
                    # Check tool_calls for content
                    for tc in step.get('tool_calls', []):
                        for k, v in tc.get('arguments', {}).items():
                            if isinstance(v, str) and len(v) > len(content):
                                content = v
                
                if '"Chaos Intelligence Bot v5' in content and '"nodes"' in content:
                    # Find the JSON object
                    idx = content.find('{\n  "name": "Chaos Intelligence Bot v5')
                    if idx == -1:
                        idx = content.find('{"name": "Chaos Intelligence Bot v5')
                    if idx == -1:
                        idx = content.find('{  "name": "Chaos Intelligence Bot v5')
                    if idx == -1:
                        # Try broader match
                        idx = content.find('"Chaos Intelligence Bot v5')
                        if idx > 0:
                            idx = content.rfind('{', 0, idx)
                    
                    if idx >= 0:
                        # Try to find the matching closing brace
                        depth = 0
                        end_idx = -1
                        for i in range(idx, len(content)):
                            if content[i] == '{':
                                depth += 1
                            elif content[i] == '}':
                                depth -= 1
                                if depth == 0:
                                    end_idx = i + 1
                                    break
                        
                        if end_idx > idx and (end_idx - idx) > best_len:
                            candidate = content[idx:end_idx]
                            # Quick validation
                            try:
                                parsed = json.loads(candidate)
                                if 'nodes' in parsed:
                                    best_json = parsed
                                    best_len = end_idx - idx
                                    print(f"  Found valid v5 JSON at line {line_num}, length={best_len}, nodes={len(parsed.get('nodes',[]))}")
                            except json.JSONDecodeError as e:
                                # Try to fix common issues
                                try:
                                    # Replace control characters
                                    cleaned = re.sub(r'[\x00-\x1f]', lambda m: '\\n' if m.group() == '\n' else '', candidate)
                                    parsed = json.loads(cleaned)
                                    if 'nodes' in parsed:
                                        best_json = parsed
                                        best_len = end_idx - idx
                                        print(f"  Found cleaned v5 JSON at line {line_num}, length={best_len}")
                                except:
                                    print(f"  Found v5 JSON candidate at line {line_num} but couldn't parse ({e})")
            except Exception as e:
                pass
    
    if best_json is None:
        print("\nCouldn't extract from transcript. Trying to read from user's latest message...")
        # Fallback: try to read all .json files in the directory
        # and also try to reconstruct from the n8n/code directory
        print("Building workflow from scratch using known v5 structure...")
        best_json = build_v5_from_scratch()
    
    if best_json is None:
        print("FAILED to build workflow. Exiting.")
        return
        
    print(f"\nBase workflow: '{best_json.get('name')}' with {len(best_json.get('nodes',[]))} nodes")
    
    # Now build the complete v7 workflow
    build_v7(best_json)

def build_v5_from_scratch():
    """Reconstruct the v5 workflow from known node structure"""
    return {
        "name": "Chaos Intelligence Bot v5",
        "nodes": [
            {
                "parameters": {"rule": {"interval": [{"triggerAtMinute": 1}]}},
                "type": "n8n-nodes-base.scheduleTrigger",
                "typeVersion": 1.3,
                "position": [-1400, -200],
                "id": "c09c379c-schedule",
                "name": "Schedule Trigger"
            },
            {
                "parameters": {
                    "jsCode": "// CONFIG - ADD YOUR KEYS HERE\nreturn [{ json: {\n  OPENROUTER_KEY: 'YOUR_OPENROUTER_KEY_HERE',\n  NEWSAPI_KEY: 'YOUR_NEWSAPI_KEY_HERE',\n  FRED_KEY: 'YOUR_FRED_KEY_HERE'\n}}];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [-1200, -200],
                "id": "config-node",
                "name": "⚙️ CONFIG"
            },
            {
                "parameters": {"url": "https://gamma-api.polymarket.com/markets?limit=10&active=true&closed=false&order=volume24hr&ascending=false", "options": {"timeout": 10000}},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-1000, -200],
                "id": "polymarket-node",
                "name": "Get Top Markets",
                "continueOnFail": True
            },
            {
                "parameters": {"jsCode": "try {\n  const items = $input.all().map(item => {\n    const d = item.json;\n    if (d.Title || d.error || d.code) return { json: d };\n    const prices = d.outcomePrices ? JSON.parse(d.outcomePrices) : [];\n    const yesOdds = prices[0] ? (parseFloat(prices[0]) * 100).toFixed(1) : '50.0';\n    return { json: {\n      Title: d.question || d.title || 'Unknown',\n      Odds: yesOdds,\n      Volume: d.volume ? '$' + Math.round(parseFloat(d.volume)).toLocaleString() : '$0',\n      Link: d.slug ? 'https://polymarket.com/event/' + d.slug : 'https://polymarket.com'\n    }};\n  });\n  return items;\n} catch(e) {\n  return [{ json: { Title: 'Market Data Unavailable', Odds: '50.0', Volume: '$0', Link: 'https://polymarket.com' }}];\n}"},
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [-800, -200],
                "id": "format-signals",
                "name": "Format Signals",
                "continueOnFail": True
            },
            {
                "parameters": {},
                "type": "n8n-nodes-base.limit",
                "typeVersion": 1,
                "position": [-600, -200],
                "id": "limit-top1",
                "name": "Limit to Top 1",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://api.alternative.me/fng/?limit=2", "options": {"timeout": 10000}},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-1200, 0],
                "id": "fear-greed",
                "name": "FearGreedAPI",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=BTCUSDT"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-1000, 0],
                "id": "binance-btc",
                "name": "BinanceBTC",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=ETHUSDT"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-800, 0],
                "id": "binance-eth",
                "name": "BinanceETH",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=2d"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-600, 0],
                "id": "vix-node",
                "name": "VIX Index",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX?interval=1d&range=2d"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-400, 0],
                "id": "treasury-node",
                "name": "10Y Treasury",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB?interval=1d&range=2d"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-200, 0],
                "id": "dxy-node",
                "name": "DXY Dollar",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=2d"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [0, 0],
                "id": "spx-node",
                "name": "S&P 500",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "={{ 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=' + $('⚙️ CONFIG').first().json.NEWSAPI_KEY }}"},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [200, 0],
                "id": "news-node",
                "name": "ContextNews",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://api.coingecko.com/api/v3/global", "options": {"timeout": 10000}},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-1200, 200],
                "id": "coingecko-node",
                "name": "CoinGecko",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "https://www.reddit.com/r/wallstreetbets/hot.json?limit=10", "options": {"timeout": 10000}, "headerParameters": {"parameters": [{"name": "User-Agent", "value": "chaos-bot/1.0"}]}},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-1000, 200],
                "id": "reddit-node",
                "name": "Reddit WSB",
                "continueOnFail": True
            },
            {
                "parameters": {"url": "={{ 'https://api.stlouisfed.org/fred/series/observations?series_id=RECPROUSM156N&limit=1&sort_order=desc&file_type=json&api_key=' + $('⚙️ CONFIG').first().json.FRED_KEY }}", "options": {"timeout": 10000}},
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.3,
                "position": [-800, 200],
                "id": "fred-node",
                "name": "FRED Recession",
                "continueOnFail": True
            }
        ],
        "connections": {}
    }


def build_v7(base_workflow):
    """Merge v5 base with all 3 new brains + OpenRouter routing"""
    
    workflow = base_workflow.copy()
    workflow['name'] = 'Chaos Intelligence v7 — Ultimate Edition (3 Brains + OpenRouter)'
    
    # Ensure connections dict exists
    if 'connections' not in workflow:
        workflow['connections'] = {}
    
    # ================================================================
    # ADD NEW NODES: Alpha Brain, Autopsy Brain, Geopolitical Brain
    # ================================================================
    
    new_nodes = [
        # ── ALPHA BRAIN ──
        {
            "parameters": {"url": "https://fapi.binance.com/fapi/v1/trades?symbol=BTCUSDT&limit=1000", "options": {}},
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [-1200, 600],
            "id": "alpha-trades",
            "name": "🐋 Binance Trades",
            "continueOnFail": True
        },
        {
            "parameters": {"url": "https://fapi.binance.com/fapi/v1/allForceOrders?symbol=BTCUSDT&limit=100", "options": {}},
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [-1000, 600],
            "id": "alpha-liqs",
            "name": "🐋 Binance Liquidations",
            "continueOnFail": True
        },
        {
            "parameters": {
                "jsCode": "// ═══════════════════════════════════════════════════════════\n// ALPHA DATA AGGREGATOR — Whale + Liquidation Intelligence\n// ═══════════════════════════════════════════════════════════\nlet trades = [];\ntry { trades = $('🐋 Binance Trades').first().json; if (!Array.isArray(trades)) trades = []; } catch(e) { trades = []; }\nlet liqs = [];\ntry { liqs = $('🐋 Binance Liquidations').first().json; if (!Array.isArray(liqs)) liqs = []; } catch(e) { liqs = []; }\n\nlet whaleBlocks = 'No singular block trades over $500k detected.';\nif (Array.isArray(trades) && trades.length > 0) {\n  const big = trades\n    .map(t => {\n      const price = parseFloat(t.price || 0);\n      const qty = parseFloat(t.qty || 0);\n      const totalValue = price * qty;\n      return { price, qty, totalValue, type: t.isBuyerMaker ? 'SELL' : 'BUY', time: t.time };\n    })\n    .filter(t => t.totalValue >= 500000)\n    .sort((a, b) => b.time - a.time)\n    .slice(0, 5);\n  if (big.length > 0) {\n    whaleBlocks = big.map(t => `${t.type} ${t.qty.toFixed(2)} BTC @ $${t.price.toLocaleString('en-US')} ($${(t.totalValue/1e6).toFixed(2)}M)`).join(' | ');\n  }\n}\n\nlet liqSummary = 'No recent liquidation clusters detected.';\nif (Array.isArray(liqs) && liqs.length > 0) {\n  let longLiq = 0, shortLiq = 0;\n  liqs.forEach(l => {\n    const val = parseFloat(l.p || 0) * parseFloat(l.q || 0);\n    if (l.S === 'BUY') shortLiq += val;\n    if (l.S === 'SELL') longLiq += val;\n  });\n  const total = ((longLiq + shortLiq) / 1e6).toFixed(2);\n  if (parseFloat(total) > 0) {\n    const dom = longLiq > shortLiq ? 'LONGS' : 'SHORTS';\n    liqSummary = `Structural Flush: $${total}M wiped. Dominant cascade: ${dom}. (Longs: $${(longLiq/1e6).toFixed(2)}M, Shorts: $${(shortLiq/1e6).toFixed(2)}M).`;\n  }\n}\n\nreturn [{ json: { whale_blocks: whaleBlocks, liquidation_data: liqSummary } }];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [-800, 600],
            "id": "alpha-aggregator",
            "name": "🐋 Alpha Aggregator"
        },
        {
            "parameters": {
                "jsCode": "// ═══════════════════════════════════════════════════════════\n// 🐋 ALPHA WHALE PROMPT — OpenRouter\n// ═══════════════════════════════════════════════════════════\nconst alphaData = $input.first().json || {};\nconst liqData = alphaData.liquidation_data || 'No data';\nconst blocks = alphaData.whale_blocks || 'No data';\n\nconst prompt = `ROLE: You are the ALPHA TELEMETRY ENGINE for an elite macro trading terminal.\nTASK: Analyze raw orderbook and liquidation data. Output strict terminal-grade JSON.\nTONE: Clinical, robotic, precise. Use exact numbers.\n\nRAW DATA:\n- Liquidation Clusters: ${liqData}\n- Recent Whale Executions: ${blocks}\n\nOUTPUT (valid JSON only, no markdown):\n{\n  \"flush_detection\": {\n    \"cumulative_leverage\": \"e.g. $142.4M\",\n    \"support_margin_lower\": \"e.g. $72,300\",\n    \"support_margin_upper\": \"e.g. $72,550\",\n    \"analysis\": \"1 sentence on cascade velocity.\"\n  },\n  \"whale_blocks\": [\n    { \"timestamp\": \"HH:MM:SS\", \"asset\": \"BTCUSDT\", \"type\": \"SHORT SWEEP / LIMIT BID WALL / BLOCK TWAP\", \"size\": \"e.g. 420.50 BTC\", \"venue\": \"BINANCE FUTURES\" }\n  ]\n}`;\n\nreturn [{ json: {\n  model: 'meta-llama/llama-3.1-8b-instruct:free',\n  messages: [{ role: 'user', content: prompt }],\n  temperature: 0.3,\n  response_format: { type: 'json_object' }\n}}];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [-600, 600],
            "id": "alpha-prompt",
            "name": "📝 Alpha Prompt"
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {"parameters": [
                    {"name": "Authorization", "value": "=Bearer {{ $('⚙️ CONFIG').first().json.OPENROUTER_KEY }}"},
                    {"name": "Content-Type", "value": "application/json"}
                ]},
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({ model: $json.model, messages: $json.messages, temperature: $json.temperature, response_format: $json.response_format }) }}",
                "options": {"timeout": 30000}
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [-400, 600],
            "id": "alpha-openrouter",
            "name": "🐋 OpenRouter (Alpha)",
            "continueOnFail": True
        },

        # ── AUTOPSY BRAIN ──
        {
            "parameters": {
                "jsCode": "// ═══════════════════════════════════════════════════════════\n// 📝 AUTOPSY / RESOLUTION BRAIN — OpenRouter\n// Grades past signals as WIN / LOSS / OPEN\n// ═══════════════════════════════════════════════════════════\nlet pastSignals = [];\ntry { pastSignals = $('Read signals.json').first().json.ledger || []; } catch(e) {}\nlet currentMarket = {};\ntry { currentMarket = $('Chaos Pre-Processor v5').first().json || {}; } catch(e) {}\n\nconst openSignals = pastSignals.filter(s => s.status === 'OPEN' || s.status === 'PENDING').slice(0, 8);\nif (openSignals.length === 0) {\n  return [{ json: { skip: true, message: 'No open signals to resolve.' } }];\n}\n\nconst prompt = `ROLE: You are the AUTOPSY / RESOLUTION ENGINE for Chaos Intelligence.\nTASK: Review past trading signals against CURRENT market reality. Be ruthless and objective.\n\nCURRENT PRICES:\nBTC: ${currentMarket.btcPrice || 'N/A'}\nETH: ${currentMarket.ethPrice || 'N/A'}\nSPX: ${currentMarket.spxVal || 'N/A'}\nVIX: ${currentMarket.vixVal || 'N/A'}\n10Y: ${currentMarket.yieldVal || 'N/A'}%\n\nPAST SIGNALS:\n${JSON.stringify(openSignals, null, 2)}\n\nFor each signal, output ONLY this JSON:\n{\n  \"resolutions\": [\n    {\n      \"signal_hash\": \"exact_hash_from_input\",\n      \"status\": \"WIN | LOSS | OPEN\",\n      \"close_price\": \"current price if closed\",\n      \"pnl_percent\": \"+4.2 or -1.8\",\n      \"autopsy_note\": \"One brutal honest sentence.\"\n    }\n  ]\n}`;\n\nreturn [{ json: {\n  model: 'google/gemini-2.5-flash',\n  messages: [{ role: 'user', content: prompt }],\n  temperature: 0.1,\n  response_format: { type: 'json_object' }\n}}];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [-600, 800],
            "id": "autopsy-prompt",
            "name": "📝 Autopsy Prompt"
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {"parameters": [
                    {"name": "Authorization", "value": "=Bearer {{ $('⚙️ CONFIG').first().json.OPENROUTER_KEY }}"},
                    {"name": "Content-Type", "value": "application/json"}
                ]},
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({ model: $json.model, messages: $json.messages, temperature: $json.temperature, response_format: $json.response_format }) }}",
                "options": {"timeout": 30000}
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [-400, 800],
            "id": "autopsy-openrouter",
            "name": "📝 OpenRouter (Autopsy)",
            "continueOnFail": True
        },

        # ── GEOPOLITICAL BRAIN ──
        {
            "parameters": {
                "jsCode": "// ═══════════════════════════════════════════════════════════\n// 🌍 GEOPOLITICAL WIRES BRAIN — Narrative Arbitrage Engine\n// ═══════════════════════════════════════════════════════════\nlet articles = [];\ntry { articles = $('ContextNews').first().json.articles || []; } catch(e) {}\nif (articles.length === 0) return [{ json: { skip: true, message: 'No news data.' } }];\n\nconst rawNews = articles.slice(0, 15).map((a, i) => `[${a.source?.name || 'Wire'}] ${a.title}`).join('\\n');\n\nconst prompt = `ROLE: You are the CHIEF MACRO STRATEGIST for an elite quantitative hedge fund.\nTASK: Review the raw headline firehose. Extract the 3 most critical events moving liquidity today. Ignore noise.\nTONE: Terse, analytical, focused on second-order effects and asset correlation.\n\nRAW HEADLINES:\n${rawNews}\n\nOUTPUT (valid JSON only, no markdown):\n{\n  \"intel_wires\": [\n    {\n      \"source\": \"e.g. REUTERS, MACRO DESK, GEO-POL\",\n      \"title\": \"Punchy 5-7 word summary\",\n      \"impact\": \"2 sentences on second-order impact on BTC, DXY, SPX, or 10Y Yields.\",\n      \"forces\": [\"Pick 1-2 from: MONEY, TECH, ENERGY, POLITICS, WAR, DEBT, JOBS, FOOD, PEOPLE\"]\n    }\n  ]\n}`;\n\nreturn [{ json: {\n  model: 'anthropic/claude-3.5-sonnet',\n  messages: [{ role: 'user', content: prompt }],\n  temperature: 0.4,\n  response_format: { type: 'json_object' }\n}}];"
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [-600, 1000],
            "id": "geo-prompt",
            "name": "🌍 Geo Wires Prompt"
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {"parameters": [
                    {"name": "Authorization", "value": "=Bearer {{ $('⚙️ CONFIG').first().json.OPENROUTER_KEY }}"},
                    {"name": "Content-Type", "value": "application/json"}
                ]},
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({ model: $json.model, messages: $json.messages, temperature: $json.temperature, response_format: $json.response_format }) }}",
                "options": {"timeout": 30000}
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [-400, 1000],
            "id": "geo-openrouter",
            "name": "🌍 OpenRouter (Geo)",
            "continueOnFail": True
        }
    ]

    # Add new nodes
    workflow['nodes'].extend(new_nodes)

    # ================================================================
    # WIRE ALL CONNECTIONS
    # ================================================================
    conns = workflow['connections']

    def add_conn(source, target, index=0):
        if source not in conns:
            conns[source] = {"main": [[]]}
        if 'main' not in conns[source]:
            conns[source]['main'] = [[]]
        while len(conns[source]['main']) <= 0:
            conns[source]['main'].append([])
        conns[source]['main'][0].append({"node": target, "type": "main", "index": index})

    # ── Original v5 pipeline ──
    add_conn("Schedule Trigger", "⚙️ CONFIG")
    add_conn("⚙️ CONFIG", "Get Top Markets")
    add_conn("⚙️ CONFIG", "FearGreedAPI")
    add_conn("⚙️ CONFIG", "BinanceBTC")
    add_conn("⚙️ CONFIG", "BinanceETH")
    add_conn("⚙️ CONFIG", "VIX Index")
    add_conn("⚙️ CONFIG", "10Y Treasury")
    add_conn("⚙️ CONFIG", "DXY Dollar")
    add_conn("⚙️ CONFIG", "S&P 500")
    add_conn("⚙️ CONFIG", "ContextNews")
    add_conn("⚙️ CONFIG", "CoinGecko")
    add_conn("⚙️ CONFIG", "Reddit WSB")
    add_conn("⚙️ CONFIG", "FRED Recession")
    # New: also trigger alpha data fetches
    add_conn("⚙️ CONFIG", "🐋 Binance Trades")
    add_conn("⚙️ CONFIG", "🐋 Binance Liquidations")

    add_conn("Get Top Markets", "Format Signals")
    add_conn("Format Signals", "Limit to Top 1")

    # All data sources -> Pre-Processor
    add_conn("Limit to Top 1", "Chaos Pre-Processor v5")
    add_conn("FearGreedAPI", "Chaos Pre-Processor v5")
    add_conn("BinanceBTC", "Chaos Pre-Processor v5")
    add_conn("BinanceETH", "Chaos Pre-Processor v5")
    add_conn("VIX Index", "Chaos Pre-Processor v5")
    add_conn("10Y Treasury", "Chaos Pre-Processor v5")
    add_conn("DXY Dollar", "Chaos Pre-Processor v5")
    add_conn("S&P 500", "Chaos Pre-Processor v5")
    add_conn("ContextNews", "Chaos Pre-Processor v5")
    add_conn("CoinGecko", "Chaos Pre-Processor v5")
    add_conn("Reddit WSB", "Chaos Pre-Processor v5")
    add_conn("FRED Recession", "Chaos Pre-Processor v5")

    # ── Alpha Brain wiring ──
    add_conn("🐋 Binance Trades", "🐋 Alpha Aggregator")
    add_conn("🐋 Binance Liquidations", "🐋 Alpha Aggregator")
    add_conn("🐋 Alpha Aggregator", "📝 Alpha Prompt")
    add_conn("📝 Alpha Prompt", "🐋 OpenRouter (Alpha)")

    # ── Autopsy Brain wiring (fed by Pre-Processor) ──
    add_conn("Chaos Pre-Processor v5", "📝 Autopsy Prompt")
    add_conn("📝 Autopsy Prompt", "📝 OpenRouter (Autopsy)")

    # ── Geopolitical Brain wiring (fed by ContextNews) ──
    add_conn("ContextNews", "🌍 Geo Wires Prompt")
    add_conn("🌍 Geo Wires Prompt", "🌍 OpenRouter (Geo)")

    # ── All 3 brain outputs + Pre-Processor -> Parse + Validate ──
    # (These nodes exist in the original workflow)
    add_conn("🐋 OpenRouter (Alpha)", "Parse + Validate Output")
    add_conn("📝 OpenRouter (Autopsy)", "Parse + Validate Output")
    add_conn("🌍 OpenRouter (Geo)", "Parse + Validate Output")

    # Save
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chaos_v7_complete.json')
    
    # Convert Python True/False to JSON true/false
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    node_count = len(workflow['nodes'])
    conn_count = sum(len(v.get('main',[[]])[0]) for v in conns.values())
    print("\n" + "="*60)
    print("CHAOS INTELLIGENCE v7 - COMPLETE WORKFLOW")
    print("="*60)
    print(f"Nodes: {node_count}")
    print(f"Connections: {conn_count}")
    print("Brains: Alpha (Whale) + Autopsy (Resolution) + Geopolitical (Macro)")
    print(f"File: {output_path}")
    print("="*60)
    print("\nImport this file into n8n: Menu > Import from File")
    print("Don't forget to add your OPENROUTER_KEY in the CONFIG node!")

extract_and_merge()
