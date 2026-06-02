import fs from 'fs';
import path from 'path';

// Log the final JSON into a rolling history file capped at 100 entries.
export function appendHistory(latestJson) {
  console.log("💾 Appending entry to local history ledger...");
  
  const historyPath = path.resolve('src/data', 'history.json');
  
  // Ensure directory exists
  if (!fs.existsSync(path.dirname(historyPath))) {
    fs.mkdirSync(path.dirname(historyPath), { recursive: true });
  }

  let history = [];
  if (fs.existsSync(historyPath)) {
    try {
      history = JSON.parse(fs.readFileSync(historyPath, 'utf8'));
    } catch (e) {
      console.warn("⚠️ History file corrupt, starting fresh.");
    }
  }

  // Create a minimal history entry for the ledger with grading capabilities
  const btcRaw = latestJson.market?.btcPrice ? parseFloat(latestJson.market.btcPrice.replace(/[^0-9.-]+/g, "")) : 0;
  
  const entry = {
    date: new Date().toISOString().split('T')[0],
    timestamp: new Date().toISOString(),
    signal_hash: latestJson.signal?.signal_hash || Date.now().toString(36),
    signal: latestJson.brief?.signal || "NEUTRAL",
    headline: latestJson.brief?.headline || "Data Sync",
    btc_entry: btcRaw,
    resolved: false,
    resolution_status: "OPEN"
  };

  history.unshift(entry); // Add to beginning
  
  // Cap at 100 entries
  if (history.length > 100) {
    history = history.slice(0, 100);
  }

  fs.writeFileSync(historyPath, JSON.stringify(history, null, 2), 'utf8');
  
  // Also push to the public api/signals.json for the frontend to read
  const publicSignalsPath = path.resolve('api', 'signals.json');
  if (!fs.existsSync(path.dirname(publicSignalsPath))) {
    fs.mkdirSync(path.dirname(publicSignalsPath), { recursive: true });
  }
  fs.writeFileSync(publicSignalsPath, JSON.stringify(history, null, 2), 'utf8');
  
  console.log("✅ History ledger updated.");
}
