#include "wifi_manager.h"

WiFiManager::WiFiManager() : connected(false), lastReconnectAttempt(0) {
}

bool WiFiManager::begin(const char* ssid, const char* password) {
    this->ssid = String(ssid);
    this->password = String(password);
    
    Serial.print("Connexion au WiFi: ");
    Serial.println(ssid);
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    // Attendre jusqu'à 20 secondes pour la connexion
    unsigned long startAttempt = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 20000) {
        delay(500);
        Serial.print(".");
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.print("Connecté avec succès! Adresse IP: ");
        Serial.println(WiFi.localIP());
        connected = true;
        return true;
    } else {
        Serial.println();
        Serial.println("Échec de la connexion WiFi");
        connected = false;
        return false;
    }
}

void WiFiManager::handle() {
    // Vérifier l'état de la connexion et tenter une reconnexion si nécessaire
    if (WiFi.status() != WL_CONNECTED) {
        if (connected) {
            Serial.println("Connexion WiFi perdue!");
            connected = false;
        }
        
        // Tenter de se reconnecter toutes les 30 secondes
        unsigned long currentMillis = millis();
        if (currentMillis - lastReconnectAttempt > reconnectInterval) {
            lastReconnectAttempt = currentMillis;
            Serial.println("Tentative de reconnexion WiFi...");
            
            WiFi.disconnect();
            WiFi.begin(ssid.c_str(), password.c_str());
        }
    } else if (!connected) {
        // Nous sommes connectés mais l'état était déconnecté
        connected = true;
        Serial.println("WiFi reconnecté!");
        Serial.print("Adresse IP: ");
        Serial.println(WiFi.localIP());
    }
}

bool WiFiManager::isConnected() {
    return WiFi.status() == WL_CONNECTED;
}

IPAddress WiFiManager::getLocalIP() {
    return WiFi.localIP();
}
