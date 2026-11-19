#!/usr/bin/env python3
"""Gera o index.html do site a partir do procoach.html do build.

Uso:
  python3 gerar-index.py caminho/do/procoach.html [--rotulo "6.7 (teste 3)"]

O que faz (o jogo em si não é alterado, exceto o texto do rótulo, se --rotulo for usado):
  - cabeçalho de PWA (declaração de página, ajuste de celular, manifesto, ícones);
  - popup de notas de atualização (lê o novidades.json: aparece uma vez por 'versao');
  - faixa "Nova versão disponível" (compara o 'build' do novidades.json com o da página aberta);
  - pede armazenamento persistente ao navegador (protege os saves);
  - registro do sw.js;
  - grava o 'build' (impressão digital do jogo) dentro do novidades.json.
Antes de rodar: editar o novidades.json (versao, data, titulo, itens). Não mexer no campo 'build'.
"""
import sys, json, hashlib, os

args = sys.argv[1:]
rotulo = None
if '--rotulo' in args:
    i = args.index('--rotulo')
    rotulo = args[i + 1]
    del args[i:i + 2]
if len(args) != 1:
    sys.exit(__doc__)

src = open(args[0], encoding='utf-8').read()
if rotulo:
    velho = 'Versão 6.6.1 · uso pessoal'
    if src.count(velho) != 1:
        sys.exit('Rótulo do menu não encontrado (o texto "%s" deve aparecer 1 vez). Ajuste o script.' % velho)
    src = src.replace(velho, 'Versão %s · uso pessoal' % rotulo)

build = hashlib.sha1(src.encode('utf-8')).hexdigest()[:12]

aqui = os.path.dirname(os.path.abspath(__file__))
caminho_nov = os.path.join(aqui, 'novidades.json')
nov = json.load(open(caminho_nov, encoding='utf-8'))
nov['build'] = build
with open(caminho_nov, 'w', encoding='utf-8') as f:
    json.dump(nov, f, ensure_ascii=False, indent=2)
    f.write('\n')

HEAD = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0A1628">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="ProCoach">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="procoach-build" content="__BUILD__">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
'''.replace('__BUILD__', build)

TAIL = r'''
<script>
(function(){
  var CHAVE='procoach-nota-vista';
  function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
  function el(tag,css,txt){var e=document.createElement(tag);if(css)e.style.cssText=css;if(txt!=null)e.textContent=txt;return e}
  function buscar(){return fetch('novidades.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}

  // C: pedir armazenamento persistente (protege os saves)
  try{if(navigator.storage&&navigator.storage.persist){navigator.storage.persist().catch(function(){})}}catch(e){}

  // A: popup de notas de atualização (uma vez por versão)
  function popup(nov){
    if(!nov||!nov.versao||ls(CHAVE)===nov.versao)return;
    var fundo=el('div','position:fixed;inset:0;z-index:99998;background:rgba(5,10,18,.72);display:flex;align-items:center;justify-content:center;padding:16px;padding-top:max(16px,env(safe-area-inset-top));padding-bottom:max(16px,env(safe-area-inset-bottom));font-family:Barlow,system-ui,sans-serif');
    fundo.setAttribute('role','dialog');fundo.setAttribute('aria-modal','true');
    var cx=el('div','max-width:420px;width:100%;max-height:85vh;overflow:auto;background:#0E1A2B;color:#E6EDF7;border:1px solid #2A4366;border-radius:14px;padding:20px 18px;box-shadow:0 12px 40px rgba(0,0,0,.5)');
    cx.appendChild(el('div','font-family:\'Barlow Condensed\',Barlow,system-ui,sans-serif;font-size:22px;font-weight:700;color:#F2C230;margin-bottom:4px',nov.titulo||'Novidades'));
    if(nov.data)cx.appendChild(el('div','font-size:12px;color:#8FA3BF;margin-bottom:12px','Atualização de '+nov.data));
    var ul=el('ul','margin:0 0 16px;padding-left:20px;font-size:15px;line-height:1.45');
    (nov.itens||[]).forEach(function(t){var li=el('li','margin-bottom:8px',t);ul.appendChild(li)});
    cx.appendChild(ul);
    var b=el('button','display:block;width:100%;min-height:46px;border:0;border-radius:10px;background:#F2C230;color:#14201A;font-size:16px;font-weight:700;cursor:pointer','Entendi');
    b.onclick=function(){ls(CHAVE,nov.versao);fundo.remove()};
    cx.appendChild(b);fundo.appendChild(cx);document.body.appendChild(fundo);
  }

  // B: faixa "Nova versão disponível"
  var meu=(document.querySelector('meta[name="procoach-build"]')||{}).content;
  var faixa=null;
  function mostrarFaixa(){
    if(faixa)return;
    faixa=el('div','position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:99997;display:flex;align-items:center;gap:8px;background:#F2C230;color:#14201A;border-radius:12px;padding:10px 12px;box-shadow:0 6px 24px rgba(0,0,0,.45);font-family:Barlow,system-ui,sans-serif;font-size:15px;font-weight:600');
    faixa.setAttribute('role','status');
    faixa.appendChild(el('span','flex:1','Nova versão disponível.'));
    var a=el('button','min-height:40px;border:0;border-radius:8px;background:#14201A;color:#F2C230;font-weight:700;padding:0 14px;cursor:pointer','Atualizar');
    a.onclick=function(){location.reload()};
    var d=el('button','min-height:40px;border:0;border-radius:8px;background:transparent;color:#14201A;font-weight:600;padding:0 8px;cursor:pointer','Depois');
    d.onclick=function(){faixa.remove();faixa=null;adiado=Date.now()};
    faixa.appendChild(a);faixa.appendChild(d);document.body.appendChild(faixa);
  }
  var adiado=0;
  function conferir(){
    if(!meu||Date.now()-adiado<600000)return;
    buscar().then(function(n){if(n&&n.build&&n.build!==meu)mostrarFaixa()});
  }

  window.addEventListener('load',function(){
    setTimeout(function(){
      buscar().then(function(n){
        if(n&&n.build&&meu&&n.build!==meu)mostrarFaixa(); else popup(n);
      });
    },800);
    document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')conferir()});
    window.addEventListener('online',conferir);
    setInterval(conferir,300000);
    if('serviceWorker' in navigator && location.protocol!=='file:'){navigator.serviceWorker.register('sw.js').catch(function(){})}
  });
})();
</script>
</body>
</html>
'''

open(os.path.join(aqui, 'index.html'), 'w', encoding='utf-8').write(HEAD + src + TAIL)
print('index.html gerado (build %s, %d bytes). novidades.json atualizado.' % (build, len(HEAD + src + TAIL)))
