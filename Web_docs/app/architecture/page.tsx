import { MainNav } from "@/components/main-nav"
import { DocHeader } from "@/components/doc-header"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function Architecture() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section id="architecture" className="mb-12">
              <h2 className="mb-4 text-3xl font-bold tracking-tight text-primary">🧹 Architecture Docker</h2>
              <p className="mb-4">Chaque service est containerisé et interconnecté.</p>

              <h3 className="mb-3 text-2xl font-semibold">Services</h3>
              <div className="overflow-x-auto mb-6">
                <table className="w-full border-collapse">
                  <thead>
                    <tr>
                      <th className="border border-muted-foreground bg-muted p-2 text-left">Service</th>
                      <th className="border border-muted-foreground bg-muted p-2 text-left">Rôle</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="border border-muted-foreground p-2">
                        <code>mcp_server</code>
                      </td>
                      <td className="border border-muted-foreground p-2">
                        Serveur central (FastAPI) qui gère le protocole MCP et le contexte
                      </td>
                    </tr>
                    <tr>
                      <td className="border border-muted-foreground p-2">
                        <code>database</code>
                      </td>
                      <td className="border border-muted-foreground p-2">PostgreSQL pour la mémoire à long terme</td>
                    </tr>
                    <tr>
                      <td className="border border-muted-foreground p-2">
                        <code>web_interface</code>
                      </td>
                      <td className="border border-muted-foreground p-2">
                        Interface Flask (port 8000) pour l&apos;interaction utilisateur
                      </td>
                    </tr>
                    <tr>
                      <td className="border border-muted-foreground p-2">
                        <code>speech_service</code>
                      </td>
                      <td className="border border-muted-foreground p-2">STT/TTS pour la parole</td>
                    </tr>
                    <tr>
                      <td className="border border-muted-foreground p-2">
                        <code>vision_service</code>
                      </td>
                      <td className="border border-muted-foreground p-2">
                        Traitement d&apos;image et reconnaissance visuelle
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <h3 className="mb-3 text-2xl font-semibold">Schéma d&apos;architecture</h3>
              <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                <code>{`ESP32 <--> MCP Server <--> (Database, LLM, Speech, Vision)
                      |
                   Web Interface`}</code>
              </pre>
            </section>

            <div className="flex justify-between">
              <a
                href="/installation"
                className="inline-flex items-center justify-center rounded-md bg-muted px-6 py-3 text-lg font-medium shadow transition-colors hover:bg-muted/90"
              >
                ← Installation
              </a>
              <a
                href="/protocole"
                className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-lg font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
              >
                Protocole MCP →
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

