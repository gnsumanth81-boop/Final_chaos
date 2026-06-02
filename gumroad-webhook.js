import express from 'express';
import crypto from 'crypto';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
// Gumroad sends application/x-www-form-urlencoded data
app.use(express.urlencoded({ extended: true }));

// Your Gumroad product's secret to verify the webhook signature
const GUMROAD_SECRET = process.env.GUMROAD_SECRET || 'your_gumroad_secret';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || 'your_telegram_bot_token';
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || 'your_private_channel_id';

app.post('/webhook/gumroad', async (req, res) => {
  try {
    // 1. Verify the signature from Gumroad (optional but highly recommended)
    // Currently, we will just parse the basic ping data.
    const { email, price, product_id, sale_id } = req.body;

    console.log(`\n💰 New Purchase Detected: ${email} paid $${(price / 100).toFixed(2)} for product ${product_id}`);

    // 2. Generate a single-use invite link to the PRO Telegram Channel
    console.log(`Generating unique Telegram invite link for ${email}...`);
    
    const tgUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/createChatInviteLink`;
    const tgResponse = await axios.post(tgUrl, {
      chat_id: TELEGRAM_CHAT_ID,
      name: `PRO_${sale_id.substring(0, 6)}`,
      member_limit: 1, // Single-use link
      expire_date: Math.floor(Date.now() / 1000) + (86400 * 7) // Expires in 7 days
    });

    if (tgResponse.data.ok) {
      const inviteLink = tgResponse.data.result.invite_link;
      console.log(`✅ Success! Invite Link Generated: ${inviteLink}`);
      
      // 3. (Optional) Email the invite link to the buyer using an email service like Resend or SendGrid
      // For now, if Gumroad handles the email, you can attach the link to the Gumroad receipt via Gumroad API,
      // or send a separate email.
      
    } else {
      console.error(`❌ Failed to generate Telegram link:`, tgResponse.data);
    }

    // Always return 200 OK to Gumroad so they know we received the ping
    res.status(200).send('Webhook received.');

  } catch (error) {
    console.error('Webhook Error:', error.message);
    res.status(500).send('Internal Server Error');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`\n🔌 Chaos Monetization Webhook running on port ${PORT}`);
  console.log(`👉 Add http://your-server-ip:${PORT}/webhook/gumroad to your Gumroad product ping URL.`);
});
