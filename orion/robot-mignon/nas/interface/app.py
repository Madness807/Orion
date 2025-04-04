import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import httpx
import aiofiles
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL du serveur MCP
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://mcp_server:8080")
VISION_SERVICE_URL = os.environ.get("VISION_SERVICE_URL", "http://vision_service:8060")
SPEECH_SERVICE_URL = os.environ.get("SPEECH_SERVICE_URL", "http://speech_service:8050")
ROBOT_ID = os.environ.get("ROBOT_ID", "MignonBot1")

# Création de l'application
app = FastAPI(
    title="Interface Robot Mignon",
    description="Interface web pour contrôler et surveiller le robot mignon",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des templates et fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Gestionnaires de connexions WebSocket
websocket_connections = []

# Classe pour les connexions WebSocket
class WebSocketConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.client_id = id(websocket)

    async def send_message(self, message: Dict[str, Any]):
        """Envoie un message au client WebSocket."""
        await self.websocket.send_json(message)

# Modèle de commande pour le robot
class RobotCommand(BaseModel):
    command_type: str
    params: Dict[str, Any]

# Route principale
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Page d'accueil de l'interface."""
    return templates.TemplateResponse("index.html", {"request": request})

# Route d'état du robot
@app.get("/api/robot/status")
async def get_robot_status():
    """Récupère l'état actuel du robot depuis le serveur MCP."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MCP_SERVER_URL}/api/robot_status/{ROBOT_ID}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur lors de la récupération de l'état du robot: {response.status_code}")
                return {"success": False, "message": "Erreur lors de la récupération de l'état du robot"}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état du robot: {e}")
        return {"success": False, "message": str(e)}

# Route pour récupérer l'historique des événements
@app.get("/api/robot/events")
async def get_robot_events(limit: int = 10):
    """Récupère l'historique des événements du robot."""
    try:
        async with httpx.AsyncClient() as client:
            # Cette route est fictive, à adapter selon l'API réelle du serveur MCP
            response = await client.get(f"{MCP_SERVER_URL}/api/events?robot_id={ROBOT_ID}&limit={limit}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur lors de la récupération des événements: {response.status_code}")
                return {"success": False, "message": "Erreur lors de la récupération des événements"}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des événements: {e}")
        return {"success": False, "message": str(e)}

# Route pour envoyer une commande au robot
@app.post("/api/robot/command")
async def send_command(command: RobotCommand):
    """Envoie une commande au robot via le serveur MCP."""
    try:
        # Construire la commande au format attendu par le serveur MCP
        mcp_command = {
            "command_type": command.command_type
        }

        # Ajouter les paramètres spécifiques selon le type de commande
        if command.command_type == "emotion":
            mcp_command["emotion"] = {
                "emotion": command.params.get("emotion", "neutre"),
                "intensity": command.params.get("intensity", 50)
            }
        elif command.command_type == "movement":
            mcp_command["movement"] = {
                "direction": command.params.get("direction", "stop"),
                "speed": command.params.get("speed", 50),
                "duration": command.params.get("duration", 1000)
            }
        elif command.command_type == "sound":
            mcp_command["sound"] = {
                "frequency": command.params.get("frequency", 1000),
                "duration": command.params.get("duration", 500)
            }

        # Envoyer la commande au serveur MCP
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/api/send_command",
                params={"robot_id": ROBOT_ID},
                json=mcp_command
            )
            if response.status_code == 200:
                # Diffuser la commande aux clients WebSocket
                await broadcast_message({
                    "type": "command_sent",
                    "command": mcp_command,
                    "timestamp": datetime.now().isoformat()
                })
                return response.json()
            else:
                logger.error(f"Erreur lors de l'envoi de la commande: {response.status_code}")
                return {"success": False, "message": "Erreur lors de l'envoi de la commande"}
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de la commande: {e}")
        return {"success": False, "message": str(e)}

