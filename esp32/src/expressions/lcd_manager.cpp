#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "../emotions/emotion_types.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define SCREEN_ADDRESS 0x3C

class LCDManager {
private:
    Adafruit_SSD1306 _display;
    bool _initialise = false;
    EmotionBase _emotionActuelle = EmotionBase::NEUTRE;
    uint8_t _clignementYeux = 0;  // Compteur pour le clignement
    unsigned long _dernierClignement = 0;
    
public:
    LCDManager() : _display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET) {}
    
    bool initialiser() {
        // Initialiser l'écran OLED
        if (!_display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
            Serial.println(F("Échec d'initialisation de l'écran SSD1306"));
            return false;
        }
        
        // Configuration de base
        _display.setTextColor(SSD1306_WHITE);
        _display.clearDisplay();
        _display.display();
        
        _initialise = true;
        Serial.println("Gestionnaire LCD initialisé");
        
        // Afficher un visage neutre au démarrage
        afficherEmotion(EmotionBase::NEUTRE);
        
        return true;
    }
    
    void mettreAJour() {
        if (!_initialise) return;
        
        // Gérer le clignement des yeux
        unsigned long maintenant = millis();
        
        // Clignement automatique toutes les 3-7 secondes
        if (_clignementYeux == 0 && maintenant - _dernierClignement > 3000) {
            // Probabilité aléatoire de clignement
            if (random(100) < 20 || maintenant - _dernierClignement > 7000) {
                _clignementYeux = 5; // Durée du clignement (5 frames)
                _dernierClignement = maintenant;
            }
        }
        
        // Animation de clignement en cours
        if (_clignementYeux > 0) {
            _clignementYeux--;
            // Redessiner le visage avec les yeux fermés/ouverts
            dessinerVisage(_emotionActuelle, _clignementYeux > 0);
        }
    }
    
    void afficherEmotion(EmotionBase emotion) {
        if (!_initialise) return;
        
        _emotionActuelle = emotion;
        dessinerVisage(emotion, false);
        
        Serial.printf("LCD: Expression de l'émotion %d\n", (int)emotion);
    }
    
    void afficherTexte(const char* texte) {
        if (!_initialise) return;
        
        _display.clearDisplay();
        _display.setTextSize(1);
        _display.setCursor(0, 0);
        _display.println(texte);
        _display.display();
    }
    
