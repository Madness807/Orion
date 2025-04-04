import os
import sys
import uvicorn
import logging
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importation des modules de parole
from stt_engine import STTEngine, STTEngineType
from tts_engine import TTSEngine, TTSEngineType

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("speech_service.log")
    ]
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Service de Parole pour Robot Mignon",
    description="API pour la reconnaissance et la synthèse vocale du robot mignon",
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

# Modèle pour la synthèse vocale
class TextToSpeechRequest(BaseModel):
    text: str
    language: Optional[str] = "fr"
    engine: Optional[str] = "gtts"
    play_audio: Optional[bool] = False

# Modèle pour la reconnaissance vocale
class SpeechToTextRequest(BaseModel):
    audio_file: Optional[str] = None
    duration: Optional[int] = 5
    language: Optional[str] = "fr-FR"
    engine: Optional[str] = "vosk"
    send_to_mcp: Optional[bool] = True

# Instances des moteurs
tts_engine = None
stt_engine = None

# État de l'écoute continue
continuous_listening = False

def init_engines():
    """Initialise les moteurs de parole."""
    global tts_engine, stt_engine
    
    # Initialiser le moteur TTS par défaut
    default_tts_engine = os.environ.get("DEFAULT_TTS_ENGINE", "gtts")
    default_tts_language = os.environ.get("DEFAULT_TTS_LANGUAGE", "fr")
    
    try:
        tts_engine = TTSEngine(
            engine_type=TTSEngineType(default_tts_engine),
            language=default_tts_language
        )
        logger.info(f"Moteur TTS initialisé: {default_tts_engine}, langue: {default_tts_language}")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du moteur TTS: {e}")
        tts_engine = None
    
    # Initialiser le moteur STT par défaut
    default_stt_engine = os.environ.get("DEFAULT_STT_ENGINE", "vosk")
    default_stt_language = os.environ.get("DEFAULT_STT_LANGUAGE", "fr-FR")
    
    try:
        stt_engine = STTEngine(
            engine_type=STTEngineType(default_stt_engine),
            language=default_stt_language
        )
        logger.info(f"Moteur STT initialisé: {default_stt_engine}, langue: {default_stt_language}")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du moteur STT: {e}")
        stt_engine = None

# Route pour vérifier l'état du service
@app.get("/health")
async def health_check():
    """Vérifie l'état du service."""
    return {
        "status": "ok",
        "tts_engine": tts_engine.engine_type if tts_engine else "not_initialized",
        "stt_engine": stt_engine.engine_type if stt_engine else "not_initialized",
        "continuous_listening": continuous_listening
    }

