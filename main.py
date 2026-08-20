from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
