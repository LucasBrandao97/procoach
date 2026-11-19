#!/usr/bin/env python3
"""Gera o index.html do site a partir do procoach.html do build.
Uso: python3 gerar-index.py caminho/do/procoach.html
Coloca na frente o cabeçalho de PWA (declaração de página, ajuste de celular, manifesto)
e no fim o registro do sw.js. O jogo em si não é alterado."""
import sys
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
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
'''
TAIL = '''
<script>
if('serviceWorker' in navigator && location.protocol!=='file:'){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){})})}
</script>
</body>
</html>
'''
src = open(sys.argv[1], encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(HEAD + src + TAIL)
print('index.html gerado:', len(HEAD + src + TAIL), 'bytes')
