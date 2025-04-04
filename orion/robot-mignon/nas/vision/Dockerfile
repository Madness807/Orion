FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système pour OpenCV et face-recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libfontconfig1 \
    libjpeg-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer les dossiers pour les données
RUN mkdir -p /app/data/images
RUN mkdir -p /app/data/videos
RUN mkdir -p /app/data/models
RUN mkdir -p /app/data/detected

# Télécharger les modèles pré-entraînés pour YOLOv8
RUN pip install --no-cache-dir ultralytics && \
    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Variable d'environnement pour le service MCP
ENV MCP_SERVER_URL=http://mcp_server:8080

# Exposer le port de l'API
EXPOSE 8060

# Commande de démarrage
CMD ["python", "main.py"] 