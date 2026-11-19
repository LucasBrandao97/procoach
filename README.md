# ProCoach Football

Jogo de gerenciamento de futebol inspirado no Brasfoot. Projeto pessoal, sem fins comerciais, feito para jogar com amigos e família.

**Jogar:** https://lucasbrandao97.github.io/procoach/

## Como instalar no celular

1. Abra o link acima no **Chrome** (Android) com internet e espere o menu do jogo aparecer.
2. Menu do Chrome (três pontinhos) > **Adicionar à tela inicial** (ou **Instalar app**).
3. Abra uma vez pelo ícone, ainda com internet, para o jogo ficar guardado.
4. Pronto: depois disso o jogo abre mesmo sem internet.

No iPhone: abra no **Safari** > Compartilhar > **Adicionar à Tela de Início**.

## Como atualizar

Não precisa baixar nada. Abra o app com internet: se houver versão nova, aparece a faixa **"Nova versão disponível"**. Toque em **Atualizar**. As carreiras salvas continuam.
Quando houver novidades, uma janelinha mostra o resumo do que mudou.

## Salvar e levar uma carreira

O jogo guarda as carreiras no próprio navegador. Para fazer backup ou levar de um aparelho para outro:

- **Exportar:** em *Carregar jogo*, toque em **Exportar** ao lado da carreira (ou em Configurações > Exportar carreira) e depois em **Baixar arquivo**.
- **Importar:** em *Carregar jogo* (ou em Configurações), toque em **Importar carreira** e escolha o arquivo `.json`.

Limpar os dados do navegador apaga as carreiras. Exporte antes.

## Versão anterior (backup)

Se uma atualização der problema, a versão anterior fica em: https://lucasbrandao97.github.io/procoach/anterior/

## Para quem mantém o site

- `index.html` é gerado por `python3 gerar-index.py <procoach.html do build> [--rotulo "6.7"]`.
- Antes de gerar, edite `novidades.json` (versão, data, título e itens da nota). O campo `build` é preenchido pelo script.
- Antes de substituir o `index.html`, copie o atual para `anterior/index.html` (guarda-se só uma versão antiga).
