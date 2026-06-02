with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('function chaosSpeak(paneId,btn){')
end_idx = html.find('function copyLine(){')

if start_idx != -1 and end_idx != -1:
    correct_audio_js = '''function chaosSpeak(paneId,btn){
    if(!('speechSynthesis' in window))return;
    if(btn.classList.contains('playing')){speechSynthesis.cancel();btn.classList.remove('playing');btn.textContent='LISTEN';return}
    document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='LISTEN'});
    const text=document.getElementById(paneId)?.innerText.replace(/\s+/g,' ').trim();
    if(!text)return;
    const u=new SpeechSynthesisUtterance(text);
    u.lang='en-US';
    if(paneId.includes('eli5')){ u.rate=1.1; u.pitch=1.2; }
    else if(paneId.includes('quant')){ u.rate=0.9; u.pitch=0.7; }
    else { u.rate=1.0; u.pitch=1.0; }
    btn.classList.add('playing');btn.textContent='PLAYING';
    u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};
    speechSynthesis.cancel();speechSynthesis.speak(u);
}
'''
    html = html[:start_idx] + correct_audio_js + html[end_idx:]
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Fixed JS syntax')
else:
    print('Could not find start or end index')
