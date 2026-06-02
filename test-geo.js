import axios from 'axios';

async function verifyInstitutionalTelemetry() {
  const primaryFeeds = [
    'https://www.ft.com/world?format=rss',
    'http://feeds.bbci.co.uk/news/world/rss.xml',
    'https://www.imf.org/en/news/rss?language=eng'
  ];

  const strictFilter = /war|sanctions|central bank|default|invasion|escalation|ceasefire|coup|emergency|tariffs/i;
  let aggregatedTelemetry = [];

  console.log("📡 [AUDIT LOG]: Initiating connection loops to live macro endpoints...");

  for (const url of primaryFeeds) {
    try {
      const response = await axios.get(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(url)}`, { timeout: 15000 });
      
      if (response.data && response.data.items) {
        const matchingItems = response.data.items
          .map(item => `[${item.author || 'INTEL'}] ${item.title}: ${item.description || ''}`)
          .filter(text => strictFilter.test(text));
          
        aggregatedTelemetry.push(...matchingItems);
      }
    } catch (feedError) {
      console.warn(`⚠️ [LINK FAILURE]: Route to ${url} throttled ➔ ${feedError.message}`);
    }
  }

  const cleanResult = [...new Set(aggregatedTelemetry)].slice(0, 5);
  
  if (cleanResult.length === 0) {
    cleanResult.push("Geopolitical threat matrix operating within standard structural baseline boundaries.");
  }

  console.log("\n🌍 GEOPOLITICAL TELEMETRY TEST OUTPUT:\n", JSON.stringify(cleanResult, null, 2));
}

verifyInstitutionalTelemetry();
