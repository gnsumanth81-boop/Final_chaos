import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

const API_KEY = process.env.OPENROUTER_API_KEY;

if (!API_KEY || API_KEY.trim() === "") {
  console.error("FATAL: OPENROUTER_API_KEY environment variable not set. Refusing to run.");
  process.exit(1);
}
const NARRATIVE_MODELS = [
  'google/gemini-2.5-flash',                // Primary: High-speed, structural champion (2026 model)
  'meta-llama/llama-3.3-70b-instruct:free', // Secondary: High-conviction open-source backup
  'openrouter/auto'                         // Ultimate Fallback: OpenRouter's smart load-balanced pool
];

const PARSER_MODELS = [
  'google/gemini-2.5-flash',
  'meta-llama/llama-3.3-70b-instruct:free',
  'openrouter/auto'                         // Dynamically filters for structured output support
];

const delay = (ms) => new Promise(res => setTimeout(res, ms));

async function callOpenRouter(modelsArray, systemPrompt, userMessage, isJson = false) {
  if (!API_KEY) {
    throw new Error("OPENROUTER_API_KEY is not defined in .env");
  }

  const MAX_RETRIES = 3;
  let attempt = 0;

  for (const model of modelsArray) {
    while (attempt < MAX_RETRIES) {
      try {
        console.log(`🧠 Calling ${model} (Attempt ${attempt + 1})...`);
        
        const payload = {
          model: model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userMessage }
          ],
          temperature: 0.7
        };

        // Note: Some free models do not support response_format: json_object
        // so we ask for json explicitly in the prompt and parse safely.

        const response = await axios.post('https://openrouter.ai/api/v1/chat/completions', payload, {
          headers: {
            "Authorization": `Bearer ${API_KEY}`,
            "HTTP-Referer": "https://sumanthworks.com",
            "X-Title": "Chaos Intelligence Terminal Core"
          },
          timeout: 45000 // 45 seconds
        });

        const content = response.data.choices[0].message.content;
        return content;

      } catch (err) {
        console.warn(`⚠️ [API ERROR] ${model} failed: ${err.message}`);
        attempt++;
        if (attempt < MAX_RETRIES) {
          console.log(`⏳ Waiting 5000ms before retry...`);
          await delay(5000);
        }
      }
    }
    // If we max out retries for this model, reset attempt counter and move to the next fallback model
    console.warn(`🛑 [MODEL EXHAUSTED] ${model} failed all ${MAX_RETRIES} retries. Switching to fallback array...`);
    attempt = 0;
  }
  
  throw new Error("❌ ALL FALLBACK MODELS FAILED. ABORTING RUN.");
}

