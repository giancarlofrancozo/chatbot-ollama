# 🤖 Chatbot com Ollama + FastAPI

Um chatbot inteligente construído com FastAPI e Ollama, utilizando o modelo Mistral. O chatbot possui uma base de conhecimento personalizável e responde em português do Brasil.

## 📋 Pré-requisitos

- Python 3.8+
- [Ollama](https://ollama.com/) instalado e rodando
- Modelo Mistral baixado no Ollama

## 🚀 Instalação

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

## 📚 Base de Conhecimento

Edite o arquivo `data/knowledge.txt` com as informações que o chatbot deve utilizar para responder. Quanto mais conteúdo, mais completo serão as respostas.

## ▶️ Executando

1. Certifique-se de que o Ollama está rodando:
```bash
ollama serve
```

2. Inicie o servidor FastAPI:
```bash
python main.py
```

3. Acesse o chatbot em: **http://localhost:8000**

## 🏗️ Estrutura do Projeto

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

## 📄 Licença

Este projeto está sob a licença MIT.
