#  Chatbot com Ollama + FastAPI

Um chatbot inteligente construído com FastAPI e Ollama, utilizando o modelo Mistral. O chatbot possui uma base de conhecimento personalizável, responde em português do Brasil e pode ser integrado ao **WhatsApp** via Twilio.

##  Pré-requisitos

- Python 3.8+
- [Ollama](https://ollama.com/) instalado e rodando
- Modelo Mistral baixado no Ollama

##  Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/chatbot-ollama.git
cd chatbot-ollama
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Baixe o modelo Mistral no Ollama:
```bash
ollama pull mistral
```

##  Base de Conhecimento

Edite o arquivo `data/knowledge.txt` com as informações que o chatbot deve utilizar para responder. Quanto mais conteúdo, mais completo serão as respostas.

## ▶️ Executando

1. Crie o arquivo `.env` a partir do exemplo:
```bash
cp .env.example .env
```

2. Certifique-se de que o Ollama está rodando:
```bash
ollama serve
```

3. Inicie o servidor FastAPI:
```bash
python main.py
```

4. Acesse o chatbot em: **http://localhost:8000**

##  Estrutura do Projeto

```
├── main.py              # Servidor FastAPI com rotas do chatbot
├── requirements.txt     # Dependências do projeto
├── data/
│   └── knowledge.txt    # Base de conhecimento do chatbot
└── static/
    ├── index.html       # Interface do chat
    ├── style.css        # Estilos
    └── script.js        # Lógica do frontend
```

## 🔧 Como Funciona

- O backend utiliza **FastAPI** para servir a API e os arquivos estáticos
- A comunicação com o **Ollama** é feita via HTTP (porta 11434)
- O modelo **Mistral** gera as respostas com base na base de conhecimento
- A rota `/health` verifica se o Ollama está online

## 📱 Integrando com WhatsApp (Twilio)

Para receber e responder mensagens do WhatsApp automaticamente:

### 1. Crie uma conta no Twilio
- Acesse [twilio.com](https://www.twilio.com/try-twilio) e crie uma conta gratuita
- No Console do Twilio, copie o **Account SID** e **Auth Token**

### 2. Configure o WhatsApp Sandbox
- No Twilio Console, vá em **Messaging → Try it → Send a WhatsApp message**
- Anote o número do sandbox (ex: `whatsapp:+14155238886`)
- Envie a mensagem de ativação para o sandbox

### 3. Configure as variáveis de ambiente
Edite o arquivo `.env` com suas credenciais:
```
TWILIO_ACCOUNT_SID=SEU_ACCOUNT_SID
TWILIO_AUTH_TOKEN=SEU_AUTH_TOKEN
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 4. Configure o Webhook no Twilio
No Twilio Console:
1. Vá em **Messaging → Settings → WhatsApp Sandbox Settings**
2. Em **"When a message come in"**, coloque:
   ```
   https://SEU_DOMINIO/whatsapp/webhook
   ```
3. Selecione **HTTP POST**
4. Clique em **Save**

### 5. Para produção (número oficial)
- Solicite um número oficial de WhatsApp no Twilio
- Configure o webhook para o seu domínio (use ngrok para testes locais)

### Teste local com ngrok
```bash
# Instale o ngrok e exponha a porta 8000
ngrok http 8000
```

Copie a URL HTTPS e use no webhook do Twilio.

## 📄 Licença

Este projeto está sob a licença MIT.
