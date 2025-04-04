#include "mcp_client.h"

MCPClient::MCPClient() : serverIP(nullptr), serverPort(0), lastCommunication(0) {
}

bool MCPClient::begin(const char* serverIP, int serverPort, const char* robotId) {
    this->serverIP = serverIP;
    this->serverPort = serverPort;
    this->robotId = String(robotId);
    
    Serial.print("Initialisation du client MCP - Serveur: ");
    Serial.print(serverIP);
    Serial.print(":");
    Serial.println(serverPort);
    
    return checkConnection();
}

bool MCPClient::sendSensorData(const SensorData& data) {
    // Créer le document JSON
    doc.clear();
    
    // En-tête du message MCP
    doc["type"] = "sensor_data";
    doc["robot_id"] = robotId;
    doc["timestamp"] = data.timestamp;
    
    // Données des capteurs
    JsonObject sensors = doc.createNestedObject("sensors");
    
    // Sons
    JsonObject sound = sensors.createNestedObject("sound");
    sound["big_sound"] = data.bigSound;
    sound["small_sound"] = data.smallSound;
    
    // Vision
    JsonObject vision = sensors.createNestedObject("vision");
    vision["distance"] = data.distance;
    vision["light_level"] = data.lightLevel;
    vision["ir_detected"] = data.irDetected;
    
    // Toucher
    JsonObject touch = sensors.createNestedObject("touch");
    touch["tap"] = data.tapDetected;
    touch["shock"] = data.shockDetected;
    touch["touch"] = data.touchDetected;
    touch["button"] = data.buttonPressed;
    
    // Température
    JsonObject temperature = sensors.createNestedObject("temperature");
    temperature["dht11"] = data.dht11Temp;
    temperature["ds18b20"] = data.ds18b20Temp;
    temperature["analog"] = data.analogTemp;
    temperature["humidity"] = data.humidity;
    
    // Magnétisme
    JsonObject magnetic = sensors.createNestedObject("magnetic");
    magnetic["hall"] = data.hallValue;
    magnetic["reed"] = data.reedDetected;
    
    // Eau
    sensors["water_level"] = data.waterLevel;
    
    // Proprioception
    JsonObject proprioception = sensors.createNestedObject("proprioception");
    
    JsonArray accel = proprioception.createNestedArray("acceleration");
    accel.add(data.acceleration[0]);
    accel.add(data.acceleration[1]);
    accel.add(data.acceleration[2]);
    
    JsonArray gyroscope = proprioception.createNestedArray("gyro");
    gyroscope.add(data.gyro[0]);
    gyroscope.add(data.gyro[1]);
    gyroscope.add(data.gyro[2]);
    
    proprioception["tilt"] = data.tiltDetected;
    
    // Sérialiser le JSON
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    // Envoyer les données au serveur MCP
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/sensors";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(jsonPayload);
    
    // Vérifier le résultat
    bool success = false;
    if (httpCode == HTTP_CODE_OK) {
        String response = http.getString();
        Serial.println("Données des capteurs envoyées avec succès");
        success = true;
        lastCommunication = millis();
    } else {
        Serial.print("Erreur lors de l'envoi des données des capteurs: ");
        Serial.println(httpCode);
    }
    
    http.end();
    return success;
}

bool MCPClient::sendEmotionalState(const EmotionalState& state) {
    // Créer le document JSON
    doc.clear();
    
    // En-tête du message MCP
    doc["type"] = "emotional_state";
    doc["robot_id"] = robotId;
    doc["timestamp"] = millis();
    
    // État émotionnel
    JsonObject emotion = doc.createNestedObject("emotion");
    
    // Convertir l'émotion en chaîne
    const char* emotionStr;
    switch (state.currentEmotion) {
        case JOIE: emotionStr = "joie"; break;
        case PEUR: emotionStr = "peur"; break;
        case CURIOSITE: emotionStr = "curiosite"; break;
        case TRISTESSE: emotionStr = "tristesse"; break;
        case COLERE: emotionStr = "colere"; break;
        case FATIGUE: emotionStr = "fatigue"; break;
        case SURPRISE: emotionStr = "surprise"; break;
        case TENDRESSE: emotionStr = "tendresse"; break;
        default: emotionStr = "neutre"; break;
    }
    
    emotion["type"] = emotionStr;
    emotion["intensity"] = state.intensity;
    emotion["duration"] = millis() - state.lastChange;
    
    // Sérialiser le JSON
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    // Envoyer les données au serveur MCP
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/emotion";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(jsonPayload);
    
    // Vérifier le résultat
    bool success = false;
    if (httpCode == HTTP_CODE_OK) {
        String response = http.getString();
        Serial.println("État émotionnel envoyé avec succès");
        success = true;
        lastCommunication = millis();
    } else {
        Serial.print("Erreur lors de l'envoi de l'état émotionnel: ");
        Serial.println(httpCode);
    }
    
    http.end();
    return success;
}

bool MCPClient::receiveCommands(String& commands) {
    // Récupérer les commandes du serveur MCP
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/commands?robot_id=" + robotId;
    http.begin(url);
    
    int httpCode = http.GET();
    
    // Vérifier le résultat
    bool success = false;
    if (httpCode == HTTP_CODE_OK) {
        commands = http.getString();
        Serial.println("Commandes reçues avec succès");
        success = true;
        lastCommunication = millis();
    } else {
        Serial.print("Erreur lors de la réception des commandes: ");
        Serial.println(httpCode);
    }
    
    http.end();
    return success;
}

bool MCPClient::checkConnection() {
    // Vérifier la connexion au serveur MCP
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/ping";
    http.begin(url);
    
    int httpCode = http.GET();
    
    // Vérifier le résultat
    bool success = false;
    if (httpCode == HTTP_CODE_OK) {
        String response = http.getString();
        Serial.println("Connexion au serveur MCP réussie");
        success = true;
        lastCommunication = millis();
    } else {
        Serial.print("Erreur de connexion au serveur MCP: ");
        Serial.println(httpCode);
    }
    
    http.end();
    return success;
}
