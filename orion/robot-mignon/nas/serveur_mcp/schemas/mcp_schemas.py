from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Any
from enum import Enum
from datetime import datetime

# Énumération des types d'émotions
class EmotionType(str, Enum):
    JOIE = "joie"
    PEUR = "peur"
    CURIOSITE = "curiosite"
    TRISTESSE = "tristesse"
    COLERE = "colere"
    FATIGUE = "fatigue"
    SURPRISE = "surprise"
    TENDRESSE = "tendresse"
    NEUTRE = "neutre"

# Schéma pour les données sonores
class SoundData(BaseModel):
    big_sound: int = Field(..., description="Niveau sonore élevé")
    small_sound: int = Field(..., description="Niveau sonore faible")

# Schéma pour les données visuelles
class VisionData(BaseModel):
    distance: float = Field(..., description="Distance en cm (capteur ultrasonique)")
    light_level: int = Field(..., description="Niveau de lumière (photorésistance)")
    ir_detected: bool = Field(..., description="Détection infrarouge")

# Schéma pour les données tactiles
class TouchData(BaseModel):
    tap: bool = Field(..., description="Détection de tapotement")
    shock: bool = Field(..., description="Détection de choc")
    touch: bool = Field(..., description="Détection de toucher")
    button: bool = Field(..., description="Bouton pressé")

# Schéma pour les données de température
class TemperatureData(BaseModel):
    dht11: float = Field(..., description="Température (DHT11)")
    ds18b20: float = Field(..., description="Température (DS18B20)")
    analog: float = Field(..., description="Température (analogique)")
    humidity: float = Field(..., description="Humidité")

# Schéma pour les données magnétiques
class MagneticData(BaseModel):
    hall: int = Field(..., description="Valeur du capteur à effet Hall")
    reed: bool = Field(..., description="Détection par interrupteur Reed")

# Schéma pour les données de proprioception
class ProprioceptionData(BaseModel):
    acceleration: List[float] = Field(..., description="Accélération [x, y, z]")
    gyro: List[float] = Field(..., description="Gyroscope [x, y, z]")
    tilt: bool = Field(..., description="Détection d'inclinaison")

# Schéma pour toutes les données des capteurs
class SensorDataPayload(BaseModel):
    sound: SoundData
    vision: VisionData
    touch: TouchData
    temperature: TemperatureData
    magnetic: MagneticData
    water_level: int = Field(..., description="Niveau d'eau")
    proprioception: ProprioceptionData

# Schéma pour une émotion
class EmotionData(BaseModel):
    type: EmotionType
    intensity: int = Field(..., ge=0, le=100, description="Intensité de l'émotion (0-100)")
    duration: int = Field(..., description="Durée en millisecondes depuis le changement d'émotion")

# Message MCP complet pour les données de capteurs
class SensorMCPMessage(BaseModel):
    type: str = "sensor_data"
    robot_id: str
    timestamp: int = Field(..., description="Timestamp en millisecondes")
    sensors: SensorDataPayload

# Message MCP complet pour l'état émotionnel
class EmotionalMCPMessage(BaseModel):
    type: str = "emotional_state"
    robot_id: str
    timestamp: int = Field(..., description="Timestamp en millisecondes")
    emotion: EmotionData

# Commande pour changer d'émotion
class EmotionCommand(BaseModel):
    emotion: EmotionType
    intensity: int = Field(..., ge=0, le=100)

# Commande pour bouger
class MovementCommand(BaseModel):
    direction: str = Field(..., description="Direction (forward, backward, left, right, stop)")
    speed: int = Field(..., ge=0, le=100, description="Vitesse (0-100)")
    duration: Optional[int] = Field(None, description="Durée en millisecondes (optionnel)")

# Commande pour faire un son
class SoundCommand(BaseModel):
    frequency: int = Field(..., description="Fréquence en Hz")
    duration: int = Field(..., description="Durée en millisecondes")

# Union de tous les types de commandes possibles
class RobotCommand(BaseModel):
    command_type: str = Field(..., description="Type de commande (emotion, movement, sound)")
    emotion: Optional[EmotionCommand] = None
    movement: Optional[MovementCommand] = None
    sound: Optional[SoundCommand] = None

# Message de réponse standard
class MCPResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Stockage en base de données
class SensorDataRecord(BaseModel):
    id: Optional[int] = None
    robot_id: str
    timestamp: datetime
    data: Dict[str, Any]
    
class EmotionalStateRecord(BaseModel):
    id: Optional[int] = None
    robot_id: str
    timestamp: datetime
    emotion_type: str
    intensity: int
    duration: int 