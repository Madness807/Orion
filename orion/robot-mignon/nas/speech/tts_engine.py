import os
import logging
import tempfile
from typing import Optional, Dict, Any, List, Union
from enum import Enum
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import gtts
import pyttsx3
from pathlib import Path
import requests
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSEngineType(str, Enum):
    GTTS = "gtts"      # Google Text-to-Speech (nécessite internet)
    PYTTSX3 = "pyttsx3"  # Synthèse vocale locale
    ESPEAK = "espeak"   # Espeak-ng (synthèse vocale légère)
    COQUI = "coqui"     # Coqui TTS (nécessite des modèles préentraînés)

class TTSEngine:
    """
    Moteur de synthèse vocale (Text-to-Speech).
    
    Cette classe permet de convertir du texte en parole en utilisant différents backends:
    - Google TTS (nécessite une connexion internet)
    - PyTTSX3 (local, Windows/Mac/Linux)
    - eSpeak-ng (local, multiplateforme)
    - Coqui TTS (local, qualité élevée mais nécessite des ressources)
    """
    
    def __init__(self, engine_type: TTSEngineType = TTSEngineType.GTTS, language: str = "fr"):
        """
        Initialise le moteur de synthèse vocale.
        
        Args:
            engine_type: Type de moteur à utiliser
            language: Code de langue (fr, en, etc.)
        """
        self.engine_type = engine_type
        self.language = language
        
        # Dossier pour sauvegarder les fichiers audio générés
        self.output_dir = os.environ.get("TTS_OUTPUT_DIR", "/app/data/synthesized")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialiser le moteur local si nécessaire
        self.local_engine = None
        if engine_type == TTSEngineType.PYTTSX3:
            self._init_pyttsx3()
        elif engine_type == TTSEngineType.COQUI:
            self._init_coqui()
        
        logger.info(f"Moteur TTS initialisé avec {engine_type}, langue: {language}")
    
    def _init_pyttsx3(self):
        """Initialise le moteur pyttsx3."""
        try:
            self.local_engine = pyttsx3.init()
            
            # Configurer la voix en fonction de la langue
            voices = self.local_engine.getProperty('voices')
            for voice in voices:
                if self.language in voice.id.lower():
                    self.local_engine.setProperty('voice', voice.id)
                    break
            
            # Configurer le débit de parole (mots par minute)
            self.local_engine.setProperty('rate', 150)
            
            logger.info("Moteur pyttsx3 initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du moteur pyttsx3: {e}")
            self.local_engine = None
    
    def _init_coqui(self):
        """Initialise le moteur Coqui TTS."""
        try:
            from TTS.api import TTS
            
            # Charger le modèle Coqui TTS approprié pour la langue
            model_name = "tts_models/fr/mai/tacotron2-DDC"
            if self.language == "en":
                model_name = "tts_models/en/ljspeech/tacotron2-DDC"
            
            logger.info(f"Chargement du modèle Coqui TTS: {model_name}")
            self.local_engine = TTS(model_name)
            logger.info("Moteur Coqui TTS initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du moteur Coqui TTS: {e}")
            self.local_engine = None
    
    def synthesize(self, text: str, output_file: Optional[str] = None) -> Optional[str]:
        """
        Synthétise du texte en parole et sauvegarde le résultat dans un fichier.
        
        Args:
            text: Texte à synthétiser
            output_file: Chemin du fichier de sortie (optionnel)
            
        Returns:
            Chemin du fichier audio généré ou None en cas d'erreur
        """
        try:
            # Générer un nom de fichier si non spécifié
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(self.output_dir, f"tts_{timestamp}.wav")
            
            # S'assurer que le répertoire de sortie existe
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Synthétiser le texte avec le moteur approprié
            if self.engine_type == TTSEngineType.GTTS:
                self._synthesize_gtts(text, output_file)
            elif self.engine_type == TTSEngineType.PYTTSX3:
                self._synthesize_pyttsx3(text, output_file)
            elif self.engine_type == TTSEngineType.ESPEAK:
                self._synthesize_espeak(text, output_file)
            elif self.engine_type == TTSEngineType.COQUI:
                self._synthesize_coqui(text, output_file)
            else:
                logger.error(f"Moteur TTS non reconnu: {self.engine_type}")
                return None
            
            logger.info(f"Texte synthétisé avec succès: '{text}' -> {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse vocale: {e}")
            return None
    
    def _synthesize_gtts(self, text: str, output_file: str):
        """Synthétise le texte avec Google TTS."""
        # Créer l'objet gTTS
        tts = gtts.gTTS(text=text, lang=self.language, slow=False)
        
        # Si le fichier demandé n'est pas un MP3, utiliser un fichier temporaire
        if not output_file.lower().endswith('.mp3'):
            mp3_file = output_file + '.mp3'
            tts.save(mp3_file)
            
            # Convertir MP3 en WAV
            from pydub import AudioSegment
            sound = AudioSegment.from_mp3(mp3_file)
            sound.export(output_file, format="wav")
            
            # Supprimer le fichier MP3 temporaire
            os.unlink(mp3_file)
        else:
            # Sauvegarder directement en MP3
            tts.save(output_file)
    
    def _synthesize_pyttsx3(self, text: str, output_file: str):
        """Synthétise le texte avec pyttsx3."""
        if self.local_engine is None:
            self._init_pyttsx3()
            if self.local_engine is None:
                raise Exception("Impossible d'initialiser le moteur pyttsx3")
        
        # Sauvegarder la parole dans un fichier
        self.local_engine.save_to_file(text, output_file)
        self.local_engine.runAndWait()
    
    def _synthesize_espeak(self, text: str, output_file: str):
        """Synthétise le texte avec eSpeak-ng."""
        import subprocess
        
        # Construire la commande espeak-ng
        cmd = [
            "espeak-ng",
            "-v", self.language,
            "-w", output_file,
            "-s", "140",  # Vitesse de parole
            text
        ]
        
        # Exécuter la commande
        subprocess.run(cmd, check=True, capture_output=True)
    
    def _synthesize_coqui(self, text: str, output_file: str):
        """Synthétise le texte avec Coqui TTS."""
        if self.local_engine is None:
            self._init_coqui()
            if self.local_engine is None:
                raise Exception("Impossible d'initialiser le moteur Coqui TTS")
        
        # Synthétiser et sauvegarder
        self.local_engine.tts_to_file(text=text, file_path=output_file)
    
    def play(self, file_path: str) -> bool:
        """
        Joue un fichier audio.
        
        Args:
            file_path: Chemin du fichier audio à jouer
            
        Returns:
            True si la lecture a réussi, False sinon
        """
        try:
            # Charger le fichier audio
            data, samplerate = sf.read(file_path)
            
            # Lecture du son
            sd.play(data, samplerate)
            sd.wait()  # Attendre la fin de la lecture
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du fichier audio: {e}")
            return False
    
    def speak(self, text: str, play_audio: bool = True) -> Optional[str]:
        """
        Synthétise le texte en parole et le joue (optionnel).
        
        Args:
            text: Texte à synthétiser et à jouer
            play_audio: Indique si le son doit être joué immédiatement
            
        Returns:
            Chemin du fichier audio généré ou None en cas d'erreur
        """
        # Synthétiser le texte
        audio_file = self.synthesize(text)
        
        if audio_file and play_audio:
            # Jouer le son
            self.play(audio_file)
        
        return audio_file
    
    def greet(self) -> Optional[str]:
        """
        Génère une salutation aléatoire.
        
        Returns:
            Fichier audio de la salutation ou None en cas d'erreur
        """
        import random
        
        greetings = [
            "Bonjour, je suis MignonBot, votre robot de compagnie !",
            "Salut ! Comment allez-vous aujourd'hui ?",
            "Coucou ! Je suis content de vous voir !",
            "Bonjour ! Que puis-je faire pour vous aider ?",
            "Salutations humain ! Je suis à votre service."
        ]
        
        if self.language.startswith("en"):
            greetings = [
                "Hello, I am MignonBot, your companion robot!",
                "Hi! How are you today?",
                "Hey there! I'm happy to see you!",
                "Hello! What can I do to help you?",
                "Greetings human! I am at your service."
            ]
        
        greeting = random.choice(greetings)
        return self.speak(greeting)
    
    def send_to_mcp(self, text: str, audio_file: str, mcp_url: Optional[str] = None) -> bool:
        """
        Envoie l'information sur la synthèse vocale au serveur MCP.
        
        Args:
            text: Texte synthétisé
            audio_file: Chemin du fichier audio généré
            mcp_url: URL du serveur MCP (optionnel)
            
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
                "interaction_type": "speech_synthesis",
                "content": text,
                "metadata": {
                    "source": "text_to_speech",
                    "engine": self.engine_type,
                    "language": self.language,
                    "audio_file": os.path.basename(audio_file),
                    "timestamp": time.time()
                }
            }
            
            # Envoyer la requête au serveur MCP
            url = f"{mcp_url}/api/interaction"
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info(f"Information TTS envoyée avec succès au serveur MCP: '{text}'")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi au serveur MCP: {response.status_code}, {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi au serveur MCP: {e}")
            return False
