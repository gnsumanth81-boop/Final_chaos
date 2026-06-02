import axios from 'axios';
import 'dotenv/config';

export async function sendDiscordAlert(latestJson) {
  const webhookUrl = process.env.DISCORD_WEBHOOK_URL;
  
  if (!webhookUrl || !webhookUrl.startsWith('https://discord.com')) {
    console.error("🚨 [SECURITY EXCEPTION]: Invalid or missing DISCORD_WEBHOOK_URL endpoint mapping.");
    return; // Silent fail-safe protect
  }

  console.log("🔔 Pushing Rich Embed to Discord...");

  const brief = latestJson.brief || {};
  const market = latestJson.market || {};
  const signal = brief.signal || "NEUTRAL";
  
  let color = 15764259; // Gray/Neutral
  if (signal === "BULLISH") color = 2282586; // Green
  if (signal === "BEARISH") color = 15219018; // Red

  // Strip HTML from text
  const stripHtml = (html) => {
    if (!html) return "";
    return html.replace(/<[^>]*>?/gm, '');
  };

  const embed = {
    title: `CHAOS. | ${brief.headline || "Macro Update"}`,
    url: "https://chaos.sumanthworks.com",
    description: `*${stripHtml(brief.chaos_line)}*\n\n**Market Vitals:**\nBTC: ${market.btcPrice} | S&P 500: ${market.spxVal} | Fear: ${market.fearIndex} (${market.fearLabel})`,
    color: color,
    fields: [
      {
        name: "🤖 Agent Consensus",
        value: stripHtml(brief.eli5 || ""),
      },
      {
        name: "🔒 Alpha Trade Plays",
        value: `Check the live terminal to unlock the execution parameters.\n[View Terminal](https://chaos.sumanthworks.com)`
      }
    ],
    footer: {
      text: "Chaos Intelligence Terminal • Automated Broadcast",
      icon_url: "https://chaos.sumanthworks.com/favicon.ico"
    },
    timestamp: new Date().toISOString()
  };

  try {
    await axios.post(webhookUrl, { embeds: [embed] });
    console.log("✅ Discord alert pushed successfully.");
  } catch (err) {
    console.warn("⚠️ Failed to push Discord alert:", err.message);
  }
}
