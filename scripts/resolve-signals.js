import { readFile, writeFile } from "node:fs/promises";
import { getBinanceTicker, getYahooLast } from "../src/data-collectors.js";
import { pctChange, toNumber } from "../src/chaos-core.js";

const signalsPath = new URL("../public/api/signals.json", import.meta.url);

async function main() {
  const signals = JSON.parse(await readFile(signalsPath, "utf8"));
  const btc = await getBinanceTicker("BTCUSDT");
  const spx = await getYahooLast("^GSPC");
  const now = Date.now();
  let changed = 0;

  const updated = signals.map((signal) => {
    if (signal.resolved) return signal;
    const ageHours = (now - new Date(signal.timestamp).getTime()) / 36e5;
    if (ageHours < 24) return signal;

    const entry = toNumber(signal.btc_entry, null);
    const current = btc.price ?? null;
    const pnl = pctChange(current, entry);
    if (pnl === null) return signal;

    const bullishWin = signal.signal === "BULLISH" && pnl > 0;
    const bearishWin = signal.signal === "BEARISH" && pnl < 0;
    const neutralWin = signal.signal === "NEUTRAL" && Math.abs(pnl) < 1.5;
    const volatileWin = signal.signal === "VOLATILE" && Math.abs(pnl) >= 1.5;
    const win = bullishWin || bearishWin || neutralWin || volatileWin;
    changed += 1;
    return {
      ...signal,
      resolved: true,
      resolved_at: new Date().toISOString(),
      btc_exit: current,
      spx_exit: spx.last ?? null,
      pnl_percent: Math.round(pnl * 100) / 100,
      result: win ? "WIN" : "LOSS"
    };
  });

  await writeFile(signalsPath, JSON.stringify(updated, null, 2));
  console.log(`Resolved ${changed} signal(s).`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
