import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json
from typing import Dict, List, Any, Optional

# Récupérer l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/robot_mignon")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base de modèles déclaratifs
Base = declarative_base()

# Modèle pour les données des capteurs
class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)  # Stocke toutes les données des capteurs en JSON

# Modèle pour l'état émotionnel
class EmotionalState(Base):
    __tablename__ = "emotional_states"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotion_type = Column(String, index=True)
    intensity = Column(Integer)
    duration = Column(Integer)

# Modèle pour les événements importants
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String, index=True)
    description = Column(String)
    data = Column(JSON, nullable=True)

# Modèle pour les souvenirs à long terme
class LongTermMemory(Base):
    __tablename__ = "long_term_memories"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    memory_type = Column(String, index=True)
    content = Column(String)
    importance = Column(Integer, default=50)  # Importance de 0 à 100
    embedding = Column(JSON, nullable=True)  # Pour la recherche sémantique

# Modèle pour les interactions
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(String, index=True)
    content = Column(String)
    metadata = Column(JSON, nullable=True)

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_tables(self):
        """Crée toutes les tables dans la base de données."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Retourne une nouvelle session de base de données."""
        return self.SessionLocal()
    
    # Méthodes pour les données des capteurs
    def save_sensor_data(self, robot_id: str, data: Dict[str, Any]) -> SensorData:
        """Enregistre les données des capteurs dans la base de données."""
        db = self.get_session()
        try:
            db_sensor_data = SensorData(
                robot_id=robot_id,
                timestamp=datetime.utcnow(),
                data=data
            )
            db.add(db_sensor_data)
            db.commit()
            db.refresh(db_sensor_data)
            return db_sensor_data
        finally:
            db.close()
    
    def get_recent_sensor_data(self, robot_id: str, limit: int = 10) -> List[SensorData]:
        """Récupère les données récentes des capteurs."""
        db = self.get_session()
        try:
            return db.query(SensorData).filter(SensorData.robot_id == robot_id).order_by(
                SensorData.timestamp.desc()).limit(limit).all()
        finally:
            db.close()
    
    # Méthodes pour l'état émotionnel
    def save_emotional_state(self, robot_id: str, emotion_type: str, intensity: int, duration: int) -> EmotionalState:
        """Enregistre l'état émotionnel dans la base de données."""
        db = self.get_session()
        try:
            db_emotional_state = EmotionalState(
                robot_id=robot_id,
                timestamp=datetime.utcnow(),
                emotion_type=emotion_type,
                intensity=intensity,
                duration=duration
            )
            db.add(db_emotional_state)
            db.commit()
            db.refresh(db_emotional_state)
            return db_emotional_state
        finally:
            db.close()
    
    def get_current_emotion(self, robot_id: str) -> Optional[EmotionalState]:
        """Récupère l'état émotionnel actuel."""
        db = self.get_session()
        try:
            return db.query(EmotionalState).filter(EmotionalState.robot_id == robot_id).order_by(
                EmotionalState.timestamp.desc()).first()
        finally:
            db.close()
    
    # Méthodes pour les événements
    def save_event(self, robot_id: str, event_type: str, description: str, data: Dict[str, Any] = None) -> Event:
        """Enregistre un événement dans la base de données."""
        db = self.get_session()
        try:
            db_event = Event(
                robot_id=robot_id,
                timestamp=datetime.utcnow(),
                event_type=event_type,
                description=description,
                data=data
            )
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return db_event
        finally:
            db.close()
    
    def get_recent_events(self, robot_id: str, limit: int = 10) -> List[Event]:
        """Récupère les événements récents."""
        db = self.get_session()
        try:
            return db.query(Event).filter(Event.robot_id == robot_id).order_by(
                Event.timestamp.desc()).limit(limit).all()
        finally:
            db.close()
    
    # Méthodes pour la mémoire à long terme
    def save_memory(self, robot_id: str, memory_type: str, content: str, 
                   importance: int = 50, embedding: List[float] = None) -> LongTermMemory:
        """Enregistre un souvenir dans la mémoire à long terme."""
        db = self.get_session()
        try:
            db_memory = LongTermMemory(
                robot_id=robot_id,
                memory_type=memory_type,
                content=content,
                importance=importance,
                embedding=embedding
            )
            db.add(db_memory)
            db.commit()
            db.refresh(db_memory)
            return db_memory
        finally:
            db.close()
    
    def get_memories_by_type(self, robot_id: str, memory_type: str, limit: int = 10) -> List[LongTermMemory]:
        """Récupère les souvenirs par type."""
        db = self.get_session()
        try:
            return db.query(LongTermMemory).filter(
                LongTermMemory.robot_id == robot_id,
                LongTermMemory.memory_type == memory_type
            ).order_by(LongTermMemory.importance.desc()).limit(limit).all()
        finally:
            db.close()
    
    # Méthodes pour les interactions
    def save_interaction(self, robot_id: str, interaction_type: str, content: str, 
                        metadata: Dict[str, Any] = None) -> Interaction:
        """Enregistre une interaction dans la base de données."""
        db = self.get_session()
        try:
            db_interaction = Interaction(
                robot_id=robot_id,
                interaction_type=interaction_type,
                content=content,
                metadata=metadata
            )
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            return db_interaction
        finally:
            db.close()
    
    def get_recent_interactions(self, robot_id: str, limit: int = 10) -> List[Interaction]:
        """Récupère les interactions récentes."""
        db = self.get_session()
        try:
            return db.query(Interaction).filter(Interaction.robot_id == robot_id).order_by(
                Interaction.timestamp.desc()).limit(limit).all()
        finally:
            db.close()


# Instancier le gestionnaire de base de données
db_manager = DatabaseManager()

# Fonction pour initialiser la base de données
def init_db():
    db_manager.create_tables()
    print("Base de données initialisée avec succès!")
