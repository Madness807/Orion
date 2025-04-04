FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système pour l'audio
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libsndfile1 \
    espeak-ng \
    espeak-ng-data \
    libespeak-ng-dev \
    ffmpeg \
    libavcodec-extra \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer les dossiers pour les données audio
RUN mkdir -p /app/data/recordings
RUN mkdir -p /app/data/synthesized
RUN mkdir -p /app/models

# Télécharger le modèle Vosk pour la reconnaissance vocale en français
RUN mkdir -p /app/models/vosk && \
    wget -q -O /app/models/vosk/fr.zip https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip && \
    unzip /app/models/vosk/fr.zip -d /app/models/vosk/ && \
    rm /app/models/vosk/fr.zip && \
    mv /app/models/vosk/vosk-model-small-fr-0.22 /app/models/vosk/fr

# Variable d'environnement pour le service MCP
ENV MCP_SERVER_URL=http://mcp_server:8080

# Exposer le port de l'API
EXPOSE 8050

# Commande de démarrage
CMD ["python", "main.py"] 