/**
 * Script pour la page de surveillance du Robot Mignon
 * Créé le 4 avril 2025
 */

document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let sensorsChart = null;
    let emotionMap = null;
    let streamInterval = null;
    let isStreaming = false;
    
    // Initialiser les graphiques
    initSensorsChart();
    initEmotionMap();
    
    // Initialiser les gestionnaires d'événements
    initEventListeners();
    
    // Charger les données initiales
    loadSystemStatus();
    loadEventLog();
    
    // Mise à jour périodique des données
    setInterval(loadSystemStatus, 10000); // Toutes les 10 secondes
    
    /**
     * Initialise le graphique des capteurs
     */
    function initSensorsChart() {
        const ctx = document.getElementById('sensors-chart').getContext('2d');
        
        sensorsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // Sera rempli avec les horodatages
                datasets: [
                    {
                        label: 'Température (°C)',
                        data: [],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.2,
                        fill: true
                    },
                    {
                        label: 'Humidité (%)',
                        data: [],
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.2,
                        fill: true
                    },
                    {
                        label: 'Luminosité',
                        data: [],
                        borderColor: 'rgb(255, 205, 86)',
                        backgroundColor: 'rgba(255, 205, 86, 0.1)',
                        tension: 0.2,
                        fill: true
                    },
                    {
                        label: 'Distance (cm)',
                        data: [],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.2,
                        fill: true
                    },
                    {
                        label: 'Son',
                        data: [],
                        borderColor: 'rgb(153, 102, 255)',
                        backgroundColor: 'rgba(153, 102, 255, 0.1)',
                        tension: 0.2,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Charger les données initiales
        loadSensorHistory('1h');
    }
    
    /**
     * Initialise la carte émotionnelle
     */
    function initEmotionMap() {
        const ctx = document.getElementById('emotion-map').getContext('2d');
        
        // Créer un graphique de type scatter pour la carte émotionnelle
        emotionMap = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Carte émotionnelle',
                        data: [
                            { x: 0.8, y: 0.8, emotion: 'Joie' },
                            { x: -0.8, y: 0.5, emotion: 'Colère' },
                            { x: -0.6, y: -0.7, emotion: 'Tristesse' },
                            { x: 0.6, y: -0.6, emotion: 'Peur' },
                            { x: 0.9, y: 0.0, emotion: 'Surprise' },
                            { x: 0.0, y: 0.9, emotion: 'Tendresse' },
                            { x: -0.9, y: -0.2, emotion: 'Fatigue' },
                            { x: 0.2, y: -0.9, emotion: 'Curiosité' },
                            { x: 0.0, y: 0.0, emotion: 'Neutre' }
                        ],
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        pointRadius: 10,
                        pointHoverRadius: 12
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.raw.emotion;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        min: -1,
                        max: 1,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.2)'
                        },
                        ticks: {
                            display: false
                        }
                    },
                    y: {
                        min: -1,
                        max: 1,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.2)'
                        },
                        ticks: {
                            display: false
                        }
                    }
                }
            }
        });
        
        // Positionner le marqueur d'émotion actuelle
        updateEmotionMarker('neutre', 50);
    }
    
    /**
     * Initialise les gestionnaires d'événements
     */
    function initEventListeners() {
        // Boutons de période pour le graphique des capteurs
        document.querySelectorAll('[data-chart-period]').forEach(button => {
            button.addEventListener('click', function() {
                // Mettre à jour l'UI
                document.querySelectorAll('[data-chart-period]').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                
                // Charger les données pour la période sélectionnée
                loadSensorHistory(this.getAttribute('data-chart-period'));
            });
        });
        
        // Bouton de rafraîchissement des logs
        document.getElementById('refresh-logs-btn').addEventListener('click', function() {
            loadEventLog();
        });
        
        // Bouton de capture d'image
        document.getElementById('capture-snapshot-btn').addEventListener('click', function() {
            captureSnapshot();
        });
        
        // Boutons de contrôle du flux vidéo
        document.getElementById('start-stream-btn').addEventListener('click', function() {
            startVideoStream();
        });
        
        document.getElementById('stop-stream-btn').addEventListener('click', function() {
            stopVideoStream();
        });
    }
    
    /**
     * Charge l'historique des données des capteurs
     */
    async function loadSensorHistory(period) {
        try {
            const response = await fetch(`/api/robot/sensor_history?period=${period}`);
            const data = await response.json();
            
            if (data.success && data.history) {
                // Mettre à jour le graphique avec les nouvelles données
                sensorsChart.data.labels = data.history.timestamps.map(ts => {
                    const date = new Date(ts);
                    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                });
                
                // Mettre à jour les datasets
                sensorsChart.data.datasets[0].data = data.history.temperature;
                sensorsChart.data.datasets[1].data = data.history.humidity;
                sensorsChart.data.datasets[2].data = data.history.light;
                sensorsChart.data.datasets[3].data = data.history.distance;
                sensorsChart.data.datasets[4].data = data.history.sound;
                
                sensorsChart.update();
            } else {
                console.error('Erreur lors du chargement de l\'historique des capteurs:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors du chargement de l\'historique des capteurs:', error);
        }
    }
    
    /**
     * Charge le journal des événements
     */
    async function loadEventLog() {
        try {
            const response = await fetch('/api/robot/events?limit=20');
            const data = await response.json();
            
            const eventLogContainer = document.getElementById('event-log');
            
            if (data.success && data.events) {
                // Effacer les événements actuels
                eventLogContainer.innerHTML = '';
                
                // Ajouter les nouveaux événements
                if (data.events.length === 0) {
                    eventLogContainer.innerHTML = `
                        <li class="list-group-item text-center text-muted">
                            <small>Aucun événement récent</small>
                        </li>
                    `;
                } else {
                    data.events.forEach(event => {
                        // Formater l'horodatage
                        const timestamp = new Date(event.timestamp);
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
                        
                        // Créer l'élément HTML
                        const eventItem = document.createElement('li');
                        eventItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                        eventItem.innerHTML = `
                            <div>
                                <span class="event-icon"><i class="${icon}"></i></span>
                                <span class="event-message">${event.message}</span>
                            </div>
                            <small class="text-muted">${timeString}</small>
                        `;
                        
                        // Ajouter l'élément à la liste
                        eventLogContainer.appendChild(eventItem);
                    });
                }
            } else {
                console.error('Erreur lors du chargement des événements:', data.message);
                eventLogContainer.innerHTML = `
                    <li class="list-group-item text-center text-danger">
                        <small>Erreur lors du chargement des événements</small>
                    </li>
                `;
            }
        } catch (error) {
            console.error('Erreur lors du chargement des événements:', error);
            document.getElementById('event-log').innerHTML = `
                <li class="list-group-item text-center text-danger">
                    <small>Erreur lors du chargement des événements</small>
                </li>
            `;
        }
    }
    
    /**
     * Charge l'état du système
     */
    async function loadSystemStatus() {
        try {
            const response = await fetch('/api/robot/system_status');
            const data = await response.json();
            
            if (data.success && data.status) {
                // Mettre à jour les indicateurs d'état du système
                const status = data.status;
                
                // État général
                const systemStatusEl = document.getElementById('system-status');
                systemStatusEl.textContent = status.online ? 'En ligne' : 'Hors ligne';
                systemStatusEl.className = status.online ? 'badge bg-success' : 'badge bg-danger';
                
                // CPU
                const cpuEl = document.getElementById('cpu-usage');
                cpuEl.style.width = `${status.cpu_usage}%`;
                cpuEl.textContent = `${status.cpu_usage}%`;
                cpuEl.className = status.cpu_usage > 80 ? 'progress-bar bg-danger' : 
                                 status.cpu_usage > 60 ? 'progress-bar bg-warning' : 
                                 'progress-bar bg-info';
                
                // Mémoire
                const memoryEl = document.getElementById('memory-usage');
                memoryEl.style.width = `${status.memory_usage}%`;
                memoryEl.textContent = `${status.memory_usage}%`;
                memoryEl.className = status.memory_usage > 80 ? 'progress-bar bg-danger' : 
                                   status.memory_usage > 60 ? 'progress-bar bg-warning' : 
                                   'progress-bar bg-info';
                
                // Température
                const tempEl = document.getElementById('temperature');
                const tempWidth = Math.min(100, (status.temperature / 100) * 100);
                tempEl.style.width = `${tempWidth}%`;
                tempEl.textContent = `${status.temperature}°C`;
                tempEl.className = status.temperature > 70 ? 'progress-bar bg-danger' : 
                                 status.temperature > 50 ? 'progress-bar bg-warning' : 
                                 'progress-bar bg-info';
                
                // Batterie
                const batteryEl = document.getElementById('battery');
                batteryEl.style.width = `${status.battery}%`;
                batteryEl.textContent = `${status.battery}%`;
                batteryEl.className = status.battery < 20 ? 'progress-bar bg-danger' : 
                                   status.battery < 40 ? 'progress-bar bg-warning' : 
                                   'progress-bar bg-success';
                
                // WiFi
                const wifiEl = document.getElementById('wifi-strength');
                const wifiStrength = status.wifi_strength;
                let wifiIcon = 'fas fa-wifi';
                if (wifiStrength < -90) {
                    wifiIcon = 'fas fa-wifi text-danger';
                } else if (wifiStrength < -70) {
                    wifiIcon = 'fas fa-wifi text-warning';
                } else {
                    wifiIcon = 'fas fa-wifi text-success';
                }
                wifiEl.innerHTML = `<i class="${wifiIcon}"></i> <span>${wifiStrength} dBm</span>`;
                
                // Uptime
                const uptime = status.uptime; // en secondes
                const hours = Math.floor(uptime / 3600);
                const minutes = Math.floor((uptime % 3600) / 60);
                const seconds = uptime % 60;
                document.getElementById('uptime').textContent = 
                    `${hours}h ${minutes}m ${seconds}s`;
                
                // Mettre à jour l'état émotionnel si disponible
                if (status.emotional_state) {
                    updateEmotionMarker(
                        status.emotional_state.currentEmotion,
                        status.emotional_state.intensity
                    );
                }
            } else {
                console.error('Erreur lors du chargement de l\'état du système:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors du chargement de l\'état du système:', error);
        }
    }
    
    /**
     * Met à jour le marqueur d'émotion sur la carte émotionnelle
     */
    function updateEmotionMarker(emotion, intensity) {
        const marker = document.getElementById('current-emotion-marker');
        
        // Position par défaut (neutre)
        let x = 0;
        let y = 0;
        
        // Ajuster la position en fonction de l'émotion
        switch(emotion.toLowerCase()) {
            case 'joie':
                x = 0.8;
                y = 0.8;
                break;
            case 'colere':
                x = -0.8;
                y = 0.5;
                break;
            case 'tristesse':
                x = -0.6;
                y = -0.7;
                break;
            case 'peur':
                x = 0.6;
                y = -0.6;
                break;
            case 'surprise':
                x = 0.9;
                y = 0.0;
                break;
            case 'tendresse':
                x = 0.0;
                y = 0.9;
                break;
            case 'fatigue':
                x = -0.9;
                y = -0.2;
                break;
            case 'curiosite':
                x = 0.2;
                y = -0.9;
                break;
            default: // neutre
                x = 0;
                y = 0;
        }
        
        // Ajuster l'intensité (moduler la distance par rapport au centre)
        const intensityFactor = intensity / 100;
        x = x * intensityFactor;
        y = y * intensityFactor;
        
        // Convertir les coordonnées normalisées (-1 à 1) en position réelle sur le graphique
        const chartWidth = emotionMap.canvas.width;
        const chartHeight = emotionMap.canvas.height;
        
        // Position relative en pixels (ajuster en fonction des marges du graphique)
        const canvasRect = emotionMap.canvas.getBoundingClientRect();
        const marginX = canvasRect.width * 0.1; // 10% de marge
        const marginY = canvasRect.height * 0.1; // 10% de marge
        
        const posX = ((x + 1) / 2) * (canvasRect.width - 2 * marginX) + marginX;
        const posY = ((1 - y) / 2) * (canvasRect.height - 2 * marginY) + marginY;
        
        // Mettre à jour la position et la taille du marqueur
        marker.style.left = `${posX}px`;
        marker.style.top = `${posY}px`;
        marker.style.width = `${20 * (intensity / 100 + 0.5)}px`;
        marker.style.height = `${20 * (intensity / 100 + 0.5)}px`;
        
        // Mettre à jour la couleur du marqueur en fonction de l'émotion
        let color = '#888888'; // neutre
        switch(emotion.toLowerCase()) {
            case 'joie':
                color = '#FFD700'; // or
                break;
            case 'colere':
                color = '#FF0000'; // rouge
                break;
            case 'tristesse':
                color = '#4169E1'; // bleu royal
                break;
            case 'peur':
                color = '#800080'; // violet
                break;
            case 'surprise':
                color = '#FF00FF'; // magenta
                break;
            case 'tendresse':
                color = '#FFC0CB'; // rose
                break;
            case 'fatigue':
                color = '#708090'; // gris ardoise
                break;
            case 'curiosite':
                color = '#00FFFF'; // cyan
                break;
        }
        
        marker.style.backgroundColor = color;
        marker.style.borderColor = color;
    }
    
    /**
     * Capture une image
     */
    async function captureSnapshot() {
        try {
            const response = await fetch('/api/vision/capture', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success && data.image_path) {
                // Ajouter l'image à l'historique
                addImageToHistory(data.image_path, new Date().toISOString());
            } else {
                console.error('Erreur lors de la capture d\'image:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de la capture d\'image:', error);
        }
    }
    
    /**
     * Ajoute une image à l'historique
     */
    function addImageToHistory(imagePath, timestamp) {
        const imageHistory = document.getElementById('image-history');
        
        // Supprimer le message "Aucune capture récente" s'il existe
        const emptyMessage = imageHistory.querySelector('.text-muted');
        if (emptyMessage) {
            imageHistory.innerHTML = '';
        }
        
        // Limiter le nombre d'images dans l'historique
        const maxImages = 5;
        while (imageHistory.children.length >= maxImages) {
            imageHistory.removeChild(imageHistory.lastChild);
        }
        
        // Formater l'horodatage
        const date = new Date(timestamp);
        const timeString = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        // Créer un conteneur pour l'image
        const imageContainer = document.createElement('div');
        imageContainer.className = 'thumbnail-container mb-2';
        
        // Ajouter un timestamp pour éviter le cache
        const imgSrc = imagePath + '?t=' + new Date().getTime();
        
        // Ajouter l'image et l'horodatage
        imageContainer.innerHTML = `
            <img src="${imgSrc}" alt="Capture" class="img-thumbnail">
            <div class="thumbnail-overlay">
                <small>${timeString}</small>
            </div>
        `;
        
        // Ajouter un gestionnaire d'événements pour afficher l'image en grand
        imageContainer.addEventListener('click', function() {
            document.getElementById('video-stream').src = imgSrc;
        });
        
        // Ajouter l'image au début de l'historique
        imageHistory.insertBefore(imageContainer, imageHistory.firstChild);
    }
    
    /**
     * Démarre le flux vidéo
     */
    function startVideoStream() {
        if (isStreaming) return;
        
        // Masquer le bouton de démarrage et afficher le bouton d'arrêt
        document.getElementById('start-stream-btn').classList.add('d-none');
        document.getElementById('stop-stream-btn').classList.remove('d-none');
        
        // Simuler un flux vidéo en mettant à jour l'image périodiquement
        isStreaming = true;
        streamVideo();
        
        // Mettre à jour toutes les 2 secondes
        streamInterval = setInterval(streamVideo, 2000);
    }
    
    /**
     * Arrête le flux vidéo
     */
    function stopVideoStream() {
        if (!isStreaming) return;
        
        // Masquer le bouton d'arrêt et afficher le bouton de démarrage
        document.getElementById('stop-stream-btn').classList.add('d-none');
        document.getElementById('start-stream-btn').classList.remove('d-none');
        
        // Arrêter le minuteur
        clearInterval(streamInterval);
        isStreaming = false;
    }
    
    /**
     * Met à jour l'image du flux vidéo
     */
    async function streamVideo() {
        try {
            // Appeler l'API pour obtenir une nouvelle image
            const response = await fetch('/api/vision/capture', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success && data.image_path) {
                // Ajouter un timestamp pour éviter le cache
                const imgSrc = data.image_path + '?t=' + new Date().getTime();
                
                // Mettre à jour l'image
                document.getElementById('video-stream').src = imgSrc;
                
                // Si des détections sont présentes, les afficher
                const detectionOverlay = document.getElementById('detection-overlay');
                if (data.detections && Object.keys(data.detections).length > 0) {
                    // Logique pour afficher les détections (rectangles, etc.)
                    // Cette partie nécessiterait une implémentation spécifique en fonction
                    // du format des données de détection
                }
            } else {
                console.error('Erreur lors de la capture d\'image pour le flux:', data.message);
            }
        } catch (error) {
            console.error('Erreur lors de la mise à jour du flux vidéo:', error);
            stopVideoStream();
        }
    }
}); 