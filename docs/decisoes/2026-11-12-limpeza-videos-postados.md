# Limpeza automática dos vídeos depois de postar (12/11/2026)

Status: APROVADO (GO 12/11, grupos A e B). Script pronto; publicador e relatorio-diario ligados.

## Por quê
Mac com 6 GB livres. Vídeo e áudio dos posts somam ~1,1 GB em posts/ e crescem a cada reel. Depois que o post sai, o Zernio guarda a mídia e o Instagram também; a cópia local não serve mais.

## Regra
Post PUBLICADO (confirmado no Zernio) perde a mídia pesada local. Fica o que é texto e o que refaz o vídeo.

Apaga (dentro da pasta do post):
- arquivos .mp4 .mov .m4a .wav .mp3 .webm em qualquer subpasta
- pastas versoes/, saida/frames*/ e renders do HyperFrames (hf/renders, hf/.cache)

Fica:
- gravacao.md, legenda*.txt, grupo.md, presente.md, dossie.md, *.json
- capa/capa-reel.jpg e slides finais .jpg/.png de carrossel (pequenos)
- geradores (gera.py, roteiro.json, HTML das cenas)

## Arquivos
1. NOVO `scripts/limpar_post.py <pasta> [--apagar] [--sem-zernio "motivo"]`
   - Sem `--apagar` só lista o que sairia e o tamanho (simulação).
   - O ID vem SÓ do `zernio.txt` da pasta, nunca da linha de comando.
   - Com `--apagar` consulta o post no Zernio (ZERNIO_API_KEY do .env) e só apaga se o status for publicado. Agendado, rascunho ou erro: recusa e sai com código 1.
   - Grava `limpeza.md` na pasta (data, arquivos apagados, MB). Idempotente: rodar de novo apaga 0 arquivos.
   - `rm` direto, sem Lixeira (Lixeira não libera espaço).
2. `.claude/skills/relatorio-diario`: no relatório das 07:00, para cada post que o Analista confere como publicado ontem, roda `limpar_post.py --apagar` e põe a linha "Limpeza: N MB liberados" no relatório. É o gatilho automático.
3. `.claude/agents/publicador.md`: ao trocar o card do Notion pra Publicado, anota o ID do Zernio em `zernio.txt` na pasta do post (o script lê dali).
4. Backup `.bak-pre-limpeza` dos 2 arquivos antes de editar.

## Descartado
- Apagar logo ao agendar: se o agendamento falhar, precisa subir de novo.
- Mover pra Lixeira: não libera espaço até esvaziar.
- Apagar a pasta inteira: perde roteiro, legenda e gerador.

## Verificação
1. `limpar_post.py posts/2026-11-12-reel-diagnostico --apagar` deve RECUSAR (não publicado).
2. Simulação em posts/2026-11-09-reel-audio lista 11 arquivos, ~263 MB.
3. Com `--apagar`: `du -sh` cai pra menos de 20 MB; gravacao.md, legenda.txt e capa-reel.jpg continuam lá.
4. Rodar de novo: "0 arquivos". Se algo falhar, nada a restaurar além do próprio post (Zernio tem a mídia); paro e mostro a saída.

## Incidente (12/11)
No teste, o Gerente passou à mão o ID de OUTRO post (FINANCEIRO, publicado) pra pasta do DIAGNÓSTICO, e a 1ª versão do script apagava trabalho/ inteira. Resultado: sumiram o gera.py e o v5 do DIAGNÓSTICO (sem cópia). Correções: ID só pelo zernio.txt da pasta, trabalho/ fica (só perde a mídia). O Editor recriou o gerador e o v5.
