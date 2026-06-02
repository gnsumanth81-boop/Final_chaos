import { createHash } from "node:crypto";

export const VALID_SIGNALS = new Set(["BULLISH", "BEARISH", "NEUTRAL", "VOLATILE"]);
export const VALID_REGIMES = new Set(["RISK-ON", "RISK-OFF", "LIQUIDITY TRAP", "TRANSITION"]);
export const VALID_FORCES = new Set([
  "MONEY",
  "TECH",
  "ENERGY",
  "POLITICS",
  "WAR",
  "DEBT",
  "JOBS",
  "FOOD",
  "PEOPLE"
]);

export function toNumber(value, fallback = null) {
  if (value === null || value === undefined) return fallback;
  const clean = String(value).replace(/[^0-9.+-]/g, "");
  if (!clean) return fallback;
  const n = Number.parseFloat(clean);
  return Number.isFinite(n) ? n : fallback;
}

export function clamp(value, min, max) {
  const n = toNumber(value, min);
  return Math.min(max, Math.max(min, n));
}

export function pctChange(current, previous) {
  const curr = toNumber(current);
  const prev = toNumber(previous);
  if (!Number.isFinite(curr) || !Number.isFinite(prev) || prev <= 0) return null;
  const pct = ((curr - prev) / prev) * 100;
  return Number.isFinite(pct) && Math.abs(pct) < 50 ? pct : null;
}

export function money(value, digits = 0) {
  const n = toNumber(value);
  if (!Number.isFinite(n)) return "N/A";
  return "$" + n.toLocaleString("en-US", { maximumFractionDigits: digits });
}

export function fixed(value, digits = 2, fallback = "N/A") {
  const n = toNumber(value);
  return Number.isFinite(n) ? n.toFixed(digits) : fallback;
}

export function safeJsonParse(text, fallback = null) {
  try {
    return JSON.parse(text);
  } catch {
    return fallback;
  }
}

export function extractJsonObject(text) {
  if (!text || typeof text !== "string") return null;
  const stripped = text.replace(/```json/gi, "").replace(/```/g, "").trim();
  const match = stripped.match(/\{[\s\S]*\}/);
  return safeJsonParse(match ? match[0] : stripped, null);
}

export function sessionInfo(now = new Date()) {
  const utcHour = now.getUTCHours();
  let session = "US SESSION";
  let marketStatus = "WATCH";

  if (utcHour >= 0 && utcHour < 7) session = "ASIA SESSION";
  else if (utcHour >= 7 && utcHour < 13) session = "EUROPE SESSION";
  else if (utcHour >= 13 && utcHour < 21) session = "US SESSION";
  else session = "AFTER HOURS";

  const ny = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).formatToParts(now);
  const part = (type) => ny.find((p) => p.type === type)?.value;
  const weekday = part("weekday");
  const hour = Number(part("hour"));
  const minute = Number(part("minute"));
  const isWeekday = !["Sat", "Sun"].includes(weekday);
  const nyDecimal = hour + minute / 60;
  const usOpen = isWeekday && nyDecimal >= 9.5 && nyDecimal < 16;
  marketStatus = usOpen ? "NYSE OPEN" : "NYSE CLOSED";

  return {
    session,
    marketStatus,
    utcTime: now.toISOString(),
    label: `${session} / ${marketStatus}`
  };
}

export function computeCvx(data = {}) {
  const fearIndex = clamp(data.fearIndex ?? data.fear_index ?? 50, 0, 100);
  const vix = clamp(data.vix ?? data.vixVal ?? 20, 5, 90);
  const btcChange = toNumber(data.btcChange ?? data.btc_change, 0);
  const ethChange = toNumber(data.ethChange ?? data.eth_change, 0);
  const yield10y = toNumber(data.yield10y ?? data.yieldVal ?? data.yield_10y, 4.2);
  const spxChange = toNumber(data.spxChange ?? data.spx_change, 0);
  const btcHigh = toNumber(data.btcHigh, null);
  const btcLow = toNumber(data.btcLow, null);
  const btcPrice = toNumber(data.btcPrice ?? data.btc_price, null);

  const vixNorm = clamp(((vix - 10) / 70) * 100, 0, 100);
  const intradayRange =
    btcHigh && btcLow && btcPrice && btcHigh > btcLow ? (btcHigh - btcLow) / btcPrice : 0.02;
  const btcEwmaVol = clamp(intradayRange * Math.sqrt(252) * 100 * 4, 0, 100);
  const fearInv = 100 - fearIndex;
  const yieldStress = clamp((Math.abs(yield10y - 3.5) / 3) * 100, 0, 100);
  const btcDrawdown = clamp(Math.max(0, -btcChange) * 5, 0, 100);
  const spxStress = clamp(Math.max(0, -spxChange) * 8, 0, 100);
  const crossAssetDiv = clamp(Math.abs(btcChange - ethChange) * 10, 0, 100);

  const linear =
    vixNorm * 0.25 +
    btcEwmaVol * 0.2 +
    fearInv * 0.15 +
    yieldStress * 0.1 +
    btcDrawdown * 0.12 +
    spxStress * 0.08 +
    crossAssetDiv * 0.1;

  const sigmoid = 100 / (1 + Math.exp(-0.08 * (linear - 50)));
  const score = clamp(0.6 * sigmoid + 0.4 * linear, 1, 100);

  let regime = "CALM";
  if (score > 80) regime = "CHAOS";
  else if (score > 60) regime = "FEAR";
  else if (score > 40) regime = "STRESSED";
  else if (score > 20) regime = "ALERT";

  return {
    score: Math.round(score * 10) / 10,
    regime,
    components: {
      vixNorm: Math.round(vixNorm * 10) / 10,
      btcEwmaVol: Math.round(btcEwmaVol * 10) / 10,
      fearInv: Math.round(fearInv * 10) / 10,
      yieldStress: Math.round(yieldStress * 10) / 10,
      btcDrawdown: Math.round(btcDrawdown * 10) / 10,
      spxStress: Math.round(spxStress * 10) / 10,
      crossAssetDiv: Math.round(crossAssetDiv * 10) / 10
    }
  };
}

