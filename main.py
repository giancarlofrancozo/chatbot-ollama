from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("MODEL", "mistral")

# Twilio WhatsApp Config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

def load_knowledge():
    knowlodge_path = "data/knowledge.txt"
    if os.path.exists(knowlodge_path):
        with open(knowlodge_path, "r", encoding="utf-8") as f:
            content = f.read()
            print("Knowledge carregado com sucesso.")
            return content
    else:
        print("Arquivo de conhecimento não encontrado, verefique a pasta data se possui o knowledge.txt.")
        return ""
    
KNOWLEDGE = load_knowledge()

SYSTEM_PROMPT = """Você é um assistente inteligente e amigável. 
Responda em português do Brasil de forma clara e concisa.
Seja útil, honesto e educado."""

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat_endpoint(message: dict):
    user_message = message.get("message", "")
    if not user_message.strip():
        return {"error": "Mensagem vazia."}

    try:
        if KNOWLEDGE:
            prompt_completo = f"""{SYSTEM_PROMPT} 
BASE DE CONHECIMENTO:
{KNOWLEDGE}

Pergunta do usuário: {user_message}

Responda baseado na base de conhecimento acima:"""
        else:
            prompt_completo = f"{SYSTEM_PROMPT}\nPergunta do usuário: {user_message}\nResponda de forma clara e concisa."
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt_completo,
                "stream": False,
                "temperature": 0.7
            },
            timeout=120
        )
        if response.status_code == 200:
            result = response.json()
            assistant_mensagem = result.get("response", "")
            return {"response": assistant_mensagem}
        else:
            return {"error": f"Erro ao se comunicar com Ollama: {response.status_code} - {response.text}"}
        
    except requests.exceptions.ConnectionError:
        return {"error": "Erro de conexão com o servidor ou Ollama não está em execução."}
    except Exception as e:
        return {"error": f"Ocorreu um erro: {str(e)}"}

@app.get("/health")
async def health():
    try:
        requests.get("http://localhost:11434/api/tags", timeout=5)
        return {"status": "Ollama online"}
    except:
        return {"status": "Ollama offline"}


# ============================================
# WhatsApp Webhook - Twilio Integration
# ============================================

@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    """
    Webhook que recebe mensagens do WhatsApp via Twilio.
    Configura no Twilio Console: https://console.twilio.com
    """
    form_data = await request.form()
    incoming_msg = form_data.get("Body", "")
    from_number = form_data.get("From", "")

    print(f"[WhatsApp] Mensagem de {from_number}: {incoming_msg}")

    if not incoming_msg.strip():
        return Response(
            content="<Response><Message>Mensagem vazia.</Message></Response>",
            media_type="application/xml"
        )

    try:
        # Monta o prompt com base de conhecimento
        if KNOWLEDGE:
            prompt_completo = f"""{SYSTEM_PROMPT}
BASE DE CONHECIMENTO:
{KNOWLEDGE}

Pergunta do usuário (WhatsApp): {incoming_msg}

Responda baseado na base de conhecimento acima:"""
        else:
            prompt_completo = f"{SYSTEM_PROMPT}\nPergunta do usuário (WhatsApp): {incoming_msg}\nResponda de forma clara e concisa."

        # Chama o Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt_completo,
                "stream": False,
                "temperature": 0.7
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            assistant_msg = result.get("response", "Desculpe, não consegui gerar uma resposta.")
        else:
            assistant_msg = "Erro ao processar sua mensagem. Tente novamente mais tarde."

    except requests.exceptions.ConnectionError:
        assistant_msg = "Servidor offline. Por favor, tente novamente em alguns instantes."
    except Exception as e:
        assistant_msg = f"Ocorreu um erro: {str(e)}"

    print(f"[WhatsApp] Resposta: {assistant_msg[:100]}...")

    # Retorna XML no formato TwiML que o Twilio espera
    xml_response = f"""<Response>
    <Message>{escape_xml(assistant_msg)}</Message>
</Response>"""

    return Response(content=xml_response, media_type="application/xml")


@app.get("/whatsapp/webhook")
async def whatsapp_webhook_verify(request: Request):
    """
    Verificação do webhook (Twilio pode chamar GET para validar).
    """
    return {"status": "Webhook WhatsApp ativo"}


def escape_xml(text: str) -> str:
    """Escapa caracteres especiais para XML/TwiML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&apos;")
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