# Route pour convertir du texte en parole
@app.post("/api/speech/tts")
async def text_to_speech(text: str = Form(...), language: str = Form("fr"), play: bool = Form(True)):
    """Convertit du texte en parole en utilisant le service de parole."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SPEECH_SERVICE_URL}/tts",
                json={
                    "text": text,
                    "language": language,
                    "engine": "gtts",
                    "play_audio": play
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur lors de la synthèse vocale: {response.status_code}")
                return {"success": False, "message": "Erreur lors de la synthèse vocale"}
    except Exception as e:
        logger.error(f"Erreur lors de la synthèse vocale: {e}")
        return {"success": False, "message": str(e)}

# Route pour démarrer l'écoute vocale
@app.post("/api/speech/listen")
async def start_speech_recognition():
    """Démarre la reconnaissance vocale continue."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SPEECH_SERVICE_URL}/stt/listen/start",
                json={
                    "language": "fr-FR",
                    "engine": "vosk",
                    "send_to_mcp": True
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur lors du démarrage de la reconnaissance vocale: {response.status_code}")
                return {"success": False, "message": "Erreur lors du démarrage de la reconnaissance vocale"}
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de la reconnaissance vocale: {e}")
        return {"success": False, "message": str(e)}

# Route pour arrêter l'écoute vocale
@app.post("/api/speech/stop")
async def stop_speech_recognition():
    """Arrête la reconnaissance vocale continue."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{SPEECH_SERVICE_URL}/stt/listen/stop")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur lors de l'arrêt de la reconnaissance vocale: {response.status_code}")
                return {"success": False, "message": "Erreur lors de l'arrêt de la reconnaissance vocale"}
    except Exception as e:
        logger.error(f"Erreur lors de l'arrêt de la reconnaissance vocale: {e}")
        return {"success": False, "message": str(e)}

# Route pour capturer une image
@app.post("/api/vision/capture")
async def capture_image(camera_id: int = 0, detection_types: str = ""):
    """Capture une image et applique éventuellement des détections."""
    try:
        # Préparer les types de détection
        detection_types_list = [t.strip() for t in detection_types.split(",")] if detection_types else []
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VISION_SERVICE_URL}/capture",
                json={
                    "camera_id": camera_id,
                    "save": True,
                    "detection_types": detection_types_list,
                    "send_to_mcp": True
                }
            )
            if response.status_code == 200:
                result = response.json()
                # Diffuser l'image capturée aux clients WebSocket
                await broadcast_message({
                    "type": "image_captured",
                    "image_path": result.get("image_path", ""),
                    "detections": result.get("detections", {}),
                    "timestamp": datetime.now().isoformat()
                })
                return result
            else:
                logger.error(f"Erreur lors de la capture d'image: {response.status_code}")
                return {"success": False, "message": "Erreur lors de la capture d'image"}
    except Exception as e:
        logger.error(f"Erreur lors de la capture d'image: {e}")
        return {"success": False, "message": str(e)}

# Route pour téléverser une image pour analyse
@app.post("/api/vision/upload")
async def upload_image(file: UploadFile = File(...), detection_types: str = Form("faces,objects")):
    """Téléverser et analyser une image."""
    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Créer un client httpx avec la capacité de téléverser des fichiers
        async with httpx.AsyncClient() as client:
            files = {"file": (file.filename, content, file.content_type)}
            data = {"detection_types": detection_types, "send_to_mcp": "true"}
            
            response = await client.post(f"{VISION_SERVICE_URL}/upload", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                # Diffuser les résultats aux clients WebSocket
                await broadcast_message({
                    "type": "image_analyzed",
                    "filename": file.filename,
                    "detections": result.get("detections", {}),
                    "timestamp": datetime.now().isoformat()
                })
                return result
            else:
                logger.error(f"Erreur lors du traitement de l'image: {response.status_code}")
                return {"success": False, "message": "Erreur lors du traitement de l'image"}
    except Exception as e:
        logger.error(f"Erreur lors du téléversement de l'image: {e}")
        return {"success": False, "message": str(e)}

# Endpoint WebSocket pour les mises à jour en temps réel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Gère les connexions WebSocket pour les mises à jour en temps réel."""
    await websocket.accept()
    
    # Créer une nouvelle connexion
    connection = WebSocketConnection(websocket)
    websocket_connections.append(connection)
    
    try:
        # Envoyer un message de bienvenue
        await connection.send_message({
            "type": "connected",
            "message": "Connecté à l'interface du robot mignon",
            "timestamp": datetime.now().isoformat()
        })
        
        # Boucle de réception des messages
        while True:
            # Attendre un message du client
            message = await websocket.receive_text()
            
            # Traiter le message
            try:
                data = json.loads(message)
                # Diffuser le message aux autres clients
                await broadcast_message({
                    "type": "client_message",
                    "client_id": connection.client_id,
                    "content": data,
                    "timestamp": datetime.now().isoformat()
                }, exclude=[connection])
            except json.JSONDecodeError:
                await connection.send_message({
                    "type": "error",
                    "message": "Format JSON invalide",
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        # Supprimer la connexion lorsque le client se déconnecte
        websocket_connections.remove(connection)
        logger.info(f"Client {connection.client_id} déconnecté")
    
    except Exception as e:
        # Gérer les autres erreurs
        logger.error(f"Erreur WebSocket: {e}")
        if connection in websocket_connections:
            websocket_connections.remove(connection)

async def broadcast_message(message: Dict[str, Any], exclude: List[WebSocketConnection] = None):
    """Diffuse un message à tous les clients WebSocket connectés."""
    if exclude is None:
        exclude = []
    
    for connection in websocket_connections:
        if connection not in exclude:
            try:
                await connection.send_message(message)
            except Exception as e:
                logger.error(f"Erreur lors de la diffusion du message: {e}")
                # Supprimer la connexion si elle est fermée
                if connection in websocket_connections:
                    websocket_connections.remove(connection)

# Démarrage du serveur
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
