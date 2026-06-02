def apply_voice_personalities():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    original_func = r"""function chaosSpeak(paneId,btn){if(!('speechSynthesis' in window))return;if(btn.classList.contains('playing')){speechSynthesis.cancel();btn.classList.remove('playing');btn.textContent='LISTEN';return}document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='LISTEN'});const text=document.getElementById(paneId)?.innerText.replace(/\s+/g,' ').trim();if(!text)return;const u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=paneId.includes('quant')?1.05:paneId.includes('eli5')?.9:.95;btn.classList.add('playing');btn.textContent='PLAYING';u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};speechSynthesis.cancel();speechSynthesis.speak(u)}"""

    female_voices_js = r"""
    window.findVoice = function(patterns) {
      const vs = speechSynthesis.getVoices();
      for (const p of patterns) {
        const v = vs.find(x => p.test(x.name));
        if (v) return v;
      }
      return vs.find(x => /en-(US|GB)/i.test(x.lang)) || vs[0];
    };

    function chaosSpeak(paneId, btn) {
      if (!('speechSynthesis' in window)) return;
      if (btn.classList.contains('playing')) {
        speechSynthesis.cancel();
        btn.classList.remove('playing');
        btn.textContent = 'LISTEN';
        return;
      }
      document.querySelectorAll('.voice-btn').forEach(b => {
        b.classList.remove('playing');
        b.textContent = 'LISTEN';
      });
      const text = document.getElementById(paneId)?.innerText.replace(/\s+/g, ' ').trim();
      if (!text) return;
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      
      if (paneId.includes('eli5')) {
        u.rate = 1.0; u.pitch = 1.2;
        u.voice = window.findVoice([/Samantha/i, /Victoria/i, /Google US English/i, /Zira/i]);
      } else if (paneId.includes('quant')) {
        u.rate = 1.25; u.pitch = 0.9;
        u.voice = window.findVoice([/Fred/i, /Ralph/i, /Albert/i, /Microsoft Mark/i, /Richard/i, /Google UK/i]);
      } else {
        u.rate = 1.1; u.pitch = 1.0;
        u.voice = window.findVoice([/Daniel/i, /Oliver/i, /Arthur/i, /Google UK/i]);
      }
      
      btn.classList.add('playing');
      btn.textContent = 'PLAYING';
      u.onend = () => {
        btn.classList.remove('playing');
        btn.textContent = 'LISTEN';
      };
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
    }
    
    if ('speechSynthesis' in window) {
      speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
    }
"""

    if original_func in html:
        html = html.replace(original_func, female_voices_js)
        with open('public/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully injected the female/male voices code!")
    else:
        print("ERROR: Could not find original function in index.html")

apply_voice_personalities()
