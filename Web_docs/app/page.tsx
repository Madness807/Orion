import { MainNav } from "@/components/main-nav"
import { DocHeader } from "@/components/doc-header"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section id="introduction" className="mb-12">
              <h2 className="mb-4 text-3xl font-bold tracking-tight text-primary">Introduction</h2>
              <p className="mb-4">
                Ce projet vise à créer un <strong>robot expressif, intelligent et mignon</strong>, capable
                d&apos;interagir avec son environnement de manière contextuelle et émotionnelle.
              </p>
              <p className="mb-4">Il combine :</p>
              <ul className="ml-6 list-disc space-y-2">
                <li>La modularité d&apos;un ESP32 pour le corps (capteurs, moteurs)</li>
                <li>La puissance d&apos;un NAS pour le cerveau (LLM, mémoire, API)</li>
                <li>
                  Une communication via le <strong>protocole MCP (Model Context Protocol)</strong>
                </li>
              </ul>
              <div className="my-8 flex justify-center">
                <img
                  src="/WhatsApp Image 2025-04-04 à 15.18.44_cbdaf525.jpg"
                  alt="Robot mignon Orion"
                  className="rounded-lg shadow-md"
                  width={600}
                  height={400}
                />
              </div>
            </section>

            <section id="fonctionnalites" className="mb-12">
              <h2 className="mb-4 text-3xl font-bold tracking-tight text-primary">🧠 Fonctionnalités principales</h2>
              <ul className="ml-6 list-disc space-y-2">
                <li>Système sensoriel complet : son, vision, toucher, température...</li>
                <li>Carte émotionnelle avec 9 émotions</li>
                <li>Intelligence artificielle avec LLM (LLaMA 3 ou autre)</li>
                <li>Mémoire à long terme via PostgreSQL</li>
                <li>Synthèse et reconnaissance vocale</li>
                <li>Interface web de contrôle</li>
                <li>Communication bidirectionnelle avec l&apos;ESP32</li>
              </ul>
            </section>

            <section id="structure" className="mb-12">
              <h2 className="mb-4 text-3xl font-bold tracking-tight text-primary">📂 Structure du projet</h2>
              <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                <code>{`robot-mignon/
├── serveur_mcp/         # Serveur FastAPI + gestion du protocole MCP
├── llm/                 # Interface avec le modèle de langage
├── memoire/             # Mémoire à long terme (PostgreSQL)
├── speech/              # Synthèse et reconnaissance vocale
├── vision/              # Vision par ordinateur
├── interface/           # Interface web (Flask)
├── tests/               # Tests unitaires et d'intégration
├── docker-compose.yml   # Orchestration des services
└── README.md            # Documentation principale`}</code>
              </pre>
            </section>

            <div className="flex justify-center">
              <a
                href="/installation"
                className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-lg font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
              >
                Continuer vers l&apos;installation →
              </a>
            </div>
          </div>
        </main>
      </div>
      <Footer />
      <BackToTop />
    </div>
  )
}

