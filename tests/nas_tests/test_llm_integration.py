import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json
# Remplacer l'import numpy par un mock
# import numpy as np

# Ajout du chemin racine du projet pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Création des mocks pour les dépendances externes
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()
sys.modules['langchain.embeddings'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()
# Mock pour numpy
sys.modules['numpy'] = MagicMock()
# Créer des fonctionnalités numpy nécessaires
mock_np = sys.modules['numpy']
mock_np.dot = lambda v1, v2: sum(a*b for a, b in zip(v1, v2))
mock_np.linalg = MagicMock()
mock_np.linalg.norm = lambda v: (sum(x*x for x in v))**0.5
mock_np.array = lambda x: x

# Import du gestionnaire de modèles LLM
from nas.llm.model_manager import LLMManager, get_llm_manager

class TestLLMIntegration(unittest.TestCase):
    def setUp(self):
        """Configuration avant chaque test."""
        # Patcher les imports pour les tests
        self.huggingface_patcher = patch('nas.llm.model_manager.AutoModelForCausalLM')
        self.tokenizer_patcher = patch('nas.llm.model_manager.AutoTokenizer')
        self.embeddings_patcher = patch('nas.llm.model_manager.HuggingFaceEmbeddings')
        self.llama_patcher = patch('nas.llm.model_manager.Llama')
        
        # Démarrer les patchers
        self.mock_huggingface = self.huggingface_patcher.start()
        self.mock_tokenizer = self.tokenizer_patcher.start()
        self.mock_embeddings = self.embeddings_patcher.start()
        self.mock_llama = self.llama_patcher.start()
        
        # Configurer les mocks
        self.mock_model = MagicMock()
        self.mock_tokenizer_instance = MagicMock()
        self.mock_embedder = MagicMock()
        self.mock_llama_instance = MagicMock()
        
        self.mock_huggingface.from_pretrained.return_value = self.mock_model
        self.mock_tokenizer.from_pretrained.return_value = self.mock_tokenizer_instance
        self.mock_embeddings.return_value = self.mock_embedder
        self.mock_llama.return_value = self.mock_llama_instance
        
        # Configurer le mock pour l'embedding
        self.mock_embedder.embed_documents.return_value = [
            [0.1, 0.2, 0.3] * 128,  # Vecteur 384D pour le premier document
            [0.2, 0.3, 0.4] * 128   # Vecteur 384D pour le deuxième document
        ]
        
        # Configurer le mock pour la génération de texte
        self.mock_llama_instance.return_value = {
            "choices": [{"text": "Réponse générée par le modèle"}]
        }
        
        # Patcher os.path.exists pour le test du chargement de modèle
        self.path_exists_patcher = patch('os.path.exists')
        self.mock_path_exists = self.path_exists_patcher.start()
        self.mock_path_exists.return_value = True
        
        # Patcher os.environ.get pour contrôler les variables d'environnement
        self.env_patcher = patch('os.environ.get')
        self.mock_env = self.env_patcher.start()
        self.mock_env.side_effect = lambda key, default=None: {
            "LLM_MODEL_PATH": "./models",
            "LLM_ENGINE": "llama3",
            "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
        }.get(key, default)
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        self.huggingface_patcher.stop()
        self.tokenizer_patcher.stop()
        self.embeddings_patcher.stop()
        self.llama_patcher.stop()
        self.path_exists_patcher.stop()
        self.env_patcher.stop()
    
    def test_llm_manager_initialization(self):
        """Test de l'initialisation du gestionnaire de modèles."""
        # Créer une instance du gestionnaire
        llm = LLMManager(model_path="./models")
        
        # Vérifier que les modèles sont chargés correctement
        self.mock_embeddings.assert_called_once()
        self.mock_llama.assert_called_once()
        
        # Vérifier que les attributs ont été correctement définis
        self.assertEqual(llm.model_path, "./models")
        self.assertEqual(llm.engine, "llama3")
        self.assertEqual(llm.embedding_model, "sentence-transformers/all-MiniLM-L6-v2")
        self.assertIsNotNone(llm.embedder)
        self.assertIsNotNone(llm.llama_model)
    
    def test_llm_manager_huggingface_initialization(self):
        """Test de l'initialisation du gestionnaire avec HuggingFace."""
        # Modifier le mock pour simuler l'engine huggingface
        self.mock_env.side_effect = lambda key, default=None: {
            "LLM_MODEL_PATH": "./models",
            "LLM_ENGINE": "huggingface",
            "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
        }.get(key, default)
        
        # Créer une instance du gestionnaire
        llm = LLMManager(model_path="./models")
        
        # Vérifier que les bons modèles sont chargés
        self.mock_huggingface.from_pretrained.assert_called_once()
        self.mock_tokenizer.from_pretrained.assert_called_once()
        self.mock_embeddings.assert_called_once()
        
        # Vérifier que les attributs sont corrects
        self.assertEqual(llm.engine, "huggingface")
        self.assertIsNotNone(llm.model)
        self.assertIsNotNone(llm.tokenizer)
        self.assertIsNotNone(llm.embedder)
    
    def test_generate_text_llama(self):
        """Test de la génération de texte avec LLAMA."""
        # Configurer le mock pour la génération
        self.mock_llama_instance.return_value = {
            "choices": [{"text": "Réponse générée par le modèle LLAMA"}]
        }
        
        # Créer l'instance
        llm = LLMManager()
        
        # Tester la génération
        result = llm.generate_text("Prompt de test", max_tokens=100, temperature=0.7)
        
        # Vérifier le résultat
        self.assertEqual(result, "Réponse générée par le modèle LLAMA")
        
        # Vérifier que la méthode a été appelée avec les bons arguments
        self.mock_llama_instance.assert_called_once()
        call_args = self.mock_llama_instance.call_args[0][0]
        self.assertIn("<|begin_of_text|><|user|>", call_args)
        self.assertIn("Prompt de test", call_args)
    
    def test_get_embeddings(self):
        """Test de l'obtention des embeddings."""
        # Configurer le mock
        self.mock_embedder.embed_documents.return_value = [
            [0.1, 0.2, 0.3] * 128,  # 384D vector
            [0.4, 0.5, 0.6] * 128   # 384D vector
        ]
        
        # Créer l'instance
        llm = LLMManager()
        
        # Tester avec une chaîne
        single_result = llm.get_embeddings("Texte de test")
        self.assertEqual(len(single_result), 1)
        self.assertEqual(len(single_result[0]), 384)
        
        # Tester avec une liste
        multi_result = llm.get_embeddings(["Texte 1", "Texte 2"])
        self.assertEqual(len(multi_result), 2)
        self.assertEqual(len(multi_result[0]), 384)
        self.assertEqual(len(multi_result[1]), 384)
        
        # Vérifier les appels
        self.mock_embedder.embed_documents.assert_called()
    
    def test_semantic_search(self):
        """Test de la recherche sémantique."""
        # Configurer des embeddings qui produiront des similarités prévisibles
        self.mock_embedder.embed_documents.side_effect = lambda texts: [
            [0.9, 0.1, 0.1] * 128 if i == 0 else  # Query embedding
            [0.9, 0.1, 0.1] * 128 if i == 1 else  # Very similar to query (doc 0)
            [0.5, 0.5, 0.5] * 128 if i == 2 else  # Somewhat similar (doc 1)
            [0.1, 0.9, 0.9] * 128                 # Not similar (doc 2)
            for i in range(len(texts))
        ]
        
        # Créer l'instance
        llm = LLMManager()
        
        # Documents de test
        documents = [
            "Document très similaire à la requête",
            "Document moyennement similaire",
            "Document pas du tout similaire"
        ]
        
        # Effectuer la recherche
        results = llm.semantic_search("Requête de test", documents, top_k=2)
        
        # Vérifier les résultats (les indices devraient être [0, 1] car ce sont les plus similaires)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], 0)  # Premier résultat = document 0
        self.assertEqual(results[1][0], 1)  # Deuxième résultat = document 1
        
        # Vérifier que les scores sont dans l'ordre décroissant
        self.assertGreater(results[0][1], results[1][1])
    
    def test_analyze_sensors(self):
        """Test de l'analyse des données de capteurs."""
        # Configurer le mock pour retourner une réponse JSON
        mock_json_response = """
        {
          "interpretation": "Le robot détecte une présence humaine",
          "suggested_actions": ["sourire", "saluer"],
          "emotional_response": {
            "emotion": "joie", 
            "intensity": 75,
            "justification": "Une interaction humaine positive"
          }
        }
        """
        
        # Faire en sorte que generate_text retourne cette réponse
        llm = LLMManager()
        llm.generate_text = MagicMock(return_value=mock_json_response)
        
        # Données de test
        sensor_data = {"toucher": {"is_touched": True}}
        emotional_state = {"type": "neutre", "intensity": 50}
        
        # Analyser les données
        result = llm.analyze_sensors(sensor_data, emotional_state)
        
        # Vérifier le résultat
        self.assertIn("interpretation", result)
        self.assertEqual(result["interpretation"], "Le robot détecte une présence humaine")
        self.assertIn("suggested_actions", result)
        self.assertEqual(len(result["suggested_actions"]), 2)
        self.assertIn("emotional_response", result)
        self.assertEqual(result["emotional_response"]["emotion"], "joie")
        
        # Vérifier que generate_text a été appelé
        llm.generate_text.assert_called_once()
    
    def test_get_llm_manager(self):
        """Test de la fonction singleton get_llm_manager."""
        # Obtenir deux instances
        manager1 = get_llm_manager()
        manager2 = get_llm_manager()
        
        # Vérifier que c'est bien la même instance (singleton)
        self.assertIs(manager1, manager2)
        
        # Vérifier que c'est bien une instance de LLMManager
        self.assertIsInstance(manager1, LLMManager)

if __name__ == "__main__":
    unittest.main()
