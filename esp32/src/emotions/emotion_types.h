#ifndef EMOTION_TYPES_H
#define EMOTION_TYPES_H

#include <Arduino.h>

// Énumération des émotions de base
enum class EmotionBase {
    JOIE,
    TRISTESSE,
    PEUR,
    COLERE,
    SURPRISE,
    DEGOUT,
    CONFIANCE,
    ANTICIPATION,
    NEUTRE
};

// Structure pour représenter une émotion composite
struct Emotion {
    // Niveaux des émotions de base (0-100)
    uint8_t joie = 0;
    uint8_t tristesse = 0;
    uint8_t peur = 0;
    uint8_t colere = 0;
    uint8_t surprise = 0;
    uint8_t degout = 0;
    uint8_t confiance = 0;
    uint8_t anticipation = 0;
    
    // Intensité globale de l'émotion
    uint8_t intensite = 0;
    
    // Timestamp de la dernière mise à jour
    unsigned long derniereMaj = 0;
    
    // Émotions nommées (presets) pour faciliter l'utilisation
    static Emotion neutre() {
        Emotion e;
        e.intensite = 0;
        return e;
    }
    
    static Emotion joie(uint8_t intensite = 100) {
        Emotion e;
        e.joie = intensite;
        e.intensite = intensite;
        return e;
    }
    
    static Emotion tristesse(uint8_t intensite = 100) {
        Emotion e;
        e.tristesse = intensite;
        e.intensite = intensite;
        return e;
    }
    
    static Emotion peur(uint8_t intensite = 100) {
        Emotion e;
        e.peur = intensite;
        e.intensite = intensite;
        return e;
    }
    
    static Emotion colere(uint8_t intensite = 100) {
        Emotion e;
        e.colere = intensite;
        e.intensite = intensite;
        return e;
    }
    
    static Emotion surprise(uint8_t intensite = 100) {
        Emotion e;
        e.surprise = intensite;
        e.intensite = intensite;
        return e;
    }
    
    static Emotion curieux() {
        Emotion e;
        e.anticipation = 70;
        e.surprise = 30;
        e.intensite = 50;
        return e;
    }
    
    static Emotion inquiet() {
        Emotion e;
        e.peur = 50;
        e.anticipation = 50;
        e.intensite = 40;
        return e;
    }
    
    // Identifie l'émotion dominante
    EmotionBase getDominante() const {
        uint8_t max = 0;
        EmotionBase dominante = EmotionBase::NEUTRE;
        
        if (joie > max) { max = joie; dominante = EmotionBase::JOIE; }
        if (tristesse > max) { max = tristesse; dominante = EmotionBase::TRISTESSE; }
        if (peur > max) { max = peur; dominante = EmotionBase::PEUR; }
        if (colere > max) { max = colere; dominante = EmotionBase::COLERE; }
        if (surprise > max) { max = surprise; dominante = EmotionBase::SURPRISE; }
        if (degout > max) { max = degout; dominante = EmotionBase::DEGOUT; }
        if (confiance > max) { max = confiance; dominante = EmotionBase::CONFIANCE; }
        if (anticipation > max) { max = anticipation; dominante = EmotionBase::ANTICIPATION; }
        
        return dominante;
    }
    
    // Converti l'émotion dominante en chaîne
    const char* getNom() const {
        switch(getDominante()) {
            case EmotionBase::JOIE: return "Joie";
            case EmotionBase::TRISTESSE: return "Tristesse";
            case EmotionBase::PEUR: return "Peur";
            case EmotionBase::COLERE: return "Colère";
            case EmotionBase::SURPRISE: return "Surprise";
            case EmotionBase::DEGOUT: return "Dégoût";
            case EmotionBase::CONFIANCE: return "Confiance";
            case EmotionBase::ANTICIPATION: return "Anticipation";
            case EmotionBase::NEUTRE: return "Neutre";
            default: return "Inconnu";
        }
    }
};

// Structure pour un événement déclencheur d'émotion
struct EvenementEmotionnel {
    const char* source;      // Source de l'événement (capteur, etc.)
    const char* type;        // Type d'événement (toucher, son fort, etc.)
    Emotion emotion;         // Émotion associée
    uint8_t importance;      // Importance de l'événement (0-100)
    unsigned long timestamp; // Timestamp de l'événement
    
    EvenementEmotionnel(const char* src, const char* t, const Emotion& e, uint8_t imp) 
        : source(src), type(t), emotion(e), importance(imp), timestamp(millis()) {}
};

#endif // EMOTION_TYPES_H
