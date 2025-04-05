import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function EmotionsPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Système d&apos;émotions</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Le robot dispose d&apos;un système émotionnel complexe qui lui permet d&apos;exprimer et de ressentir 
                différentes émotions, rendant son comportement plus naturel et engageant.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Carte émotionnelle</h2>
                <p className="mb-4">
                  Le robot utilise une carte émotionnelle à deux dimensions :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li><strong>Axe X</strong> : Valence (négative à positive)</li>
                  <li><strong>Axe Y</strong> : Activation (calme à excité)</li>
                </ul>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=400&width=400"
                    alt="Carte émotionnelle du robot"
                    className="rounded-lg shadow-md"
                    width={400}
                    height={400}
                  />
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Émotions principales</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold text-yellow-500 mb-2">Joie</h3>
                    <p>Émotions positives en réponse à des stimuli agréables</p>
                    <ul className="ml-4 list-disc mt-2">
                      <li>Expressions: mouvements rapides, sons aigus</li>
                      <li>Déclencheurs: interactions positives, accomplissements</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold text-green-500 mb-2">Curiosité</h3>
                    <p>Intérêt pour les nouveaux stimuli et environnements</p>
                    <ul className="ml-4 list-disc mt-2">
                      <li>Expressions: orientation vers les stimuli, mouvements d&apos;exploration</li>
                      <li>Déclencheurs: nouveaux objets, sons inhabituels</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold text-blue-500 mb-2">Peur</h3>
                    <p>Réaction de protection face aux dangers potentiels</p>
                    <ul className="ml-4 list-disc mt-2">
                      <li>Expressions: mouvements de recul, posture défensive</li>
                      <li>Déclencheurs: mouvements brusques, objets menaçants</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold text-red-500 mb-2">Colère</h3>
                    <p>Réaction aux obstacles et aux frustrations</p>
                    <ul className="ml-4 list-disc mt-2">
                      <li>Expressions: mouvements saccadés, sons graves</li>
                      <li>Déclencheurs: obstacles répétés, interactions négatives</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Système de mélanges émotionnels</h2>
                <p className="mb-4">
                  Les émotions ne sont pas discrètes mais peuvent se mélanger pour créer des états émotionnels complexes :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Intensité variable pour chaque émotion (0-100%)</li>
                  <li>Transitions douces entre les états émotionnels</li>
                  <li>Mémoire émotionnelle pour apprentissage des préférences</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Implémentation</h2>
                <p className="mb-4">
                  Le système émotionnel est implémenté via une combinaison de :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Module de gestion des émotions sur l&apos;ESP32</li>
                  <li>Intégration avec le LLM pour des réactions contextuelles</li>
                  <li>Analyse des données sensorielles pour déclencher des émotions</li>
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