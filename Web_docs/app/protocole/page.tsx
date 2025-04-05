import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function ProtocolePage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Protocole MCP</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Le protocole MCP (Model Context Protocol) est le cœur de la communication entre l&apos;ESP32 (corps du robot) et le NAS (cerveau).
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Principe de fonctionnement</h2>
                <p className="mb-4">
                  Le protocole MCP permet de transmettre des informations contextuelles entre le robot et son &quot;cerveau&quot;. Il s&apos;agit d&apos;un protocole bidirectionnel qui :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Transmet les données des capteurs vers le LLM</li>
                  <li>Envoie les commandes d&apos;actions du LLM vers l&apos;ESP32</li>
                  <li>Associe les données à des émotions et contextes</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Structure des messages</h2>
                <p className="mb-4">
                  Les messages MCP sont formatés en JSON et contiennent des champs essentiels :
                </p>
                <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                  <code>{`{
  "type": "SENSOR_DATA",      // Type de message
  "timestamp": 1680123456,    // Horodatage
  "data": {                   // Données spécifiques au message
    "sensor": "temperature",
    "value": 24.5,
    "unit": "C"
  },
  "context": {                // Contexte optionnel
    "emotion": "curious",
    "intensity": 0.7
  }
}`}</code>
                </pre>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Types de messages</h2>
                <ul className="ml-6 list-disc space-y-2">
                  <li><strong>SENSOR_DATA</strong> : Envoi de données des capteurs</li>
                  <li><strong>ACTION_COMMAND</strong> : Commande d&apos;action à exécuter</li>
                  <li><strong>EMOTION_UPDATE</strong> : Mise à jour de l&apos;état émotionnel</li>
                  <li><strong>SYSTEM_STATUS</strong> : État du système</li>
                  <li><strong>ERROR</strong> : Message d&apos;erreur</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Implémentation</h2>
                <p className="mb-4">
                  Le protocole est implémenté à la fois côté ESP32 (en C++) et côté serveur (en Python). Les messages sont transmis via WebSockets pour assurer une communication en temps réel.
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