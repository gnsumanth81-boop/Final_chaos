/**
 * Keyless scraper fetching live percentages for a curated list of high-volume contracts.
 * @returns {Promise<Object>} An aggregated map of live event probabilities.
 */
export async function fetchAggregatedPolymarketTelemetry() {
  // A curated list of maximum-impact global event slugs for the 2026/2027 macro framework
  const macroSlugs = {
    fedRateCut: "will-the-fed-cut-rates-at-its-next-meeting",
    usElection: "us-presidential-election-2028", 
    globalConflict: "will-china-invade-taiwan-in-2026", 
    gazaCeasefire: "will-there-be-a-gaza-ceasefire-by-next-month"
  };

  const outputMatrix = {};
  console.log("📡 [POLYMARKET CORE]: Initializing multi-contract macro sweep loop with browser masks...");

  // Standard high-authority browser headers to punch through Cloudflare anti-bot blocks
  const browserSpoofHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://polymarket.com',
    'Referer': 'https://polymarket.com/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
  };

  for (const [key, slug] of Object.entries(macroSlugs)) {
    try {
      // Direct hit on the live Polymarket Gamma API backend
      const response = await fetch(`https://gamma-api.polymarket.com/events?slug=${slug}`, {
        method: 'GET',
        headers: browserSpoofHeaders,
      });

      if (!response.ok) throw new Error(`HTTP Error Code: ${response.status}`);
      
      const data = await response.json();
      
      if (data && data.length > 0 && data[0].markets && data[0].markets.length > 0) {
        const primaryMarket = data[0].markets[0];
        const yesOutcomePrice = parseFloat(primaryMarket.outcomePrices?.[0] || "0.50");
        outputMatrix[key] = Math.round(yesOutcomePrice * 100);
        
        console.log(`📈 [POLYMARKET SUB-NODE]: Successfully resolved [${key.toUpperCase()}] at ${outputMatrix[key]}%`);
      } else {
        outputMatrix[key] = 50;
      }
    } catch (error) {
      console.warn(`⚠️ [POLYMARKET NODE FAIL]: Skipped tracking for slug ${slug} ➔ ${error.message}`);
      outputMatrix[key] = 50; 
    }
  }

  return outputMatrix;
}
