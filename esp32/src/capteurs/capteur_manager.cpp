#include "capteur_manager.h"
#include <algorithm>

CapteurManager& CapteurManager::getInstance() {
    static CapteurManager instance;
    return instance;
}

CapteurManager::CapteurManager() {
    // Le constructeur est privé pour le pattern singleton
}

void CapteurManager::initialiserTousCapteurs() {
    for (auto& capteur : _capteurs) {
        if (capteur->estActif()) {
            capteur->initialiser();
            Serial.printf("Capteur %s initialisé\n", capteur->getNom());
        }
    }
}

void CapteurManager::lireTousCapteurs() {
    for (auto& capteur : _capteurs) {
        if (capteur->estActif()) {
            capteur->lire();
        }
    }
}

void CapteurManager::ajouterCapteur(std::shared_ptr<Capteur> capteur) {
    _capteurs.push_back(capteur);
}

std::shared_ptr<Capteur> CapteurManager::getCapteur(const char* nom) {
    auto it = std::find_if(_capteurs.begin(), _capteurs.end(),
        [nom](const std::shared_ptr<Capteur>& c) {
            return strcmp(c->getNom(), nom) == 0;
        });
    
    if (it != _capteurs.end()) {
        return *it;
    }
    
    return nullptr;
}

std::shared_ptr<CapteurProprio> CapteurManager::getProprio() {
    auto capteur = getCapteur("Proprioception");
    return std::static_pointer_cast<CapteurProprio>(capteur);
}

std::shared_ptr<CapteurToucher> CapteurManager::getToucher() {
    auto capteur = getCapteur("Toucher");
    return std::static_pointer_cast<CapteurToucher>(capteur);
}

std::shared_ptr<CapteurMagnetisme> CapteurManager::getMagnetisme() {
    auto capteur = getCapteur("Magnetisme");
    return std::static_pointer_cast<CapteurMagnetisme>(capteur);
}

std::shared_ptr<CapteurTemperature> CapteurManager::getTemperature() {
    auto capteur = getCapteur("Temperature");
    return std::static_pointer_cast<CapteurTemperature>(capteur);
}

std::shared_ptr<CapteurHumidite> CapteurManager::getHumidite() {
    auto capteur = getCapteur("Humidite");
    return std::static_pointer_cast<CapteurHumidite>(capteur);
}

std::shared_ptr<CapteurVue> CapteurManager::getVue() {
    auto capteur = getCapteur("Vue");
    return std::static_pointer_cast<CapteurVue>(capteur);
}

std::shared_ptr<CapteurOuie> CapteurManager::getOuie() {
    auto capteur = getCapteur("Ouie");
    return std::static_pointer_cast<CapteurOuie>(capteur);
}
