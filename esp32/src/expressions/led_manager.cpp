#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include "../emotions/emotion_types.h"

// Configuration du ruban LED
#define LED_PIN     13  // Broche pour les LEDs
#define LED_COUNT   12  // Nombre de LEDs
#define BRIGHTNESS  50  // Luminosité (0-255)

class LEDManager {
private:
    Adafruit_NeoPixel _pixels;
    bool _initialise = false;
    EmotionBase _emotionActuelle = EmotionBase::NEUTRE;
    
    // Paramètres d'animation
    uint8_t _animationEtape = 0;
    uint8_t _animationVitesse = 5;
    unsigned long _derniereMaj = 0;
    
    // Couleurs prédéfinies pour les émotions
    const uint32_t COULEUR_JOIE = 0xFFFF00;       // Jaune
    const uint32_t COULEUR_TRISTESSE = 0x0000FF;  // Bleu
    const uint32_t COULEUR_PEUR = 0x800080;       // Violet
    const uint32_t COULEUR_COLERE = 0xFF0000;     // Rouge
    const uint32_t COULEUR_SURPRISE = 0x00FFFF;   // Cyan
    const uint32_t COULEUR_DEGOUT = 0x00FF00;     // Vert
    const uint32_t COULEUR_CONFIANCE = 0xFF8000;  // Orange
    const uint32_t COULEUR_NEUTRE = 0x808080;     // Gris
    
public:
    LEDManager() : _pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800) {}
    
    bool initialiser() {
        _pixels.begin();
        _pixels.setBrightness(BRIGHTNESS);
        _pixels.clear();
        _pixels.show();
        
        _initialise = true;
        Serial.println("Gestionnaire LED initialisé");
        
        // Afficher une séquence de démarrage
        sequenceDemarrage();
        
        return true;
    }
    
    void mettreAJour() {
        if (!_initialise) return;
        
        unsigned long maintenant = millis();
        
        // Limiter la fréquence de mise à jour
        if (maintenant - _derniereMaj < 50) return;
        _derniereMaj = maintenant;
        
        // Mettre à jour l'animation en cours
        switch (_emotionActuelle) {
            case EmotionBase::JOIE:
                animationJoie();
                break;
                
            case EmotionBase::TRISTESSE:
                animationTristesse();
                break;
                
            case EmotionBase::PEUR:
                animationPeur();
                break;
                
            case EmotionBase::COLERE:
                animationColere();
                break;
                
            case EmotionBase::SURPRISE:
                animationSurprise();
                break;
                
            default:
                animationNeutre();
                break;
        }
        
        _pixels.show();
        _animationEtape = (_animationEtape + 1) % 255;
    }
    
    void exprimer(EmotionBase emotion) {
        if (!_initialise) return;
        
        _emotionActuelle = emotion;
        _animationEtape = 0; // Réinitialiser l'animation
        
        // Notification initiale
        Serial.printf("LED: Expression de l'émotion %d\n", (int)emotion);
        
        // Appliquer immédiatement la nouvelle émotion
        mettreAJour();
    }
    
private:
    // Animations pour différentes émotions
    
    void sequenceDemarrage() {
        // Animation en spirale au démarrage
        for (int i = 0; i < LED_COUNT * 2; i++) {
            _pixels.clear();
            _pixels.setPixelColor(i % LED_COUNT, _pixels.Color(255, 255, 255));
            _pixels.show();
            delay(50);
        }
        _pixels.clear();
        _pixels.show();
    }
    
    void animationJoie() {
        // Animation de pulsation jaune joyeuse
        float intensite = (sin(_animationEtape * 0.05) + 1) * 0.5;
        
        for (int i = 0; i < LED_COUNT; i++) {
            _pixels.setPixelColor(i, colorScale(COULEUR_JOIE, intensite));
        }
    }
    
    void animationTristesse() {
        // Animation de vague lente bleue
        for (int i = 0; i < LED_COUNT; i++) {
            float phase = sin((_animationEtape * 0.02) + (i * 0.5));
            float intensite = (phase + 1) * 0.3; // Réduit l'intensité max (triste)
            _pixels.setPixelColor(i, colorScale(COULEUR_TRISTESSE, intensite));
        }
    }
    
    void animationPeur() {
        // Animation de scintillement aléatoire violet
        for (int i = 0; i < LED_COUNT; i++) {
            if (random(10) < 3) { // 30% de chance de scintiller
                float intensite = random(40, 100) / 100.0;
                _pixels.setPixelColor(i, colorScale(COULEUR_PEUR, intensite));
            } else {
                float baseIntensite = 0.2;
                _pixels.setPixelColor(i, colorScale(COULEUR_PEUR, baseIntensite));
            }
        }
    }
    
    void animationColere() {
        // Animation de pulsation rouge rapide
        float intensite = (sin(_animationEtape * 0.2) + 1) * 0.5;
        
        for (int i = 0; i < LED_COUNT; i++) {
            _pixels.setPixelColor(i, colorScale(COULEUR_COLERE, intensite));
        }
    }
    
    void animationSurprise() {
        // Flash cyan qui diminue
        float intensite = max(0.0, 1.0 - (_animationEtape % 50) / 50.0);
        
        for (int i = 0; i < LED_COUNT; i++) {
            _pixels.setPixelColor(i, colorScale(COULEUR_SURPRISE, intensite));
        }
    }
    
    void animationNeutre() {
        // Respiration douce en gris
        float intensite = (sin(_animationEtape * 0.01) + 1) * 0.3; // Faible intensité
        
        for (int i = 0; i < LED_COUNT; i++) {
            _pixels.setPixelColor(i, colorScale(COULEUR_NEUTRE, intensite));
        }
    }
    
    // Utilitaires pour les couleurs
    
    uint32_t colorScale(uint32_t color, float factor) {
        uint8_t r = ((color >> 16) & 0xFF) * factor;
        uint8_t g = ((color >> 8) & 0xFF) * factor;
        uint8_t b = (color & 0xFF) * factor;
        return _pixels.Color(r, g, b);
    }
};

// Instance globale
LEDManager ledManager;

// Fonctions à exposer
void initialiserLED() {
    ledManager.initialiser();
}

void mettreAJourLED() {
    ledManager.mettreAJour();
}

void exprimerLED(int emotion) {
    ledManager.exprimer(static_cast<EmotionBase>(emotion));
}
