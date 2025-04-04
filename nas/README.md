# Serveur NAS pour Robot Mignon

Ce répertoire contient le code du cerveau centralisé pour le robot mignon, qui tourne sur un NAS (Network Attached Storage). Il est responsable du traitement de l'intelligence artificielle, de la mémoire à long terme, et de la communication avec le robot physique (ESP32) via le protocole MCP (Model Context Protocol).

## Structure du projet

- `serveur_mcp/` : Serveur principal qui gère le protocole MCP et la communication avec le robot
- `llm/` : Intégration du modèle de langage (LLM) pour l'intelligence du robot
- `memoire/` : Gestion de la mémoire à court et long terme
- `speech/` : Services de reconnaissance et synthèse vocale
- `vision/` : Services de traitement d'image et de vision par ordinateur
- `interface/` : Interface web pour visualiser l'état du robot et interagir avec lui

## Installation

### Prérequis

- Docker et Docker Compose
- Un NAS avec au moins 8GB de RAM et 50GB d'espace disque
- Accès réseau au robot ESP32

### Configuration

1. Copiez le fichier `.env.example` vers `.env` et modifiez les variables selon votre configuration :

```bash
cp .env.example .env
nano .env
```

2. Téléchargez les modèles LLM nécessaires :

```bash
mkdir -p llm/models
# Téléchargez le modèle Llama 3 (ou autre modèle compatible)
# Exemple pour Llama 3 :
# wget https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf -O llm/models/llama-3-8b-instruct.gguf
```

### Démarrage

Lancez les services avec Docker Compose :

```bash
docker-compose up -d
```

## Utilisation

### API MCP

Le serveur MCP expose une API REST sur le port 8080 :

- `GET /api/ping` : Vérifier la connectivité
- `POST /api/sensors` : Recevoir les données des capteurs
- `POST /api/emotion` : Recevoir l'état émotionnel
- `GET /api/commands?robot_id=ROBOT_ID` : Obtenir les commandes à exécuter
- `POST /api/send_command` : Envoyer une commande manuellement
- `GET /api/robot_status/{robot_id}` : Obtenir l'état actuel du robot
- `POST /api/interaction` : Ajouter une interaction manuelle

### Interface Web

L'interface web est accessible sur le port 8000 : `http://IP_DU_NAS:8000`

L'interface permet de :
- Visualiser l'état actuel du robot et ses capteurs en temps réel
- Consulter l'historique des interactions et des émotions
- Envoyer des commandes manuelles au robot
- Configurer la personnalité et les paramètres du robot

## Modules détaillés

### Serveur MCP

Le serveur MCP (`serveur_mcp/`) est le composant central qui :
- Gère les communications via le protocole MCP (Model Context Protocol)
- Coordonne les différents services (LLM, mémoire, etc.)
- Maintient l'état contextuel du robot
- Transforme les données des capteurs en entrées pour le LLM

Fichiers principaux :
- `main.py` : Point d'entrée de l'application qui initialise la base de données et démarre le serveur web FastAPI avec Uvicorn.
- `mcp_server.py` : Implémentation du serveur REST avec FastAPI qui définit toutes les routes pour le protocole MCP (ping, reception des données des capteurs, état émotionnel, commandes, etc.).
- `context_manager.py` : Gestion du contexte du robot, responsable du traitement des données des capteurs, de l'analyse de l'état émotionnel, de la génération de commandes et de la coordination avec le LLM.
- `schemas/` : Définition des modèles de données pour les messages MCP, y compris les types d'émotions et les structures de données des capteurs.

### LLM (Large Language Model)

Le module LLM (`llm/`) gère l'intelligence artificielle du robot :
- Interface avec le modèle de langage (Llama 3 par défaut)
- Templates de personnalité et prompts système
- Traitement contextuel des entrées

Fichiers principaux :
- `model_manager.py` : Gestionnaire du modèle LLM qui gère le chargement de modèles (HuggingFace ou Llama.cpp), l'intégration d'embeddings, la génération de texte, et l'analyse des capteurs pour produire des interprétations, suggestions d'actions et réponses émotionnelles.
- `prompts/` : Templates de prompts pour différentes situations, y compris `robot_personality.txt` qui définit la personnalité de base du robot.
- `personality_templates/` : Définitions de personnalités pour le robot, permettant de configurer différents comportements et caractères.

### Mémoire

