import os
import sys
import uvicorn
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mcp_server.log")
    ]
)
logger = logging.getLogger(__name__)

# Ajouter les chemins pour l'importation des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Importer le gestionnaire de base de données et initialiser les tables
from memoire.db_manager import init_db

# Importer le serveur FastAPI
from mcp_server import app

def init_app():
    """Initialise l'application et ses dépendances."""
    try:
        # Initialiser la base de données
        logger.info("Initialisation de la base de données...")
        init_db()
        
        # Journaliser les informations de configuration
        logger.info(f"Robot ID: {os.environ.get('ROBOT_ID', 'MignonBot1')}")
        logger.info(f"Moteur LLM: {os.environ.get('LLM_ENGINE', 'llama3')}")
        logger.info(f"Chemin des modèles LLM: {os.environ.get('LLM_MODEL_PATH', './models')}")
        
        logger.info("Initialisation terminée avec succès!")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        return False

def main():
    """Point d'entrée principal de l'application."""
    logger.info("Démarrage du serveur MCP (Model Context Protocol)...")
    
    # Initialiser l'application
    if not init_app():
        logger.error("Échec de l'initialisation. Arrêt du serveur.")
        sys.exit(1)
    
    # Configurer le serveur Uvicorn
    host = os.environ.get("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_SERVER_PORT", "8080"))
    
    # Démarrer le serveur
    logger.info(f"Démarrage du serveur sur {host}:{port}")
    uvicorn.run(
        "mcp_server:app",
        host=host,
        port=port,
        reload=False,
        workers=1
    )

if __name__ == "__main__":
    main()
