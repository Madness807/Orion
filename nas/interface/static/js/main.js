/**
 * Script principal pour l'interface de contrôle du Robot Mignon
 * Créé le 4 avril 2025
 */

// Script principal pour l'interface du Robot Mignon
document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let websocket;
    let selectedDetectionTypes = ['faces', 'objects']; // Types de détection par défaut
    let currentEmotion = 'neutre';
    let currentIntensity = 50;
    let currentSpeed = 50;
    
    // Éléments DOM
    const statusIndicator = document.getElementById('status-indicator');
    const connectionText = document.getElementById('connection-text');
    const currentEmotionDisplay = document.getElementById('current-emotion');
    const speedValue = document.getElementById('speed-value');
    const intensityValue = document.getElementById('intensity-value');
    const speedRange = document.getElementById('speed-range');
    const intensityRange = document.getElementById('intensity-range');
    const latestImage = document.getElementById('latest-image');
    const speechText = document.getElementById('speech-text');
    const speechResult = document.getElementById('speech-result');
    const eventsListContainer = document.getElementById('events-list');
    const sensorsListContainer = document.getElementById('sensors-list');
    
    // Initialisation de la connexion WebSocket
    function initWebSocket() {
        // Créer l'URL du WebSocket en fonction de l'URL actuelle
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = function(event) {
            console.log('Connexion WebSocket établie');
            updateConnectionStatus(true);
        };
        
        websocket.onclose = function(event) {
            console.log('Connexion WebSocket fermée');
            updateConnectionStatus(false);
            
            // Tentative de reconnexion après un délai
            setTimeout(function() {
                initWebSocket();
            }, 5000);
        };
        
        websocket.onerror = function(error) {
            console.error('Erreur WebSocket:', error);
            updateConnectionStatus(false);
        };
        
        websocket.onmessage = function(event) {
            handleWebSocketMessage(event.data);
        };
    }
    
    // Gérer les messages WebSocket reçus
    function handleWebSocketMessage(data) {
        try {
            const message = JSON.parse(data);
            console.log('Message WebSocket reçu:', message);
            
            switch(message.type) {
                case 'connected':
                    // Message de bienvenue, rien à faire de spécial
                    break;
                    
                case 'robot_status':
                    updateRobotStatus(message.status);
                    break;
                    
                case 'sensor_data':
                    updateSensorData(message.data);
                    break;
                    
                case 'emotional_state':
                    updateEmotionalState(message.state);
                    break;
                    
                case 'image_captured':
                    updateCapturedImage(message);
                    break;
                    
                case 'event':
                    addEvent(message);
                    break;
                    
                case 'speech_recognition':
                    updateSpeechResult(message.text);
                    break;
                    
                default:
                    console.log('Type de message inconnu:', message.type);
            }
        } catch (error) {
            console.error('Erreur lors du traitement du message WebSocket:', error);
        }
    }
    
    // Mise à jour du statut de connexion
    function updateConnectionStatus(connected) {
        if (connected) {
            statusIndicator.classList.remove('disconnected');
            statusIndicator.classList.add('connected');
            connectionText.textContent = 'Connecté';
        } else {
            statusIndicator.classList.remove('connected');
            statusIndicator.classList.add('disconnected');
            connectionText.textContent = 'Déconnecté';
        }
    }
    
    // Mise à jour de l'état du robot
    function updateRobotStatus(status) {
        updateEmotionalState(status.emotional_state);
        updateSensorData(status.sensor_data);
    }
    
    // Mise à jour des données des capteurs
    function updateSensorData(data) {
        if (!data) return;
        
        // Mettre à jour les valeurs des capteurs dans l'UI
        if (data.dht11Temp) {
            document.getElementById('sensor-temperature').textContent = `${data.dht11Temp.toFixed(1)}°C`;
        }
        
        if (data.humidity) {
            document.getElementById('sensor-humidity').textContent = `${data.humidity.toFixed(1)}%`;
        }
        
        if (data.lightLevel) {
            document.getElementById('sensor-light').textContent = data.lightLevel;
        }
        
        if (data.distance) {
            document.getElementById('sensor-distance').textContent = `${data.distance.toFixed(1)} cm`;
        }
        
        if (data.bigSound) {
            document.getElementById('sensor-sound').textContent = data.bigSound;
        }
    }
    
    // Mise à jour de l'état émotionnel
    function updateEmotionalState(state) {
        if (!state) return;
        
        currentEmotion = state.currentEmotion ? state.currentEmotion.toLowerCase() : 'neutre';
        currentIntensity = state.intensity || 50;
        
        // Mettre à jour l'affichage de l'émotion
        const emotionIcon = currentEmotionDisplay.querySelector('.emotion-icon i');
        const emotionText = currentEmotionDisplay.querySelector('.emotion-text');
        
        // Mettre à jour le texte
        emotionText.textContent = currentEmotion.charAt(0).toUpperCase() + currentEmotion.slice(1);
        
        // Mettre à jour l'icône
        emotionIcon.className = 'fas';
        switch(currentEmotion) {
            case 'joie':
                emotionIcon.classList.add('fa-smile');
                break;
            case 'peur':
                emotionIcon.classList.add('fa-flushed');
                break;
            case 'curiosite':
                emotionIcon.classList.add('fa-search');
                break;
            case 'tristesse':
                emotionIcon.classList.add('fa-sad-tear');
                break;
            case 'colere':
                emotionIcon.classList.add('fa-angry');
                break;
            case 'fatigue':
                emotionIcon.classList.add('fa-tired');
                break;
            case 'surprise':
                emotionIcon.classList.add('fa-surprise');
                break;
            default:
                emotionIcon.classList.add('fa-meh');
        }
        
        // Mettre à jour la valeur du curseur d'intensité
        intensityRange.value = currentIntensity;
        intensityValue.textContent = currentIntensity;
    }
    
    // Mise à jour de l'image capturée
    function updateCapturedImage(message) {
        if (message.image_path) {
            // Ajouter un timestamp pour éviter le cache
            latestImage.src = message.image_path + '?t=' + new Date().getTime();
            
            // Ajouter un événement pour cette capture
            addEvent({
                type: 'event',
                event_type: 'capture',
                message: 'Image capturée',
                timestamp: message.timestamp
            });
            
            // Si des détections sont présentes, les ajouter à l'événement
            if (message.detections && Object.keys(message.detections).length > 0) {
                for (const type in message.detections) {
                    const count = message.detections[type].length;
                    const typeName = type === 'faces' ? 'visage' : 
                                    type === 'objects' ? 'objet' : 
                                    type === 'emotions' ? 'émotion' : 
                                    type === 'colors' ? 'couleur' : type;
                    
                    const text = `${count} ${typeName}${count > 1 ? 's' : ''} détecté${count > 1 ? 's' : ''}`;
                    
                    addEvent({
                        type: 'event',
                        event_type: 'detection',
                        message: text,
                        timestamp: message.timestamp
                    });
                }
            }
        }
    }
    
    // Mise à jour du résultat de la reconnaissance vocale
    function updateSpeechResult(text) {
        if (text) {
            speechResult.innerHTML = `<q>${text}</q>`;
            
            // Ajouter un événement pour cette reconnaissance
            addEvent({
                type: 'event',
                event_type: 'speech',
                message: `Parole détectée: "${text}"`,
                timestamp: new Date().toISOString()
            });
        }
    }
    
    // Ajouter un événement à la liste
    function addEvent(event) {
        // Supprimer le message "Aucun événement récent" s'il existe
        const noEventsMessage = eventsListContainer.querySelector('.text-muted');
        if (noEventsMessage) {
            eventsListContainer.innerHTML = '';
        }
        
        // Limiter le nombre d'événements affichés
        const maxEvents = 10;
        while (eventsListContainer.children.length >= maxEvents) {
            eventsListContainer.removeChild(eventsListContainer.lastChild);
        }
        
        // Créer un nouvel élément de liste pour l'événement
        const eventItem = document.createElement('li');
        eventItem.className = 'list-group-item';
        
        // Formater l'horodatage
        let timestamp = new Date();
        if (event.timestamp) {
            timestamp = new Date(event.timestamp);
        }
        const timeString = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        // Déterminer l'icône en fonction du type d'événement
        let icon = 'fas fa-info-circle';
        if (event.event_type === 'capture') {
            icon = 'fas fa-camera';
        } else if (event.event_type === 'detection') {
            icon = 'fas fa-search';
        } else if (event.event_type === 'speech') {
            icon = 'fas fa-comment-alt';
        } else if (event.event_type === 'emotion') {
            icon = 'fas fa-heart';
        } else if (event.event_type === 'movement') {
            icon = 'fas fa-arrows-alt';
        }
        
        // Définir le contenu HTML de l'élément
        eventItem.innerHTML = `
            <div>
                <span class="event-icon"><i class="${icon}"></i></span>
                <span class="event-message">${event.message}</span>
            </div>
            <small class="text-muted">${timeString}</small>
        `;
        
        // Ajouter l'élément au début de la liste
        eventsListContainer.insertBefore(eventItem, eventsListContainer.firstChild);
    }
    
    // Envoyer une commande d'émotion au robot
    async function sendEmotionCommand(emotion, intensity) {
        try {
            const response = await fetch('/api/robot/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    command_type: 'emotion',
                    params: {
                        emotion: emotion,
                        intensity: intensity
                    }
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                addEvent({
                    type: 'event',
                    event_type: 'emotion',
                    message: `Émotion ${emotion} (${intensity}%) envoyée`,
                    timestamp: new Date().toISOString()
                });
            } else {
                console.error('Erreur lors de l\'envoi de la commande d\'émotion:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de l\'envoi de la commande d\'émotion:', error);
        }
    }
    
    // Envoyer une commande de mouvement au robot
    async function sendMovementCommand(direction, speed) {
        try {
            const response = await fetch('/api/robot/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    command_type: 'movement',
                    params: {
                        direction: direction,
                        speed: speed,
                        duration: direction === 'stop' ? 0 : 1000 // 1 seconde par défaut
                    }
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                addEvent({
                    type: 'event',
                    event_type: 'movement',
                    message: `Mouvement ${direction} (${speed}%) envoyé`,
                    timestamp: new Date().toISOString()
                });
            } else {
                console.error('Erreur lors de l\'envoi de la commande de mouvement:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de l\'envoi de la commande de mouvement:', error);
        }
    }
    
    // Capturer une image
    async function captureImage(detect = false) {
        try {
            const detectionParam = detect ? selectedDetectionTypes.join(',') : '';
            const response = await fetch(`/api/vision/capture?detection_types=${detectionParam}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (!data.success) {
                console.error('Erreur lors de la capture d\'image:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de la capture d\'image:', error);
        }
    }
    
    // Synthèse vocale
    async function textToSpeech(text) {
        try {
            const formData = new FormData();
            formData.append('text', text);
            formData.append('language', 'fr');
            formData.append('play', 'true');
            
            const response = await fetch('/api/speech/tts', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                addEvent({
                    type: 'event',
                    event_type: 'speech',
                    message: `Synthèse vocale: "${text}"`,
                    timestamp: new Date().toISOString()
                });
            } else {
                console.error('Erreur lors de la synthèse vocale:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de la synthèse vocale:', error);
        }
    }
    
    // Démarrer la reconnaissance vocale
    async function startSpeechRecognition() {
        try {
            const response = await fetch('/api/speech/listen', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('listen-start-btn').disabled = true;
                document.getElementById('listen-stop-btn').disabled = false;
                
                addEvent({
                    type: 'event',
                    event_type: 'speech',
                    message: 'Reconnaissance vocale démarrée',
                    timestamp: new Date().toISOString()
                });
            } else {
                console.error('Erreur lors du démarrage de la reconnaissance vocale:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors du démarrage de la reconnaissance vocale:', error);
        }
    }
    
    // Arrêter la reconnaissance vocale
    async function stopSpeechRecognition() {
        try {
            const response = await fetch('/api/speech/stop', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('listen-start-btn').disabled = false;
                document.getElementById('listen-stop-btn').disabled = true;
                
                addEvent({
                    type: 'event',
                    event_type: 'speech',
                    message: 'Reconnaissance vocale arrêtée',
                    timestamp: new Date().toISOString()
                });
            } else {
                console.error('Erreur lors de l\'arrêt de la reconnaissance vocale:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de l\'arrêt de la reconnaissance vocale:', error);
        }
    }
    
    // Récupérer les événements récents
    async function fetchRecentEvents() {
        try {
            const response = await fetch('/api/robot/events?limit=10');
            const data = await response.json();
            
            if (data.success && data.events) {
                // Effacer les événements actuels
                eventsListContainer.innerHTML = '';
                
                // Ajouter les nouveaux événements
                if (data.events.length === 0) {
                    eventsListContainer.innerHTML = `
                        <li class="list-group-item text-center text-muted">
                            <small>Aucun événement récent</small>
                        </li>
                    `;
                } else {
                    data.events.forEach(event => {
                        addEvent(event);
                    });
                }
            } else {
                console.error('Erreur lors de la récupération des événements:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de la récupération des événements:', error);
        }
    }
    
    // Initialiser les gestionnaires d'événements
    function initEventListeners() {
        // Boutons d'émotion
        document.querySelectorAll('.btn-emotion').forEach(button => {
            button.addEventListener('click', function() {
                const emotion = this.getAttribute('data-emotion');
                const intensity = parseInt(intensityRange.value);
                sendEmotionCommand(emotion, intensity);
            });
        });
        
        // Boutons de mouvement
        document.querySelectorAll('.btn-movement').forEach(button => {
            button.addEventListener('click', function() {
                const direction = this.getAttribute('data-direction');
                const speed = parseInt(speedRange.value);
                sendMovementCommand(direction, speed);
            });
        });
        
        // Curseur de vitesse
        speedRange.addEventListener('input', function() {
            currentSpeed = parseInt(this.value);
            speedValue.textContent = currentSpeed;
        });
        
        // Curseur d'intensité
        intensityRange.addEventListener('input', function() {
            currentIntensity = parseInt(this.value);
            intensityValue.textContent = currentIntensity;
        });
        
        // Bouton de capture d'image
        document.getElementById('capture-btn').addEventListener('click', function() {
            captureImage(false);
        });
        
        // Bouton de détection d'objets
        document.getElementById('detect-objects-btn').addEventListener('click', function() {
            captureImage(true);
        });
        
        // Options de détection
        document.querySelectorAll('.detection-option').forEach(option => {
            option.addEventListener('click', function() {
                const type = this.getAttribute('data-type');
                
                // Basculer la sélection
                const index = selectedDetectionTypes.indexOf(type);
                if (index >= 0) {
                    selectedDetectionTypes.splice(index, 1);
                    this.classList.remove('active');
                } else {
                    selectedDetectionTypes.push(type);
                    this.classList.add('active');
                }
            });
        });
        
        // Bouton de synthèse vocale
        document.getElementById('speak-btn').addEventListener('click', function() {
            const text = speechText.value.trim();
            if (text) {
                textToSpeech(text);
            }
        });
        
        // Bouton de démarrage de la reconnaissance vocale
        document.getElementById('listen-start-btn').addEventListener('click', function() {
            startSpeechRecognition();
        });
        
        // Bouton d'arrêt de la reconnaissance vocale
        document.getElementById('listen-stop-btn').addEventListener('click', function() {
            stopSpeechRecognition();
        });
        
        // Bouton de rafraîchissement des événements
        document.getElementById('refresh-events-btn').addEventListener('click', function() {
            fetchRecentEvents();
        });
    }
    
    // Initialisation
    function init() {
        initWebSocket();
        initEventListeners();
        fetchRecentEvents();
    }
    
    // Démarrer l'application
    init();
}); 