# Route pour la synthèse vocale
@app.post("/tts")
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convertit du texte en parole.
    
    Args:
        request: Paramètres de la synthèse vocale
    
    Returns:
        Chemin du fichier audio généré
    """
    global tts_engine
    
    try:
        # Réinitialiser le moteur TTS si nécessaire
        if not tts_engine or tts_engine.engine_type != request.engine or tts_engine.language != request.language:
            tts_engine = TTSEngine(
                engine_type=TTSEngineType(request.engine),
                language=request.language
            )
        
        # Synthétiser le texte
        audio_file = tts_engine.speak(request.text, play_audio=request.play_audio)
        
        if not audio_file:
            raise HTTPException(status_code=500, detail="Échec de la synthèse vocale")
        
        # Envoyer l'information au serveur MCP
        tts_engine.send_to_mcp(request.text, audio_file)
        
        return {
            "success": True,
            "message": "Texte synthétisé avec succès",
            "audio_file": audio_file,
            "text": request.text
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de la synthèse vocale: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour la reconnaissance vocale depuis un fichier
@app.post("/stt/file")
async def speech_to_text_file(request: SpeechToTextRequest):
    """
    Convertit de la parole en texte à partir d'un fichier audio.
    
    Args:
        request: Paramètres de la reconnaissance vocale
    
    Returns:
        Texte reconnu
    """
    global stt_engine
    
    try:
        # Vérifier que le fichier audio est spécifié
        if not request.audio_file:
            raise HTTPException(status_code=400, detail="Fichier audio non spécifié")
        
        # Vérifier que le fichier existe
        if not os.path.exists(request.audio_file):
            raise HTTPException(status_code=404, detail="Fichier audio non trouvé")
        
        # Réinitialiser le moteur STT si nécessaire
        if not stt_engine or stt_engine.engine_type != request.engine or stt_engine.language != request.language:
            stt_engine = STTEngine(
                engine_type=STTEngineType(request.engine),
                language=request.language
            )
        
        # Reconnaître la parole
        text = stt_engine.recognize_from_file(request.audio_file)
        
        if not text:
            logger.warning("Aucun texte reconnu")
            text = ""
        
        # Envoyer le texte au serveur MCP si demandé
        if request.send_to_mcp and text:
            stt_engine.send_to_mcp(text)
        
        return {
            "success": True,
            "message": "Parole reconnue avec succès" if text else "Aucun texte reconnu",
            "text": text,
            "audio_file": request.audio_file
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de la reconnaissance vocale: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour la reconnaissance vocale depuis le microphone
@app.post("/stt/mic")
async def speech_to_text_mic(request: SpeechToTextRequest):
    """
    Convertit de la parole en texte à partir du microphone.
    
    Args:
        request: Paramètres de la reconnaissance vocale
    
    Returns:
        Texte reconnu
    """
    global stt_engine
    
    try:
        # Réinitialiser le moteur STT si nécessaire
        if not stt_engine or stt_engine.engine_type != request.engine or stt_engine.language != request.language:
            stt_engine = STTEngine(
                engine_type=STTEngineType(request.engine),
                language=request.language
            )
        
        # Reconnaître la parole
        text = stt_engine.recognize_from_microphone(duration=request.duration)
        
        if not text:
            logger.warning("Aucun texte reconnu")
            text = ""
        
        # Envoyer le texte au serveur MCP si demandé
        if request.send_to_mcp and text:
            stt_engine.send_to_mcp(text)
        
        return {
            "success": True,
            "message": "Parole reconnue avec succès" if text else "Aucun texte reconnu",
            "text": text
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de la reconnaissance vocale: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Fonction de callback pour l'écoute continue
def continuous_listening_callback(text):
    """Fonction appelée lorsqu'une phrase est reconnue pendant l'écoute continue."""
    if text:
        logger.info(f"Texte reconnu: {text}")
        
        # Envoyer le texte au serveur MCP
        stt_engine.send_to_mcp(text)

# Route pour démarrer l'écoute continue
@app.post("/stt/listen/start")
async def start_listening(request: SpeechToTextRequest, background_tasks: BackgroundTasks):
    """
    Démarre l'écoute continue du microphone.
    
    Args:
        request: Paramètres de la reconnaissance vocale
    
    Returns:
        État de l'écoute continue
    """
    global stt_engine, continuous_listening
    
    try:
        # Vérifier si l'écoute continue est déjà active
        if continuous_listening:
            return {
                "success": False,
                "message": "L'écoute continue est déjà active"
            }
        
        # Réinitialiser le moteur STT si nécessaire
        if not stt_engine or stt_engine.engine_type != request.engine or stt_engine.language != request.language:
            stt_engine = STTEngine(
                engine_type=STTEngineType(request.engine),
                language=request.language
            )
        
        # Démarrer l'écoute continue
        continuous_listening = True
        background_tasks.add_task(
            stt_engine.start_continuous_listening,
            continuous_listening_callback
        )
        
        return {
            "success": True,
            "message": "Écoute continue démarrée",
            "listening": True
        }
    
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'écoute continue: {e}")
        continuous_listening = False
        raise HTTPException(status_code=500, detail=str(e))

# Route pour arrêter l'écoute continue
@app.post("/stt/listen/stop")
async def stop_listening():
    """
    Arrête l'écoute continue du microphone.
    
    Returns:
        État de l'écoute continue
    """
    global stt_engine, continuous_listening
    
    try:
        # Vérifier si l'écoute continue est active
        if not continuous_listening:
            return {
                "success": False,
                "message": "L'écoute continue n'est pas active"
            }
        
        # Arrêter l'écoute continue
        if stt_engine:
            stt_engine.stop_continuous_listening()
        
        continuous_listening = False
        
        return {
            "success": True,
            "message": "Écoute continue arrêtée",
            "listening": False
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de l'arrêt de l'écoute continue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route pour jouer une salutation
@app.post("/greet")
async def greet():
    """
    Joue une salutation aléatoire.
    
    Returns:
        Fichier audio de la salutation
    """
    global tts_engine
    
    try:
        if not tts_engine:
            init_engines()
            if not tts_engine:
                raise HTTPException(status_code=500, detail="Moteur TTS non initialisé")
        
        # Jouer une salutation
        audio_file = tts_engine.greet()
        
        if not audio_file:
            raise HTTPException(status_code=500, detail="Échec de la synthèse vocale")
        
        return {
            "success": True,
            "message": "Salutation jouée avec succès",
            "audio_file": audio_file
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de la salutation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Route principale
@app.get("/")
async def root():
    """Page d'accueil du service de parole."""
    return {
        "name": "Service de Parole pour Robot Mignon",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Vérifier l'état du service"},
            {"path": "/tts", "method": "POST", "description": "Convertir du texte en parole"},
            {"path": "/stt/file", "method": "POST", "description": "Convertir de la parole en texte (fichier)"},
            {"path": "/stt/mic", "method": "POST", "description": "Convertir de la parole en texte (microphone)"},
            {"path": "/stt/listen/start", "method": "POST", "description": "Démarrer l'écoute continue"},
            {"path": "/stt/listen/stop", "method": "POST", "description": "Arrêter l'écoute continue"},
            {"path": "/greet", "method": "POST", "description": "Jouer une salutation aléatoire"}
        ]
    }

# Démarrage du serveur
if __name__ == "__main__":
    # Initialiser les moteurs
    init_engines()
    
    # Configurer le serveur Uvicorn
    host = os.environ.get("SPEECH_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("SPEECH_SERVICE_PORT", "8050"))
    
    # Démarrer le serveur
    logger.info(f"Démarrage du service de parole sur {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False
    ) 