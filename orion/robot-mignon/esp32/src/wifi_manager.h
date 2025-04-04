#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include "config.h"

class WiFiManager {
private:
    String ssid;
    String password;
    bool connected;
    unsigned long lastReconnectAttempt;
    const unsigned long reconnectInterval = 30000; // 30 secondes

public:
    WiFiManager();
    
    // Initialiser la connexion WiFi
    bool begin(const char* ssid, const char* password);
    
    // Gérer la connexion WiFi (à appeler dans la boucle principale)
    void handle();
    
    // Vérifier si le WiFi est connecté
    bool isConnected();
    
    // Obtenir l'adresse IP
    IPAddress getLocalIP();
};

#endif // WIFI_MANAGER_H
