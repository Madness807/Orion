# Protocole MCP (Model Context Protocol)

## Introduction

Le protocole MCP (Model Context Protocol) est un protocole de communication basé sur JSON qui définit les échanges entre le robot physique (ESP32) et le cerveau centralisé (NAS). Il permet de structurer les données des capteurs, l'état émotionnel et les commandes dans un format cohérent et extensible.

## Principes généraux

- Communication via HTTP/REST
- Messages au format JSON
- Authentification simple par identifiant de robot
- Structure hiérarchique des données
- Horodatage de tous les messages

## Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/ping` | GET | Vérifier la connectivité |
| `/api/sensors` | POST | Envoyer les données des capteurs |
| `/api/emotion` | POST | Envoyer l'état émotionnel |
| `/api/commands` | GET | Recevoir les commandes à exécuter |
| `/api/send_command` | POST | Envoyer une commande manuellement |
| `/api/robot_status/{robot_id}` | GET | Obtenir l'état actuel du robot |
| `/api/interaction` | POST | Ajouter une interaction manuelle |

## Format des messages

### Message MCP de base

Tous les messages MCP partagent une structure de base :

```json
{
  "type": "message_type",
  "robot_id": "ROBOT_ID",
  "timestamp": 1639012345678
}
```

- `type` : Type de message (sensor_data, emotional_state, command, etc.)
- `robot_id` : Identifiant unique du robot
- `timestamp` : Horodatage en millisecondes (epoch)

### Données des capteurs

```json
{
  "type": "sensor_data",
  "robot_id": "MignonBot1",
  "timestamp": 1639012345678,
  "sensors": {
    "sound": {
      "big_sound": 423,
      "small_sound": 127
    },
    "vision": {
      "distance": 45.2,
      "light_level": 2340,
      "ir_detected": false
    },
    "touch": {
      "tap": false,
      "shock": false,
      "touch": true,
      "button": false
    },
    "temperature": {
      "dht11": 23.5,
      "ds18b20": 23.8,
      "analog": 24.1,
      "humidity": 45.2
    },
    "magnetic": {
      "hall": 512,
      "reed": false
    },
    "water_level": 0,
    "proprioception": {
      "acceleration": [0.01, 0.02, 9.81],
      "gyro": [0.0, 0.0, 0.0],
      "tilt": false
    }
  }
}
```

### État émotionnel

```json
{
  "type": "emotional_state",
  "robot_id": "MignonBot1",
  "timestamp": 1639012345678,
  "emotion": {
    "type": "joie",
    "intensity": 75,
    "duration": 5000
  }
}
```

- `type` : Type d'émotion (joie, peur, curiosite, tristesse, colere, fatigue, surprise, tendresse, neutre)
- `intensity` : Intensité de l'émotion (0-100)
- `duration` : Durée en millisecondes depuis le changement d'émotion

### Commandes

```json
{
  "commands": [
    {
      "command_type": "emotion",
      "emotion": {
        "emotion": "joie",
        "intensity": 80
      }
    },
    {
      "command_type": "movement",
      "movement": {
        "direction": "forward",
        "speed": 60,
        "duration": 2000
      }
    },
    {
      "command_type": "sound",
      "sound": {
        "frequency": 1000,
        "duration": 500
      }
    }
  ]
}
```

## Flux de communication

1. Le robot envoie périodiquement les données de ses capteurs (`POST /api/sensors`)
2. Le robot envoie son état émotionnel lorsqu'il change (`POST /api/emotion`)
3. Le robot demande régulièrement s'il y a des commandes à exécuter (`GET /api/commands?robot_id=ROBOT_ID`)
4. Le serveur traite les données, analyse la situation avec le LLM et génère des commandes
5. Le robot exécute les commandes reçues

## Codes d'erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 400 | Requête invalide (mauvais format JSON, paramètres manquants) |
| 401 | Non autorisé (robot_id inconnu) |
| 500 | Erreur serveur (erreur de traitement, base de données, etc.) |

## Extensions futures

Le protocole MCP est conçu pour être extensible. Voici quelques extensions envisagées :

- Support pour la vidéo et l'audio en streaming
- Modes de communication en temps réel via WebSockets
- Authentification plus robuste
- Compression des données pour les réseaux à faible bande passante
