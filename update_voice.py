def update_voice_engine():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    original_func = r"""function chaosSpeak(paneId,btn){if(!('speechSynthesis' in window))return;if(btn.classList.contains('playing')){speechSynthesis.cancel();btn.classList.remove('playing');btn.textContent='LISTEN';return}document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='LISTEN'});const text=document.getElementById(paneId)?.innerText.replace(/\s+/g,' ').trim();if(!text)return;const u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=paneId.includes('quant')?1.05:paneId.includes('eli5')?.9:.95;btn.classList.add('playing');btn.textContent='PLAYING';u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};speechSynthesis.cancel();speechSynthesis.speak(u)}"""
    
    better_func = r"""function chaosSpeak(paneId,btn){if(!('speechSynthesis' in window))return;if(btn.classList.contains('playing')){speechSynthesis.cancel();btn.classList.remove('playing');btn.textContent='LISTEN';return}document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='LISTEN'});const text=document.getElementById(paneId)?.innerText.replace(/\s+/g,' ').trim();if(!text)return;const u=new SpeechSynthesisUtterance(text);u.lang='en-US';if(paneId.includes('eli5')){u.rate=1.1;u.pitch=1.2;}else if(paneId.includes('quant')){u.rate=0.9;u.pitch=0.7;}else{u.rate=1.0;u.pitch=1.0;}btn.classList.add('playing');btn.textContent='PLAYING';u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};speechSynthesis.cancel();speechSynthesis.speak(u)}"""

    if original_func in html:
        html = html.replace(original_func, better_func)
        with open('public/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully updated the Voice Engine to the 3 distinct personalities!")
    else:
        print("ERROR: Could not find original function in index.html")

update_voice_engine()
