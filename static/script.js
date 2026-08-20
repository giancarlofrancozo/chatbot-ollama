async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const message = userInput.value.trim();

    if (!message) return;

   
    addMessageToChat(message, "user");
    userInput.value = "";
    userInput.focus();

    
    addMessageToChat("Pensando...", "bot");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

       
        chatBox.lastChild.remove();

        if (data.error) {
            addMessageToChat(`Erro: ${data.error}`, "bot");
        } else {
            addMessageToChat(data.response, "bot");
        }
    } catch (error) {
        chatBox.lastChild.remove();
        addMessageToChat(`Erro de conexão: ${error}`, "bot");
    }

    
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addMessageToChat(message, sender) {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;
    chatBox.appendChild(messageDiv);
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Dando uma olhada se o ollama nao morreu
async function checkHealth() {
    try {
        const response = await fetch("/health");
        const data = await response.json();
        document.getElementById("status").textContent = data.status;
    } catch {
        document.getElementById("status").textContent = " Ollama offline";
    }
}

checkHealth();