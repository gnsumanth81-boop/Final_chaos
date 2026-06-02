import fs from 'fs/promises';
import path from 'path';

const historyFilePath = path.resolve('./src/data/history.json');

/**
 * Sweeps the historical ledger, resolves expired predictions exactly 24 hours later,
 * and computes the absolute win rate and current streak.
 * @param {number|string} currentBtcPriceRaw - The real-time BTC price.
 * @returns {Object} Performance stats to inject into the live terminal.
 */
export async function resolveExpiredSignals(currentBtcPriceRaw) {
  try {
    let history = [];
    try {
      const fileData = await fs.readFile(historyFilePath, 'utf-8');
      history = JSON.parse(fileData);
    } catch (e) {
      console.log("📝 [AUTOPSY BRAIN]: No historical log database discovered. Skipping verification.");
      return { win_rate: 0, current_streak: 0, streak_direction: "NONE", total_resolved: 0, total_wins: 0, total_losses: 0, total_scratch: 0 };
    }

    const currentBtcPrice = typeof currentBtcPriceRaw === 'string' 
      ? parseFloat(currentBtcPriceRaw.replace(/[^0-9.-]+/g, "")) 
      : parseFloat(currentBtcPriceRaw);

    const now = new Date();
    let newlyResolved = 0;

    // First Pass: Grade un-resolved signals older than 24 hours
    for (let signal of history) {
      // Must be an object with timestamp and btc_entry
      if (!signal || !signal.timestamp || signal.btc_entry === undefined || signal.btc_entry === null) continue;
      
      // Skip if already resolved
      if (signal.resolved === true) continue;

      const signalTime = new Date(signal.timestamp);
      const signalAgeHours = (now - signalTime) / (1000 * 60 * 60);

      // Expiry Condition: Wait exactly 24 hours
      if (signalAgeHours < 24) continue;

      console.log(`🔬 [AUTOPSY BRAIN]: Resolving expired signal [${signal.signal_hash}]`);

      const btcEntry = parseFloat(signal.btc_entry);
      const priceDelta = currentBtcPrice - btcEntry;
      let rawPnlPercent = (priceDelta / btcEntry) * 100;
      
      const vibeText = String(signal.signal).toUpperCase();
      
      // Invert PNL for BEARISH calls so correct short plays show positive PNL
      if (vibeText.includes('BEARISH')) {
        rawPnlPercent = -rawPnlPercent;
      }

      let finalVerdict = 'LOSS';

      if (Math.abs(rawPnlPercent) <= 0.3) {
        finalVerdict = 'SCRATCH';
      } else if (vibeText.includes('BULLISH') && priceDelta > 0) {
        finalVerdict = 'WIN';
      } else if (vibeText.includes('BEARISH') && priceDelta < 0) {
        finalVerdict = 'WIN';
      } else if (vibeText.includes('NEUTRAL') && Math.abs(rawPnlPercent) <= 1.5) {
        finalVerdict = 'WIN';
      }

      signal.resolved = true;
      signal.resolution_status = finalVerdict;
      signal.btc_exit = currentBtcPrice;
      signal.pnl_percent = parseFloat(rawPnlPercent.toFixed(2));
      signal.resolved_at = now.toISOString();
      signal.grading_method = "24h_btc_close";
      signal.autopsy_note = finalVerdict === "WIN" 
        ? "Price moved favorably beyond target within 24h window." 
        : finalVerdict === "LOSS" 
        ? "Price broke key support level against signal thesis." 
        : "Movement insufficient to trigger win or loss.";

      newlyResolved++;
    }

    // Edge Case: If zero expired signals, write nothing to avoid empty commits
    if (newlyResolved > 0) {
      await fs.writeFile(historyFilePath, JSON.stringify(history, null, 2), 'utf-8');
      const signalsApiPath = path.resolve('api', 'signals.json');
      await fs.writeFile(signalsApiPath, JSON.stringify(history, null, 2), 'utf-8');
    }

    // Second Pass: Calculate Global Statistics
    let totalWins = 0;
    let totalLosses = 0;
    let totalScratch = 0;
    let currentStreak = 0;
    let streakDirection = "NONE";
    let streakActive = true;
    let lastResolvedAt = null;

    // Since history is newest-first, we calculate streak from the top down.
    // However, the newest entries might be OPEN. We only care about resolved entries.
    const resolvedSignals = history.filter(s => s.resolved === true);

    if (resolvedSignals.length > 0) {
      lastResolvedAt = resolvedSignals[0].resolved_at;
      
      for (let s of resolvedSignals) {
        if (s.resolution_status === 'WIN') totalWins++;
        else if (s.resolution_status === 'LOSS') totalLosses++;
        else if (s.resolution_status === 'SCRATCH') totalScratch++;

        if (streakActive) {
          if (s.resolution_status === 'SCRATCH') {
            // Scratch doesn't break streak, just ignores it
            continue;
          } else if (s.resolution_status === 'WIN') {
            if (streakDirection === "NONE") streakDirection = "WIN";
            if (streakDirection === "WIN") currentStreak++;
            else streakActive = false; // hit a WIN while on a LOSS streak
          } else if (s.resolution_status === 'LOSS') {
            if (streakDirection === "NONE") streakDirection = "LOSS";
            if (streakDirection === "LOSS") currentStreak++;
            else streakActive = false; // hit a LOSS while on a WIN streak
          }
        }
      }
    }

    const totalValid = totalWins + totalLosses;
    const computedWinRate = totalValid > 0 ? parseFloat(((totalWins / totalValid) * 100).toFixed(1)) : 0;

    if (newlyResolved > 0) {
      console.log(`📊 [AUTOPSY SUCCESS]: Track Record updated: ${totalWins}W / ${totalLosses}L (${computedWinRate}% WR). Current Streak: ${currentStreak} ${streakDirection}.`);
    }

    return {
      win_rate: computedWinRate,
      current_streak: currentStreak,
      streak_direction: streakDirection,
      total_resolved: resolvedSignals.length,
      total_wins: totalWins,
      total_losses: totalLosses,
      total_scratch: totalScratch,
      last_resolved_at: lastResolvedAt
    };

  } catch (err) {
    console.error("⛔ [AUTOPSY BRAIN CRITICAL EXCEPTION]:", err.message);
    return { win_rate: 0, current_streak: 0, streak_direction: "NONE", total_resolved: 0, total_wins: 0, total_losses: 0, total_scratch: 0 };
  }
}
