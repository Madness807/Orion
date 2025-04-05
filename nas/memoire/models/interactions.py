from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from nas.memoire.db_manager import Interaction, db_manager


class InteractionModel:
    """
    Modèle pour gérer les interactions du robot avec les utilisateurs et son environnement.
    Fournit une interface pour enregistrer, récupérer et analyser les interactions.
    """
    
    def __init__(self, robot_id: str):
        """
        Initialise le modèle avec l'ID du robot.
        
        Args:
            robot_id: L'identifiant unique du robot
        """
        self.robot_id = robot_id
    
    def save_conversation(self, content: str, is_robot: bool = False, 
                          sentiment: Optional[str] = None, 
                          metadata: Dict[str, Any] = None) -> Interaction:
        """
        Enregistre une interaction de type conversation.
        
        Args:
            content: Le contenu de la conversation
            is_robot: True si c'est le robot qui parle, False si c'est l'utilisateur
            sentiment: Analyse optionnelle du sentiment (positif, négatif, neutre)
            metadata: Métadonnées additionnelles (ex: utilisateur identifié)
            
        Returns:
            L'objet interaction créé
        """
        if metadata is None:
            metadata = {}
            
        metadata["is_robot"] = is_robot
        if sentiment:
            metadata["sentiment"] = sentiment
            
        return db_manager.save_interaction(
            robot_id=self.robot_id,
            interaction_type="conversation",
            content=content,
            metadata=metadata
        )
    
    def save_reaction(self, stimulus: str, reaction: str, 
                      intensity: int = 50, 
                      metadata: Dict[str, Any] = None) -> Interaction:
        """
        Enregistre une réaction du robot à un stimulus.
        
        Args:
            stimulus: Description du stimulus déclencheur
            reaction: Description de la réaction du robot
            intensity: Intensité de la réaction (0-100)
            metadata: Métadonnées additionnelles
            
        Returns:
            L'objet interaction créé
        """
        if metadata is None:
            metadata = {}
            
        metadata["stimulus"] = stimulus
        metadata["intensity"] = intensity
        
        return db_manager.save_interaction(
            robot_id=self.robot_id,
            interaction_type="reaction",
            content=reaction,
            metadata=metadata
        )
    
    def save_instruction(self, instruction: str, source: str, 
                        executed: bool = False,
                        metadata: Dict[str, Any] = None) -> Interaction:
        """
        Enregistre une instruction donnée au robot.
        
        Args:
            instruction: Le contenu de l'instruction
            source: La source de l'instruction (utilisateur, système, etc.)
            executed: Si l'instruction a été exécutée
            metadata: Métadonnées additionnelles
            
        Returns:
            L'objet interaction créé
        """
        if metadata is None:
            metadata = {}
            
        metadata["source"] = source
        metadata["executed"] = executed
        
        return db_manager.save_interaction(
            robot_id=self.robot_id,
            interaction_type="instruction",
            content=instruction,
            metadata=metadata
        )
    
    def save_action(self, action: str, result: str = None, 
                   success: bool = True,
                   metadata: Dict[str, Any] = None) -> Interaction:
        """
        Enregistre une action effectuée par le robot.
        
        Args:
            action: Description de l'action
            result: Résultat de l'action (optionnel)
            success: Si l'action a réussi
            metadata: Métadonnées additionnelles
            
        Returns:
            L'objet interaction créé
        """
        if metadata is None:
            metadata = {}
            
        metadata["success"] = success
        if result:
            metadata["result"] = result
        
        return db_manager.save_interaction(
            robot_id=self.robot_id,
            interaction_type="action",
            content=action,
            metadata=metadata
        )
    
    def get_recent_interactions(self, interaction_type: Optional[str] = None, 
                               limit: int = 10) -> List[Interaction]:
        """
        Récupère les interactions récentes du robot.
        
        Args:
            interaction_type: Type d'interaction à récupérer
            limit: Nombre maximum d'interactions à récupérer
            
        Returns:
            Liste des interactions correspondant aux critères
        """
        db = db_manager.get_session()
        try:
            query = db.query(Interaction).filter(
                Interaction.robot_id == self.robot_id
            )
            
            if interaction_type:
                query = query.filter(Interaction.interaction_type == interaction_type)
                
            return query.order_by(Interaction.timestamp.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_conversation_history(self, minutes: int = 30, 
                                limit: int = 20) -> List[Dict[str, Any]]:
        """
        Récupère l'historique récent des conversations, formaté pour faciliter l'utilisation.
        
        Args:
            minutes: Récupérer les conversations des x dernières minutes
            limit: Nombre maximum de messages à récupérer
            
        Returns:
            Liste des messages de conversation formatés
        """
        db = db_manager.get_session()
        try:
            # Calculer la date limite
            time_threshold = datetime.utcnow() - datetime.timedelta(minutes=minutes)
            
            # Récupérer les conversations récentes
            conversations = db.query(Interaction).filter(
                Interaction.robot_id == self.robot_id,
                Interaction.interaction_type == "conversation",
                Interaction.timestamp >= time_threshold
            ).order_by(Interaction.timestamp).limit(limit).all()
            
            # Formater les messages
            formatted_history = []
            for convo in conversations:
                is_robot = convo.metadata.get("is_robot", False) if convo.metadata else False
                
                formatted_history.append({
                    "role": "assistant" if is_robot else "user",
                    "content": convo.content,
                    "timestamp": convo.timestamp.isoformat(),
                    "sentiment": convo.metadata.get("sentiment") if convo.metadata else None
                })
                
            return formatted_history
        finally:
            db.close()
    
    def get_interactions_by_content(self, search_query: str, 
                                   limit: int = 10) -> List[Interaction]:
        """
        Recherche des interactions par contenu.
        
        Args:
            search_query: Texte à rechercher dans le contenu
            limit: Nombre maximum d'interactions à récupérer
            
        Returns:
            Liste des interactions correspondantes
        """
        db = db_manager.get_session()
        try:
            # Note: cette implémentation est basique et pourrait être améliorée
            # avec une recherche fulltext dans PostgreSQL
            interactions = db.query(Interaction).filter(
                Interaction.robot_id == self.robot_id,
                Interaction.content.ilike(f"%{search_query}%")
            ).order_by(Interaction.timestamp.desc()).limit(limit).all()
            
            return interactions
        finally:
            db.close()
    
    def analyze_interaction_patterns(self) -> Dict[str, Any]:
        """
        Analyse les tendances et motifs dans les interactions récentes.
        
        Returns:
            Dictionnaire contenant différentes statistiques et analyses
        """
        db = db_manager.get_session()
        try:
            # Période d'analyse: dernières 24 heures
            time_threshold = datetime.utcnow() - datetime.timedelta(hours=24)
            
            # Récupérer toutes les interactions récentes
            interactions = db.query(Interaction).filter(
                Interaction.robot_id == self.robot_id,
                Interaction.timestamp >= time_threshold
            ).all()
            
            # Compter les types d'interactions
            interaction_types = {}
            for interaction in interactions:
                interaction_type = interaction.interaction_type
                interaction_types[interaction_type] = interaction_types.get(interaction_type, 0) + 1
            
            # Compter les conversations par sentiment
            sentiment_counts = {"positif": 0, "neutre": 0, "négatif": 0}
            for interaction in interactions:
                if interaction.interaction_type == "conversation" and interaction.metadata:
                    sentiment = interaction.metadata.get("sentiment")
                    if sentiment in sentiment_counts:
                        sentiment_counts[sentiment] += 1
            
            # Taux de succès des actions
            action_count = 0
            successful_actions = 0
            for interaction in interactions:
                if interaction.interaction_type == "action" and interaction.metadata:
                    action_count += 1
                    if interaction.metadata.get("success", False):
                        successful_actions += 1
            
            success_rate = (successful_actions / action_count) * 100 if action_count > 0 else 0
            
            return {
                "total_interactions": len(interactions),
                "interaction_types": interaction_types,
                "sentiment_distribution": sentiment_counts,
                "action_success_rate": success_rate,
                "period": "last_24_hours"
            }
        finally:
            db.close()
