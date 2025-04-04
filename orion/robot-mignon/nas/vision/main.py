import os
import sys
import uvicorn
import logging
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importation du processeur d'images
from image_processor import ImageProcessor, DetectionType

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("vision_service.log")
    ]
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Service de Vision pour Robot Mignon",
    description="API pour la détection d'éléments visuels pour le robot mignon",
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

# Instance du processeur d'images
image_processor = None

# Modèle pour les requêtes de traitement d'images
class ImageProcessRequest(BaseModel):
    image_path: str
    detection_types: List[str]
    send_to_mcp: Optional[bool] = True

# Modèle pour les requêtes de capture d'images
class CaptureRequest(BaseModel):
    camera_id: Optional[int] = 0
    save: Optional[bool] = True
    detection_types: Optional[List[str]] = []
    send_to_mcp: Optional[bool] = True

def init_processor():
    """Initialise le processeur d'images."""
    global image_processor
    try:
        image_processor = ImageProcessor()
        logger.info("Processeur d'images initialisé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du processeur d'images: {e}")
        image_processor = None

# Route pour vérifier l'état du service
@app.get("/health")
async def health_check():
    """Vérifie l'état du service."""
    return {
        "status": "ok",
        "image_processor": "initialized" if image_processor else "not_initialized"
    }

# Route pour traiter une image
@app.post("/process")
async def process_image(request: ImageProcessRequest):
    """
    Traite une image avec les types de détection spécifiés.
    
    Args:
        request: Paramètres de traitement de l'image
    
    Returns:
        Résultats des détections
    """
    global image_processor
    
    try:
        # Vérifier que le processeur d'images est initialisé
        if not image_processor:
            init_processor()
            if not image_processor:
                raise HTTPException(
                    status_code=500, 
                    detail="Erreur lors de l'initialisation du processeur d'images"
                )
        
        # Vérifier que l'image existe
        if not os.path.exists(request.image_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Image non trouvée: {request.image_path}"
            )
        
        # Convertir les types de détection en enum
        detection_types = []
        for detection_type in request.detection_types:
            try:
                detection_types.append(DetectionType(detection_type.lower()))
            except ValueError:
                logger.warning(f"Type de détection non reconnu: {detection_type}")
        
        if not detection_types:
            raise HTTPException(
                status_code=400, 
                detail="Aucun type de détection valide spécifié"
            )
        
        # Traiter l'image
        results = image_processor.process_image(request.image_path, detection_types)
        
        # Vérifier s'il y a eu une erreur
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        # Envoyer les résultats au serveur MCP si demandé
        if request.send_to_mcp:
            image_processor.send_to_mcp(results)
        
        return results
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour traiter une image téléchargée
@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    detection_types: str = Form(...),
    send_to_mcp: bool = Form(True)
):
    """
    Traite une image téléchargée avec les types de détection spécifiés.
    
    Args:
        file: Fichier image téléchargé
        detection_types: Types de détection séparés par des virgules
        send_to_mcp: Indique si les résultats doivent être envoyés au serveur MCP
    
    Returns:
        Résultats des détections
    """
    global image_processor
    
    try:
        # Vérifier que le processeur d'images est initialisé
        if not image_processor:
            init_processor()
            if not image_processor:
                raise HTTPException(
                    status_code=500, 
                    detail="Erreur lors de l'initialisation du processeur d'images"
                )
        
        # Créer un fichier temporaire pour sauvegarder l'image
        import tempfile
        suffix = Path(file.filename).suffix if file.filename else ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
            # Lire le contenu du fichier et l'écrire dans le fichier temporaire
            contents = await file.read()
            temp.write(contents)
            temp.flush()
            
            # Traiter l'image
            types = [t.strip().lower() for t in detection_types.split(",")]
            request = ImageProcessRequest(
                image_path=temp.name,
                detection_types=types,
                send_to_mcp=send_to_mcp
            )
            
            results = await process_image(request)
            
            # Supprimer le fichier temporaire
            os.unlink(temp.name)
            
            return results
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'image téléchargée: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour capturer une image depuis une caméra
@app.post("/capture")
async def capture_image(request: CaptureRequest):
    """
    Capture une image depuis une caméra et la traite.
    
    Args:
        request: Paramètres de capture et de traitement
    
    Returns:
        Résultats des détections et chemin de l'image capturée
    """
    global image_processor
    
    try:
        # Vérifier que le processeur d'images est initialisé
        if not image_processor:
            init_processor()
            if not image_processor:
                raise HTTPException(
                    status_code=500, 
                    detail="Erreur lors de l'initialisation du processeur d'images"
                )
        
        # Capturer une image
        image_path = image_processor.capture_image(
            camera_id=request.camera_id,
            save=request.save
        )
        
        if not image_path:
            raise HTTPException(
                status_code=500, 
                detail="Erreur lors de la capture d'image"
            )
        
        # Si aucun type de détection n'est spécifié, retourner simplement le chemin de l'image
        if not request.detection_types:
            return {
                "success": True,
                "image_path": image_path
            }
        
        # Sinon, traiter l'image
        process_request = ImageProcessRequest(
            image_path=image_path,
            detection_types=request.detection_types,
            send_to_mcp=request.send_to_mcp
        )
        
        results = await process_image(process_request)
        results["image_path"] = image_path
        
        return results
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la capture et du traitement de l'image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour obtenir une image
@app.get("/image/{image_id}")
async def get_image(image_id: str):
    """
    Récupère une image.
    
    Args:
        image_id: Identifiant de l'image (nom du fichier)
    
    Returns:
        Fichier image
    """
    global image_processor
    
    try:
        # Vérifier que le processeur d'images est initialisé
        if not image_processor:
            init_processor()
            if not image_processor:
                raise HTTPException(
                    status_code=500, 
                    detail="Erreur lors de l'initialisation du processeur d'images"
                )
        
        # Construire le chemin de l'image
        image_path = os.path.join(image_processor.images_dir, image_id)
        
        # Vérifier si l'image existe dans le répertoire images
        if not os.path.exists(image_path):
            # Vérifier dans le répertoire detected
            image_path = os.path.join(image_processor.detected_dir, image_id)
            
            if not os.path.exists(image_path):
                raise HTTPException(
                    status_code=404, 
                    detail=f"Image non trouvée: {image_id}"
                )
        
        return FileResponse(image_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route principale
@app.get("/")
async def root():
    """Page d'accueil du service de vision."""
    return {
        "name": "Service de Vision pour Robot Mignon",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Vérifier l'état du service"},
            {"path": "/process", "method": "POST", "description": "Traiter une image"},
            {"path": "/upload", "method": "POST", "description": "Traiter une image téléchargée"},
            {"path": "/capture", "method": "POST", "description": "Capturer une image depuis une caméra"},
            {"path": "/image/{image_id}", "method": "GET", "description": "Récupérer une image"}
        ],
        "detection_types": [
            {"name": "faces", "description": "Détection de visages"},
            {"name": "objects", "description": "Détection d'objets"},
            {"name": "emotions", "description": "Détection d'émotions"},
            {"name": "colors", "description": "Analyse des couleurs dominantes"},
            {"name": "movement", "description": "Détection de mouvements"},
            {"name": "qrcode", "description": "Détection de QR codes"}
        ]
    }

# Démarrage du serveur
if __name__ == "__main__":
    # Initialiser le processeur d'images
    init_processor()
    
    # Configurer le serveur Uvicorn
    host = os.environ.get("VISION_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("VISION_SERVICE_PORT", "8060"))
    
    # Démarrer le serveur
    logger.info(f"Démarrage du service de vision sur {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False
    ) 