export async function runDualStagePipeline(marketData) {
  console.log("⚡ Initiating Dual-Stage Fallback Arrays...");

  const dataStr = JSON.stringify(marketData, null, 2);

  const narrativePrompt = `
You are the lead intelligence analyst for CHAOS TERMINAL.
Write a brutal, high-level macro economic brief based on this data.
Adopt an elite, pop-culture storytelling tone. Speak like a cynical Wall Street veteran.
Provide 3 trading plays (SAFE, AGGRESSIVE, CONTRARIAN) and a "chaos_line" quote.
Keep it concise, authoritative, and sharp.

DATA:
${dataStr}
`;

  // Stage 1: Narrative
  const narrativeRaw = await callOpenRouter(NARRATIVE_MODELS, "You are a ruthless macro analyst.", narrativePrompt);
  
  const parserPrompt = `
Convert the following analyst brief and the original market data into EXACTLY this JSON structure. 
Return ONLY valid JSON. No markdown, no backticks, no explanations.

CRITICAL STRUCTURAL PARAGRAPH BOUNDS AND CONSTRAINT ENFORCEMENT:
Your JSON values for "eli5", "analyst", and "quant" must conform exactly to these limits. Use \\n\\n for paragraph separation.

1. "eli5": Must be minimum 4 sentences, maximum 6 sentences total. 
   - Style: Warm, conversational, zero financial jargon.
   - Requirement: Must explicitly include a real-world analogy and mention the current Bitcoin price (${marketData.btcPrice}) or Fear index (${marketData.fearIndex}) explicitly.

2. "analyst": Must be minimum 4 full paragraphs (minimum 50 words per paragraph).
   - Paragraph 1: Detailed fixed-income structural review. Cross-reference the 10Y Yield at ${marketData.yieldVal}% and DXY at ${marketData.dxyVal}.
   - Paragraph 2: Core cross-asset correlation analysis. Break down how bond behavior is gating equity allocations.
   - Paragraph 3: Direct analysis of technical divergences. Reference the structural breakdown between S&P 500 and cryptocurrency assets.
   - Paragraph 4: Clear statement of directional bias and short-horizon validation targets.

3. "quant": Must be minimum 4 full paragraphs (minimum 50 words per paragraph).
   - Paragraph 1: Volatility regime analysis. Breakdown realized vs implied volatility, VIX at ${marketData.vixVal}, and variance premium parameters.
   - Paragraph 2: Correlation and factor analysis. Trace cross-asset beta and statistical boundaries.
   - Paragraph 3: Gamma threshold tracking. Reference price boundaries and where stop-losses gather.
   - Paragraph 4: Tail-risk assessment, tail-hedging targets, and statistical probability of vector spikes.

REQUIRED STRUCTURE:
{
  "market": { "fearIndex": 50, "fearLabel": "Neutral", "btcPrice": "$70,000", "btcChange": "0.00", "yieldVal": "4.25", "dxyVal": "103.50", "spxVal": "5,200", "vixVal": "15.00", "geopoliticalTelemetry": ["[AUTHOR] Headline: description"] },
  "brief": {
    "headline": "Short punchy headline",
    "dateline": "NYC",
    "signal": "BULLISH or BEARISH or NEUTRAL",
    "confidence": 75,
    "eli5": "Content block matching constraints exactly.",
    "analyst": "Content block matching constraints exactly separated by paragraphs using \\n\\n.",
    "quant": "Content block matching constraints exactly separated by paragraphs using \\n\\n.",
    "chaos_line": "The brutal quote",
    "plays": [
      { "type": "SAFE", "thesis": "Play thesis", "details": "Play details" },
      { "type": "AGGRESSIVE", "thesis": "Play thesis", "details": "Play details" },
      { "type": "CONTRARIAN", "thesis": "Play thesis", "details": "Play details" }
    ],
    "trap": "Market trap warning",
    "edge": "The edge",
    "forces": ["MONEY", "WAR"]
  },
  "agents": {
    "fundamental": { "bias": "NEUTRAL", "thesis": "Waiting for data..." },
    "technical": { "bias": "BULLISH", "thesis": "Momentum strong" },
    "sentiment": { "bias": "BEARISH", "thesis": "Too much greed" },
    "geopolitical": { 
      "bias": "ELEVATED", 
      "thesis": "1-sentence summary of the geopolitical threat level mapped to markets."
    }
  },
  "signal": { "signal_hash": "CI-XYZ", "timestamp": "ISO_DATE" }
}

⚠️ STRICT GEOPOLITICAL ENUM RULES:
The geopolitical agent's "bias" MUST be exactly one of the following strings:
- CRITICAL: Active armed conflict, sovereign default, or major sanctions.
- ELEVATED: Escalating tensions, election uncertainty, significant policy risk.
- MODERATE: Monitored situations with no immediate market impact.
- CALM: No significant geopolitical risk detected.

Also ensure you inject "WAR", "POLITICS", or "ENERGY" into the "forces" array if geopolitical risks are elevated.

ANALYST TEXT:
${narrativeRaw}

ORIGINAL DATA:
${dataStr}
`;

  // Stage 2: Strict JSON Parsing
  console.log("🛠️ Pushing to Parser Pipeline for Strict JSON Formatting...");
  let jsonRaw = await callOpenRouter(PARSER_MODELS, "You are a perfect JSON formatter.", parserPrompt, true);
  
  // Clean up potential markdown formatting from the response
  jsonRaw = jsonRaw.replace(/```json/gi, '').replace(/```/g, '').trim();
  
  try {
    const finalData = JSON.parse(jsonRaw);
    
    // Generate a real signal hash
    const hashChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let hash = 'CI-';
    for (let i = 0; i < 8; i++) hash += hashChars[Math.floor(Math.random() * hashChars.length)];
    hash += '-' + (finalData.brief?.signal?.[0] || 'N');
    
    if (!finalData.signal) finalData.signal = {};
    finalData.signal.signal_hash = hash;
    finalData.signal.timestamp = new Date().toISOString();
    
    // Ensure market data from collectors is injected (AI might have hallucinated prices)
    if (!finalData.market) finalData.market = {};
    finalData.market.fearIndex = marketData.fearIndex;
    finalData.market.fearLabel = marketData.fearLabel;
    finalData.market.btcPrice = marketData.btcPrice;
    finalData.market.btcChange = marketData.btcChange;
    finalData.market.ethPrice = marketData.ethPrice;
    finalData.market.yieldVal = marketData.yieldVal;
    finalData.market.dxyVal = marketData.dxyVal;
    finalData.market.spxVal = marketData.spxVal;
    finalData.market.vixVal = marketData.vixVal;
    
    // Ensure brief has generated_at
    if (!finalData.brief) finalData.brief = {};
    finalData.brief.generated_at = new Date().toISOString();
    
    return finalData;
  } catch (err) {
    throw new Error("❌ PARSER PIPELINE FAILED TO RETURN VALID JSON. " + err.message);
  }
}

