import axios from 'axios';
import https from 'https';
import fs from 'fs';
import path from 'path';
import 'dotenv/config';
import { exec } from 'child_process';
import util from 'util';

const execPromise = util.promisify(exec);

const GITHUB_PAT = process.env.GITHUB_PAT;
if (!GITHUB_PAT) {
  console.warn("MOCK RUN: GITHUB_PAT missing, bypassing push to github.");
}

const REPO_OWNER = "gnsumanth81-boop";
const REPO_NAME = "Final_chaos";

function githubRequest(method, apiPath, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${REPO_OWNER}/${REPO_NAME}/contents/${apiPath}`,
      method: method,
      headers: {
        'Authorization': `token ${GITHUB_PAT}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'ChaosTerminal/7.0'
      }
    };
    if (data) options.headers['Content-Length'] = Buffer.byteLength(data);

    const req = https.request(options, (res) => {
      let chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString();
        try { resolve({ status: res.statusCode, data: JSON.parse(raw) }); }
        catch { resolve({ status: res.statusCode, data: raw }); }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function getSha(filePath) {
  try {
    const res = await githubRequest('GET', filePath);
    if (res.status === 200 && res.data.sha) return res.data.sha;
  } catch {}
  return null;
}

async function pushFile(filePath, localPath, commitMsg) {
  const content = fs.readFileSync(localPath);
  const b64 = content.toString('base64');
  const sha = await getSha(filePath);

  const body = {
    message: commitMsg,
    content: b64
  };
  if (sha) body.sha = sha;

  const res = await githubRequest('PUT', filePath, body);
  if (res.status === 200 || res.status === 201) {
    console.log(`  ✅ Pushed: ${filePath} -> ${res.data.commit?.sha?.substring(0, 8) || 'ok'}`);
    return true;
  } else {
    console.error(`  ❌ Failed to push ${filePath}: ${res.status}`);
    return false;
  }
}

export async function syncWithGitHub(latestJson) {
  console.log("📦 Initializing live UI synchronization with GitHub...");

  const headline = latestJson?.brief?.headline || "Market Update";
  const ts = new Date().toISOString().slice(0, 16).replace('T', ' ');
  const commitMsg = `Chaos Intelligence v7 — ${headline} | ${ts}`;

  const latestPath = path.resolve('api', 'latest.json');
  const signalsPath = path.resolve('api', 'signals.json');

  let ok = true;
  if (fs.existsSync(latestPath)) {
    ok = await pushFile('api/latest.json', latestPath, commitMsg) && ok;
  }
  if (fs.existsSync(signalsPath)) {
    ok = await pushFile('api/signals.json', signalsPath, commitMsg + ' [ledger]') && ok;
  }
  
  // Push SEO Brief Archive
  const briefsDir = path.resolve('api/briefs');
  if (fs.existsSync(briefsDir)) {
    const files = fs.readdirSync(briefsDir).filter(f => f.endsWith('.html'));
    for (const f of files) {
      const p = path.resolve('api/briefs', f);
      ok = await pushFile(`api/briefs/${f}`, p, commitMsg + ' [seo archive]') && ok;
    }
  }

  // Push audio files if they exist
  const audioFiles = ['eli5.mp3', 'analyst.mp3', 'quant.mp3'];
  for (const f of audioFiles) {
    const p = path.resolve('api/audio', f);
    if (fs.existsSync(p)) {
      ok = await pushFile(`api/audio/${f}`, p, commitMsg + ` [audio: ${f}]`) && ok;
    }
  }

  if (ok) {
    console.log("🌐 UI and Audio successfully updated live at chaos.sumanthworks.com!");
  } else {
    console.warn("⚠️ Some files failed to push. The UI may be stale.");
  }
}
