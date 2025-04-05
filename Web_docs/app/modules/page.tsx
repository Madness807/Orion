import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function ModulesPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Modules</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Le robot est conçu de manière modulaire, ce qui permet d&apos;ajouter, modifier ou retirer 
                facilement des composants selon les besoins du projet.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Modules ESP32</h2>
                <p className="mb-4">
                  Ces modules fonctionnent sur le microcontrôleur ESP32 et gèrent les aspects physiques du robot.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Capteurs</h3>
                    <p className="mb-2">Gère tous les capteurs et transmet les données au serveur.</p>
                    <ul className="ml-4 list-disc">
                      <li>Capteurs de température, lumière, son</li>
                      <li>Caméra pour la vision</li>
                      <li>Microphone pour le son</li>
                      <li>Détecteurs de proximité et de mouvement</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Moteurs</h3>
                    <p className="mb-2">Contrôle les mouvements physiques du robot.</p>
                    <ul className="ml-4 list-disc">
                      <li>Servomoteurs pour les mouvements précis</li>
                      <li>Moteurs DC pour la propulsion</li>
                      <li>Contrôle PWM pour la vitesse</li>
                    </ul>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Émotions</h3>
                    <p className="mb-2">Gère les expressions émotionnelles du robot.</p>
                    <ul className="ml-4 list-disc">
                      <li>Écran LED pour le visage</li>
                      <li>Haut-parleur pour les sons</li>
                      <li>LEDs RGB pour l&apos;ambiance</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Communication</h3>
                    <p className="mb-2">Gère les communications avec le serveur.</p>
                    <ul className="ml-4 list-disc">
                      <li>WiFi pour la connexion au réseau</li>
                      <li>Implémentation du protocole MCP</li>
                      <li>Gestion des connexions WebSocket</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Modules Serveur (NAS)</h2>
                <p className="mb-4">
                  Ces modules fonctionnent sur le serveur NAS et gèrent les aspects &quot;cérébraux&quot; du robot.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module LLM</h3>
                    <p className="mb-2">Interface avec le modèle de langage.</p>
                    <ul className="ml-4 list-disc">
                      <li>Intégration avec LLaMA 3 ou autre LLM</li>
                      <li>Construction de prompts contextuels</li>
                      <li>Analyse des réponses et extraction d&apos;actions</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Mémoire</h3>
                    <p className="mb-2">Gère la mémoire à long terme du robot.</p>
                    <ul className="ml-4 list-disc">
                      <li>Base de données PostgreSQL</li>
                      <li>Stockage vectoriel pour recherche sémantique</li>
                      <li>Journalisation des événements et interactions</li>
                    </ul>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Vocal</h3>
                    <p className="mb-2">Gère la reconnaissance et la synthèse vocale.</p>
                    <ul className="ml-4 list-disc">
                      <li>Reconnaissance vocale en temps réel</li>
                      <li>Synthèse vocale pour réponses</li>
                      <li>Analyse du ton et des émotions</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module Vision</h3>
                    <p className="mb-2">Analyse les images capturées par le robot.</p>
                    <ul className="ml-4 list-disc">
                      <li>Reconnaissance d&apos;objets</li>
                      <li>Détection de visages et d&apos;expressions</li>
                      <li>Analyse de scène et navigation</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Création de nouveaux modules</h2>
                <p className="mb-4">
                  L&apos;architecture modulaire permet d&apos;étendre facilement les capacités du robot :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Chaque module doit implémenter l&apos;interface de base correspondante</li>
                  <li>Les nouveaux modules sont automatiquement détectés au démarrage</li>
                  <li>Documentation complète disponible pour le développement de modules personnalisés</li>
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