import fs from 'fs';
import path from 'path';

import { collectMarketData, fetchGeopoliticalTelemetry } from './data-collectors.js';
import { runDualStagePipeline, enforceStructuralIntegrity } from './openrouter-agents.js';
import { appendHistory } from './history-logger.js';
import { sendDiscordAlert } from './discord-alerts.js';
import { generateCinematicAudio } from './tts-engine.js';
import { syncWithGitHub } from './github-sync.js';
import { resolveExpiredSignals } from './autopsy-brain.js';
import { sendTelegramBrief } from './telegram-alerts.js';
import { fetchAggregatedPolymarketTelemetry } from './polymarket-hooks.js';
async function main() {
  console.log("==============================================");
  console.log("🚀 CHAOS TERMINAL: CRON SEQUENCE INITIATED");
  console.log(`🕒 Timestamp: ${new Date().toISOString()}`);
  console.log("==============================================");

  try {
    // 1. Data Collection
    const marketData = await collectMarketData();
    console.log(`✅ Telemetry fetched (BTC: ${marketData.btcPrice}, Fear: ${marketData.fearIndex})`);

    const geoData = await fetchGeopoliticalTelemetry();
    console.log("🌍 GEOPOLITICAL TELEMETRY TEST OUTPUT:");
    console.log(JSON.stringify(geoData, null, 2));

    marketData.geopoliticalTelemetry = geoData;

    // 2. OpenRouter AI Analysis
    let finalData = await runDualStagePipeline(marketData);
    finalData = enforceStructuralIntegrity(finalData);

    // 2.5 Polymarket Live Odds Injection (Multi-Contract Sweep)
    const livePolymarketMatrix = await fetchAggregatedPolymarketTelemetry();
    finalData.polymarketOdds = livePolymarketMatrix.fedRateCut; // Main HUD tracking
    finalData.extendedPolymarketVitals = livePolymarketMatrix; // Full matrix for UI

    let processedNewsWires = [];
    if (Array.isArray(geoData) && geoData.length > 0) {
      processedNewsWires = geoData.slice(0, 5).map(str => {
        let title = str;
        let impact = 'Geopolitical macro narrative change impacting core treasury yield allocation gating.';
        if (typeof str === 'string') {
           const parts = str.replace(/\[.*?\]\s*/, '').split(':');
           title = parts[0]?.trim() || str;
           impact = parts.slice(1).join(':').trim() || impact;
        }
        return { source: 'GEOPOLITICS', title: title, impact: impact };
      });
    }
    
    if (!finalData.brief) finalData.brief = {};
    finalData.brief.news_wires = processedNewsWires;

    // 3. Write to api/latest.json safely
    const apiPath = path.resolve('api', 'latest.json');
    if (!fs.existsSync(path.dirname(apiPath))) {
      fs.mkdirSync(path.dirname(apiPath), { recursive: true });
    }
    
    // 4. Log to history
    appendHistory(finalData);

    // 4.5. Run Autopsy Brain to grade past signals and calculate performance
    console.log("🔬 [CORE PIPELINE]: Initializing performance audit routines...");
    const performanceStats = await resolveExpiredSignals(marketData.btcPrice);
    finalData.performance = performanceStats;

    // Save state locally
    fs.writeFileSync(apiPath, JSON.stringify(finalData, null, 2), 'utf8');
    console.log("✅ State overwritten in ./api/latest.json with zero data loss.");

    // 5. Discord & Telegram Alerts
    await Promise.all([
      sendDiscordAlert(finalData),
      sendTelegramBrief(finalData)
    ]);
    // 5.5 Render Voiceovers
    await generateCinematicAudio(finalData);

    // 6. Push to GitHub via API
    await syncWithGitHub(finalData);

    console.log("==============================================");
    console.log("🏁 SEQUENCE COMPLETE. TERMINAL UPDATED.");
    console.log("==============================================");

  } catch (err) {
    console.error("🛑 CRITICAL FAILURE IN PIPELINE:", err.message);
    console.error("The UI will continue displaying the previous successful session seamlessly.");
    process.exit(1);
  }
}

main();
