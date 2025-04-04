#include <Arduino.h>
#include "config.h"
#include "wifi_manager.h"
#include "mcp_client.h"

// Gestionnaires
WiFiManager wifiManager;
MCPClient mcpClient;

// Variables pour les données des capteurs
SensorData sensorData;
EmotionalState emotionalState;

// Variables pour le minutage
unsigned long lastSensorUpdate = 0;
unsigned long lastEmotionUpdate = 0;
unsigned long lastMCPUpdate = 0;

// Déclaration des fonctions
void setupSensors();
void updateSensors();
void updateEmotionalState();
void executeCommands(const String& commands);
void expressEmotion(const EmotionalState& state);

void setup() {
  // Initialiser la communication série
  Serial.begin(115200);
  delay(1000);  // Attendre la stabilisation
  
  Serial.println("\n=== Robot Mignon - Initialisation ===");
  
  // Initialiser les capteurs
  setupSensors();
  
  // Initialiser la connexion WiFi
  if (wifiManager.begin(WIFI_SSID, WIFI_PASSWORD)) {
    Serial.println("WiFi connecté!");
  } else {
    Serial.println("Échec de la connexion WiFi. Redémarrage...");
    ESP.restart();
  }
  
  // Initialiser le client MCP
  if (mcpClient.begin(MCP_SERVER_IP, MCP_SERVER_PORT, ROBOT_ID)) {
    Serial.println("Client MCP initialisé!");
  } else {
    Serial.println("Échec de l'initialisation du client MCP. Continuons quand même...");
  }
  
  // Initialiser l'état émotionnel
  emotionalState.currentEmotion = NEUTRE;
  emotionalState.intensity = 50;
  emotionalState.lastChange = millis();
  
  Serial.println("=== Initialisation terminée ===\n");
}

void loop() {
  // Gérer la connexion WiFi
  wifiManager.handle();
  
  // Mettre à jour les données des capteurs
  if (millis() - lastSensorUpdate >= SENSOR_UPDATE_INTERVAL) {
    updateSensors();
    lastSensorUpdate = millis();
  }
  
  // Mettre à jour l'état émotionnel
  if (millis() - lastEmotionUpdate >= EMOTION_UPDATE_INTERVAL) {
    updateEmotionalState();
    lastEmotionUpdate = millis();
  }
  
  // Communiquer avec le serveur MCP
  if (millis() - lastMCPUpdate >= MCP_SEND_INTERVAL && wifiManager.isConnected()) {
    // Envoyer les données des capteurs
    mcpClient.sendSensorData(sensorData);
    
    // Envoyer l'état émotionnel
    mcpClient.sendEmotionalState(emotionalState);
    
    // Recevoir les commandes
    String commands;
    if (mcpClient.receiveCommands(commands)) {
      executeCommands(commands);
    }
    
    lastMCPUpdate = millis();
  }
  
  // Exprimer l'émotion actuelle
  expressEmotion(emotionalState);
  
  // Délai court pour éviter de surcharger la boucle
  delay(50);
}