private:
    void dessinerVisage(EmotionBase emotion, bool yeuxFermes) {
        _display.clearDisplay();
        
        // Dessiner les yeux (sauf si clignement)
        if (!yeuxFermes) {
            dessinerYeux(emotion);
        } else {
            dessinerYeuxFermes();
        }
        
        // Dessiner la bouche selon l'émotion
        dessinerBouche(emotion);
        
        // Afficher le résultat
        _display.display();
    }
    
    void dessinerYeux(EmotionBase emotion) {
        // Position des yeux
        int yeux_y = 20;
        
        switch (emotion) {
            case EmotionBase::JOIE:
                // Yeux souriants / plissés
                _display.fillCircle(40, yeux_y, 10, SSD1306_WHITE);
                _display.fillCircle(88, yeux_y, 10, SSD1306_WHITE);
                _display.fillCircle(40, yeux_y, 6, SSD1306_BLACK);
                _display.fillCircle(88, yeux_y, 6, SSD1306_BLACK);
                break;
                
            case EmotionBase::TRISTESSE:
                // Yeux tombants
                _display.fillCircle(40, yeux_y, 8, SSD1306_WHITE);
                _display.fillCircle(88, yeux_y, 8, SSD1306_WHITE);
                _display.fillCircle(40, yeux_y+2, 4, SSD1306_BLACK);
                _display.fillCircle(88, yeux_y+2, 4, SSD1306_BLACK);
                break;
                
            case EmotionBase::COLERE:
                // Yeux froncés
                _display.fillCircle(40, yeux_y, 8, SSD1306_WHITE);
                _display.fillCircle(88, yeux_y, 8, SSD1306_WHITE);
                _display.fillCircle(40, yeux_y, 4, SSD1306_BLACK);
                _display.fillCircle(88, yeux_y, 4, SSD1306_BLACK);
                // Sourcils froncés
                _display.drawLine(30, yeux_y-12, 45, yeux_y-8, SSD1306_WHITE);
                _display.drawLine(78, yeux_y-8, 93, yeux_y-12, SSD1306_WHITE);
                break;
                
            case EmotionBase::SURPRISE:
                // Yeux grands ouverts
                _display.drawCircle(40, yeux_y, 12, SSD1306_WHITE);
                _display.drawCircle(88, yeux_y, 12, SSD1306_WHITE);
                _display.fillCircle(40, yeux_y, 5, SSD1306_WHITE);
                _display.fillCircle(88, yeux_y, 5, SSD1306_WHITE);
                break;
                
            case EmotionBase::PEUR:
                // Yeux instables
                _display.drawCircle(40, yeux_y, 10, SSD1306_WHITE);
                _display.drawCircle(88, yeux_y, 10, SSD1306_WHITE);
                _display.fillCircle(40+random(-2,3), yeux_y+random(-2,3), 4, SSD1306_WHITE);
                _display.fillCircle(88+random(-2,3), yeux_y+random(-2,3), 4, SSD1306_WHITE);
                break;
                
            default: // Neutre et autres
                // Yeux ronds standard
                _display.drawCircle(40, yeux_y, 10, SSD1306_WHITE);
                _display.drawCircle(88, yeux_y, 10, SSD1306_WHITE);
                _display.fillCircle(40, yeux_y, 4, SSD1306_WHITE);
                _display.fillCircle(88, yeux_y, 4, SSD1306_WHITE);
                break;
        }
    }
    
    void dessinerYeuxFermes() {
        // Yeux fermés (lignes horizontales)
        int yeux_y = 20;
        _display.drawLine(30, yeux_y, 50, yeux_y, SSD1306_WHITE);
        _display.drawLine(78, yeux_y, 98, yeux_y, SSD1306_WHITE);
    }
    
    void dessinerBouche(EmotionBase emotion) {
        // Position de la bouche
        int bouche_y = 45;
        
        switch (emotion) {
            case EmotionBase::JOIE:
                // Sourire
                _display.drawCircle(64, bouche_y+10, 20, SSD1306_WHITE);
                _display.fillRect(44, bouche_y-10, 40, 20, SSD1306_BLACK);
                break;
                
            case EmotionBase::TRISTESSE:
                // Bouche triste
                _display.drawCircle(64, bouche_y+30, 20, SSD1306_WHITE);
                _display.fillRect(44, bouche_y, 40, 30, SSD1306_BLACK);
                break;
                
            case EmotionBase::COLERE:
                // Ligne droite avec dents
                _display.drawLine(44, bouche_y, 84, bouche_y, SSD1306_WHITE);
                // Dents apparentes
                for (int i = 0; i < 5; i++) {
                    _display.drawLine(48 + i*8, bouche_y, 52 + i*8, bouche_y+5, SSD1306_WHITE);
                }
                break;
                
            case EmotionBase::SURPRISE:
                // Bouche en O
                _display.drawCircle(64, bouche_y, 10, SSD1306_WHITE);
                break;
                
            case EmotionBase::PEUR:
                // Bouche tremblante
                for (int i = 0; i < 3; i++) {
                    int offset = random(-2, 3);
                    _display.drawLine(44, bouche_y+offset, 84, bouche_y+offset, SSD1306_WHITE);
                }
                break;
                
            default: // Neutre et autres
                // Ligne droite simple
                _display.drawLine(44, bouche_y, 84, bouche_y, SSD1306_WHITE);
                break;
        }
    }
};

// Instance globale
LCDManager lcdManager;

// Fonctions à exposer
void initialiserLCD() {
    lcdManager.initialiser();
}

void mettreAJourLCD() {
    lcdManager.mettreAJour();
}

void afficherEmotionLCD(int emotion) {
    lcdManager.afficherEmotion(static_cast<EmotionBase>(emotion));
}

void afficherTexteLCD(const char* texte) {
    lcdManager.afficherTexte(texte);
}
