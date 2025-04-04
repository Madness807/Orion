#ifndef MCP_CLIENT_H
#define MCP_CLIENT_H

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"

// Structure pour les données des capteurs
struct SensorData {
    // Sons
    int bigSound;
    int smallSound;
    
    // Vision
    float distance; // ultrasonique
    int lightLevel; // photorésistance
    bool irDetected; // IR
    
    // Toucher
    bool tapDetected;
    bool shockDetected;
    bool touchDetected;
    bool buttonPressed;
    
    // Température
    float dht11Temp;
    float ds18b20Temp;
    float analogTemp;
    float humidity;
    
    // Magnétisme
    int hallValue;
    bool reedDetected;
    
    // Humidité/Eau
    int waterLevel;
    
    // Proprioception
    float acceleration[3]; // x, y, z
    float gyro[3]; // x, y, z
    bool tiltDetected;
    
    // Timestamp
    unsigned long timestamp;
};

// Enum pour les émotions du robot
enum EmotionType {
    JOIE,
    PEUR,
    CURIOSITE,
    TRISTESSE,
    COLERE,
    FATIGUE,
    SURPRISE,
    TENDRESSE,
    NEUTRE
};

// Structure pour l'état émotionnel
struct EmotionalState {
    EmotionType currentEmotion;
    int intensity; // 0-100
    unsigned long lastChange;
};

class MCPClient {
private:
    const char* serverIP;
    int serverPort;
    String robotId;
    
    HTTPClient http;
    
    // Structure JSON pour le message MCP
    StaticJsonDocument<2048> doc;
    
    // Timestamp de la dernière communication
    unsigned long lastCommunication;

public:
    MCPClient();
    
    // Initialiser le client MCP
    bool begin(const char* serverIP, int serverPort, const char* robotId);
    
    // Envoyer les données des capteurs au serveur MCP
    bool sendSensorData(const SensorData& data);
    
    // Envoyer l'état émotionnel au serveur MCP
    bool sendEmotionalState(const EmotionalState& state);
    
    // Recevoir les commandes du serveur MCP
    bool receiveCommands(String& commands);
    
    // Vérifier la connexion au serveur MCP
    bool checkConnection();
};

#endif // MCP_CLIENT_H
