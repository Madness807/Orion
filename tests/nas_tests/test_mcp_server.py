import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os
from typing import Dict, List, Any, Optional

# Ajout du chemin racine du projet pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Créer des modèles Pydantic simplifiés pour les tests
from pydantic import BaseModel, Field

# Modèles simplifiés pour remplacer les imports
class SensorMCPMessage(BaseModel):
    robot_id: str
    timestamp: str
    sensors: Dict[str, Any]

class EmotionalMCPMessage(BaseModel):
    robot_id: str
    timestamp: str
    emotion: Dict[str, Any]

class RobotCommand(BaseModel):
    type: str
    payload: Dict[str, Any]

class MCPResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Patcher les modules
sys.modules['schemas'] = MagicMock()
sys.modules['schemas.mcp_schemas'] = MagicMock()
sys.modules['context_manager'] = MagicMock()

# Remplacer les classes dans le module mocké
sys.modules['schemas.mcp_schemas'].SensorMCPMessage = SensorMCPMessage
sys.modules['schemas.mcp_schemas'].EmotionalMCPMessage = EmotionalMCPMessage
sys.modules['schemas.mcp_schemas'].RobotCommand = RobotCommand
sys.modules['schemas.mcp_schemas'].MCPResponse = MCPResponse

# Configurer le mock du gestionnaire de contexte
mock_context_manager = MagicMock()
sys.modules['context_manager'].get_context_manager = mock_context_manager

# Import du serveur MCP (après les patches)
from nas.serveur_mcp.mcp_server import app

class TestMCPServer(unittest.TestCase):
    def setUp(self):
        """Configuration avant chaque test."""
        # Création d'un client de test pour l'API FastAPI
        from fastapi.testclient import TestClient
        self.client = TestClient(app)
        
        # Setup du mock pour le gestionnaire de contexte
        self.context_patcher = patch('nas.serveur_mcp.mcp_server.get_context_manager')
        self.mock_context = self.context_patcher.start()
        
        # Création d'un mock pour le gestionnaire de contexte
        self.mock_context_instance = MagicMock()
        self.mock_context.return_value = self.mock_context_instance
        
    def tearDown(self):
        """Nettoyage après chaque test."""
        self.context_patcher.stop()
    
    def test_ping(self):
        """Test de la route ping."""
        response = self.client.get("/api/ping")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("timestamp", data)
    
    def test_receive_sensor_data(self):
        """Test de la route pour recevoir les données des capteurs."""
        # Configuration du mock pour retourner une réponse valide
        self.mock_context_instance.process_sensor_data.return_value = {
            "success": True,
            "message": "Données traitées avec succès",
            "analysis": {"interpretation": "Test d'interprétation"},
            "commands": [{"type": "test", "payload": {}}]
        }
        
        # Données de test pour la requête
        sensor_data = {
            "robot_id": "test_robot",
            "timestamp": "2025-04-04T12:00:00Z",
            "sensors": {
                "toucher": {"is_touched": False, "values": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]},
                "proprio": {"position": {"x": 0, "y": 0, "z": 0}, "orientation": {"roll": 0, "pitch": 0, "yaw": 0}}
            }
        }
        
        # Envoi de la requête
        response = self.client.post("/api/sensors", json=sensor_data)
        
        # Vérification de la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Données traitées avec succès")
        self.assertIn("data", data)
        self.assertIn("analysis", data["data"])
        self.assertIn("commands", data["data"])
        
        # Vérification que la méthode a été appelée avec les bonnes données
        self.mock_context_instance.process_sensor_data.assert_called_once()
    
    def test_receive_emotional_state(self):
        """Test de la route pour recevoir l'état émotionnel."""
        # Configuration du mock pour retourner une réponse valide
        self.mock_context_instance.process_emotional_state.return_value = {
            "success": True,
            "message": "État émotionnel traité avec succès",
            "emotion": {"type": "joie", "intensity": 75}
        }
        
        # Données de test pour la requête
        emotion_data = {
            "robot_id": "test_robot",
            "timestamp": "2025-04-04T12:00:00Z",
            "emotion": {
                "type": "joie",
                "intensity": 75,
                "trigger": "interaction_user"
            }
        }
        
        # Envoi de la requête
        response = self.client.post("/api/emotion", json=emotion_data)
        
        # Vérification de la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "État émotionnel traité avec succès")
        
        # Vérification que la méthode a été appelée avec les bonnes données
        self.mock_context_instance.process_emotional_state.assert_called_once()
    
    def test_get_commands(self):
        """Test de la route pour récupérer les commandes."""
        # Configuration du mock pour retourner des commandes valides
        mock_commands = [
            {"type": "expression", "payload": {"expression": "sourire", "duration": 5}},
            {"type": "mouvement", "payload": {"direction": "avant", "vitesse": 50}}
        ]
        self.mock_context_instance.get_commands.return_value = mock_commands
        
        # Envoi de la requête
        response = self.client.get("/api/commands?robot_id=test_robot")
        
        # Vérification de la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("commands", data["data"])
        self.assertEqual(len(data["data"]["commands"]), 2)
        
        # Vérification que la méthode a été appelée avec le bon ID
        self.mock_context_instance.get_commands.assert_called_once_with("test_robot")
    
    def test_send_command(self):
        """Test de la route pour envoyer une commande."""
        # Configuration du mock pour retourner un succès
        self.mock_context_instance.add_command.return_value = True
        
        # Données de test pour la commande
        command_data = {
            "type": "expression",
            "payload": {"expression": "surprise", "duration": 3}
        }
        
        # Envoi de la requête
        response = self.client.post("/api/send_command?robot_id=test_robot", json=command_data)
        
        # Vérification de la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("command", data["data"])
        
        # Vérification que la méthode a été appelée avec les bonnes données
        self.mock_context_instance.add_command.assert_called_once()
    
    def test_get_robot_status(self):
        """Test de la route pour obtenir l'état du robot."""
        # Configuration du mock pour retourner un état robot valide
        self.mock_context_instance.robot_id = "test_robot"
        self.mock_context_instance.current_context = {
            "sensors": {"toucher": {"is_touched": False}},
            "emotion": {"type": "curiosité", "intensity": 60},
            "recent_events": ["activation", "détection_utilisateur"],
            "last_interaction": "2025-04-04T11:55:00Z"
        }
        
        # Envoi de la requête
        response = self.client.get("/api/robot_status/test_robot")
        
        # Vérification de la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("sensors", data["data"])
        self.assertIn("emotion", data["data"])
        self.assertIn("recent_events", data["data"])
        self.assertIn("last_interaction", data["data"])
    
    def test_root(self):
        """Test de la route principale."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "online")
        self.assertIn("endpoints", data)

if __name__ == "__main__":
    unittest.main()
