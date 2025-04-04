import os
import cv2
import numpy as np
import logging
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple, Union
import time
from pathlib import Path
import uuid
from datetime import datetime
import face_recognition
from ultralytics import YOLO
import requests
import json

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DetectionType(str, Enum):
    """Types de détection disponibles."""
    FACES = "faces"
    OBJECTS = "objects"
    EMOTIONS = "emotions"
    COLORS = "colors"
    MOVEMENT = "movement"
    QRCODE = "qrcode"

class ImageProcessor:
    """
    Processeur d'images pour la détection d'éléments visuels.
    
    Cette classe fournit des méthodes pour:
    - Détecter des visages
    - Reconnaître des objets
    - Analyser des couleurs
    - Détecter des mouvements
    - Lire des QR codes
    """
    
    def __init__(self):
        """Initialise le processeur d'images."""
        # Chemins des répertoires
        self.data_dir = os.environ.get("VISION_DATA_DIR", "/app/data")
        self.models_dir = os.path.join(self.data_dir, "models")
        self.images_dir = os.path.join(self.data_dir, "images")
        self.detected_dir = os.path.join(self.data_dir, "detected")
        
        # S'assurer que les répertoires existent
        for directory in [self.models_dir, self.images_dir, self.detected_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Modèles de détection
        self.face_detector = None
        self.emotion_detector = None
        self.object_detector = None
        self.qr_detector = None
        
        # Modèle YOLOv8 pour la détection d'objets
        try:
            self.object_detector = YOLO("yolov8n.pt")
            logger.info("Modèle YOLOv8 chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle YOLOv8: {e}")
            self.object_detector = None
        
        # Détecteur de QR codes
        try:
            self.qr_detector = cv2.QRCodeDetector()
            logger.info("Détecteur de QR codes initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du détecteur de QR codes: {e}")
            self.qr_detector = None
        
        logger.info("Processeur d'images initialisé avec succès")
    
    def process_image(self, image_path: str, detection_types: List[DetectionType]) -> Dict[str, Any]:
        """
        Traite une image avec les types de détection spécifiés.
        
        Args:
            image_path: Chemin vers l'image à traiter
            detection_types: Liste des types de détection à effectuer
            
        Returns:
            Résultats des détections
        """
        try:
            # Vérifier que l'image existe
            if not os.path.exists(image_path):
                logger.error(f"Image non trouvée: {image_path}")
                return {"error": "Image non trouvée"}
            
            # Charger l'image
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Impossible de charger l'image: {image_path}")
                return {"error": "Impossible de charger l'image"}
            
            # Convertir l'image en RGB pour face_recognition
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Initialiser les résultats
            results = {
                "image_path": image_path,
                "timestamp": datetime.now().isoformat(),
                "width": image.shape[1],
                "height": image.shape[0],
                "detections": {}
            }
            
            # Effectuer les détections demandées
            for detection_type in detection_types:
                if detection_type == DetectionType.FACES:
                    results["detections"]["faces"] = self._detect_faces(rgb_image, image_path)
                
                elif detection_type == DetectionType.OBJECTS:
                    results["detections"]["objects"] = self._detect_objects(rgb_image, image_path)
                
                elif detection_type == DetectionType.EMOTIONS:
                    results["detections"]["emotions"] = self._detect_emotions(rgb_image, image_path)
                
                elif detection_type == DetectionType.COLORS:
                    results["detections"]["colors"] = self._detect_colors(rgb_image)
                
                elif detection_type == DetectionType.MOVEMENT:
                    # Pour la détection de mouvements, il faudrait une séquence d'images
                    results["detections"]["movement"] = {"error": "La détection de mouvements nécessite une séquence d'images"}
                
                elif detection_type == DetectionType.QRCODE:
                    results["detections"]["qrcode"] = self._detect_qrcode(image)
            
            return results
        
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'image: {e}")
            return {"error": str(e)}
    
    def _detect_faces(self, image: np.ndarray, image_path: str) -> Dict[str, Any]:
        """
        Détecte les visages dans une image.
        
        Args:
            image: Image au format RGB
            image_path: Chemin de l'image originale
            
        Returns:
            Informations sur les visages détectés
        """
        try:
            # Détecter les visages
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            # Préparer les résultats
            faces = []
            for i, (top, right, bottom, left) in enumerate(face_locations):
                face = {
                    "id": i,
                    "confidence": 1.0,  # face_recognition ne donne pas de score de confiance
                    "position": {
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "left": left
                    },
                    "size": {
                        "width": right - left,
                        "height": bottom - top
                    }
                }
                faces.append(face)
            
            # Sauvegarder l'image avec les visages encadrés
            if faces:
                output_image = image.copy()
                for face in faces:
                    top = face["position"]["top"]
                    right = face["position"]["right"]
                    bottom = face["position"]["bottom"]
                    left = face["position"]["left"]
                    
                    # Dessiner un rectangle autour du visage
                    cv2.rectangle(
                        output_image, 
                        (left, top), 
                        (right, bottom), 
                        (0, 255, 0), 
                        2
                    )
                
                # Convertir en BGR pour OpenCV
                output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
                
                # Sauvegarder l'image
                filename = os.path.basename(image_path)
                output_path = os.path.join(
                    self.detected_dir, 
                    f"faces_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                )
                cv2.imwrite(output_path, output_image)
            
            return {
                "count": len(faces),
                "faces": faces,
                "output_image": output_path if faces else None
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des visages: {e}")
            return {"error": str(e)}
    
    def _detect_objects(self, image: np.ndarray, image_path: str) -> Dict[str, Any]:
        """
        Détecte les objets dans une image.
        
        Args:
            image: Image au format RGB
            image_path: Chemin de l'image originale
            
        Returns:
            Informations sur les objets détectés
        """
        try:
            if self.object_detector is None:
                return {"error": "Détecteur d'objets non initialisé"}
            
            # Détecter les objets avec YOLOv8
            results = self.object_detector(image)
            
            # Extraire les résultats
            objects = []
            for i, detection in enumerate(results[0].boxes.data.tolist()):
                x1, y1, x2, y2, confidence, class_id = detection
                class_name = results[0].names[int(class_id)]
                
                obj = {
                    "id": i,
                    "class": class_name,
                    "confidence": float(confidence),
                    "position": {
                        "top": int(y1),
                        "right": int(x2),
                        "bottom": int(y2),
                        "left": int(x1)
                    },
                    "size": {
                        "width": int(x2 - x1),
                        "height": int(y2 - y1)
                    }
                }
                objects.append(obj)
            
            # Sauvegarder l'image avec les objets détectés
            filename = os.path.basename(image_path)
            output_path = os.path.join(
                self.detected_dir, 
                f"objects_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            )
            
            # Les résultats de YOLOv8 contiennent l'image avec les annotations
            result_image = results[0].plot()
            cv2.imwrite(output_path, result_image)
            
            return {
                "count": len(objects),
                "objects": objects,
                "output_image": output_path if objects else None
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des objets: {e}")
            return {"error": str(e)}
    
    def _detect_emotions(self, image: np.ndarray, image_path: str) -> Dict[str, Any]:
        """
        Détecte les émotions des visages dans une image.
        
        Note: Cette fonction utilise une approche simplifiée basée sur la détection de visages.
        Pour une véritable détection d'émotions, il faudrait intégrer un modèle spécifique.
        
        Args:
            image: Image au format RGB
            image_path: Chemin de l'image originale
            
        Returns:
            Informations sur les émotions détectées
        """
        try:
            # Détecter les visages
            face_results = self._detect_faces(image, image_path)
            
            if "error" in face_results:
                return face_results
            
            # Simuler la détection d'émotions (pour une véritable détection, un modèle spécifique serait nécessaire)
            import random
            
            emotions = ["neutre", "joie", "tristesse", "colere", "surprise", "peur", "degout"]
            
            for face in face_results["faces"]:
                # Assigner une émotion aléatoire à chaque visage
                face["emotion"] = {
                    "type": random.choice(emotions),
                    "confidence": random.uniform(0.6, 0.95)
                }
            
            return {
                "count": face_results["count"],
                "faces": face_results["faces"],
                "output_image": face_results["output_image"]
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des émotions: {e}")
            return {"error": str(e)}
    
    def _detect_colors(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Détecte les couleurs dominantes dans une image.
        
        Args:
            image: Image au format RGB
            
        Returns:
            Informations sur les couleurs détectées
        """
        try:
            # Réduire la taille de l'image pour un traitement plus rapide
            height, width = image.shape[:2]
            scale = min(1.0, 300 / max(height, width))
            resized = cv2.resize(image, (int(width * scale), int(height * scale)))
            
            # Convertir l'image en numpy array
            pixels = resized.reshape(-1, 3)
            
            # K-means pour détecter les couleurs dominantes
            from sklearn.cluster import KMeans
            n_colors = 5
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Obtenir les couleurs dominantes
            colors = kmeans.cluster_centers_.astype(int)
            
            # Calculer le pourcentage de chaque couleur
            counts = np.bincount(kmeans.labels_)
            percentages = counts / len(pixels) * 100
            
            # Créer le résultat
            dominant_colors = []
            for i, (color, percentage) in enumerate(zip(colors, percentages)):
                r, g, b = color
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                dominant_colors.append({
                    "id": i,
                    "rgb": color.tolist(),
                    "hex": hex_color,
                    "percentage": float(percentage)
                })
            
            # Trier par pourcentage décroissant
            dominant_colors.sort(key=lambda x: x["percentage"], reverse=True)
            
            return {
                "count": len(dominant_colors),
                "colors": dominant_colors
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des couleurs: {e}")
            return {"error": str(e)}
    
    def _detect_qrcode(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Détecte les QR codes dans une image.
        
        Args:
            image: Image au format BGR (OpenCV)
            
        Returns:
            Informations sur les QR codes détectés
        """
        try:
            if self.qr_detector is None:
                return {"error": "Détecteur de QR codes non initialisé"}
            
            # Détecter et décoder les QR codes
            ret, decoded_info, points, straight_qrcode = self.qr_detector.detectAndDecodeMulti(image)
            
            if not ret:
                return {
                    "count": 0,
                    "qrcodes": []
                }
            
            # Préparer les résultats
            qrcodes = []
            for i, (info, pts) in enumerate(zip(decoded_info, points)):
                # Calculer la boîte englobante
                pts = pts.astype(np.int32)
                x_min, y_min = np.min(pts, axis=0)
                x_max, y_max = np.max(pts, axis=0)
                
                qrcode = {
                    "id": i,
                    "data": info,
                    "position": {
                        "top": int(y_min),
                        "right": int(x_max),
                        "bottom": int(y_max),
                        "left": int(x_min)
                    },
                    "size": {
                        "width": int(x_max - x_min),
                        "height": int(y_max - y_min)
                    }
                }
                qrcodes.append(qrcode)
            
            return {
                "count": len(qrcodes),
                "qrcodes": qrcodes
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la détection des QR codes: {e}")
            return {"error": str(e)}
    
    def capture_image(self, camera_id: int = 0, save: bool = True) -> Optional[str]:
        """
        Capture une image depuis une caméra.
        
        Args:
            camera_id: ID de la caméra à utiliser
            save: Indique si l'image doit être sauvegardée
            
        Returns:
            Chemin de l'image sauvegardée ou None en cas d'erreur
        """
        try:
            # Ouvrir la caméra
            cap = cv2.VideoCapture(camera_id)
            
            if not cap.isOpened():
                logger.error(f"Impossible d'ouvrir la caméra {camera_id}")
                return None
            
            # Capturer une image
            ret, frame = cap.read()
            
            # Libérer la caméra
            cap.release()
            
            if not ret:
                logger.error(f"Échec de la capture d'image depuis la caméra {camera_id}")
                return None
            
            if save:
                # Générer un nom de fichier unique
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"
                image_path = os.path.join(self.images_dir, filename)
                
                # Sauvegarder l'image
                cv2.imwrite(image_path, frame)
                logger.info(f"Image capturée et sauvegardée: {image_path}")
                
                return image_path
            else:
                # Créer un fichier temporaire
                import tempfile
                fd, temp_path = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                
                # Sauvegarder l'image dans le fichier temporaire
                cv2.imwrite(temp_path, frame)
                logger.info(f"Image capturée et sauvegardée temporairement: {temp_path}")
                
                return temp_path
        
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'image: {e}")
            return None
    
    def send_to_mcp(self, results: Dict[str, Any], mcp_url: Optional[str] = None) -> bool:
        """
        Envoie les résultats de détection au serveur MCP.
        
        Args:
            results: Résultats de la détection
            mcp_url: URL du serveur MCP (optionnel)
            
        Returns:
            True si l'envoi a réussi, False sinon
        """
        try:
            # Récupérer l'URL du serveur MCP
            if mcp_url is None:
                mcp_url = os.environ.get("MCP_SERVER_URL", "http://mcp_server:8080")
            
            # Convertir les résultats en format compatible JSON
            # (Numpy arrays, etc. ne sont pas JSON serializable)
            def convert_to_json_compatible(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, dict):
                    return {k: convert_to_json_compatible(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_to_json_compatible(item) for item in obj]
                else:
                    return obj
            
            json_compatible_results = convert_to_json_compatible(results)
            
            # Préparer les données à envoyer
            payload = {
                "robot_id": os.environ.get("ROBOT_ID", "MignonBot1"),
                "interaction_type": "vision_detection",
                "content": "Détection visuelle",
                "metadata": json_compatible_results
            }
            
            # Envoyer la requête au serveur MCP
            url = f"{mcp_url}/api/interaction"
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info("Résultats de détection envoyés avec succès au serveur MCP")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi au serveur MCP: {response.status_code}, {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi au serveur MCP: {e}")
            return False