Le module de mémoire (`memoire/`) gère le stockage persistant :
- Base de données PostgreSQL pour la mémoire à long terme
- Stockage des interactions, des données des capteurs et des émotions
- Récupération contextuelle pour alimenter le LLM

Fichier principal :
- `db_manager.py` : Interface avec la base de données PostgreSQL qui définit les modèles de données (SensorData, EmotionalState, Event, LongTermMemory, Interaction) et fournit des méthodes pour sauvegarder et récupérer les données. Gère également l'initialisation et la création des tables.

### Speech (Parole)

Le service de parole (`speech/`) gère les aspects audio :
- Reconnaissance vocale (STT - Speech to Text)
- Synthèse vocale (TTS - Text to Speech)
- Traitement des commandes vocales

Fichiers principaux :
- `stt_engine.py` : Moteur de reconnaissance vocale qui transforme les signaux audio en texte, utilisant des modèles pré-entraînés pour la reconnaissance vocale.
- `tts_engine.py` : Moteur de synthèse vocale qui convertit le texte en parole, avec différentes voix et paramètres de configuration.
- `main.py` : Coordination des fonctionnalités vocales qui intègre les moteurs STT et TTS et communique avec le serveur MCP.

### Vision

Le service de vision (`vision/`) traite les images :
- Analyse des flux vidéo
- Reconnaissance d'objets
- Détection de visages et d'émotions

Fichiers principaux :
- `image_processor.py` : Traitement d'images et analyse visuelle qui implémente des algorithmes de détection d'objets, reconnaissance faciale, et analyse d'émotions à partir d'images.
- `main.py` : Coordination des fonctionnalités visuelles qui intègre le traitement d'images et communique avec le serveur MCP pour envoyer les analyses.

### Interface Web

L'interface web (`interface/`) fournit un tableau de bord :
- Affichage temps réel de l'état du robot
- Contrôles manuels et configuration
- Visualisation des données historiques

Fichiers principaux :
- `app.py` : Application web Flask qui définit les routes, gère l'affichage des données du robot et fournit les contrôles pour interagir avec le robot.
- `static/` : Ressources statiques (CSS, JS) pour le style et les fonctionnalités frontend de l'interface.
- `templates/` : Templates HTML pour la génération des pages web, incluant les vues pour le tableau de bord, la configuration et les contrôles.

## Fonctionnement

1. Le robot ESP32 envoie régulièrement les données de ses capteurs au serveur MCP
2. Le serveur traite ces données et les analyse avec le LLM
3. En fonction de l'analyse, le serveur met à jour l'état émotionnel du robot
4. Le robot interroge régulièrement le serveur pour récupérer des commandes à exécuter
5. Le serveur stocke l'historique des données, émotions et interactions en base de données

## Protocole MCP

Le protocole MCP (Model Context Protocol) définit la communication entre l'ESP32 et le NAS :
- Format JSON standardisé
- Messages typés (sensor_data, emotional_state, command)
- Voir `docs/protocole_mcp.md` pour les spécifications complètes

## Carte émotionnelle

Le robot utilise une carte émotionnelle pour représenter son état :
- 9 émotions de base (joie, peur, curiosité, tristesse, colère, fatigue, surprise, tendresse, neutre)
- Intensité variable (0-100)
- Transitions d'émotions basées sur les entrées sensorielles et le contexte
- Voir `docs/carte_emotionnelle.md` pour plus de détails

## Développement

### Extensions

Pour ajouter de nouvelles fonctionnalités, vous pouvez :

- Créer de nouveaux services dans le docker-compose
- Ajouter des endpoints à l'API MCP
- Étendre les capacités du LLM avec de nouveaux prompts
- Améliorer l'interface web
- Ajouter de nouveaux capteurs dans le code ESP32

### Contribution

1. Créez une branche pour votre fonctionnalité
2. Implémentez et testez votre code
3. Mettez à jour la documentation
4. Soumettez une pull request

### Tests

```bash
# Lancer les tests unitaires
cd tests
python -m unittest discover
```

## Dépannage

### Problèmes courants

- Si le robot ne se connecte pas, vérifiez les paramètres réseau dans `config.h`
- Si le LLM ne répond pas, vérifiez que le modèle est correctement téléchargé
- Pour les problèmes de base de données, consultez les logs avec `docker-compose logs database`

### Logs

Consultez les logs des services :
```bash
docker-compose logs -f mcp_server
docker-compose logs -f speech_service
```

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
