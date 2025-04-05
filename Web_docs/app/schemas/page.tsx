import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function SchemasPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Schémas</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Cette section présente les schémas techniques du robot, incluant les circuits électroniques,
                les connexions des composants et l&apos;architecture logicielle.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Schéma du circuit principal</h2>
                <p className="mb-4">
                  Le circuit principal est centré autour de l&apos;ESP32 et connecte tous les capteurs et actionneurs :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=400&width=600"
                    alt="Schéma du circuit principal"
                    className="rounded-lg shadow-md"
                    width={600}
                    height={400}
                  />
                </div>
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Composants principaux</h3>
                  <ul className="ml-4 list-disc">
                    <li>ESP32 (microcontrôleur principal)</li>
                    <li>Module d&apos;alimentation (régulateurs 3.3V et 5V)</li>
                    <li>Connecteurs I2C pour les capteurs</li>
                    <li>Contrôleurs pour servomoteurs</li>
                    <li>Pilotes pour les LEDs RGB</li>
                    <li>Amplificateur audio</li>
                  </ul>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Schéma de connexion des capteurs</h2>
                <p className="mb-4">
                  Détail des connexions pour les différents capteurs utilisés dans le robot :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=350&width=600"
                    alt="Schéma de connexion des capteurs"
                    className="rounded-lg shadow-md"
                    width={600}
                    height={350}
                  />
                </div>
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Connectivité des capteurs</h3>
                  <pre className="overflow-x-auto">
                    <code>{`// Connexions I2C
SDA -> GPIO 21
SCL -> GPIO 22

// Capteur APDS9960 (vue)
VIN -> 3.3V
GND -> GND
SDA -> GPIO 21
SCL -> GPIO 22
INT -> GPIO 4

// Capteur BME280 (température/humidité)
VIN -> 3.3V
GND -> GND
SDA -> GPIO 21
SCL -> GPIO 22

// Capteur sonore (MAX9814)
VCC -> 5V
GND -> GND
OUT -> GPIO 36 (ADC)`}</code>
                  </pre>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Architecture du système</h2>
                <p className="mb-4">
                  Vue d&apos;ensemble de l&apos;architecture système, montrant l&apos;interaction entre l&apos;ESP32 et le serveur NAS :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=400&width=700"
                    alt="Architecture du système"
                    className="rounded-lg shadow-md"
                    width={700}
                    height={400}
                  />
                </div>
                <p className="mb-4">
                  L&apos;architecture est divisée en deux parties principales qui communiquent via le protocole MCP :
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">ESP32 (Corps)</h3>
                    <ul className="ml-4 list-disc">
                      <li>Gestion des capteurs et actionneurs</li>
                      <li>Traitement de signal de base</li>
                      <li>Communication WiFi</li>
                      <li>Contrôle des expressions</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Serveur NAS (Cerveau)</h3>
                    <ul className="ml-4 list-disc">
                      <li>Modèle de langage (LLM)</li>
                      <li>Base de données et mémoire</li>
                      <li>Traitement audio et visuel avancé</li>
                      <li>Interface web de contrôle</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Modèle 3D</h2>
                <p className="mb-4">
                  Schéma du modèle 3D pour l&apos;impression du boîtier et des pièces mobiles :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=350&width=600"
                    alt="Modèle 3D du robot"
                    className="rounded-lg shadow-md"
                    width={600}
                    height={350}
                  />
                </div>
                <p className="mb-4">
                  Les fichiers STL sont disponibles dans le dépôt du projet pour impression 3D. 
                  Le boîtier est conçu pour accueillir tous les composants électroniques et permettre 
                  un accès facile pour la maintenance.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Diagramme de flux de données</h2>
                <p className="mb-4">
                  Ce diagramme montre comment les données circulent dans le système :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=350&width=600"
                    alt="Diagramme de flux de données"
                    className="rounded-lg shadow-md"
                    width={600}
                    height={350}
                  />
                </div>
                <p className="mb-4">
                  Le flux de données suit généralement ce chemin :
                </p>
                <ol className="ml-6 list-decimal space-y-2">
                  <li>Capture des données par les capteurs</li>
                  <li>Prétraitement sur l&apos;ESP32</li>
                  <li>Transmission au serveur via MCP</li>
                  <li>Traitement et interprétation par le LLM</li>
                  <li>Génération des commandes d&apos;action</li>
                  <li>Transmission des commandes à l&apos;ESP32</li>
                  <li>Exécution des actions par les actionneurs</li>
                </ol>
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