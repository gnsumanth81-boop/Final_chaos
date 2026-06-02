import { readFile } from "node:fs/promises";
import { buildTelegramFree, buildTelegramPro } from "../src/chaos-core.js";

const latestPath = new URL("../public/api/latest.json", import.meta.url);

async function sendMessage(text, chatId, env = process.env) {
  if (!env.TELEGRAM_BOT_TOKEN) throw new Error("TELEGRAM_BOT_TOKEN is not configured.");
  if (!chatId) throw new Error("Telegram chat id is not configured.");
  const res = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      disable_web_page_preview: true
    })
  });
  if (!res.ok) throw new Error(`Telegram error ${res.status}: ${await res.text()}`);
}

async function main() {
  const tier = process.argv[2] ?? "free";
  const latest = JSON.parse(await readFile(latestPath, "utf8"));
  const text =
    tier === "pro"
      ? buildTelegramPro(latest.brief, latest.market, process.env)
      : buildTelegramFree(latest.brief, latest.market, process.env);
  const chatId = tier === "pro" ? process.env.TELEGRAM_PRO_CHAT_ID : process.env.TELEGRAM_FREE_CHAT_ID;
  await sendMessage(text, chatId, process.env);
  console.log(`Sent ${tier} Telegram message.`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