void setupSensors() {
  Serial.println("Initialisation des capteurs...");
  
  // Initialiser les broches pour les capteurs
  // Sons
  pinMode(PIN_BIG_SOUND, INPUT);
  pinMode(PIN_SMALL_SOUND, INPUT);
  
  // Vision
  pinMode(PIN_ULTRASONIC_TRIG, OUTPUT);
  pinMode(PIN_ULTRASONIC_ECHO, INPUT);
  pinMode(PIN_PHOTORESISTOR, INPUT);
  pinMode(PIN_IR_RECEIVER, INPUT);
  
  // Toucher
  pinMode(PIN_TAP, INPUT);
  pinMode(PIN_SHOCK, INPUT);
  pinMode(PIN_TOUCH, INPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  
  // Température
  // (Utilisation des bibliothèques DHT et Dallas Temperature)
  
  // Magnétisme
  pinMode(PIN_HALL, INPUT);
  pinMode(PIN_REED, INPUT);
  
  // Humidité/Eau
  pinMode(PIN_WATER_LEVEL, INPUT);
  
  // Expression
  pinMode(PIN_RGB_LED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  
  // Initialisation I2C pour la communication avec GY-521 (MPU6050) et LCD
  Wire.begin(PIN_SDA, PIN_SCL);
  
  Serial.println("Capteurs initialisés!");
}

void updateSensors() {
  // Mettre à jour les données des capteurs
  Serial.println("Mise à jour des données des capteurs...");
  
  sensorData.timestamp = millis();
  
  // Lecture des capteurs de son
  sensorData.bigSound = analogRead(PIN_BIG_SOUND);
  sensorData.smallSound = analogRead(PIN_SMALL_SOUND);
  
  // Lecture du capteur de distance ultrasonique
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
  
  long duration = pulseIn(PIN_ULTRASONIC_ECHO, HIGH);
  sensorData.distance = duration * 0.034 / 2; // en cm
  
  // Lecture de la photorésistance
  sensorData.lightLevel = analogRead(PIN_PHOTORESISTOR);
  
  // Lecture du capteur IR
  sensorData.irDetected = !digitalRead(PIN_IR_RECEIVER); // Généralement actif à l'état bas
  
  // Lecture des capteurs de toucher
  sensorData.tapDetected = digitalRead(PIN_TAP);
  sensorData.shockDetected = digitalRead(PIN_SHOCK);
  sensorData.touchDetected = digitalRead(PIN_TOUCH);
  sensorData.buttonPressed = !digitalRead(PIN_BUTTON); // Actif à l'état bas avec pull-up
  
  // Note: pour les capteurs plus complexes comme DHT11, DS18B20, GY-521 (MPU6050),
  // il faudrait initialiser et utiliser les bibliothèques correspondantes.
  // Cette implémentation est simplifiée.
  
  // Placeholders pour les autres capteurs
  sensorData.dht11Temp = 25.0;  // Exemple de valeur
  sensorData.humidity = 50.0;   // Exemple de valeur
  sensorData.ds18b20Temp = 25.0; // Exemple de valeur
  sensorData.analogTemp = analogRead(PIN_ANALOG_TEMP) * 0.1; // Conversion simplifiée
  
  sensorData.hallValue = analogRead(PIN_HALL);
  sensorData.reedDetected = digitalRead(PIN_REED);
  
  sensorData.waterLevel = analogRead(PIN_WATER_LEVEL);
  
  // Placeholders pour les données de l'accéléromètre/gyroscope
  sensorData.acceleration[0] = 0.0;
  sensorData.acceleration[1] = 0.0;
  sensorData.acceleration[2] = 9.8; // Gravité en z
  
  sensorData.gyro[0] = 0.0;
  sensorData.gyro[1] = 0.0;
  sensorData.gyro[2] = 0.0;
  
  sensorData.tiltDetected = false; // À implémenter avec le GY-521
  
  Serial.println("Données des capteurs mises à jour!");
}

void updateEmotionalState() {
  // Mettre à jour l'état émotionnel en fonction des capteurs
  Serial.println("Mise à jour de l'état émotionnel...");
  
  EmotionType previousEmotion = emotionalState.currentEmotion;
  int previousIntensity = emotionalState.intensity;
  
  // Logique simple pour déterminer l'émotion
  // Ceci est un exemple simplifié - à améliorer avec une logique plus sophistiquée
  
  // Joie: lumière douce, interaction
  if (sensorData.lightLevel > 2000 && (sensorData.buttonPressed || sensorData.touchDetected)) {
    emotionalState.currentEmotion = JOIE;
    emotionalState.intensity = 80;
  }
  // Peur: obstacle soudain
  else if (sensorData.distance < 10.0) {
    emotionalState.currentEmotion = PEUR;
    emotionalState.intensity = 90;
  }
  // Curiosité: changement, mouvement
  else if (sensorData.distance < 30.0 && sensorData.distance > 10.0) {
    emotionalState.currentEmotion = CURIOSITE;
    emotionalState.intensity = 70;
  }
  // Tristesse: froid, obscurité
  else if (sensorData.lightLevel < 500 || sensorData.dht11Temp < 20.0) {
    emotionalState.currentEmotion = TRISTESSE;
    emotionalState.intensity = 60;
  }
  // Colère: choc
  else if (sensorData.shockDetected || sensorData.tapDetected) {
    emotionalState.currentEmotion = COLERE;
    emotionalState.intensity = 85;
  }
  // Fatigue: inactivité
  else if (millis() - lastSensorUpdate > 60000) { // Inactif depuis 1 minute
    emotionalState.currentEmotion = FATIGUE;
    emotionalState.intensity = 40;
  }
  // Par défaut: neutre
  else {
    emotionalState.currentEmotion = NEUTRE;
    emotionalState.intensity = 50;
  }
  
  // Si l'émotion a changé, mettre à jour le timestamp
  if (previousEmotion != emotionalState.currentEmotion || abs(previousIntensity - emotionalState.intensity) > 20) {
    emotionalState.lastChange = millis();
    
    // Afficher le changement d'émotion
    Serial.print("Nouvelle émotion: ");
    switch (emotionalState.currentEmotion) {
      case JOIE: Serial.print("JOIE"); break;
      case PEUR: Serial.print("PEUR"); break;
      case CURIOSITE: Serial.print("CURIOSITE"); break;
      case TRISTESSE: Serial.print("TRISTESSE"); break;
      case COLERE: Serial.print("COLERE"); break;
      case FATIGUE: Serial.print("FATIGUE"); break;
      case SURPRISE: Serial.print("SURPRISE"); break;
      case TENDRESSE: Serial.print("TENDRESSE"); break;
      default: Serial.print("NEUTRE"); break;
    }
    Serial.print(" avec une intensité de ");
    Serial.println(emotionalState.intensity);
  }
}

void executeCommands(const String& commands) {
  // Exécuter les commandes reçues du serveur MCP
  Serial.println("Exécution des commandes...");
  Serial.println(commands);
  
  // Parser le JSON des commandes
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, commands);
  
  if (error) {
    Serial.print("Erreur de parsing JSON: ");
    Serial.println(error.c_str());
    return;
  }
  
  // Exécuter les commandes
  if (doc.containsKey("emotion")) {
    String emotion = doc["emotion"].as<String>();
    int intensity = doc["intensity"].as<int>();
    
    // Forcer une émotion spécifique
    if (emotion == "joie") emotionalState.currentEmotion = JOIE;
    else if (emotion == "peur") emotionalState.currentEmotion = PEUR;
    else if (emotion == "curiosite") emotionalState.currentEmotion = CURIOSITE;
    else if (emotion == "tristesse") emotionalState.currentEmotion = TRISTESSE;
    else if (emotion == "colere") emotionalState.currentEmotion = COLERE;
    else if (emotion == "fatigue") emotionalState.currentEmotion = FATIGUE;
    else if (emotion == "surprise") emotionalState.currentEmotion = SURPRISE;
    else if (emotion == "tendresse") emotionalState.currentEmotion = TENDRESSE;
    else emotionalState.currentEmotion = NEUTRE;
    
    emotionalState.intensity = intensity;
    emotionalState.lastChange = millis();
    
    Serial.print("Changement d'émotion forcé: ");
    Serial.print(emotion);
    Serial.print(", intensité: ");
    Serial.println(intensity);
  }
  
  // Autres types de commandes à implémenter selon les besoins...
}

void expressEmotion(const EmotionalState& state) {
  // Exprimer l'émotion actuelle via les LEDs, l'écran LCD, les buzzers, etc.
  // Il s'agit d'une implémentation simplifiée utilisant uniquement la LED intégrée
  
  // Pour une implémentation complète, il faudrait utiliser les LEDs RGB, l'écran LCD, etc.
  
  switch (state.currentEmotion) {
    case JOIE:
      // LED jaune, sons doux
      digitalWrite(PIN_RGB_LED, HIGH);
      if (millis() % 2000 < 100) {
        tone(PIN_BUZZER, 1000, 50);
      }
      break;
      
    case PEUR:
      // LED rouge, recule, buzzer
      digitalWrite(PIN_RGB_LED, millis() % 200 < 100 ? HIGH : LOW); // clignotement rapide
      if (millis() % 500 < 50) {
        tone(PIN_BUZZER, 2000, 50);
      }
      break;
      
    case CURIOSITE:
      // LED verte, avance
      digitalWrite(PIN_RGB_LED, millis() % 1000 < 500 ? HIGH : LOW); // clignotement moyen
      break;
      
    case TRISTESSE:
      // LED bleue, s'arrête
      digitalWrite(PIN_RGB_LED, millis() % 3000 < 1500 ? HIGH : LOW); // clignotement lent
      break;
      
    case COLERE:
      // LED orange, vibre, bip fort
      digitalWrite(PIN_RGB_LED, millis() % 300 < 150 ? HIGH : LOW); // clignotement assez rapide
      if (millis() % 300 < 30) {
        tone(PIN_BUZZER, 3000, 30);
      }
      break;
      
    case FATIGUE:
      // LED violette, se met en veille
      digitalWrite(PIN_RGB_LED, millis() % 5000 < 2500 ? HIGH : LOW); // clignotement très lent
      break;
      
    default: // NEUTRE
      // LED éteinte
      digitalWrite(PIN_RGB_LED, LOW);
      break;
  }
}
