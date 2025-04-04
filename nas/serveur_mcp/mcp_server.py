from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json
import os
import sys
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Ajouter les chemins pour l'importation des modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import des schémas MCP
from schemas.mcp_schemas import (
    SensorMCPMessage, EmotionalMCPMessage, RobotCommand,
    MCPResponse, EmotionType, SensorDataPayload
)

# Import du gestionnaire de contexte
from context_manager import get_context_manager

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Serveur MCP (Model Context Protocol)",
    description="API pour la communication entre le robot mignon et le cerveau IA",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dans un environnement de production, spécifiez les origines exactes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir le gestionnaire de contexte
def get_context():
    return get_context_manager()

# Route de ping pour vérifier la connectivité
@app.get("/api/ping")
async def ping():
    """Vérifie si le serveur est en ligne."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Route pour recevoir les données des capteurs
@app.post("/api/sensors", response_model=MCPResponse)
async def receive_sensor_data(
    message: SensorMCPMessage = Body(...),
    context = Depends(get_context)
):
    """
    Reçoit les données des capteurs du robot.
    
    Le message doit être au format MCP (Model Context Protocol).
    """
    try:
        logger.info(f"Données des capteurs reçues du robot {message.robot_id}")
        
        # Extraire les données des capteurs
        sensor_data = message.sensors.dict()
        
        # Traiter les données avec le gestionnaire de contexte
        response = context.process_sensor_data(sensor_data)
        
        return MCPResponse(
            success=response["success"],
            message=response["message"],
            data={"analysis": response.get("analysis", {}), "commands": response.get("commands", [])}
        )
    except Exception as e:
        logger.error(f"Erreur lors du traitement des données des capteurs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour recevoir l'état émotionnel
@app.post("/api/emotion", response_model=MCPResponse)
async def receive_emotional_state(
    message: EmotionalMCPMessage = Body(...),
    context = Depends(get_context)
):
    """
    Reçoit l'état émotionnel du robot.
    
    Le message doit être au format MCP (Model Context Protocol).
    """
    try:
        logger.info(f"État émotionnel reçu du robot {message.robot_id}")
        
        # Extraire l'état émotionnel
        emotional_state = message.emotion.dict()
        
        # Traiter l'état émotionnel avec le gestionnaire de contexte
        response = context.process_emotional_state(emotional_state)
        
        return MCPResponse(
            success=response["success"],
            message=response["message"],
            data=response.get("emotion", {})
        )
    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'état émotionnel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour obtenir les commandes
@app.get("/api/commands", response_model=MCPResponse)
async def get_commands(
    robot_id: str,
    context = Depends(get_context)
):
    """
    Récupère les commandes en attente pour le robot.
    """
    try:
        logger.info(f"Demande de commandes pour le robot {robot_id}")
        
        # Récupérer les commandes avec le gestionnaire de contexte
        commands = context.get_commands(robot_id)
        
        return MCPResponse(
            success=True,
            message="Commandes récupérées avec succès",
            data={"commands": commands}
        )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des commandes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour envoyer manuellement une commande au robot
@app.post("/api/send_command", response_model=MCPResponse)
async def send_command(
    robot_id: str,
    command: RobotCommand = Body(...),
    context = Depends(get_context)
):
    """
    Envoie une commande au robot.
    
    La commande sera mise en file d'attente et récupérée par le robot lors de sa prochaine requête.
    """
    try:
        logger.info(f"Envoi d'une commande manuelle au robot {robot_id}")
        
        # Ajouter la commande avec le gestionnaire de contexte
        success = context.add_command(command.dict())
        
        if success:
            return MCPResponse(
                success=True,
                message="Commande ajoutée avec succès",
                data={"command": command}
            )
        else:
            return MCPResponse(
                success=False,
                message="Erreur lors de l'ajout de la commande",
                data=None
            )
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi d'une commande: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour obtenir l'état actuel du robot
@app.get("/api/robot_status/{robot_id}", response_model=MCPResponse)
async def get_robot_status(
    robot_id: str,
    context = Depends(get_context)
):
    """
    Récupère l'état actuel du robot (capteurs, émotion, etc.).
    """
    try:
        logger.info(f"Demande de l'état actuel du robot {robot_id}")
        
        # Vérifier que le robot correspond à celui géré par le contexte
        if robot_id != context.robot_id:
            return MCPResponse(
                success=False,
                message=f"Robot inconnu: {robot_id}",
                data=None
            )
        
        # Récupérer le contexte actuel
        current_context = context.current_context
        
        return MCPResponse(
            success=True,
            message="État du robot récupéré avec succès",
            data={
                "sensors": current_context.get("sensors", {}),
                "emotion": current_context.get("emotion", {}),
                "recent_events": current_context.get("recent_events", []),
                "last_interaction": current_context.get("last_interaction", None)
            }
        )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état du robot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour ajouter une interaction manuelle
@app.post("/api/interaction", response_model=MCPResponse)
async def add_interaction(
    robot_id: str,
    interaction_type: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    context = Depends(get_context)
):
    """
    Ajoute une interaction manuelle (ex: une commande vocale, une interaction physique, etc.).
    """
    try:
        logger.info(f"Ajout d'une interaction manuelle pour le robot {robot_id}")
        
        # Vérifier que le robot correspond à celui géré par le contexte
        if robot_id != context.robot_id:
            return MCPResponse(
                success=False,
                message=f"Robot inconnu: {robot_id}",
                data=None
            )
        
        # Ajouter l'interaction avec le gestionnaire de contexte
        success = context.add_interaction(interaction_type, content, metadata)
        
        if success:
            return MCPResponse(
                success=True,
                message="Interaction ajoutée avec succès",
                data={"interaction_type": interaction_type, "content": content}
            )
        else:
            return MCPResponse(
                success=False,
                message="Erreur lors de l'ajout de l'interaction",
                data=None
            )
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout d'une interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route principale pour vérifier que le serveur fonctionne
@app.get("/")
async def root():
    """Page d'accueil du serveur MCP."""
    return {
        "name": "Serveur MCP (Model Context Protocol)",
        "status": "online",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/api/ping", "method": "GET", "description": "Vérifier la connectivité"},
            {"path": "/api/sensors", "method": "POST", "description": "Recevoir les données des capteurs"},
            {"path": "/api/emotion", "method": "POST", "description": "Recevoir l'état émotionnel"},
            {"path": "/api/commands", "method": "GET", "description": "Obtenir les commandes"},
            {"path": "/api/send_command", "method": "POST", "description": "Envoyer une commande manuelle"},
            {"path": "/api/robot_status/{robot_id}", "method": "GET", "description": "Obtenir l'état du robot"},
            {"path": "/api/interaction", "method": "POST", "description": "Ajouter une interaction manuelle"}
        ]
    }
