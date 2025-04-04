import os
import json
import logging
import tempfile
from typing import Optional, Dict, Any, List, Union
from enum import Enum
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import requests
import threading
import queue
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class STTEngineType(str, Enum):
    GOOGLE = "google"
    VOSK = "vosk"
    WHISPER = "whisper"
    SPHINX = "sphinx"

class STTEngine:
    """
    Moteur de reconnaissance vocale (Speech-to-Text).
    
    Cette classe permet de convertir la parole en texte en utilisant différents backends:
    - Google Speech Recognition (nécessite une connexion internet)
    - Vosk (hors ligne)
    - Whisper (hors ligne)
    - CMU Sphinx (hors ligne, moins précis mais léger)
    """
    
    def __init__(self, engine_type: STTEngineType = STTEngineType.VOSK, language: str = "fr-FR"):
        """
        Initialise le moteur de reconnaissance vocale.
        
        Args:
            engine_type: Type de moteur à utiliser
            language: Code de langue (fr-FR, en-US, etc.)
        """
        self.engine_type = engine_type
        self.language = language
        self.recognizer = sr.Recognizer()
        self.vosk_model = None
        self.recording_queue = queue.Queue()
        self.is_listening = False
        self.listen_thread = None
        
        # Paramètres d'enregistrement audio
        self.sample_rate = 16000
        self.channels = 1
        
        # Charger le modèle Vosk si nécessaire
        if engine_type == STTEngineType.VOSK:
            self._load_vosk_model()
        
        logger.info(f"Moteur STT initialisé avec {engine_type}, langue: {language}")
    
    def _load_vosk_model(self):
        """Charge le modèle Vosk pour la reconnaissance vocale hors ligne."""
        try:
            # Déterminer le chemin du modèle en fonction de la langue
            lang_code = self.language.split('-')[0].lower()
            model_path = os.path.join("/app/models/vosk", lang_code)
            
            if not os.path.exists(model_path):
                logger.warning(f"Modèle Vosk pour {lang_code} non trouvé, utilisation du français par défaut")
                model_path = "/app/models/vosk/fr"
            
            logger.info(f"Chargement du modèle Vosk depuis {model_path}")
            self.vosk_model = Model(model_path)
            logger.info("Modèle Vosk chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle Vosk: {e}")
            self.vosk_model = None
    
    def recognize_from_file(self, audio_file: str) -> Optional[str]:
        """
        Reconnaît la parole à partir d'un fichier audio.
        
        Args:
            audio_file: Chemin vers le fichier audio (WAV, FLAC, etc.)
            
        Returns:
            Texte reconnu ou None en cas d'erreur
        """
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                
                if self.engine_type == STTEngineType.GOOGLE:
                    return self.recognizer.recognize_google(audio_data, language=self.language)
                
                elif self.engine_type == STTEngineType.SPHINX:
                    return self.recognizer.recognize_sphinx(audio_data, language=self.language)
                
                elif self.engine_type == STTEngineType.VOSK:
                    if self.vosk_model is None:
                        self._load_vosk_model()
                        if self.vosk_model is None:
                            return None
                    
                    # Convertir l'audio pour Vosk
                    data, samplerate = sf.read(audio_file)
                    if len(data.shape) > 1:
                        data = data[:, 0]  # Prendre seulement le premier canal si stéréo
                    
                    rec = KaldiRecognizer(self.vosk_model, samplerate)
                    rec.AcceptWaveform(data.tobytes())
                    result = json.loads(rec.FinalResult())
                    return result.get("text", "")
                
                elif self.engine_type == STTEngineType.WHISPER:
                    # Pour Whisper, utiliser la bibliothèque transformers
                    from transformers import pipeline
                    
                    # Charger le pipeline de transcription de Whisper
                    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small")
                    result = transcriber(audio_file)
                    return result.get("text", "")
                
                else:
                    logger.error(f"Moteur STT non reconnu: {self.engine_type}")
                    return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la reconnaissance vocale: {e}")
            return None
    
    def recognize_from_microphone(self, duration: int = 5) -> Optional[str]:
        """
        Reconnaît la parole à partir du microphone.
        
        Args:
            duration: Durée d'enregistrement en secondes
            
        Returns:
            Texte reconnu ou None en cas d'erreur
        """
        try:
            # Enregistrer l'audio dans un fichier temporaire
            fd, temp_file = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            
            logger.info(f"Enregistrement audio pendant {duration} secondes...")
            
            # Enregistrer depuis le microphone
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32'
            )
            sd.wait()
            
            # Normaliser et sauvegarder l'audio
            recording = recording / np.max(np.abs(recording))
            sf.write(temp_file, recording, self.sample_rate)
            
            # Reconnaître la parole
            result = self.recognize_from_file(temp_file)
            
            # Supprimer le fichier temporaire
            os.unlink(temp_file)
            
            return result
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement ou de la reconnaissance: {e}")
            return None
    
    def start_continuous_listening(self, callback):
        """
        Démarre l'écoute continue du microphone.
        
        Args:
            callback: Fonction à appeler lorsqu'une phrase est reconnue
        """
        if self.is_listening:
            logger.warning("L'écoute continue est déjà active")
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._continuous_listening_thread, args=(callback,))
        self.listen_thread.daemon = True
        self.listen_thread.start()
        logger.info("Écoute continue démarrée")
    
    def stop_continuous_listening(self):
        """Arrête l'écoute continue."""
        self.is_listening = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2.0)
        logger.info("Écoute continue arrêtée")
    
    def _continuous_listening_thread(self, callback):
        """
        Thread d'écoute continue.
        
        Cette fonction enregistre le son en continu et détecte les silences
        pour segmenter la parole en phrases.
        """
        try:
            # Charger le reconnaisseur Vosk (plus adapté à l'écoute en continu)
            if self.vosk_model is None:
                self._load_vosk_model()
            
            recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
            
            def audio_callback(indata, frames, time, status):
                """Callback appelé pour chaque bloc audio."""
                if status:
                    logger.warning(f"Statut audio: {status}")
                
                # Ajouter les données audio à la file d'attente
                if self.is_listening:
                    self.recording_queue.put(bytes(indata))
            
            # Démarrer le flux audio
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                channels=self.channels,
                dtype='int16',
                callback=audio_callback
            ):
                logger.info("Flux audio démarré, en attente de parole...")
                
                while self.is_listening:
                    # Récupérer les données audio
                    if not self.recording_queue.empty():
                        data = self.recording_queue.get()
                        
                        # Traiter les données avec Vosk
                        if recognizer.AcceptWaveform(data):
                            result = json.loads(recognizer.Result())
                            text = result.get("text", "").strip()
                            
                            # Appeler le callback si du texte a été reconnu
                            if text:
                                callback(text)
                    
                    # Pause pour économiser le CPU
                    time.sleep(0.1)
        
        except Exception as e:
            logger.error(f"Erreur dans le thread d'écoute continue: {e}")
            self.is_listening = False
    
    def send_to_mcp(self, text: str, mcp_url: Optional[str] = None) -> bool:
        """
        Envoie le texte reconnu au serveur MCP.
        
        Args:
            text: Texte reconnu à envoyer
            mcp_url: URL du serveur MCP (optionnel, sinon utilise la variable d'environnement)
            
        Returns:
            True si l'envoi a réussi, False sinon
        """
        try:
            # Récupérer l'URL du serveur MCP
            if mcp_url is None:
                mcp_url = os.environ.get("MCP_SERVER_URL", "http://mcp_server:8080")
            
            # Préparer les données à envoyer
            payload = {
                "robot_id": os.environ.get("ROBOT_ID", "MignonBot1"),
                "interaction_type": "voice_command",
                "content": text,
                "metadata": {
                    "source": "speech_recognition",
                    "engine": self.engine_type,
                    "language": self.language,
                    "timestamp": time.time()
                }
            }
            
            # Envoyer la requête au serveur MCP
            url = f"{mcp_url}/api/interaction"
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info(f"Texte envoyé avec succès au serveur MCP: '{text}'")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi au serveur MCP: {response.status_code}, {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi au serveur MCP: {e}")
            return False
