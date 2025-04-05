from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import json
from sqlalchemy.orm import Session

from nas.memoire.db_manager import LongTermMemory, db_manager


class MemoryModel:
    """
    Modèle pour gérer les souvenirs du robot. 
    Fournit une interface pour enregistrer, récupérer et manipuler les souvenirs.
    """
    
    def __init__(self, robot_id: str):
        """
        Initialise le modèle avec l'ID du robot.
        
        Args:
            robot_id: L'identifiant unique du robot
        """
        self.robot_id = robot_id
    
    def save_episodic_memory(self, content: str, importance: int = 50, 
                           metadata: Dict[str, Any] = None) -> LongTermMemory:
        """
        Enregistre un souvenir épisodique (événement vécu).
        
        Args:
            content: Le contenu textuel du souvenir
            importance: Score d'importance (0-100)
            metadata: Métadonnées additionnelles
            
        Returns:
            L'objet mémoire créé
        """
        return db_manager.save_memory(
            robot_id=self.robot_id,
            memory_type="episodic",
            content=content,
            importance=importance,
            embedding=None  # À implémenter: convertir le contenu en embedding vectoriel
        )
    
    def save_semantic_memory(self, content: str, importance: int = 50) -> LongTermMemory:
        """
        Enregistre un souvenir sémantique (fait, connaissance).
        
        Args:
            content: Le contenu textuel du souvenir
            importance: Score d'importance (0-100)
            
        Returns:
            L'objet mémoire créé
        """
        return db_manager.save_memory(
            robot_id=self.robot_id,
            memory_type="semantic",
            content=content,
            importance=importance
        )
    
    def save_procedural_memory(self, content: str, importance: int = 50) -> LongTermMemory:
        """
        Enregistre un souvenir procédural (comment faire quelque chose).
        
        Args:
            content: Description de la procédure
            importance: Score d'importance (0-100)
            
        Returns:
            L'objet mémoire créé
        """
        return db_manager.save_memory(
            robot_id=self.robot_id,
            memory_type="procedural",
            content=content,
            importance=importance
        )
    
    def get_memories(self, memory_type: Optional[str] = None, 
                    limit: int = 10, 
                    min_importance: int = 0) -> List[LongTermMemory]:
        """
        Récupère les souvenirs du robot, filtrés par type et importance.
        
        Args:
            memory_type: Type de souvenir ("episodic", "semantic", "procedural")
            limit: Nombre maximum de souvenirs à récupérer
            min_importance: Importance minimale des souvenirs
            
        Returns:
            Liste des souvenirs correspondant aux critères
        """
        db = db_manager.get_session()
        try:
            query = db.query(LongTermMemory).filter(
                LongTermMemory.robot_id == self.robot_id,
                LongTermMemory.importance >= min_importance
            )
            
            if memory_type:
                query = query.filter(LongTermMemory.memory_type == memory_type)
                
            return query.order_by(LongTermMemory.importance.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_relevant_memories(self, query_text: str, limit: int = 5) -> List[LongTermMemory]:
        """
        Récupère les souvenirs les plus pertinents par rapport à un texte.
        Note: Cette fonction est à améliorer avec une recherche sémantique.
        
        Args:
            query_text: Texte de recherche
            limit: Nombre maximum de souvenirs à récupérer
            
        Returns:
            Liste des souvenirs les plus pertinents
        """
        # Version simple: recherche par mots-clés
        # À remplacer par une recherche sémantique avec embeddings
        db = db_manager.get_session()
        try:
            # Exemple basique: recherche de mots-clés dans le contenu
            words = query_text.lower().split()
            results = []
            
            # Récupérer tous les souvenirs et filtrer
            memories = db.query(LongTermMemory).filter(
                LongTermMemory.robot_id == self.robot_id
            ).all()
            
            for memory in memories:
                relevance = 0
                for word in words:
                    if word in memory.content.lower():
                        relevance += 1
                
                if relevance > 0:
                    results.append((memory, relevance))
            
            # Trier par pertinence et limiter les résultats
            results.sort(key=lambda x: x[1], reverse=True)
            return [memory for memory, _ in results[:limit]]
        finally:
            db.close()
    
    def forget_memory(self, memory_id: int) -> bool:
        """
        Supprime un souvenir spécifique.
        
        Args:
            memory_id: ID du souvenir à supprimer
            
        Returns:
            True si le souvenir a été supprimé, False sinon
        """
        db = db_manager.get_session()
        try:
            memory = db.query(LongTermMemory).filter(
                LongTermMemory.id == memory_id,
                LongTermMemory.robot_id == self.robot_id
            ).first()
            
            if memory:
                db.delete(memory)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def update_memory_importance(self, memory_id: int, new_importance: int) -> bool:
        """
        Met à jour l'importance d'un souvenir.
        
        Args:
            memory_id: ID du souvenir à modifier
            new_importance: Nouvelle valeur d'importance (0-100)
            
        Returns:
            True si le souvenir a été mis à jour, False sinon
        """
        db = db_manager.get_session()
        try:
            memory = db.query(LongTermMemory).filter(
                LongTermMemory.id == memory_id,
                LongTermMemory.robot_id == self.robot_id
            ).first()
            
            if memory:
                memory.importance = max(0, min(100, new_importance))  # Borner entre 0 et 100
                memory.updated_at = datetime.utcnow()
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def consolidate_memories(self) -> int:
        """
        Consolide les souvenirs du robot en fusionnant les souvenirs similaires
        et en supprimant les souvenirs peu importants.
        
        Returns:
            Nombre de souvenirs supprimés ou fusionnés
        """
        # Cette fonction est une ébauche et devra être améliorée
        # Idée: utiliser des embeddings pour trouver des souvenirs similaires
        db = db_manager.get_session()
        try:
            # Supprimer les souvenirs peu importants (importance < 10) de plus de 30 jours
            thirty_days_ago = datetime.utcnow() - datetime.timedelta(days=30)
            result = db.query(LongTermMemory).filter(
                LongTermMemory.robot_id == self.robot_id,
                LongTermMemory.importance < 10,
                LongTermMemory.created_at < thirty_days_ago
            ).delete()
            
            db.commit()
            return result
        finally:
            db.close()
