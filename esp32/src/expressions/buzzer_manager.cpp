#include <Arduino.h>
#include "../emotions/emotion_types.h"

// Configuration du buzzer
#define BUZZER_PIN  21  // Broche pour le buzzer

// Définition des notes musicales
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988

// Structure pour mélodie
struct Note {
    uint16_t frequence;  // Fréquence de la note ou 0 pour une pause
    uint16_t duree;      // Durée en ms
    
    Note(uint16_t f, uint16_t d) : frequence(f), duree(d) {}
};

class BuzzerManager {
private:
    bool _initialise = false;
    bool _actif = true;
    bool _enLecture = false;
    int _noteActuelle = 0;
    unsigned long _prochainChangement = 0;
    
    // Mélodies pour chaque émotion
    std::vector<Note> _melodieActuelle;
    std::vector<Note> _melodieJoie;
    std::vector<Note> _melodieTristesse;
    std::vector<Note> _melodiePeur;
    std::vector<Note> _melodieColere;
    std::vector<Note> _melodieSurprise;
    
public:
    BuzzerManager() {
        // Initialiser les mélodies prédéfinies
        initialiserMelodies();
    }
    
    bool initialiser() {
        pinMode(BUZZER_PIN, OUTPUT);
        noTone(BUZZER_PIN);
        
        _initialise = true;
        Serial.println("Gestionnaire buzzer initialisé");
        
        // Jouer une mélodie de démarrage
        jouerDemarrage();
        
        return true;
    }
    
    void mettreAJour() {
        if (!_initialise || !_actif) return;
        
        unsigned long maintenant = millis();
        
        if (_enLecture && maintenant >= _prochainChangement) {
            // Passer à la note suivante
            _noteActuelle++;
            
            // Vérifier si on a atteint la fin de la mélodie
            if (_noteActuelle >= _melodieActuelle.size()) {
                arreter();
                return;
            }
            
            // Jouer la note suivante
            const Note& note = _melodieActuelle[_noteActuelle];
            if (note.frequence > 0) {
                tone(BUZZER_PIN, note.frequence, note.duree);
            } else {
                noTone(BUZZER_PIN);
            }
            
            // Programmer le prochain changement
            _prochainChangement = maintenant + note.duree;
        }
    }
    
    void exprimer(EmotionBase emotion) {
        if (!_initialise || !_actif) return;
        
        // Sélectionner la mélodie appropriée
        switch (emotion) {
            case EmotionBase::JOIE:
                jouerMelodie(_melodieJoie);
                break;
                
            case EmotionBase::TRISTESSE:
                jouerMelodie(_melodieTristesse);
                break;
                
            case EmotionBase::PEUR:
                jouerMelodie(_melodiePeur);
                break;
                
            case EmotionBase::COLERE:
                jouerMelodie(_melodieColere);
                break;
                
            case EmotionBase::SURPRISE:
                jouerMelodie(_melodieSurprise);
                break;
                
            default:
                // Émotion neutre ou non gérée: ne rien jouer
                break;
        }
    }
    
    void jouerBip() {
        if (!_initialise || !_actif) return;
        
        // Arrêter la mélodie en cours
        noTone(BUZZER_PIN);
        _enLecture = false;
        
        // Jouer un simple bip
        tone(BUZZER_PIN, NOTE_A4, 100);
    }
    
    void arreter() {
        if (!_initialise) return;
        
        noTone(BUZZER_PIN);
        _enLecture = false;
    }
    
    void setActif(bool actif) {
        _actif = actif;
        if (!actif) {
            arreter();
        }
    }
    
private:
    void initialiserMelodies() {
        // Mélodie de joie (séquence ascendante rapide)
        _melodieJoie = {
            Note(NOTE_C4, 100), Note(NOTE_E4, 100), Note(NOTE_G4, 100), 
            Note(NOTE_C5, 200), Note(NOTE_G4, 100), Note(NOTE_C5, 300)
        };
        
        // Mélodie de tristesse (séquence descendante lente)
        _melodieTristesse = {
            Note(NOTE_A4, 300), Note(NOTE_G4, 300), Note(NOTE_F4, 300),
            Note(NOTE_E4, 500), Note(0, 200), Note(NOTE_D4, 300), Note(NOTE_C4, 500)
        };
        
        // Mélodie de peur (notes aiguës tremblantes)
        _melodiePeur = {
            Note(NOTE_G5, 100), Note(0, 50), Note(NOTE_G5, 100), Note(0, 100),
            Note(NOTE_A5, 100), Note(0, 50), Note(NOTE_G5, 150), Note(0, 200),
            Note(NOTE_G5, 100), Note(NOTE_A5, 100), Note(NOTE_G5, 300)
        };
        
        // Mélodie de colère (notes graves fortes)
        _melodieColere = {
            Note(NOTE_C3, 200), Note(NOTE_C3, 200), Note(NOTE_G3, 400),
            Note(NOTE_C3, 200), Note(NOTE_G3, 400)
        };
        
        // Mélodie de surprise (notes montantes rapides)
        _melodieSurprise = {
            Note(NOTE_C4, 100), Note(NOTE_D4, 100), Note(NOTE_E4, 100), 
            Note(NOTE_F4, 100), Note(NOTE_G4, 100), Note(NOTE_A4, 100),
            Note(NOTE_B4, 100), Note(NOTE_C5, 300)
        };
    }
    
    void jouerDemarrage() {
        // Mélodie de démarrage (petite fanfare)
        std::vector<Note> melodieDemarrage = {
            Note(NOTE_C4, 150), Note(NOTE_E4, 150), Note(NOTE_G4, 150),
            Note(NOTE_C5, 300), Note(0, 100), Note(NOTE_G4, 150), Note(NOTE_C5, 300)
        };
        
        jouerMelodie(melodieDemarrage);
    }
    
    void jouerMelodie(const std::vector<Note>& melodie) {
        if (melodie.empty()) return;
        
        // Arrêter la mélodie en cours
        noTone(BUZZER_PIN);
        
        // Configurer la nouvelle mélodie
        _melodieActuelle = melodie;
        _noteActuelle = 0;
        _enLecture = true;
        
        // Jouer la première note
        const Note& note = _melodieActuelle[0];
        if (note.frequence > 0) {
            tone(BUZZER_PIN, note.frequence, note.duree);
        }
        
        // Programmer le prochain changement
        _prochainChangement = millis() + note.duree;
    }
};

// Instance globale
BuzzerManager buzzerManager;

// Fonctions à exposer
void initialiserBuzzer() {
    buzzerManager.initialiser();
}

void mettreAJourBuzzer() {
    buzzerManager.mettreAJour();
}

void exprimerBuzzer(int emotion) {
    buzzerManager.exprimer(static_cast<EmotionBase>(emotion));
}

void jouerBip() {
    buzzerManager.jouerBip();
}

void arreterBuzzer() {
    buzzerManager.arreter();
}

void setBuzzerActif(bool actif) {
    buzzerManager.setActif(actif);
}
