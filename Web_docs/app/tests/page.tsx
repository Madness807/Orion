import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function TestsPage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Tests</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Cette section décrit les différents tests et procédures de validation pour s&apos;assurer 
                que tous les composants du robot fonctionnent correctement.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Tests du matériel</h2>
                
                <div className="space-y-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">1. Test des capteurs</h3>
                    <p className="mb-2">
                      Vérifiez le bon fonctionnement de chaque capteur individuellement.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-1">Test du capteur APDS9960</h4>
                        <pre className="text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                          <code>{`// Inclure les bibliothèques
#include <Wire.h>
#include <Adafruit_APDS9960.h>

Adafruit_APDS9960 apds;

void setup() {
  Serial.begin(115200);
  if(!apds.begin()) {
    Serial.println("Échec de l'initialisation");
  } else {
    Serial.println("APDS9960: OK");
    apds.enableColor(true);
  }
}

void loop() {
  uint16_t r, g, b, c;
  
  if (apds.colorDataReady()) {
    apds.getColorData(&r, &g, &b, &c);
    Serial.print("R: "); Serial.print(r);
    Serial.print(" G: "); Serial.print(g);
    Serial.print(" B: "); Serial.print(b);
    Serial.print(" C: "); Serial.println(c);
  }
  delay(500);
}`}</code>
                        </pre>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-1">Procédure de test</h4>
                        <ol className="ml-4 list-decimal space-y-1">
                          <li>Téléversez le code de test</li>
                          <li>Ouvrez le moniteur série à 115200 bauds</li>
                          <li>Vérifiez que le capteur est initialisé</li>
                          <li>Présentez différentes couleurs devant le capteur</li>
                          <li>Vérifiez que les valeurs changent en conséquence</li>
                        </ol>
                        <div className="mt-2 p-2 bg-amber-100 dark:bg-amber-950/50 rounded">
                          <p className="text-xs font-semibold">Résultats attendus</p>
                          <p className="text-xs">Le capteur doit détecter les changements de couleur et de proximité avec précision.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">2. Test des servomoteurs</h3>
                    <p className="mb-2">
                      Vérifiez que les servomoteurs fonctionnent correctement.
                    </p>
                    <pre className="text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto mb-3">
                      <code>{`#include <ESP32Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  servo1.attach(13);  // Broche GPIO pour servo 1
  servo2.attach(12);  // Broche GPIO pour servo 2
}

void loop() {
  // Test plage complète
  for (int pos = 0; pos <= 180; pos += 5) {
    servo1.write(pos);
    servo2.write(pos);
    delay(100);
  }
  
  // Test en sens inverse
  for (int pos = 180; pos >= 0; pos -= 5) {
    servo1.write(pos);
    servo2.write(pos);
    delay(100);
  }
}`}</code>
                    </pre>
                    <div className="p-2 bg-amber-100 dark:bg-amber-950/50 rounded">
                      <p className="text-xs font-semibold">Remarque</p>
                      <p className="text-xs">Si les servomoteurs vibrent ou émettent un bruit anormal, vérifiez l'alimentation.</p>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Tests logiciels</h2>
                
                <div className="space-y-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">1. Test de la communication MCP</h3>
                    <p className="mb-3">
                      Vérifiez que le protocole MCP fonctionne correctement entre l&apos;ESP32 et le serveur.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-1">Serveur de test</h4>
                        <pre className="text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                          <code>{`# Python - test_server.py
import websockets
import asyncio
import json

connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Reçu: {data}")
            
            # Echo
            response = {
                "type": "ECHO",
                "data": data
            }
            await websocket.send(json.dumps(response))
    finally:
        connected.remove(websocket)

