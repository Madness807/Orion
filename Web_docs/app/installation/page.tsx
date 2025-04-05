import { MainNav } from "@/components/main-nav"
import { DocHeader } from "@/components/doc-header"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function Installation() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section id="installation" className="mb-12">
              <h2 className="mb-4 text-3xl font-bold tracking-tight text-primary">⚙️ Installation</h2>

              <h3 className="mb-3 text-2xl font-semibold">Prérequis</h3>
              <ul className="ml-6 list-disc space-y-2 mb-6">
                <li>Docker & Docker Compose</li>
                <li>NAS avec 8 Go de RAM minimum</li>
                <li>Accès réseau au robot ESP32</li>
              </ul>

              <h3 className="mb-3 text-2xl font-semibold">Configuration</h3>
              <pre className="rounded-md bg-muted p-4 overflow-x-auto mb-6">
                <code>{`cp .env.example .env
nano .env`}</code>
              </pre>

              <h3 className="mb-3 text-2xl font-semibold">Télécharger un modèle LLM</h3>
              <pre className="rounded-md bg-muted p-4 overflow-x-auto mb-6">
                <code>{`mkdir -p llm/models
# Exemple :
wget https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf -O llm/models/llama-3-8b-instruct.gguf`}</code>
              </pre>

              <h3 className="mb-3 text-2xl font-semibold">Démarrage</h3>
              <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                <code>{`docker-compose up -d`}</code>
              </pre>
            </section>

            <div className="flex justify-between">
              <a
                href="/"
                className="inline-flex items-center justify-center rounded-md bg-muted px-6 py-3 text-lg font-medium shadow transition-colors hover:bg-muted/90"
              >
                ← Retour à l&apos;accueil
              </a>
              <a
                href="/architecture"
                className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-lg font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
              >
                Architecture →
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

