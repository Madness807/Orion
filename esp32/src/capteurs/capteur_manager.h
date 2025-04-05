#ifndef CAPTEUR_MANAGER_H
#define CAPTEUR_MANAGER_H

#include <Arduino.h>
#include <vector>
#include <memory>

// Classe de base pour tous les capteurs
class Capteur {
public:
    virtual ~Capteur() = default;
    virtual void initialiser() = 0;
    virtual void lire() = 0;
    virtual const char* getNom() const = 0;
    virtual bool estActif() const { return _actif; }
    virtual void setActif(bool actif) { _actif = actif; }

protected:
    bool _actif = true;
};

// Déclarations anticipées des classes de capteurs spécifiques
class CapteurProprio : public Capteur;
class CapteurToucher : public Capteur;
class CapteurMagnetisme : public Capteur;
class CapteurTemperature : public Capteur;
class CapteurHumidite : public Capteur;
class CapteurVue : public Capteur;
class CapteurOuie : public Capteur;

// Gestionnaire central des capteurs
class CapteurManager {
public:
    static CapteurManager& getInstance();
    
    void initialiserTousCapteurs();
    void lireTousCapteurs();
    
    void ajouterCapteur(std::shared_ptr<Capteur> capteur);
    std::shared_ptr<Capteur> getCapteur(const char* nom);
    
    // Raccourcis pour accéder aux capteurs spécifiques
    std::shared_ptr<CapteurProprio> getProprio();
    std::shared_ptr<CapteurToucher> getToucher();
    std::shared_ptr<CapteurMagnetisme> getMagnetisme();
    std::shared_ptr<CapteurTemperature> getTemperature();
    std::shared_ptr<CapteurHumidite> getHumidite();
    std::shared_ptr<CapteurVue> getVue();
    std::shared_ptr<CapteurOuie> getOuie();

private:
    CapteurManager();
    ~CapteurManager() = default;
    CapteurManager(const CapteurManager&) = delete;
    CapteurManager& operator=(const CapteurManager&) = delete;
    
    std::vector<std::shared_ptr<Capteur>> _capteurs;
};

#endif // CAPTEUR_MANAGER_H
