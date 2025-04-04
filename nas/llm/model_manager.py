import os
import torch
import json
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.embeddings import HuggingFaceEmbeddings
from llama_cpp import Llama
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMManager:
    """Gestionnaire pour les modèles de langage large (LLM) et les embeddings."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialise le gestionnaire de modèles."""
        self.model_path = model_path or os.environ.get("LLM_MODEL_PATH", "./models")
        self.engine = os.environ.get("LLM_ENGINE", "llama3")
        self.embedding_model = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.model = None
        self.tokenizer = None
        self.embedder = None
        self.llama_model = None
        
        # Charger les modèles
        self._load_embedding_model()
        if self.engine == "llama3":
            self._load_llama_model()
        else:
            self._load_huggingface_model()
    
    def _load_huggingface_model(self):
        """Charge un modèle depuis HuggingFace."""
        try:
            logger.info(f"Chargement du modèle HuggingFace depuis {self.model_path}")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path, 
                torch_dtype=torch.float16, 
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            logger.info("Modèle HuggingFace chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle HuggingFace: {e}")
            raise
    
    def _load_llama_model(self):
        """Charge un modèle LLAMA.cpp."""
        try:
            model_file = os.path.join(self.model_path, "llama-3-8b-instruct.gguf")
            if not os.path.exists(model_file):
                logger.warning(f"Fichier de modèle {model_file} non trouvé. Vérifiez le chemin.")
                raise FileNotFoundError(f"Fichier de modèle {model_file} non trouvé")
            
            logger.info(f"Chargement du modèle LLAMA depuis {model_file}")
            self.llama_model = Llama(
                model_path=model_file,
                n_ctx=4096,  # Contexte de 4096 tokens
                n_threads=4   # Utilise 4 threads
            )
            logger.info("Modèle LLAMA chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle LLAMA: {e}")
            raise
    
    def _load_embedding_model(self):
        """Charge le modèle d'embedding."""
        try:
            logger.info(f"Chargement du modèle d'embedding {self.embedding_model}")
            self.embedder = HuggingFaceEmbeddings(model_name=self.embedding_model)
            logger.info("Modèle d'embedding chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle d'embedding: {e}")
            raise
    
    def generate_text(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Génère du texte à partir d'un prompt."""
        if self.engine == "llama3":
            return self._generate_with_llama(prompt, max_tokens, temperature)
        else:
            return self._generate_with_huggingface(prompt, max_tokens, temperature)
    
    def _generate_with_huggingface(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Génère du texte avec un modèle HuggingFace."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            gen_tokens = self.model.generate(
                inputs["input_ids"],
                max_length=inputs["input_ids"].shape[1] + max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return self.tokenizer.decode(gen_tokens[0], skip_special_tokens=True)[len(prompt):]
        except Exception as e:
            logger.error(f"Erreur lors de la génération de texte avec HuggingFace: {e}")
            return f"Erreur: {str(e)}"
    
    def _generate_with_llama(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Génère du texte avec le modèle LLAMA."""
        try:
            # Format adapté pour les modèles Llama 3
            formatted_prompt = f"<|begin_of_text|><|user|>\n{prompt}<|end_of_turn|>\n<|assistant|>\n"
            
            output = self.llama_model(
                formatted_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["<|end_of_turn|>", "<|end_of_text|>"]
            )
            
            # Extrait uniquement la réponse générée
            return output["choices"][0]["text"]
        except Exception as e:
            logger.error(f"Erreur lors de la génération de texte avec LLAMA: {e}")
            return f"Erreur: {str(e)}"
    
    def get_embeddings(self, text: Union[str, List[str]]) -> List[List[float]]:
        """Obtient les embeddings pour un texte ou une liste de textes."""
        try:
            if isinstance(text, str):
                text = [text]
            
            # Utilise le modèle d'embedding pour obtenir des vecteurs
            embeddings = self.embedder.embed_documents(text)
            return embeddings
        except Exception as e:
            logger.error(f"Erreur lors de la génération d'embeddings: {e}")
            # Retourne des vecteurs vides en cas d'erreur
            return [[0.0] * 384] * len(text)
    
    def semantic_search(self, query: str, documents: List[str], top_k: int = 3) -> List[Tuple[int, float]]:
        """Effectue une recherche sémantique dans une liste de documents."""
        if not documents:
            return []
        
        # Obtenir l'embedding de la requête
        query_embedding = self.get_embeddings(query)[0]
        
        # Obtenir les embeddings des documents
        doc_embeddings = self.get_embeddings(documents)
        
        # Calculer la similarité cosinus
        scores = []
        for i, doc_emb in enumerate(doc_embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_emb)
            scores.append((i, similarity))
        
        # Trier par score de similarité décroissant
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Retourner les top_k résultats
        return scores[:top_k]
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calcule la similarité cosinus entre deux vecteurs."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def analyze_sensors(self, sensor_data: Dict[str, Any], emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les données des capteurs et l'état émotionnel pour produire une interprétation."""
        # Convertir les données en texte pour le LLM
        sensor_text = json.dumps(sensor_data, indent=2)
        emotion_text = json.dumps(emotional_state, indent=2)
        
        prompt = f"""En tant qu'intelligence artificielle du robot mignon, analyse ces données de capteurs et l'état émotionnel actuel.
        
DONNÉES DES CAPTEURS:
{sensor_text}

ÉTAT ÉMOTIONNEL ACTUEL:
{emotion_text}

Réponds avec un JSON contenant:
1. Une interprétation de la situation actuelle
2. Des suggestions d'actions à entreprendre
3. Une nouvelle émotion recommandée si nécessaire (avec une justification)

Format attendu:
{{
  "interpretation": "Ce que le robot perçoit de son environnement",
  "suggested_actions": ["action1", "action2", ...],
  "emotional_response": {{
    "emotion": "joie/peur/etc",
    "intensity": 0-100,
    "justification": "Pourquoi cette émotion est appropriée"
  }}
}}
"""
        
        # Générer l'analyse
        response_text = self.generate_text(prompt, max_tokens=1024, temperature=0.3)
        
        # Essayer de parser le JSON de la réponse
        try:
            # Extraire uniquement la partie JSON de la réponse
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                analysis = json.loads(json_text)
                return analysis
            else:
                logger.warning(f"Impossible de trouver un JSON valide dans la réponse: {response_text}")
                return {
                    "interpretation": "Erreur d'analyse",
                    "suggested_actions": ["maintenir l'état actuel"],
                    "emotional_response": {
                        "emotion": "neutre",
                        "intensity": 50,
                        "justification": "Réponse par défaut suite à une erreur d'analyse"
                    }
                }
        except Exception as e:
            logger.error(f"Erreur lors du parsing de la réponse JSON: {e}\nRéponse: {response_text}")
            return {
                "interpretation": "Erreur d'analyse",
                "suggested_actions": ["maintenir l'état actuel"],
                "emotional_response": {
                    "emotion": "neutre",
                    "intensity": 50,
                    "justification": "Réponse par défaut suite à une erreur d'analyse"
                }
            }

# Instancier le gestionnaire de modèles
llm_manager = LLMManager()

def get_llm_manager() -> LLMManager:
    """Retourne l'instance du gestionnaire de modèles."""
    return llm_manager
