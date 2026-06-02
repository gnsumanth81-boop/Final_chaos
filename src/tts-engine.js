import fs from 'fs/promises';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Generates cinematic MP3 files for ELI5, Analyst, and Quant texts using Edge TTS (Free Azure Neural).
 * @param {Object} terminalData - The finalized JSON object from OpenRouter.
 */
export async function generateCinematicAudio(terminalData) {
  const audioDir = path.resolve('./api/audio');
  await fs.mkdir(audioDir, { recursive: true });

  // Map text tiers to voices (Microsoft Azure Neural Voices)
  // ELI5: Friendly female
  // Analyst: Crisp professional male
  // Quant: Deep, serious male
  const tiers = [
    { id: 'eli5', text: terminalData.brief?.eli5 || "No data available.", voice: 'en-US-AriaNeural' },
    { id: 'analyst', text: terminalData.brief?.analyst || "No data available.", voice: 'en-US-GuyNeural' },
    { id: 'quant', text: terminalData.brief?.quant || "No data available.", voice: 'en-US-ChristopherNeural' }
  ];

  console.log("🎙️ [AUDIO ENGINE]: Initiating studio-quality voice generation via Azure Neural (Free)...");

  for (const tier of tiers) {
    try {
      // Clean out markdown wrappers/HTML tags before feeding the voice synthesiser
      const cleanText = tier.text.replace(/<\/?strong>/g, "").replace(/\*\*+/g, "").replace(/"/g, "'");

      const filePath = path.join(audioDir, `${tier.id}.mp3`);
      
      // Execute edge-tts via python module
      await execAsync(`python -m edge_tts --voice ${tier.voice} --text "${cleanText}" --write-media "${filePath}"`);
      
      console.log(`🎵 [AUDIO ENGINE]: Successfully mastered ${tier.id}.mp3 with voice ${tier.voice}`);

    } catch (error) {
      console.error(`⚠️ Republication error on [${tier.id.toUpperCase()} VOICE LOOP]:`, error.message);
    }
  }

  // Inject a single lightweight timestamp identifier to act as the global cache buster
  terminalData.audioVersionToken = new Date().getTime();
}
