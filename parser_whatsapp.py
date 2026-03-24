"""
parser_whatsapp.py
Lê o arquivo .txt exportado do WhatsApp e gera mensagens.json estruturado.

Uso:
    python parser_whatsapp.py "Conversa_do_WhatsApp.txt" mensagens.json
"""

import re
import json
import sys
from datetime import datetime

# ── Regras de categorização por palavra-chave na URL ou no texto ─────────────
CATEGORY_RULES = [
    ("dev",     [r"github\.com", r"vercel\.app", r"cloudskillsboost", r"deeplearning\.ai",
                 r"rocketseat", r"kiro\.dev", r"pythonanywhere", r"coodesh", r"bindai",
                 r"devsu\.com", r"casado\.dev", r"er-p-innova"]),
    ("job",     [r"gupy\.io", r"infojobs", r"dbccompany", r"vagas\.", r"indeed\.com",
                 r"recrutei\.com", r"bairesdev", r"gedanken", r"narwal",
                 r"vaga\b", r"analista", r"desenvolvedor", r"bolsista"]),
    ("finance", [r"lawsuit\.page", r"mercadolivre", r"dell\.com", r"bcb\.gov\.br",
                 r"shopee", r"jusbrasil", r"correios", r"fgts", r"crédito"]),
    ("media",   [r"kwai", r"youtube\.com", r"youtu\.be", r"tiktok", r"kwai-video"]),
    ("social",  [r"linkedin\.com", r"maps\.app\.goo", r"\.vcf"]),
    ("edu",     [r"alura", r"platosedu", r"anhanguera", r"academiapme", r"grancursos",
                 r"learn\.", r"curso"]),
]

# ── Regex para linha do WhatsApp ─────────────────────────────────────────────
LINE_RE = re.compile(
    r'^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - ([^:]+): (.+)$',
    re.DOTALL
)

URL_RE = re.compile(r'https?://\S+')

SKIP_PATTERNS = [
    r'^<Mídia oculta>$',
    r'^Mensagem apagada$',
    r'mensagens que você envia',
    r'mensagens temporárias',
    r'desativou as mensagens',
    r'^\s*$',
]
SKIP_RE = re.compile('|'.join(SKIP_PATTERNS), re.IGNORECASE)

# ── Helpers ──────────────────────────────────────────────────────────────────

def detect_type(content: str) -> str:
    if URL_RE.search(content):
        return "link"
    return "text"

def detect_category(content: str) -> str:
    text = content.lower()
    for category, patterns in CATEGORY_RULES:
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return category
    return "outros"

def parse_whatsapp_txt(filepath: str) -> list[dict]:
    messages = []
    current_msg = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()

            # Linha nova mensagem?
            m = LINE_RE.match(line)
            if m:
                # Salva mensagem anterior
                if current_msg:
                    messages.append(current_msg)

                date_str, time_str, sender, content = m.groups()
                content = content.strip()

                # Ignora mensagens do sistema e mídia/apagadas
                if SKIP_RE.search(content):
                    current_msg = None
                    continue

                try:
                    ts = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
                    timestamp = ts.strftime("%Y-%m-%dT%H:%M:00")
                except ValueError:
                    timestamp = f"{date_str}T{time_str}:00"

                msg_type = detect_type(content)
                category = detect_category(content)

                # Extrai só a URL se for link
                url_match = URL_RE.search(content)
                if url_match and msg_type == "link":
                    content_clean = url_match.group(0)
                else:
                    content_clean = content

                current_msg = {
                    "timestamp": timestamp,
                    "sender": sender.strip(),
                    "type": msg_type,
                    "category": category,
                    "content": content_clean,
                }
            else:
                # Continuação de mensagem multilinha
                if current_msg and line:
                    current_msg["content"] += " " + line

    if current_msg:
        messages.append(current_msg)

    return messages


def main():
    if len(sys.argv) < 3:
        print("Uso: python parser_whatsapp.py <arquivo.txt> <saida.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Lendo: {input_file}")
    messages = parse_whatsapp_txt(input_file)

    # Agrupa por remetentes únicos
    participants = sorted(set(m["sender"] for m in messages))

    output = {
        "chat_metadata": {
            "source": "WhatsApp",
            "participants": participants,
            "total_messages": len(messages),
        },
        "messages": messages,
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(messages)} mensagens salvas em: {output_file}")

    # Sumário rápido
    from collections import Counter
    cats = Counter(m["category"] for m in messages)
    types = Counter(m["type"] for m in messages)
    print("\n📊 Resumo:")
    print(f"  Tipos:      {dict(types)}")
    print(f"  Categorias: {dict(cats)}")


if __name__ == '__main__':
    main()
