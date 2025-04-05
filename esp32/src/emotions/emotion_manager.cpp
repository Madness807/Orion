#include "emotion_manager.h"
#include <cmath>

// Fonction statique pour obtenir l'instance singleton
EmotionManager& EmotionManager::getInstance() {
    static EmotionManager instance;
    return instance;
}

EmotionManager::EmotionManager() {
    // Initialisation par défaut
    _emotionActuelle = Emotion::neutre();
    
    // Configuration de la tendance (personnalité par défaut)
    _tendanceEmotionnelle = Emotion::neutre();
    _tendanceEmotionnelle.joie = 30;       // Robot légèrement joyeux par défaut
    _tendanceEmotionnelle.curiosite = 40;  // Robot plutôt curieux
    
    _derniereMaj = millis();
}

void EmotionManager::initialiser() {
    // Réinitialiser l'état émotionnel
    _emotionActuelle = _tendanceEmotionnelle;
    _historique.clear();
    
    // Vider la file d'événements
    while (!_evenements.empty()) {
        _evenements.pop();
    }
    
    Serial.println("Gestionnaire d'émotions initialisé");
}

void EmotionManager::mettreAJour() {
    unsigned long maintenant = millis();
    unsigned long deltaTemps = maintenant - _derniereMaj;
    
    // Limiter la fréquence de mise à jour à une fois toutes les 100ms
    if (deltaTemps < 100) return;
    
    _derniereMaj = maintenant;
    
    // Traiter les événements en file d'attente
    traiterEvenements();
    
    // Faire évoluer naturellement l'émotion actuelle
    evoluerNaturellement();
    
    // Enregistrer l'émotion dans l'historique (toutes les 5 secondes)
    static unsigned long dernierEnregistrement = 0;
    if (maintenant - dernierEnregistrement > 5000) {
        _historique.push_back(_emotionActuelle);
        
        // Limiter la taille de l'historique
        if (_historique.size() > 100) {
            _historique.erase(_historique.begin());
        }
        
        dernierEnregistrement = maintenant;
    }
    
    // Notifier un changement d'émotion si nécessaire
    static EmotionBase derniereEmotionExprimee = EmotionBase::NEUTRE;
    EmotionBase emotionActuelle = _emotionActuelle.getDominante();
    
    if (emotionActuelle != derniereEmotionExprimee && 
        _emotionActuelle.intensite >= _seuilExpression) {
        
        derniereEmotionExprimee = emotionActuelle;
        
        // Notifier le gestionnaire d'expressions si disponible
        if (_expressionManager != nullptr) {
            // Appel non implémenté ici car dépendance circulaire
            // _expressionManager->exprimer(_emotionActuelle);
            
            Serial.printf("Nouvelle émotion exprimée: %s (intensité: %d)\n", 
                        _emotionActuelle.getNom(), _emotionActuelle.intensite);
        }
    }
}

void EmotionManager::ajouterEvenement(const EvenementEmotionnel& evt) {
    // Éviter que la file ne devienne trop grande
    if (_evenements.size() >= MAX_QUEUE_SIZE) {
        _evenements.pop(); // Supprimer l'événement le plus ancien
    }
    
    // Ajouter le nouvel événement
    _evenements.push(evt);
}

void EmotionManager::ajouterEvenement(const char* source, const char* type, 
                                     const Emotion& emotion, uint8_t importance) {
    EvenementEmotionnel evt(source, type, emotion, importance);
    ajouterEvenement(evt);
}

void EmotionManager::setTendance(const Emotion& tendance) {
    _tendanceEmotionnelle = tendance;
    Serial.printf("Nouvelle tendance émotionnelle: %s\n", tendance.getNom());
}

void EmotionManager::traiterEvenements() {
    const int maxEvtParCycle = 5; // Limiter le nombre d'événements traités par cycle
    int compteur = 0;
    
    while (!_evenements.empty() && compteur < maxEvtParCycle) {
        // Obtenir le prochain événement
        EvenementEmotionnel evt = _evenements.front();
        _evenements.pop();
        
        // Appliquer l'événement à l'état émotionnel actuel
        appliquerEvenement(evt);
        
        compteur++;
    }
}

