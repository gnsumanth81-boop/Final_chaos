import { mkdir, readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { buildSignalRecord } from "../src/chaos-core.js";
import { collectMarketData } from "../src/data-collectors.js";
import { runAgents } from "../src/openrouter-agents.js";
import { dispatchDiscordAlert } from "../src/discord-alerts.js";
const apiDir = new URL("../public/api/", import.meta.url);
const latestPath = new URL("../public/api/latest.json", import.meta.url);
const signalsPath = new URL("../public/api/signals.json", import.meta.url);

async function readJson(path, fallback) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch {
    return fallback;
  }
}

async function main() {
  await mkdir(apiDir, { recursive: true });
  const market = await collectMarketData(process.env);
  const agents = await runAgents(market, process.env);
  const brief = agents.supervisor;
  const signal = buildSignalRecord(brief, market);

  const previousSignals = existsSync(signalsPath) ? await readJson(signalsPath, []) : [];
  const signals = [signal, ...previousSignals].slice(0, 500);

  const latest = {
    market,
    agents: {
      fundamental: agents.fundamental,
      technical: agents.technical,
      sentiment: agents.sentiment
    },
    brief,
    signal
  };

  await writeFile(latestPath, JSON.stringify(latest, null, 2));
  await writeFile(signalsPath, JSON.stringify(signals, null, 2));
  console.log(`Chaos brief generated: ${brief.headline}`);
  console.log(`Signal hash: ${signal.signal_hash}`);

  console.log("📡 Analyzing alert criteria parameters...");
  await dispatchDiscordAlert(latest);
  
  console.log("🏁 Cycle sequence completely executed. Entering background sleep state.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
