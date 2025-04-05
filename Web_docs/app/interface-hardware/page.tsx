import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function InterfaceHardwarePage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Matériel</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Cette section détaille les composants matériels utilisés dans le robot, 
                leurs caractéristiques techniques et leurs rôles dans le système.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Microcontrôleur principal</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="col-span-1">
                    <img
                      src="/placeholder.svg?height=250&width=250"
                      alt="ESP32 Dev Board"
                      className="rounded-lg shadow-md w-full"
                    />
                  </div>
                  <div className="col-span-2">
                    <h3 className="text-xl font-bold mb-3">ESP32 Dev Board</h3>
                    <p className="mb-3">
                      L&apos;ESP32 est le cœur du robot, gérant toutes les entrées/sorties et la communication.
                    </p>
                    <div className="p-3 rounded-md bg-muted mb-3">
                      <h4 className="font-semibold mb-2">Caractéristiques techniques</h4>
                      <ul className="ml-4 list-disc space-y-1">
                        <li>Processeur dual-core 240 MHz</li>
                        <li>520 Ko de SRAM</li>
                        <li>Wi-Fi 802.11 b/g/n</li>
                        <li>Bluetooth 4.2 et BLE</li>
                        <li>36 GPIO pins</li>
                        <li>18 canaux ADC 12-bit</li>
                        <li>2 DACs 8-bit</li>
                      </ul>
                    </div>
                    <p>
                      Cette plateforme offre une excellente combinaison de puissance de traitement, 
                      de connectivité et d&apos;efficacité énergétique, ce qui en fait un choix idéal 
                      pour un robot autonome et interactif.
                    </p>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Capteurs</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">APDS9960</h3>
                    <p className="mb-2">Capteur de gestes, couleurs et proximité</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Capteur APDS9960"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Interface I2C</li>
                          <li>Détection de proximité jusqu&apos;à 20 cm</li>
                          <li>Reconnaissance de gestes</li>
                          <li>Détection de couleur RGB</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">BME280</h3>
                    <p className="mb-2">Capteur de température, humidité et pression</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Capteur BME280"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Interface I2C</li>
                          <li>Précision de ±0.5°C</li>
                          <li>Mesure d&apos;humidité relative ±3%</li>
                          <li>Mesure de pression ±1 hPa</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">MAX9814</h3>
                    <p className="mb-2">Module microphone avec amplificateur</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Module MAX9814"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Gain automatique</li>
                          <li>Faible bruit</li>
                          <li>Sortie analogique</li>
                          <li>Alimentation 3-5V</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">TTP223B</h3>
                    <p className="mb-2">Capteurs tactiles capacitifs</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Capteurs TTP223B"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Interface digitale</li>
                          <li>Très faible consommation</li>
                          <li>Sensibilité réglable</li>
                          <li>Compatible 3.3V</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Actionneurs</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Servomoteurs SG90</h3>
                    <p className="mb-2">Moteurs pour mouvements précis</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Servomoteurs SG90"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Rotation 180°</li>
                          <li>Couple de 1.8 kg/cm</li>
                          <li>Contrôle PWM</li>
                          <li>Poids léger (9g)</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Module haut-parleur PAM8403</h3>
                    <p className="mb-2">Amplificateur audio et haut-parleur</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Module PAM8403"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>Classe D, 2x3W</li>
                          <li>Faible distortion</li>
                          <li>Alimentation 5V</li>
                          <li>Efficacité 90%</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Écran OLED SSD1306</h3>
                    <p className="mb-2">Écran pour les expressions faciales</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="Écran OLED SSD1306"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>128x64 pixels</li>
                          <li>Interface I2C</li>
                          <li>Monochrome</li>
                          <li>Contraste élevé</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">LEDs RGB adressables WS2812B</h3>
                    <p className="mb-2">LEDs pour l&apos;ambiance et signalisation</p>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <img
                          src="/placeholder.svg?height=120&width=120"
                          alt="LEDs WS2812B"
                          className="rounded-lg shadow-sm w-full"
                        />
                      </div>
                      <div>
                        <ul className="ml-4 list-disc text-sm">
                          <li>RGB 24-bit</li>
                          <li>Contrôle individuel</li>
                          <li>Protocole NeoPixel</li>
                          <li>5V de fonctionnement</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Alimentation</h2>
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Système d&apos;alimentation</h3>
                  <p className="mb-3">
                    Le robot est alimenté par une batterie LiPo rechargeable, avec un circuit de gestion de l&apos;alimentation.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-semibold mb-2">Batterie</h4>
                      <ul className="ml-4 list-disc">
                        <li>LiPo 3.7V 2000mAh</li>
                        <li>Autonomie de 3-4 heures</li>
                        <li>Rechargeable via USB-C</li>
                        <li>Protection contre la surcharge</li>
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">Régulation</h4>
                      <ul className="ml-4 list-disc">
                        <li>Module TP4056 pour la charge</li>
                        <li>Régulateur buck-boost pour 3.3V</li>
                        <li>Régulateur step-up pour 5V</li>
                        <li>Circuit de protection de batterie</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Serveur (NAS)</h2>
                <p className="mb-4">
                  Le cerveau du robot est hébergé sur un serveur NAS qui peut être n&apos;importe quel ordinateur 
                  capable d&apos;exécuter Docker et disposant des ressources nécessaires pour le LLM.
                </p>
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Configuration recommandée</h3>
                  <ul className="ml-4 list-disc">
                    <li>Processeur : Quad-core 2.0 GHz ou supérieur</li>
                    <li>RAM : 16 Go minimum (32 Go recommandé pour les LLM plus grands)</li>
                    <li>Stockage : 50 Go minimum d&apos;espace libre</li>
                    <li>GPU : Facultatif mais recommandé pour l&apos;accélération du LLM</li>
                    <li>Réseau : WiFi 5 GHz ou Ethernet pour une communication stable</li>
                    <li>OS : Linux (recommandé), Windows ou macOS avec Docker</li>
                  </ul>
                </div>
                <p className="mt-4">
                  Le serveur communique avec le robot via WiFi en utilisant le protocole WebSocket 
                  pour assurer une communication bidirectionnelle en temps réel.
                </p>
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