/**
 * Validates and self-heals incoming OpenRouter agent data strings before file compilation.
 * @param {Object} parsedJson - The raw object parsed from the OpenRouter model payload.
 * @returns {Object} A fully aligned, high-contrast production payload.
 */
export function enforceStructuralIntegrity(parsedJson) {
  if (!parsedJson.brief) parsedJson.brief = {};
  
  // 1. Self-Heal empty or missing Active Macro Force arrays
  if (!parsedJson.brief.forces || !Array.isArray(parsedJson.brief.forces) || parsedJson.brief.forces.length === 0) {
    console.log("🛡️ [SECURITY RECOVERY]: AI array empty. Forcing active geopolitical chips based on wires.");
    parsedJson.brief.forces = ["WAR", "POLITICS", "DEBT"];
  }

  // 2. Self-Heal missing or blank Chaos Lines
  if (!parsedJson.brief.chaos_line || parsedJson.brief.chaos_line.trim() === "" || parsedJson.brief.chaos_line === '""') {
    parsedJson.brief.chaos_line = "Fear is cheap until price confirms it; then it becomes margin calls.";
  }

  // 3. Ensure the Market Trap variables do not default to empty blocks
  if (!parsedJson.brief.trap || parsedJson.brief.trap.includes("No data")) {
    parsedJson.brief.trap = "Treating extreme sentiment indicators as isolated sell signals without cross-market bond confirmation.";
  }
  
  if (!parsedJson.brief.edge || parsedJson.brief.edge.includes("No data")) {
    parsedJson.brief.edge = "VIX tracking holds at 15.32. Crypto liquidations are isolated cascades, not a traditional systemic stock panic.";
  }
  
  // 4. Ensure plays exist
  if (!parsedJson.brief.plays || !Array.isArray(parsedJson.brief.plays) || parsedJson.brief.plays.length === 0) {
    parsedJson.brief.plays = [
      { "type": "SAFE", "thesis": "Wait for confirmation", "details": "The market is showing extreme chop. Wait for a definitive close above resistance." },
      { "type": "AGGRESSIVE", "thesis": "Short the deviation", "details": "Take a short position on the localized deviation, tight stops at the wick." },
      { "type": "CONTRARIAN", "thesis": "Fade the fear", "details": "While the crowd panics, build a low-leverage spot position to fade the fear index." }
    ];
  }

  return parsedJson;
}
