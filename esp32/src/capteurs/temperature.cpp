#include "capteur_manager.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

class CapteurTemperature : public Capteur {
private:
    Adafruit_BME280 bme;
    
    // Valeurs du capteur
    float temperature = 0;
    
    // Limites de température
    float tempMin = 5.0;
    float tempMax = 50.0;
    bool alerteTemp = false;
    
public:
    CapteurTemperature() {}
    
    virtual void initialiser() override {
        if (!bme.begin(0x76)) {  // Adresse I2C typique du BME280
            Serial.println("Impossible de trouver le capteur BME280!");
            _actif = false;
            return;
        }
        
        Serial.println("Capteur de température initialisé");
    }
    
    virtual void lire() override {
        if (!_actif) return;
        
        // Lecture de la température
        temperature = bme.readTemperature();
        
        // Vérification des alertes
        verifierAlerte();
    }
    
    virtual const char* getNom() const override {
        return "Temperature";
    }
    
    // Méthodes spécifiques
    void verifierAlerte() {
        bool nouvelleAlerte = (temperature < tempMin || temperature > tempMax);
        
        // Si changement d'état d'alerte
        if (nouvelleAlerte != alerteTemp) {
            alerteTemp = nouvelleAlerte;
            
            if (alerteTemp) {
                if (temperature < tempMin) {
                    Serial.println("Alerte: Température trop basse!");
                } else {
                    Serial.println("Alerte: Température trop élevée!");
                }
                // Peut déclencher une action ou une émotion
            }
        }
    }
    
    // Accesseurs
    float getTemperature() const { return temperature; }
    
    bool estEnAlerte() const { return alerteTemp; }
    
    void setLimitesTemperature(float min, float max) {
        tempMin = min;
        tempMax = max;
    }
};

// Fonction d'initialisation pour être ajoutée au setup() principal
void initialiserTemperature() {
    auto temperature = std::make_shared<CapteurTemperature>();
    CapteurManager::getInstance().ajouterCapteur(temperature);
}
