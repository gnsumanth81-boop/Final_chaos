import fs from 'fs/promises';

export async function sendTelegramBrief(terminalData) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHANNEL_ID; // e.g. -1001234567890 for channel

  if (!token || !chatId) {
    console.log("⚠️ Telegram credentials not set. Skipping broadcast.");
    return;
  }

  // Use the brief structure for the telegram message
  const d = terminalData.brief || {};
  const m = terminalData.market || {};

  const message = `🌍 *CHAOS INTELLIGENCE* — ${(d.dateline || 'BRIEF').toUpperCase()}\n` +
    `━━━━━━━━━━━━━━━━━━━━━━\n\n` +
    `🚨 ${d.signal || 'NEUTRAL'} • ${d.confidence || 0}% CONFIDENCE\n` +
    `📊 Fear ${m.fearIndex || 0} • BTC ${m.btcPrice || '$0'} (${m.btcChange || '0.00'}%)\n\n` +
    `*${d.headline || 'Market Update'}*\n\n` +
    `✦ CHAOS LINE ✦\n"${d.chaos_line || ''}"\n\n` +
    `SAFE PLAY: ${d.plays?.[0]?.thesis || '—'}\n\n` +
    `🔗 Full Terminal: https://chaos.sumanthworks.com\n` +
    `Pro signals → https://sumanth664.gumroad.com/l/hlpqa`;

  try {
    const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: message,
        parse_mode: 'Markdown',
        disable_web_page_preview: true
      })
    });

    if (res.ok) {
      console.log("✅ [TELEGRAM ENGINE]: Cinematic alert successfully broadcast to user acquisition channel.");
    } else {
      console.error("⛔ [TELEGRAM ENGINE ERROR]: Telegram send failed:", await res.text());
    }
  } catch (e) {
    console.error("⛔ [TELEGRAM ENGINE ERROR]: Broadcast cycle failed ➔", e.message);
  }
}
