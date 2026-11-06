#!/bin/bash
# Instala (idempotente) o AGENTS.md e as skills de um agente do OpenBot.
# Uso: openbot/instalar-agente.sh <cargo> <agent-id>
#   cargo: gerente-de-marketing | analista-de-social-media | copywriter | designer-grafico | editor-de-video | assistente-de-social-media
# Rodar 10x dá o mesmo resultado: sobrescreve AGENTS.md e recopia as skills.
set -euo pipefail
CARGO="$1"; ID="$2"
FAB="/Users/dmelo/Documents/03-Marketing/fabrica-conteudo"
JARVIS="/Users/dmelo/Documents/03-Marketing/cerebro-jarvis"
W="/Users/dmelo/OpenBot/Agents/$ID"
SRC="$FAB/openbot/agentes/$CARGO.md"
[ -d "$W" ] || { echo "workspace não existe: $W"; exit 1; }
[ -f "$SRC" ] || { echo "rascunho não existe: $SRC"; exit 1; }

# 1. AGENTS.md = rascunho do cargo + bloco comum
{ cat "$SRC"; echo; sed '1d' "$FAB/openbot/agentes/_comum.md"; } > "$W/AGENTS.md"
chmod 600 "$W/AGENTS.md"

# 2. skills por cargo (pastas com SKILL.md)
case "$CARGO" in
  gerente-de-marketing)      SKILLS="$FAB/.claude/skills/modelar-post $FAB/.claude/skills/relatorio-diario $JARVIS/skills/avaliador $JARVIS/skills/registrar-feedback" ;;
  analista-de-social-media)  SKILLS="$JARVIS/skills/pauta-matinal $JARVIS/skills/radar-concorrentes $JARVIS/skills/metricas-instagram $FAB/.claude/skills/relatorio-diario" ;;
  copywriter)                SKILLS="" ;;   # ganchos-jesse já é user level
  designer-grafico)          SKILLS="" ;;   # carrossel já é user level
  editor-de-video)           SKILLS="" ;;   # editar-reels, fio, jogo... já são user level
  assistente-de-social-media) SKILLS="" ;;
  *) echo "cargo desconhecido: $CARGO"; exit 1 ;;
esac
mkdir -p "$W/.claude/skills"
for s in $SKILLS; do
  n=$(basename "$s"); rm -rf "$W/.claude/skills/$n"; cp -R "$s" "$W/.claude/skills/$n"
done
echo "ok $CARGO -> $W"
echo "  AGENTS.md: $(wc -c < "$W/AGENTS.md") bytes"
echo "  skills: $(ls "$W/.claude/skills" | tr '\n' ' ')"
