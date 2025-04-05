#include "capteur_manager.h"
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

class CapteurProprio : public Capteur {
private:
    Adafruit_MPU6050 mpu;
    sensors_event_t a, g, temp;
    
    // Valeurs des capteurs
    float accelerationX = 0;
    float accelerationY = 0;
    float accelerationZ = 0;
    float gyroX = 0;
    float gyroY = 0;
    float gyroZ = 0;
    
    // Paramètres de calibration
    float gyroCalibX = 0;
    float gyroCalibY = 0;
    float gyroCalibZ = 0;
    
    // État de la chute
    bool enChute = false;
    
public:
    CapteurProprio() {}
    
    virtual void initialiser() override {
        if (!mpu.begin()) {
            Serial.println("Impossible de trouver le MPU6050!");
            _actif = false;
            return;
        }
        
        // Configuration du capteur
        mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
        mpu.setGyroRange(MPU6050_RANGE_500_DEG);
        mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
        
        // Calibration
        calibrer();
    }
    
    virtual void lire() override {
        if (!_actif) return;
        
        // Récupération des données
        mpu.getEvent(&a, &g, &temp);
        
        // Mise à jour des valeurs
        accelerationX = a.acceleration.x;
        accelerationY = a.acceleration.y;
        accelerationZ = a.acceleration.z;
        
        gyroX = g.gyro.x - gyroCalibX;
        gyroY = g.gyro.y - gyroCalibY;
        gyroZ = g.gyro.z - gyroCalibZ;
        
        // Détection de chute
        detecterChute();
    }
    
    virtual const char* getNom() const override {
        return "Proprioception";
    }
    
    // Méthodes spécifiques
    void calibrer() {
        float sumX = 0, sumY = 0, sumZ = 0;
        const int numSamples = 50;
        
        Serial.println("Calibration du gyroscope...");
        
        for (int i = 0; i < numSamples; i++) {
            mpu.getEvent(&a, &g, &temp);
            sumX += g.gyro.x;
            sumY += g.gyro.y;
            sumZ += g.gyro.z;
            delay(10);
        }
        
        gyroCalibX = sumX / numSamples;
        gyroCalibY = sumY / numSamples;
        gyroCalibZ = sumZ / numSamples;
        
        Serial.println("Calibration terminée!");
    }
    
    void detecterChute() {
        // Calcul de l'accélération totale
        float accelTotal = sqrt(accelerationX * accelerationX + 
                               accelerationY * accelerationY + 
                               accelerationZ * accelerationZ);
        
        // Seuil pour détecter une chute (proche de 0g pendant la chute libre)
        if (accelTotal < 2.0) { // Valeur à ajuster
            if (!enChute) {
                enChute = true;
                Serial.println("Chute détectée!");
                // Peut déclencher une action d'urgence ou une émotion
            }
        } else {
            enChute = false;
        }
    }
    
    // Accesseurs
    float getAccelX() const { return accelerationX; }
    float getAccelY() const { return accelerationY; }
    float getAccelZ() const { return accelerationZ; }
    
    float getGyroX() const { return gyroX; }
    float getGyroY() const { return gyroY; }
    float getGyroZ() const { return gyroZ; }
    
    bool estEnChute() const { return enChute; }
};

// Fonction d'initialisation pour être ajoutée au setup() principal
void initialiserProprio() {
    auto proprio = std::make_shared<CapteurProprio>();
    CapteurManager::getInstance().ajouterCapteur(proprio);
}
