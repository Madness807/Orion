import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function CapteursPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Capteurs</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Les capteurs constituent les "sens" du robot, lui permettant de percevoir et d'interagir 
                avec son environnement de manière contextuelle.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Architecture des capteurs</h2>
                <p className="mb-4">
                  Le système de capteurs est conçu de manière modulaire, avec une classe de base 
                  <code>Capteur</code> dont héritent tous les capteurs spécifiques.
                </p>
                <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                  <code>{`class Capteur {
protected:
    bool _actif = true;
    
public:
    virtual void initialiser() = 0;
    virtual void lire() = 0;
    virtual const char* getNom() const = 0;
    
    bool estActif() const { return _actif; }
    void setActif(bool actif) { _actif = actif; }
};`}</code>
                </pre>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Types de capteurs</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Capteur de vue (APDS9960)</h3>
                    <p className="mb-2">Détection de couleurs, proximité et gestes.</p>
                    <ul className="ml-4 list-disc">
                      <li>Détection de couleurs RGB</li>
                      <li>Mesure de proximité d'objets</li>
                      <li>Reconnaissance de gestes simples</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Capteur sonore (MAX9814)</h3>
                    <p className="mb-2">Détection et analyse de sons.</p>
                    <ul className="ml-4 list-disc">
                      <li>Détection du niveau sonore</li>
                      <li>Analyse de fréquence basique</li>
                      <li>Détection de la direction du son</li>
                    </ul>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Capteur tactile</h3>
                    <p className="mb-2">Capteurs capacitifs pour interactions tactiles.</p>
                    <ul className="ml-4 list-disc">
                      <li>Détection de toucher</li>
                      <li>Différenciation de zones tactiles</li>
                      <li>Mesure de pression relative</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Capteur de température (BME280)</h3>
                    <p className="mb-2">Mesure de la température et humidité.</p>
                    <ul className="ml-4 list-disc">
                      <li>Température ambiante précise</li>
                      <li>Niveau d'humidité</li>
                      <li>Pression atmosphérique</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Exemple d'implémentation</h2>
                <p className="mb-4">
                  Voici un extrait de l'implémentation du capteur de vue :
                </p>
                <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                  <code>{`class CapteurVue : public Capteur {
private:
    Adafruit_APDS9960 apds;
    uint16_t rouge, vert, bleu, clair;
    uint8_t proximite;
    bool objetDetecte;
    
public:
    virtual void initialiser() override {
        if (!apds.begin()) {
            Serial.println("Impossible de trouver le capteur APDS9960!");
            _actif = false;
            return;
        }
        apds.enableColor(true);
        apds.enableProximity(true);
    }
    
    virtual void lire() override {
        if (!_actif) return;
        
        // Lecture des couleurs
        if (apds.colorDataReady()) {
            apds.getColorData(&rouge, &vert, &bleu, &clair);
        }
        
        // Lecture de la proximité et détection d'objets
        proximite = apds.readProximity();
        detecterObjet();
    }
    
    // Autres méthodes spécifiques...
};`}</code>
                </pre>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Gestionnaire de capteurs</h2>
                <p className="mb-4">
                  Un gestionnaire centralisé s'occupe de l'initialisation et de la lecture régulière de tous les capteurs.
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Initialisation automatique de tous les capteurs au démarrage</li>
                  <li>Lecture périodique des données des capteurs</li>
                  <li>Transmission des données au système de traitement via le protocole MCP</li>
                  <li>Gestion des erreurs et reconfigurations automatiques</li>
                </ul>
              </section>
            </section>
          </div>
        </main>
      </div>
      <Footer />
      <BackToTop />
    </div>
  )
} 