import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

# Ajouter les chemins pour l'importation des modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from memoire.db_manager import db_manager
from llm.model_manager import get_llm_manager

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContextManager:
    """
    Gestionnaire de contexte pour le robot mignon.
    
    Cette classe est responsable de:
    1. Traiter les données des capteurs entrantes
    2. Maintenir le contexte actuel du robot
    3. Générer des réponses basées sur le contexte et l'entrée
    4. Gérer la mémoire à court et long terme
    5. Intégrer le LLM pour l'analyse et la prise de décision
    """
    
    def __init__(self, robot_id: str = "MignonBot1"):
        """Initialise le gestionnaire de contexte."""
        self.robot_id = robot_id
        self.db = db_manager
        self.llm = get_llm_manager()
        
        # Contexte actuel
        self.current_context = {
            "sensors": {},
            "emotion": {
                "type": "neutre",
                "intensity": 50,
                "last_change": datetime.utcnow().isoformat()
            },
            "last_interaction": None,
            "recent_events": [],
            "pending_commands": []
        }
        
        # Charger le contexte initial depuis la base de données
        self._load_initial_context()
        
        logger.info(f"Gestionnaire de contexte initialisé pour le robot {robot_id}")
    
    def _load_initial_context(self):
        """Charge le contexte initial depuis la base de données."""
        try:
            # Charger les dernières données des capteurs
            recent_sensor_data = self.db.get_recent_sensor_data(self.robot_id, limit=1)
            if recent_sensor_data:
                self.current_context["sensors"] = recent_sensor_data[0].data
            
            # Charger l'état émotionnel actuel
            current_emotion = self.db.get_current_emotion(self.robot_id)
            if current_emotion:
                self.current_context["emotion"] = {
                    "type": current_emotion.emotion_type,
                    "intensity": current_emotion.intensity,
                    "last_change": current_emotion.timestamp.isoformat()
                }
            
            # Charger les événements récents
            recent_events = self.db.get_recent_events(self.robot_id, limit=5)
            self.current_context["recent_events"] = [
                {
                    "timestamp": event.timestamp.isoformat(),
                    "type": event.event_type,
                    "description": event.description,
                    "data": event.data
                }
                for event in recent_events
            ]
            
            # Charger les interactions récentes
            recent_interactions = self.db.get_recent_interactions(self.robot_id, limit=1)
            if recent_interactions:
                self.current_context["last_interaction"] = {
                    "timestamp": recent_interactions[0].timestamp.isoformat(),
                    "type": recent_interactions[0].interaction_type,
                    "content": recent_interactions[0].content
                }
            
            logger.info("Contexte initial chargé depuis la base de données")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du contexte initial: {e}")
            # Continuer avec le contexte par défaut
    
    def process_sensor_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite les données des capteurs entrantes.
        
        Args:
            sensor_data: Dictionnaire contenant les données des capteurs
            
        Returns:
            Dictionnaire contenant la réponse du système
        """
        try:
            # Enregistrer les données dans la base de données
            self.db.save_sensor_data(self.robot_id, sensor_data)
            
            # Mettre à jour le contexte actuel
            self.current_context["sensors"] = sensor_data
            
            # Analyser les données des capteurs avec le LLM
            analysis = self.llm.analyze_sensors(
                sensor_data, 
                self.current_context["emotion"]
            )
            
            # Journaliser l'analyse
            logger.info(f"Analyse des capteurs: {json.dumps(analysis, indent=2)}")
            
            # Traiter l'analyse pour générer des événements si nécessaire
            self._process_sensor_analysis(analysis)
            
            # Générer des commandes basées sur l'analyse
            commands = self._generate_commands(analysis)
            
            # Retourner la réponse
            return {
                "success": True,
                "message": "Données des capteurs traitées avec succès",
                "analysis": analysis,
                "commands": commands
            }
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données des capteurs: {e}")
            return {
                "success": False,
                "message": f"Erreur lors du traitement des données des capteurs: {str(e)}",
                "commands": []
            }
    
    def process_emotional_state(self, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite l'état émotionnel entrant.
        
        Args:
            emotional_state: Dictionnaire contenant l'état émotionnel
            
        Returns:
            Dictionnaire contenant la réponse du système
        """
        try:
            # Extraire les données
            emotion_type = emotional_state["type"]
            intensity = emotional_state["intensity"]
            duration = emotional_state["duration"]
            
            # Enregistrer l'état émotionnel dans la base de données
            self.db.save_emotional_state(self.robot_id, emotion_type, intensity, duration)
            
            # Mettre à jour le contexte actuel
            self.current_context["emotion"] = {
                "type": emotion_type,
                "intensity": intensity,
                "last_change": datetime.utcnow().isoformat()
            }
            
            # Enregistrer un événement pour les changements d'émotion significatifs
            if intensity > 70:
                self.db.save_event(
                    self.robot_id,
                    "emotion_change",
                    f"Changement significatif d'émotion : {emotion_type} (intensité: {intensity})",
                    {"emotion": emotion_type, "intensity": intensity}
                )
                
                # Ajouter à la mémoire à long terme si l'émotion est forte
                if intensity > 85:
                    self.db.save_memory(
                        self.robot_id,
                        "emotional_event",
                        f"J'ai ressenti une forte émotion de {emotion_type} avec une intensité de {intensity}.",
                        importance=intensity
                    )
            
            # Retourner la réponse
            return {
                "success": True,
                "message": "État émotionnel traité avec succès",
                "emotion": {
                    "type": emotion_type,
                    "intensity": intensity,
                    "acknowledged": True
                }
            }
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'état émotionnel: {e}")
            return {
                "success": False,
                "message": f"Erreur lors du traitement de l'état émotionnel: {str(e)}"
            }
    
    def get_commands(self, robot_id: str) -> List[Dict[str, Any]]:
        """
        Récupère les commandes en attente pour le robot.
        
        Args:
            robot_id: Identifiant du robot
            
        Returns:
            Liste des commandes en attente
        """
        if robot_id != self.robot_id:
            logger.warning(f"Tentative d'accès aux commandes pour un robot inconnu: {robot_id}")
            return []
        
        # Récupérer et vider la liste des commandes en attente
        commands = self.current_context["pending_commands"].copy()
        self.current_context["pending_commands"] = []
        
        return commands
    
    def _process_sensor_analysis(self, analysis: Dict[str, Any]):
        """
        Traite l'analyse des capteurs pour générer des événements.
        
        Args:
            analysis: Résultat de l'analyse des capteurs par le LLM
        """
        try:
            # Créer un événement à partir de l'interprétation
            if "interpretation" in analysis and analysis["interpretation"]:
                self.db.save_event(
                    self.robot_id,
                    "sensor_interpretation",
                    analysis["interpretation"],
                    {"raw_analysis": analysis}
                )
                
                # Mettre à jour la liste des événements récents dans le contexte
                self.current_context["recent_events"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "sensor_interpretation",
                    "description": analysis["interpretation"]
                })
                
                # Limiter à 5 événements récents
                if len(self.current_context["recent_events"]) > 5:
                    self.current_context["recent_events"] = self.current_context["recent_events"][-5:]
            
            # Analyser la réponse émotionnelle recommandée
            if "emotional_response" in analysis and analysis["emotional_response"]:
                emotional_response = analysis["emotional_response"]
                
                # Si la réponse émotionnelle est significativement différente de l'état actuel,
                # l'ajouter aux commandes en attente
                current_emotion = self.current_context["emotion"]["type"]
                current_intensity = self.current_context["emotion"]["intensity"]
                
                new_emotion = emotional_response.get("emotion", "neutre")
                new_intensity = emotional_response.get("intensity", 50)
                
                if new_emotion != current_emotion or abs(new_intensity - current_intensity) > 20:
                    # Ajouter la commande de changement d'émotion
                    self.current_context["pending_commands"].append({
                        "command_type": "emotion",
                        "emotion": {
                            "emotion": new_emotion,
                            "intensity": new_intensity
                        }
                    })
                    
                    logger.info(f"Nouvelle émotion suggérée: {new_emotion} (intensité: {new_intensity})")
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'analyse des capteurs: {e}")
    
    def _generate_commands(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Génère des commandes basées sur l'analyse des capteurs.
        
        Args:
            analysis: Résultat de l'analyse des capteurs par le LLM
            
        Returns:
            Liste des commandes générées
        """
        commands = []
        
        try:
            # Traiter les actions suggérées
            if "suggested_actions" in analysis and analysis["suggested_actions"]:
                for action in analysis["suggested_actions"]:
                    # Traiter chaque action suggérée
                    if "avancer" in action.lower() or "forward" in action.lower():
                        commands.append({
                            "command_type": "movement",
                            "movement": {
                                "direction": "forward",
                                "speed": 60,
                                "duration": 2000  # 2 secondes
                            }
                        })
                    elif "reculer" in action.lower() or "backward" in action.lower():
                        commands.append({
                            "command_type": "movement",
                            "movement": {
                                "direction": "backward",
                                "speed": 60,
                                "duration": 2000  # 2 secondes
                            }
                        })
                    elif "tourner" in action.lower() and "gauche" in action.lower() or "left" in action.lower():
                        commands.append({
                            "command_type": "movement",
                            "movement": {
                                "direction": "left",
                                "speed": 50,
                                "duration": 1000  # 1 seconde
                            }
                        })
                    elif "tourner" in action.lower() and "droite" in action.lower() or "right" in action.lower():
                        commands.append({
                            "command_type": "movement",
                            "movement": {
                                "direction": "right",
                                "speed": 50,
                                "duration": 1000  # 1 seconde
                            }
                        })
                    elif "arret" in action.lower() or "stop" in action.lower():
                        commands.append({
                            "command_type": "movement",
                            "movement": {
                                "direction": "stop",
                                "speed": 0
                            }
                        })
                    elif "bip" in action.lower() or "son" in action.lower() or "sound" in action.lower():
                        commands.append({
                            "command_type": "sound",
                            "sound": {
                                "frequency": 1000,  # 1 kHz
                                "duration": 500  # 0.5 seconde
                            }
                        })
            
            # Ajouter toutes les commandes au contexte
            self.current_context["pending_commands"].extend(commands)
            
            return commands
        except Exception as e:
            logger.error(f"Erreur lors de la génération de commandes: {e}")
            return []
    
    def add_interaction(self, interaction_type: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Ajoute une interaction à la base de données et au contexte.
        
        Args:
            interaction_type: Type d'interaction
            content: Contenu de l'interaction
            metadata: Métadonnées associées à l'interaction
            
        Returns:
            True si l'interaction a été ajoutée avec succès, False sinon
        """
        try:
            # Enregistrer l'interaction dans la base de données
            self.db.save_interaction(self.robot_id, interaction_type, content, metadata)
            
            # Mettre à jour le contexte
            self.current_context["last_interaction"] = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": interaction_type,
                "content": content
            }
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'une interaction: {e}")
            return False
    
    def add_command(self, command: Dict[str, Any]) -> bool:
        """
        Ajoute une commande à la liste des commandes en attente.
        
        Args:
            command: Commande à ajouter
            
        Returns:
            True si la commande a été ajoutée avec succès, False sinon
        """
        try:
            self.current_context["pending_commands"].append(command)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'une commande: {e}")
            return False

# Instancier le gestionnaire de contexte
context_manager = ContextManager(robot_id=os.environ.get("ROBOT_ID", "MignonBot1"))

def get_context_manager() -> ContextManager:
    """Retourne l'instance du gestionnaire de contexte."""
    return context_manager
