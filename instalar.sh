#!/bin/bash
# Coloca os agentes e a skill no lugar que o Claude Code lê (.claude/). Rode uma vez nesta pasta: bash instalar.sh
cd "$(dirname "$0")"
mkdir -p .claude
cp -R instalar/agents .claude/
cp -R instalar/skills .claude/
echo "Pronto: $(ls .claude/agents | wc -l | tr -d ' ') agentes e a skill modelar-post instalados em .claude/"
