import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function ExpressionsPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Expressions</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Les expressions permettent au robot de communiquer de façon non-verbale à travers 
                des mouvements, sons et affichages visuels, rendant son comportement plus naturel et expressif.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Types d&apos;expressions</h2>
                <p className="mb-4">
                  Le robot dispose de plusieurs canaux d&apos;expression qui peuvent être combinés :
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Expressions faciales</h3>
                    <p className="mb-2">Affichées sur l&apos;écran LED principal.</p>
                    <ul className="ml-4 list-disc">
                      <li>Expressions de base (joie, tristesse, colère...)</li>
                      <li>Animations pour transitions fluides</li>
                      <li>Personnalisation via des modèles vectoriels</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Expressions sonores</h3>
                    <p className="mb-2">Sons et tonalités émis par le haut-parleur.</p>
                    <ul className="ml-4 list-disc">
                      <li>Sons courts expressifs (bips, mélodies...)</li>
                      <li>Variations de ton selon l&apos;émotion</li>
                      <li>Bibliothèque de sons extensible</li>
                    </ul>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Expressions motrices</h3>
                    <p className="mb-2">Mouvements et postures physiques.</p>
                    <ul className="ml-4 list-disc">
                      <li>Séquences de mouvements prédéfinies</li>
                      <li>Vitesse et amplitude variables selon l&apos;émotion</li>
                      <li>Réactions contextuelles aux stimuli</li>
                    </ul>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Expressions lumineuses</h3>
                    <p className="mb-2">Utilisation des LEDs RGB secondaires.</p>
                    <ul className="ml-4 list-disc">
                      <li>Couleurs associées aux émotions</li>
                      <li>Animations et effets lumineux</li>
                      <li>Intensité variable selon le contexte</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Système d&apos;expressions faciales</h2>
                <p className="mb-4">
                  Le robot utilise un écran LED pour afficher des expressions stylisées :
                </p>
                <div className="my-8 flex justify-center">
                  <img
                    src="/placeholder.svg?height=300&width=400"
                    alt="Expressions faciales du robot"
                    className="rounded-lg shadow-md"
                    width={400}
                    height={300}
                  />
                </div>
                <p className="mb-4">
                  Chaque expression est définie par un ensemble de composants faciaux :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li><strong>Yeux</strong> : Forme, taille, orientation</li>
                  <li><strong>Bouche</strong> : Courbure, ouverture</li>
                  <li><strong>Sourcils</strong> : Position, angle</li>
                  <li><strong>Accessoires</strong> : Gouttes de sueur, points d&apos;exclamation...</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Liaison émotions-expressions</h2>
                <p className="mb-4">
                  Les expressions sont liées à l&apos;état émotionnel du robot :
                </p>
                <pre className="rounded-md bg-muted p-4 overflow-x-auto">
                  <code>{`// Exemple de mapping émotion-expression
const expressionMap = {
  "joie": {
    faciale: "sourire_large",
    sonore: "melodie_joyeuse",
    motrice: "danse_enthousiaste",
    lumineuse: "jaune_pulsant"
  },
  "curiosite": {
    faciale: "yeux_grands_ouverts",
    sonore: "bip_interrogatif",
    motrice: "penche_en_avant",
    lumineuse: "vert_clignotant"
  },
  // Autres mappings...
};`}</code>
                </pre>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Expressions contextuelles</h2>
                <p className="mb-4">
                  Le système d&apos;expressions tient compte du contexte pour adapter ses réactions :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Intensité adaptée au niveau de stimulation</li>
                  <li>Réponses différentes selon le type d&apos;interaction</li>
                  <li>Apprentissage des réactions préférées par l&apos;utilisateur</li>
                  <li>Capacité à exprimer des émotions mélangées ou complexes</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Personnalisation</h2>
                <p className="mb-4">
                  Les utilisateurs peuvent personnaliser les expressions du robot :
                </p>
                <ul className="ml-6 list-disc space-y-2">
                  <li>Éditeur d&apos;expressions faciales dans l&apos;interface web</li>
                  <li>Importation de nouveaux sons expressifs</li>
                  <li>Réglage de l&apos;intensité des réactions</li>
                  <li>Création de nouvelles séquences d&apos;expressions</li>
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