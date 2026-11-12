"""Voz clonada do Jessé, receita F (decisão 12/11/2026): VoxCPM2 no Hugging Face, amostra parte4 COM transcrição.
Uso: ~/.venvs/chatterbox/bin/python scripts/voz_clonada.py <pasta>/voz.json
voz.json: {"blocos": [{"texto": "...", "tom": "tom animado, ritmo rápido", "ritmo": 1.10}, ...]}
Saída: <pasta>/voz/<i>.wav por bloco e <pasta>/voz.mp3. Idempotente: bloco já gerado não gasta cota de novo
(apague <pasta>/voz/<i>_bruto.wav pra refazer só aquele bloco). HF_TOKEN vem do .env da fabrica-conteudo.
"""
import json, subprocess, sys
from pathlib import Path
from gradio_client import Client, handle_file

RAIZ = Path(__file__).resolve().parents[1]
VOZ = RAIZ / "pesquisa" / "2026-11-12-voz-clonada"
REF = VOZ / "teste-r" / "ref_parte4.wav"
T4 = "já aproveita e já me segue que sempre vou trazer mais conteúdos para vocês e o prompt desse vídeo está nos comentários se quiser o meu arsenal de prompts para poder postar e vender muito mais no tiktok link na bio"

cfg = Path(sys.argv[1]).resolve()
blocos = json.loads(cfg.read_text())["blocos"]
OUT = cfg.parent / "voz"; OUT.mkdir(exist_ok=True)
if not REF.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/Users/dmelo/Documents/03-Marketing/tiktok-video-ia/entrada/avatar/voz/parte4.ogg",
                    "-ar", "24000", "-ac", "1", str(REF)], check=True)
tok = next((l.split("=", 1)[1].strip() for l in (RAIZ / ".env").read_text().splitlines() if l.startswith("HF_TOKEN=")), None)
if not tok:
    sys.exit("falta HF_TOKEN no .env")
c = None
partes = []
for i, b in enumerate(blocos):
    bruto, pronto = OUT / f"{i}_bruto.wav", OUT / f"{i}.wav"
    if not bruto.exists():
        c = c or Client("openbmb/VoxCPM-Demo", token=tok, verbose=False)
        r = c.predict(b["texto"], b.get("tom", ""), handle_file(str(REF)), True, T4, 2.0, False, False, api_name="/generate")
        r = r if isinstance(r, str) else r.get("path")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", r, "-ar", "24000", "-ac", "1", str(bruto)], check=True)
        print(i, "gerado", flush=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-af",
                    f"silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={b.get('ritmo', 1.10)},apad=pad_dur=0.15",
                    "-ar", "24000", "-ac", "1", str(pronto)], check=True)
    partes.append(pronto)
lista = OUT / "lista.txt"
lista.write_text("".join(f"file '{p}'\n" for p in partes))
mp3 = cfg.parent / "voz.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-b:a", "192k", str(mp3)], check=True)
print(mp3, "pronta")
