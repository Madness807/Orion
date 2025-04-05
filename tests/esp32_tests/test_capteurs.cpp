#include <Arduino.h>
#include <unity.h>
#include "../esp32/src/capteurs/capteur_manager.h"

// Mock des fonctions Arduino pour tests
int g_touchReadValues[10] = {100, 100, 100, 100, 100, 100, 100, 100, 100, 100};

// Fonction mock pour touchRead
uint16_t touchRead(uint8_t pin) {
    // Retourne la valeur mockée pour le pin donné
    return g_touchReadValues[pin];
}

// Déclaration de test pour le constructeur de CapteurToucher
void test_capteur_toucher_initialisation() {
    // Créer un capteur de toucher
    auto toucher = std::make_shared<CapteurToucher>();
    
    // Vérifier que le capteur est initialisé correctement
    TEST_ASSERT_EQUAL_STRING("Toucher", toucher->getNom());
    TEST_ASSERT_TRUE(toucher->estActif());
    
    // Initialiser le capteur
    toucher->initialiser();
    
    // Vérifier qu'aucun toucher n'est détecté initialement
    TEST_ASSERT_FALSE(toucher->estToucheQuelquePart());
    
    for (int i = 0; i < 10; i++) {
        TEST_ASSERT_FALSE(toucher->estTouche(i));
    }
}

// Test de la détection de toucher
void test_capteur_toucher_detection() {
    // Créer un capteur de toucher
    auto toucher = std::make_shared<CapteurToucher>();
    toucher->initialiser();
    
    // Simuler un toucher sur le capteur 2 (en dessous du seuil de 40)
    g_touchReadValues[2] = 30;
    
    // Lire les capteurs
    toucher->lire();
    
    // Vérifier que le toucher est détecté sur le capteur 2 uniquement
    TEST_ASSERT_TRUE(toucher->estToucheQuelquePart());
    TEST_ASSERT_TRUE(toucher->estTouche(2));
    
    for (int i = 0; i < 10; i++) {
        if (i != 2) {
            TEST_ASSERT_FALSE(toucher->estTouche(i));
        }
    }
    
    // Vérifier que la valeur correcte est retournée
    TEST_ASSERT_EQUAL(30, toucher->getValeur(2));
}

// Test de la désactivation du capteur
void test_capteur_toucher_desactivation() {
    // Créer un capteur de toucher
    auto toucher = std::make_shared<CapteurToucher>();
    toucher->initialiser();
    
    // Simuler un toucher sur le capteur 1
    g_touchReadValues[1] = 30;
    
    // Désactiver le capteur
    toucher->setActif(false);
    
    // Lire les capteurs (ne devrait pas mettre à jour les valeurs car désactivé)
    toucher->lire();
    
    // Vérifier qu'aucun toucher n'est détecté malgré g_touchReadValues[1] = 30
    TEST_ASSERT_FALSE(toucher->estToucheQuelquePart());
    TEST_ASSERT_FALSE(toucher->estTouche(1));
}

// Test du gestionnaire de capteurs
void test_capteur_manager() {
    // Obtenir l'instance du gestionnaire
    auto& manager = CapteurManager::getInstance();
    
    // Ajouter un capteur de toucher
    auto toucher = std::make_shared<CapteurToucher>();
    manager.ajouterCapteur(toucher);
    
    // Vérifier que le capteur est accessible via le gestionnaire
    auto recupere = manager.getCapteur("Toucher");
    TEST_ASSERT_NOT_NULL(recupere.get());
    
    // Vérifier que c'est bien un CapteurToucher
    auto toucherRecupere = manager.getToucher();
    TEST_ASSERT_NOT_NULL(toucherRecupere.get());
    TEST_ASSERT_EQUAL_STRING("Toucher", toucherRecupere->getNom());
    
    // Initialiser tous les capteurs
    manager.initialiserTousCapteurs();
    
    // Simuler un toucher
    g_touchReadValues[3] = 20;
    
    // Lire tous les capteurs
    manager.lireTousCapteurs();
    
    // Vérifier la détection via le gestionnaire
    TEST_ASSERT_TRUE(toucherRecupere->estTouche(3));
}

void setup() {
    // Délai pour stabiliser la connexion série
    delay(2000);
    
    // Initialiser la communication série à 115200 bauds
    Serial.begin(115200);
    
    // Exécuter les tests
    UNITY_BEGIN();
    
    RUN_TEST(test_capteur_toucher_initialisation);
    RUN_TEST(test_capteur_toucher_detection);
    RUN_TEST(test_capteur_toucher_desactivation);
    RUN_TEST(test_capteur_manager);
    
    UNITY_END();
}

void loop() {
    // Rien à faire ici pour les tests
}
