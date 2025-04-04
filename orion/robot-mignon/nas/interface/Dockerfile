FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers sources
COPY . .

# Exposition du port
EXPOSE 8000

# Variable d'environnement pour le serveur MCP
ENV MCP_SERVER_URL=http://mcp_server:8080

# Commande de démarrage
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 