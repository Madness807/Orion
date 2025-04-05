#include "capteur_manager.h"
#include <Wire.h>
#include <Adafruit_APDS9960.h>

class CapteurVue : public Capteur {
private:
    Adafruit_APDS9960 apds;
    
    // Valeurs des capteurs
    uint16_t rouge = 0;
    uint16_t vert = 0;
    uint16_t bleu = 0;
    uint16_t clair = 0;
    
    // Détection de proximité
    uint8_t proximite = 0;
    uint8_t seuilProximite = 150;
    bool objetDetecte = false;
    
    // Détection de gestes
    bool detectionGestes = false;
    uint8_t dernierGeste = 0; // 0=aucun, 1=haut, 2=bas, 3=gauche, 4=droite
    
public:
    CapteurVue() {}
    
    virtual void initialiser() override {
        if (!apds.begin()) {
            Serial.println("Impossible de trouver le capteur APDS9960!");
            _actif = false;
            return;
        }
        
        // Configuration du capteur
        apds.enableColor(true);
        apds.enableProximity(true);
        
        // Activer la détection de gestes si nécessaire
        // apds.enableGesture(true);
        // detectionGestes = true;
        
        Serial.println("Capteur de vue initialisé");
    }
    
    virtual void lire() override {
        if (!_actif) return;
        
        // Lecture des couleurs
        if (apds.colorDataReady()) {
            apds.getColorData(&rouge, &vert, &bleu, &clair);
        }
        
        // Lecture de la proximité
        proximite = apds.readProximity();
        detecterObjet();
        
        // Lecture des gestes si activée
        if (detectionGestes && apds.gestureAvailable()) {
            dernierGeste = apds.readGesture();
            interpreterGeste();
        }
    }
    
    virtual const char* getNom() const override {
        return "Vue";
    }
    
    // Méthodes spécifiques
    void detecterObjet() {
        bool nouvelleDetection = (proximite > seuilProximite);
        
        // Si changement d'état de détection
        if (nouvelleDetection != objetDetecte) {
            objetDetecte = nouvelleDetection;
            
            if (objetDetecte) {
                Serial.println("Objet détecté par le capteur de vue!");
                // Peut déclencher une action ou une émotion
            } else {
                Serial.println("Plus d'objet en vue");
            }
        }
    }
    
    void interpreterGeste() {
        if (dernierGeste == 0) return;
        
        const char* noms[] = {"", "HAUT", "BAS", "GAUCHE", "DROITE"};
        if (dernierGeste <= 4) {
            Serial.print("Geste détecté: ");
            Serial.println(noms[dernierGeste]);
        }
    }
    
    // Changement des modes
    void activerDetectionGestes(bool activer) {
        detectionGestes = activer;
        apds.enableGesture(activer);
    }
    
    // Accesseurs
    uint16_t getRouge() const { return rouge; }
    uint16_t getVert() const { return vert; }
    uint16_t getBleu() const { return bleu; }
    uint16_t getClair() const { return clair; }
    
    uint8_t getProximite() const { return proximite; }
    bool objetEstDetecte() const { return objetDetecte; }
    
    uint8_t getDernierGeste() const { return dernierGeste; }
};

// Fonction d'initialisation pour être ajoutée au setup() principal
void initialiserVue() {
    auto vue = std::make_shared<CapteurVue>();
    CapteurManager::getInstance().ajouterCapteur(vue);
}
