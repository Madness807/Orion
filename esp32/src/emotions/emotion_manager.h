#ifndef EMOTION_MANAGER_H
#define EMOTION_MANAGER_H

#include <Arduino.h>
#include <queue>
#include <vector>
#include "emotion_types.h"

// Définition de la capacité maximale de la file d'événements émotionnels
#define MAX_QUEUE_SIZE 20

// Déclaration anticipée pour éviter les dépendances circulaires
class ExpressionManager;

class EmotionManager {
public:
    static EmotionManager& getInstance();
    
    // Initialise le gestionnaire d'émotions
    void initialiser();
    
    // Met à jour l'état émotionnel (à appeler régulièrement)
    void mettreAJour();
    
    // Ajoute un événement émotionnel à la file
    void ajouterEvenement(const EvenementEmotionnel& evt);
    
    // Crée et ajoute un événement émotionnel
    void ajouterEvenement(const char* source, const char* type, 
                         const Emotion& emotion, uint8_t importance);
    
    // Accesseur pour l'émotion actuelle
    const Emotion& getEmotionActuelle() const { return _emotionActuelle; }
    
    // Accesseur pour la tendance émotionnelle (personnalité)
    const Emotion& getTendance() const { return _tendanceEmotionnelle; }
    
    // Modifie la tendance émotionnelle
    void setTendance(const Emotion& tendance);
    
    // Calcule le score de similarité entre deux émotions (0-100)
    static uint8_t similarite(const Emotion& a, const Emotion& b);
    
    // Connexion avec le gestionnaire d'expressions
    void setExpressionManager(ExpressionManager* expMan) { _expressionManager = expMan; }
    
private:
    EmotionManager();
    ~EmotionManager() = default;
    EmotionManager(const EmotionManager&) = delete;
    EmotionManager& operator=(const EmotionManager&) = delete;
    
    // Traite les événements émotionnels de la file
    void traiterEvenements();
    
    // Applique un événement émotionnel à l'état actuel
    void appliquerEvenement(const EvenementEmotionnel& evt);
    
    // Fait évoluer naturellement l'émotion actuelle (retour à la tendance)
    void evoluerNaturellement();
    
    // Émotion actuelle
    Emotion _emotionActuelle;
    
    // Tendance émotionnelle (personnalité)
    Emotion _tendanceEmotionnelle;
    
    // File d'événements émotionnels à traiter
    std::queue<EvenementEmotionnel> _evenements;
    
    // Historique des émotions récentes
    std::vector<Emotion> _historique;
    
    // Dernier instant de mise à jour
    unsigned long _derniereMaj = 0;
    
    // Paramètres de configuration
    float _tauxRetourTendance = 0.05;  // Vitesse de retour à la tendance (0.0-1.0)
    uint8_t _seuilExpression = 30;     // Seuil d'intensité pour déclencher une expression
    
    // Pointeur vers le gestionnaire d'expressions
    ExpressionManager* _expressionManager = nullptr;
};

#endif // EMOTION_MANAGER_H
