#include "capteur_manager.h"

// Définition des broches tactiles capacitives de l'ESP32
const uint8_t TOUCH_PINS[] = {T0, T1, T2, T3, T4, T5, T6, T7, T8, T9};
const int NUM_TOUCH_PINS = sizeof(TOUCH_PINS) / sizeof(TOUCH_PINS[0]);

class CapteurToucher : public Capteur {
private:
    // Seuils pour la détection du toucher (à ajuster selon les besoins)
    const uint16_t TOUCHER_SEUIL = 40;
    
    // État des capteurs tactiles
    bool touchDetecte[10] = {false};
    uint16_t touchValeurs[10] = {0};
    
    // Filtrage temporel pour éviter les faux positifs
    uint16_t touchMoyenne[10] = {0};
    const float ALPHA = 0.3; // Facteur de filtrage (0.0-1.0)
    
public:
    CapteurToucher() {}
    
    virtual void initialiser() override {
        for (int i = 0; i < NUM_TOUCH_PINS; i++) {
            // Initialisation des valeurs moyennes
            touchMoyenne[i] = touchRead(TOUCH_PINS[i]);
        }
        
        Serial.println("Capteur toucher initialisé");
    }
    
    virtual void lire() override {
        if (!_actif) return;
        
        bool toucherDetecte = false;
        
        for (int i = 0; i < NUM_TOUCH_PINS; i++) {
            // Lecture de la valeur brute du capteur
            uint16_t valeur = touchRead(TOUCH_PINS[i]);
            
            // Filtrage exponentiel pour lisser les valeurs
            touchMoyenne[i] = ALPHA * valeur + (1 - ALPHA) * touchMoyenne[i];
            
            // Mise à jour des valeurs
            touchValeurs[i] = valeur;
            
            // Détection du toucher (valeur basse = toucher détecté)
            bool estTouche = (valeur < TOUCHER_SEUIL);
            
            // Si changement d'état détecté
            if (estTouche != touchDetecte[i]) {
                touchDetecte[i] = estTouche;
                
                if (estTouche) {
                    Serial.printf("Toucher détecté sur capteur %d\n", i);
                    toucherDetecte = true;
                }
            }
        }
        
        // On pourrait ici notifier le gestionnaire d'émotions
        if (toucherDetecte) {
            // TODO: Notifier le gestionnaire d'émotions
        }
    }
    
    virtual const char* getNom() const override {
        return "Toucher";
    }
    
    // Accesseurs
    bool estTouche(int index) const {
        if (index >= 0 && index < NUM_TOUCH_PINS) {
            return touchDetecte[index];
        }
        return false;
    }
    
    bool estToucheQuelquePart() const {
        for (int i = 0; i < NUM_TOUCH_PINS; i++) {
            if (touchDetecte[i]) return true;
        }
        return false;
    }
    
    uint16_t getValeur(int index) const {
        if (index >= 0 && index < NUM_TOUCH_PINS) {
            return touchValeurs[index];
        }
        return 0;
    }
};

// Fonction d'initialisation pour être ajoutée au setup() principal
void initialiserToucher() {
    auto toucher = std::make_shared<CapteurToucher>();
    CapteurManager::getInstance().ajouterCapteur(toucher);
}