void EmotionManager::appliquerEvenement(const EvenementEmotionnel& evt) {
    // Calculer le poids de l'événement (dépend de son importance)
    float poids = evt.importance / 100.0;
    
    // Limiter l'influence des événements anciens
    unsigned long maintenant = millis();
    unsigned long age = maintenant - evt.timestamp;
    
    if (age > 5000) { // Plus de 5 secondes
        poids *= exp(-age / 5000.0); // Décroissance exponentielle
    }
    
    // Fusionner l'émotion de l'événement avec l'émotion actuelle
    Emotion& actuelle = _emotionActuelle;
    const Emotion& evtEmotion = evt.emotion;
    
    // Mise à jour pondérée de chaque composante émotionnelle
    actuelle.joie = (1.0 - poids) * actuelle.joie + poids * evtEmotion.joie;
    actuelle.tristesse = (1.0 - poids) * actuelle.tristesse + poids * evtEmotion.tristesse;
    actuelle.peur = (1.0 - poids) * actuelle.peur + poids * evtEmotion.peur;
    actuelle.colere = (1.0 - poids) * actuelle.colere + poids * evtEmotion.colere;
    actuelle.surprise = (1.0 - poids) * actuelle.surprise + poids * evtEmotion.surprise;
    actuelle.degout = (1.0 - poids) * actuelle.degout + poids * evtEmotion.degout;
    actuelle.confiance = (1.0 - poids) * actuelle.confiance + poids * evtEmotion.confiance;
    actuelle.anticipation = (1.0 - poids) * actuelle.anticipation + poids * evtEmotion.anticipation;
    
    // Mise à jour de l'intensité globale
    actuelle.intensite = (1.0 - poids) * actuelle.intensite + poids * evtEmotion.intensite;
    
    // Mettre à jour le timestamp
    actuelle.derniereMaj = maintenant;
    
    // Journaliser l'événement
    Serial.printf("Événement émotionnel: %s de %s - Émotion résultante: %s\n", 
                evt.type, evt.source, actuelle.getNom());
}

void EmotionManager::evoluerNaturellement() {
    // Faire évoluer l'émotion actuelle vers la tendance naturelle
    Emotion& actuelle = _emotionActuelle;
    const Emotion& tendance = _tendanceEmotionnelle;
    
    // Calcul du temps écoulé pour ajuster le taux de changement
    unsigned long maintenant = millis();
    float deltaTemps = (maintenant - actuelle.derniereMaj) / 1000.0; // en secondes
    
    // Facteur d'évolution qui dépend du temps écoulé
    float facteur = _tauxRetourTendance * deltaTemps;
    if (facteur > 1.0) facteur = 1.0; // Limiter à 100%
    
    // Evolution progressive vers la tendance
    actuelle.joie = (1.0 - facteur) * actuelle.joie + facteur * tendance.joie;
    actuelle.tristesse = (1.0 - facteur) * actuelle.tristesse + facteur * tendance.tristesse;
    actuelle.peur = (1.0 - facteur) * actuelle.peur + facteur * tendance.peur;
    actuelle.colere = (1.0 - facteur) * actuelle.colere + facteur * tendance.colere;
    actuelle.surprise = (1.0 - facteur) * actuelle.surprise + facteur * tendance.surprise;
    actuelle.degout = (1.0 - facteur) * actuelle.degout + facteur * tendance.degout;
    actuelle.confiance = (1.0 - facteur) * actuelle.confiance + facteur * tendance.confiance;
    actuelle.anticipation = (1.0 - facteur) * actuelle.anticipation + facteur * tendance.anticipation;
    
    // L'intensité diminue naturellement au fil du temps
    actuelle.intensite = (1.0 - facteur) * actuelle.intensite + facteur * tendance.intensite;
    
    // Mettre à jour le timestamp
    actuelle.derniereMaj = maintenant;
}

uint8_t EmotionManager::similarite(const Emotion& a, const Emotion& b) {
    // Calcul d'une distance Euclidienne dans l'espace des émotions
    float sumSquares = 
        pow(a.joie - b.joie, 2) +
        pow(a.tristesse - b.tristesse, 2) +
        pow(a.peur - b.peur, 2) +
        pow(a.colere - b.colere, 2) +
        pow(a.surprise - b.surprise, 2) +
        pow(a.degout - b.degout, 2) +
        pow(a.confiance - b.confiance, 2) +
        pow(a.anticipation - b.anticipation, 2);
    
    float distance = sqrt(sumSquares);
    
    // Convertir la distance (0-282.8) en similarité (0-100)
    // 282.8 est la distance maximale possible (racine carrée de 8*100²)
    float similarite = 100.0 * (1.0 - distance / 282.8);
    
    return (uint8_t)similarite;
}