export function normalizeForces(forces) {
  if (!Array.isArray(forces)) return ["MONEY"];
  const normalized = forces
    .map((f) => {
      if (typeof f === "string") return f.toUpperCase();
      return String(f?.label ?? f?.name ?? f?.force ?? "").toUpperCase();
    })
    .filter((f) => VALID_FORCES.has(f));
  return [...new Set(normalized)].slice(0, 4);
}

export function validateAgentOutput(raw, agent = "UNKNOWN") {
  const parsed = typeof raw === "string" ? extractJsonObject(raw) : raw;
  const bias = String(parsed?.bias ?? "NEUTRAL").toUpperCase();
  const confidence = clamp(parsed?.confidence ?? 50, 0, 100);
  const thesis = String(parsed?.thesis ?? "Agent fallback: insufficient validated data.");

  return {
    agent: String(parsed?.agent ?? agent).toUpperCase(),
    bias: ["BULLISH", "BEARISH", "NEUTRAL"].includes(bias) ? bias : "NEUTRAL",
    confidence,
    thesis: thesis.slice(0, 1000),
    valid: Boolean(parsed?.bias && parsed?.thesis)
  };
}

export function validateSupervisorOutput(raw, context = {}) {
  const parsed = typeof raw === "string" ? extractJsonObject(raw) : raw;
  const signal = String(parsed?.signal ?? "NEUTRAL").toUpperCase();
  const confidence = clamp(parsed?.confidence ?? 62, 0, 100);
  const plays = Array.isArray(parsed?.plays) ? parsed.plays : [];
  const normalizedPlays = ["SAFE", "AGGRESSIVE", "CONTRARIAN"].map((type, index) => {
    const found = plays.find((p) => String(p?.type).toUpperCase() === type) ?? plays[index] ?? {};
    return {
      type,
      thesis: String(found.thesis ?? `${type} setup pending confirmation.`).slice(0, 240),
      details: String(found.details ?? "Wait for validated levels before execution.").slice(0, 800)
    };
  });

  return {
    headline: String(parsed?.headline ?? "Markets Demand Confirmation").slice(0, 90),
    dateline: String(parsed?.dateline ?? "New York").slice(0, 40),
    signal: VALID_SIGNALS.has(signal) ? signal : "NEUTRAL",
    confidence,
    eli5: String(parsed?.eli5 ?? "Markets are sending mixed signals. The system is waiting for cleaner confirmation before leaning hard in either direction."),
    analyst: String(parsed?.analyst ?? "Cross-asset confirmation is incomplete. Treat this session as tactical rather than strategic until bonds, equities, and crypto align."),
    quant: String(parsed?.quant ?? "Volatility and correlation signals are not decisive enough for a high-conviction regime call."),
    chaos_line: String(parsed?.chaos_line ?? "When the crowd demands certainty, the market sells them leverage.").slice(0, 180),
    plays: normalizedPlays,
    trap: String(parsed?.trap ?? "The obvious trade is crowded. Wait for confirmation before chasing it."),
    edge: String(parsed?.edge ?? "The hidden signal is cross-market confirmation, not a single asset moving alone."),
    time_sensitivity: ["IMMEDIATE", "TODAY", "THIS WEEK"].includes(String(parsed?.time_sensitivity).toUpperCase())
      ? String(parsed.time_sensitivity).toUpperCase()
      : "THIS WEEK",
    forces: normalizeForces(parsed?.forces),
    active_regime: VALID_REGIMES.has(String(parsed?.active_regime).toUpperCase())
      ? String(parsed.active_regime).toUpperCase()
      : "TRANSITION",
    agent_consensus: context.agentConsensus ?? parsed?.agent_consensus ?? null,
    generated_at: new Date().toISOString(),
    valid: Boolean(parsed?.headline && parsed?.signal && plays.length >= 1)
  };
}

export function signalHash(payload) {
  return createHash("sha256").update(JSON.stringify(payload)).digest("hex");
}

