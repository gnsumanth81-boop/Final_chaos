import axios from 'axios';

// Normalizer to simulate or fetch live data
// Using real CoinGecko API for BTC/ETH, and mocked/alternative logic for the rest.
export async function collectMarketData() {
  console.log("📊 Collecting live market telemetry...");
  
  let btcPrice = 70000, btcChange = 0, ethPrice = 3500;
  try {
    const cg = await axios.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true', { timeout: 5000 });
    if (cg.data.bitcoin) {
      btcPrice = cg.data.bitcoin.usd;
      btcChange = cg.data.bitcoin.usd_24h_change;
    }
    if (cg.data.ethereum) {
      ethPrice = cg.data.ethereum.usd;
    }
  } catch (e) {
    console.warn("⚠️ CoinGecko API rate limit or error, using fallback data.");
  }

  let fearIndex = 50, fearLabel = "Neutral";
  try {
    const fgi = await axios.get('https://api.alternative.me/fng/?limit=1', { timeout: 5000 });
    if (fgi.data && fgi.data.data && fgi.data.data.length > 0) {
      fearIndex = parseInt(fgi.data.data[0].value);
      fearLabel = fgi.data.data[0].value_classification;
    }
  } catch (e) {
    console.warn("⚠️ Alternative.me API error, using fallback fear index.");
  }

  // Simulated Macro Data (In a full prod system, connect to FRED/Yahoo Finance)
  const dxyVal = (103.5 + (Math.random() - 0.5)).toFixed(2);
  const yieldVal = (4.25 + (Math.random() * 0.1)).toFixed(3);
  const vixVal = (14.5 + (Math.random() * 2)).toFixed(2);
  const spxVal = Math.round(5200 + (Math.random() * 100));
  
  // Format the data perfectly for the OpenRouter agents to consume
  return {
    fearIndex,
    fearLabel,
    btcPrice: `$${Math.round(btcPrice).toLocaleString()}`,
    btcChange: btcChange.toFixed(2),
    ethPrice: `$${Math.round(ethPrice).toLocaleString()}`,
    dxyVal,
    yieldVal,
    vixVal,
    spxVal: spxVal.toLocaleString(),
    timestamp: new Date().toISOString()
  };
}

export async function fetchGeopoliticalTelemetry() {
  console.log("📡 [SECURITY CORE]: Scanning international flashpoint news wires...");
  const feeds = [
    'https://www.ft.com/world?format=rss',
    'http://feeds.bbci.co.uk/news/world/rss.xml'
  ];
  
  let allWires = [];
  const keywords = /war|sanctions|central bank|default|invasion|escalation|ceasefire|coup|emergency|tariffs|military|missile/i;
  
  for (const feed of feeds) {
    try {
      const response = await axios.get(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(feed)}`, { timeout: 8000 });
      if (response.data && response.data.items) {
        allWires.push(...response.data.items);
      }
    } catch (e) {
      console.warn(`⚠️ Failed to fetch feed ${feed}: ${e.message}`);
    }
  }

  const urgent = allWires
    .map(item => `[${item.author || 'INTEL'}] ${item.title}: ${item.description || ''}`)
    .filter(text => keywords.test(text))
    .slice(0, 5); // top 5 high-urgency

  return urgent.length > 0 
    ? urgent 
    : ["Geopolitical theater operating inside standard macro volatility boundaries."];
}
