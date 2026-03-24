# 📊 Dashboard WhatsApp

> Transforme o histórico exportado do WhatsApp em um dashboard analítico interativo — categorize links, mensagens e padrões de comportamento de forma automática.

---

## 📌 Visão Geral

O **Dashboard WhatsApp** é uma aplicação web local composta por dois componentes principais:

1. **`parser_whatsapp.py`** — script CLI que lê o arquivo `.txt` exportado pelo WhatsApp e gera um `mensagens.json` estruturado, com tipo e categoria de cada mensagem detectados automaticamente.
2. **`app.py`** — servidor Flask que expõe uma API REST e serve o dashboard visual via templates HTML.

O fluxo completo é: exportar a conversa no WhatsApp → rodar o parser → iniciar o servidor → visualizar o dashboard no navegador.

---

## 🗂️ Estrutura do Projeto

```
dashboard_whatsup/
├── app.py                  # Servidor Flask (rotas e API)
├── parser_whatsapp.py      # Parser do .txt do WhatsApp → .json
├── mensagens.json          # Dados estruturados gerados pelo parser
├── Conversa.txt            # Arquivo de conversa exportado (exemplo)
└── templates/
    └── index.html          # Dashboard HTML servido pelo Flask
```

---

## ⚙️ Como Funciona

### 1. Exportar a conversa do WhatsApp

No WhatsApp (Android ou iOS), abra a conversa → **⋮ Menu** → **Mais** → **Exportar conversa** → **Sem mídia**. Salve o `.txt` gerado na pasta do projeto.

### 2. Rodar o Parser

```bash
python parser_whatsapp.py Conversa.txt mensagens.json
```

O script irá:
- Parsear cada linha no formato `dd/mm/yyyy hh:mm - Remetente: Mensagem`
- Detectar automaticamente o **tipo** (`text` ou `link`)
- Classificar em **categorias** por palavras-chave na URL ou no texto
- Ignorar mensagens do sistema (mídia oculta, mensagens apagadas, etc.)
- Suportar mensagens multilinha
- Gerar um sumário no terminal ao finalizar

**Exemplo de saída:**
```
Lendo: Conversa.txt
✅ 103 mensagens salvas em: mensagens.json

📊 Resumo:
  Tipos: {'link': 72, 'text': 31}
  Categorias: {'social': 5, 'dev': 15, 'job': 12, 'finance': 8, 'media': 10, 'edu': 5, 'outros': 48}
```

### 3. Iniciar o Dashboard

```bash
python app.py
```

Acesse **http://localhost:5000** no navegador.

---

## 🗃️ Estrutura do JSON Gerado

```json
{
  "chat_metadata": {
    "source": "WhatsApp",
    "participants": ["Nome do Participante"],
    "total_messages": 103
  },
  "messages": [
    {
      "timestamp": "2025-07-05T18:43:00",
      "sender": "Nome do Participante",
      "type": "link",
      "category": "social",
      "content": "https://www.linkedin.com/in/..."
    }
  ]
}
```

---

## 🏷️ Categorias de Classificação

| Categoria  | Exemplos de domínios/palavras detectadas                              |
|------------|-----------------------------------------------------------------------|
| `dev`      | github.com, vercel.app, cloudskillsboost, deeplearning.ai, kiro.dev  |
| `job`      | gupy.io, infojobs, indeed.com, recrutei.com, "vaga", "analista"      |
| `finance`  | mercadolivre, bcb.gov.br, correios, fgts, "crédito"                  |
| `media`    | youtube.com, youtu.be, tiktok, kwai                                  |
| `social`   | linkedin.com, maps.app.goo, .vcf                                     |
| `edu`      | alura, anhanguera, grancursos, "curso", "learn."                     |
| `outros`   | Mensagens que não se enquadram nas categorias acima                  |

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10+
- pip

### Instalar dependências

```bash
pip install flask
```

### Sequência completa

```bash
# 1. Clonar o repositório
git clone https://github.com/Foxactive1/dashboard_whatsup.git
cd dashboard_whatsup

# 2. Instalar dependências
pip install flask

# 3. Parsear a conversa exportada
python parser_whatsapp.py Conversa.txt mensagens.json

# 4. Iniciar o servidor
python app.py

# 5. Abrir no navegador
# http://localhost:5000
```

---

## 🔌 API REST

| Método | Rota         | Descrição                                  |
|--------|--------------|--------------------------------------------|
| GET    | `/`          | Serve o dashboard HTML (`index.html`)       |
| GET    | `/api/data`  | Retorna o conteúdo de `mensagens.json`     |

**Exemplo de consumo da API:**
```bash
curl http://localhost:5000/api/data
```

---

## 🛠️ Tecnologias Utilizadas

| Camada     | Tecnologia                  |
|------------|-----------------------------|
| Backend    | Python 3 · Flask            |
| Parser     | re · json · datetime (stdlib) |
| Frontend   | HTML · CSS · JavaScript     |
| Dados      | JSON                        |

---

## ⚠️ Aviso de Privacidade

O arquivo `Conversa.txt` e o `mensagens.json` podem conter **dados pessoais**, como números de telefone, endereços, credenciais e informações financeiras. Antes de commitar ou compartilhar o repositório:

- Remova ou anonimize o `Conversa.txt` e o `mensagens.json`
- Adicione esses arquivos ao `.gitignore`

```gitignore
Conversa.txt
mensagens.json
```

> **Nunca armazene senhas, chaves de API ou dados sensíveis no repositório.**

---

## 📄 Licença

Este projeto está disponível para uso pessoal e educacional.

---

## 👤 Autor

**Dione Castro Alves**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-dionecastroalves-blue?logo=linkedin)](https://www.linkedin.com/in/dionecastroalves)
[![GitHub](https://img.shields.io/badge/GitHub-Foxactive1-black?logo=github)](https://github.com/Foxactive1)