export function buildSignalRecord(brief, market = {}) {
  const now = new Date();
  const btcEntry = toNumber(market.btcPrice ?? market.btc_price, null);
  const spxEntry = toNumber(market.spxVal ?? market.spx, null);
  const vixEntry = toNumber(market.vixVal ?? market.vix, null);
  const id = `sig_${now.toISOString().replace(/[-:.TZ]/g, "").slice(0, 14)}`;
  const payload = {
    id,
    timestamp: now.toISOString(),
    session: sessionInfo(now).session,
    headline: brief.headline,
    signal: brief.signal,
    confidence: brief.confidence,
    forces: brief.forces,
    active_regime: brief.active_regime,
    btc_entry: btcEntry,
    spx_entry: spxEntry,
    vix_entry: vixEntry,
    plays: brief.plays,
    resolved: false,
    result: null,
    pnl_percent: null
  };
  return {
    ...payload,
    signal_hash: signalHash(payload).slice(0, 32)
  };
}

export function summarizeConsensus(fund, tech, sent, supervisorSignal) {
  const biases = [fund.bias, tech.bias, sent.bias].map((b) => String(b ?? "NEUTRAL").toUpperCase());
  const counts = biases.reduce((acc, b) => ({ ...acc, [b]: (acc[b] ?? 0) + 1 }), {});
  const majority = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "NEUTRAL";
  const debateRequired = new Set(biases).size > 1;
  const sup = String(supervisorSignal ?? majority).toUpperCase();

  return {
    fundamental: fund.bias,
    technical: tech.bias,
    sentiment: sent.bias,
    debate_required: debateRequired,
    resolution: debateRequired
      ? `Agents split ${biases.join("/")} - Supervisor resolves ${sup}`
      : `${majority} - all agents aligned`
  };
}

export function buildTelegramFree(brief, market = {}, env = process.env) {
  const site = env.CHAOS_SITE_URL || "https://chaos.sumanthworks.com";
  const checkout = env.PRO_CHECKOUT_URL || site;
  const btc = market.btcPrice ?? market.btc_price ?? "N/A";
  const fear = market.fearIndex ?? market.fear_index ?? "N/A";
  const line = [
    `CHAOS INTELLIGENCE - ${brief.time_sensitivity}`,
    "------------------------------",
    `${brief.signal} / ${brief.confidence}% confidence`,
    `Fear: ${fear} / BTC: ${btc}`,
    "",
    brief.headline,
    "",
    `Safe play: ${brief.plays?.[0]?.thesis ?? "Pending"}`,
    "",
    `Full brief: ${site}`,
    `Unlock Pro: ${checkout}`
  ];
  return line.join("\n");
}

export function buildTelegramPro(brief, market = {}, env = process.env) {
  const site = env.CHAOS_SITE_URL || "https://chaos.sumanthworks.com";
  const plays = (brief.plays ?? [])
    .map((p) => `${p.type}: ${p.thesis}\n${p.details}`)
    .join("\n\n");
  return [
    `CHAOS INTELLIGENCE PRO - ${brief.time_sensitivity}`,
    "------------------------------",
    `${brief.signal} / ${brief.confidence}% confidence`,
    `Regime: ${brief.active_regime}`,
    `Forces: ${(brief.forces ?? []).join(", ")}`,
    "",
    brief.headline,
    "",
    `Trap: ${brief.trap}`,
    "",
    `Edge: ${brief.edge}`,
    "",
    "THE PLAYS",
    plays,
    "",
    `Chaos Line: "${brief.chaos_line}"`,
    "",
    `Dashboard: ${site}`,
    "Thesis only. Not financial advice."
  ].join("\n");
}

export function evaluateAlerts(current = {}, previous = {}) {
  const alerts = [];
  const btcChange = toNumber(current.btcChange ?? current.btc_change, 0);
  const vix = toNumber(current.vixVal ?? current.vix, null);
  const prevVix = toNumber(previous.vixVal ?? previous.vix, null);
  const yield10y = toNumber(current.yieldVal ?? current.yield_10y, null);
  const liquidationUsd = toNumber(current.liquidationUsd, 0);

  if (Math.abs(btcChange) >= 3) {
    alerts.push({
      severity: "HIGH",
      type: "BTC_MOVE",
      message: `BTC 24h move is ${btcChange.toFixed(2)}%. Volatility window is open.`
    });
  }
  if (vix && (vix >= 22 || (prevVix && vix - prevVix >= 2))) {
    alerts.push({
      severity: "HIGH",
      type: "VIX_SPIKE",
      message: `VIX at ${vix.toFixed(2)}. Equity stress is rising.`
    });
  }
  if (yield10y && yield10y >= 4.6) {
    alerts.push({
      severity: "MEDIUM",
      type: "YIELD_STRESS",
      message: `10Y yield at ${yield10y.toFixed(3)}%. Risk assets face duration pressure.`
    });
  }
  if (liquidationUsd >= 100_000_000) {
    alerts.push({
      severity: "HIGH",
      type: "LIQUIDATION_SPIKE",
      message: `Crypto liquidations exceeded $${Math.round(liquidationUsd / 1_000_000)}M. Forced flow detected.`
    });
  }
  return alerts;
}