start_server = websockets.serve(echo, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()`}</code>
                        </pre>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-1">Client ESP32</h4>
                        <pre className="text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                          <code>{`#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

WebSocketsClient webSocket;

void setup() {
  Serial.begin(115200);
  WiFi.begin("SSID", "PASSWORD");
  
  webSocket.begin("192.168.1.X", 8765, "/");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();
  
  if (millis() % 5000 == 0) {
    // Envoi périodique
    StaticJsonDocument<200> doc;
    doc["type"] = "SENSOR_DATA";
    doc["data"]["temperature"] = 25.5;
    
    String json;
    serializeJson(doc, json);
    webSocket.sendTXT(json);
  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_TEXT:
      Serial.printf("Reçu: %s\\n", payload);
      break;
  }
}`}</code>
                        </pre>
                      </div>
                    </div>
                    <div className="mt-3 p-2 bg-amber-100 dark:bg-amber-950/50 rounded">
                      <p className="text-xs font-semibold">Procédure de test</p>
                      <ol className="ml-4 text-xs list-decimal">
                        <li>Démarrez le serveur Python sur votre ordinateur</li>
                        <li>Modifiez les paramètres WiFi dans le code de l'ESP32</li>
                        <li>Téléversez le code sur l'ESP32</li>
                        <li>Vérifiez que les messages sont échangés correctement</li>
                      </ol>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Tests d&apos;intégration</h2>
                
                <div className="space-y-4">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">1. Test complet du système</h3>
                    <p className="mb-3">
                      Vérifiez que tous les composants fonctionnent ensemble correctement.
                    </p>
                    <ol className="ml-4 list-decimal space-y-2">
                      <li>
                        <p className="font-medium">Démarrage du système</p>
                        <ul className="ml-4 list-disc">
                          <li>Démarrez le serveur NAS</li>
                          <li>Allumez le robot</li>
                          <li>Vérifiez que la connexion s'établit</li>
                        </ul>
                      </li>
                      <li>
                        <p className="font-medium">Test de la communication bidirectionnelle</p>
                        <ul className="ml-4 list-disc">
                          <li>Vérifiez que les données des capteurs sont reçues</li>
                          <li>Envoyez des commandes du serveur vers le robot</li>
                        </ul>
                      </li>
                      <li>
                        <p className="font-medium">Test des expressions</p>
                        <ul className="ml-4 list-disc">
                          <li>Vérifiez que les commandes d'émotion sont correctement interprétées</li>
                          <li>Testez les différentes expressions faciales</li>
                        </ul>
                      </li>
                      <li>
                        <p className="font-medium">Test de l'interface utilisateur</p>
                        <ul className="ml-4 list-disc">
                          <li>Vérifiez que l'interface web se connecte au serveur</li>
                          <li>Testez les commandes manuelles</li>
                          <li>Vérifiez l'affichage des données des capteurs</li>
                        </ul>
                      </li>
                    </ol>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">2. Test d&apos;autonomie</h3>
                    <p className="mb-3">
                      Vérifiez l&apos;autonomie de la batterie et la stabilité sur la durée.
                    </p>
                    <ul className="ml-4 list-disc">
                      <li>Démarrez le robot avec une batterie complètement chargée</li>
                      <li>Lancez un programme utilisant les capteurs et les servomoteurs</li>
                      <li>Mesurez le temps jusqu'à ce que la batterie atteigne 20%</li>
                      <li>Vérifiez la stabilité de la connexion WiFi sur la durée</li>
                      <li>Testez le comportement en cas de batterie faible</li>
                    </ul>
                    <div className="mt-3 p-2 bg-amber-100 dark:bg-amber-950/50 rounded">
                      <p className="text-xs font-semibold">Remarque</p>
                      <p className="text-xs">L'autonomie peut varier considérablement selon l'utilisation des moteurs et la fréquence d'envoi des données.</p>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Tests de performance du LLM</h2>
                
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Évaluation des capacités d&apos;IA</h3>
                  <p className="mb-3">
                    Testez les capacités du modèle de langage et ses interactions.
                  </p>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold mb-1">Test de contexte</h4>
                      <p className="text-sm">Vérifiez que le modèle peut maintenir le contexte sur plusieurs échanges.</p>
                      <pre className="text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto mt-1">
                        <code>{`# Exemple de séquence de test
1. "Bonjour, comment t'appelles-tu ?"
2. "Quel temps fait-il aujourd'hui ?"
3. "Peux-tu t'en souvenir pour plus tard ?"
4. [30 minutes plus tard] "De quoi avons-nous parlé plus tôt ?"`}</code>
                      </pre>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-1">Test d&apos;intégration sensorielle</h4>
                      <p className="text-sm">Vérifiez que le modèle intègre correctement les données des capteurs.</p>
                      <ol className="ml-4 list-decimal text-sm">
                        <li>Placez un objet rouge devant le capteur</li>
                        <li>Demandez "Quelle couleur vois-tu ?"</li>
                        <li>Vérifiez que le modèle répond correctement</li>
                        <li>Testez avec différentes conditions environnementales</li>
                      </ol>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-1">Test de la carte émotionnelle</h4>
                      <p className="text-sm">Vérifiez que le modèle génère des réponses émotionnelles appropriées.</p>
                      <ol className="ml-4 list-decimal text-sm">
                        <li>Simulez différents événements (toucher, voix forte, etc.)</li>
                        <li>Observez les transitions émotionnelles</li>
                        <li>Vérifiez la cohérence entre l'émotion affichée et le contexte</li>
                      </ol>
                    </div>
                  </div>
                </div>
              </section>
              
              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Documentation des tests</h2>
                
                <p className="mb-4">
                  Pour chaque test, documentez soigneusement les résultats en utilisant le modèle suivant :
                </p>
                
                <div className="p-4 bg-muted rounded-md">
                  <pre className="text-xs overflow-x-auto">
                    <code>{`# Rapport de test

## Informations générales
- Nom du test : [Nom du test]
- Date : [Date]
- Version du logiciel : [Version]
- Testeur : [Nom]

## Configuration matérielle
- Version de l'ESP32 : [Version]
- Périphériques connectés : [Liste]
- Alimentation : [Type et tension]

## Procédure de test
1. [Étape 1]
2. [Étape 2]
3. [Étape 3]

## Résultats
- Résultat 1 : [Succès/Échec] - [Description]
- Résultat 2 : [Succès/Échec] - [Description]

## Problèmes identifiés
- [Description du problème 1]
- [Description du problème 2]

## Actions correctives
- [Action 1]
- [Action 2]

## Conclusion
[Résumé du test et prochaines étapes]`}</code>
                  </pre>
                </div>
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