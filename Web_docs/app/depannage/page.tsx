import { DocHeader } from "@/components/doc-header"
import { MainNav } from "@/components/main-nav"
import { Footer } from "@/components/footer"
import { BackToTop } from "@/components/back-to-top"

export default function DepannagePage() {
  return (
    <div className="min-h-screen bg-background">
      <DocHeader />
      <div className="flex">
        <MainNav />
        <main className="flex-1 px-4 py-6 md:px-6 md:py-12 lg:py-16">
          <div className="container mx-auto max-w-6xl">
            <section className="mb-12">
              <h1 className="mb-4 text-4xl font-bold tracking-tight text-primary">Dépannage</h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Cette section fournit des solutions aux problèmes courants que vous pourriez rencontrer 
                lors de la construction ou de l&apos;utilisation du robot.
              </p>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Problèmes matériels</h2>
                
                <div className="space-y-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Le robot ne s&apos;allume pas</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Aucune LED ne s&apos;allume</li>
                        <li>Aucune réponse lors de la mise sous tension</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Batterie déchargée</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez la tension de la batterie avec un multimètre</li>
                            <li>Rechargez la batterie complètement</li>
                            <li>Si la batterie ne charge pas, elle peut être défectueuse et doit être remplacée</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Connexions desserrées</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez toutes les connexions d&apos;alimentation</li>
                            <li>Assurez-vous que l&apos;interrupteur est en position ON</li>
                            <li>Vérifiez l&apos;absence de courts-circuits dans le câblage</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problème avec le régulateur de tension</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez les tensions de sortie des régulateurs 3.3V et 5V</li>
                            <li>Remplacez les régulateurs défectueux si nécessaire</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Les servomoteurs ne bougent pas correctement</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Les servomoteurs vibrent ou émettent un bourdonnement</li>
                        <li>Mouvements erratiques ou saccadés</li>
                        <li>Aucun mouvement malgré les commandes</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Alimentation insuffisante</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Les servomoteurs ont besoin d&apos;une alimentation stable et suffisante</li>
                            <li>Utilisez une alimentation séparée pour les servomoteurs</li>
                            <li>Vérifiez que la capacité de courant est suffisante (au moins 1A pour plusieurs servos)</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problème de branchement ou de signal</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez que les fils sont correctement connectés (Signal, VCC, GND)</li>
                            <li>Assurez-vous que les broches GPIO sont configurées en mode sortie</li>
                            <li>Testez avec un code simple pour isoler le problème</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Servo défectueux ou bloqué mécaniquement</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez qu&apos;il n&apos;y a pas d&apos;obstruction mécanique</li>
                            <li>Testez le servo avec un autre microcontrôleur ou circuit de test</li>
                            <li>Remplacez le servo s&apos;il est défectueux</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Les capteurs ne fonctionnent pas</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Aucune donnée reçue des capteurs</li>
                        <li>Données erronées ou incohérentes</li>
                        <li>Erreurs d&apos;initialisation du capteur</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Problème de connexion I2C</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez les connexions SDA et SCL</li>
                            <li>Assurez-vous que les résistances de pull-up sont présentes (généralement 4.7kΩ)</li>
                            <li>Utilisez un analyseur logique pour vérifier les signaux I2C si possible</li>
                            <li>Vérifiez les adresses I2C avec un scanner (voir code ci-dessous)</li>
                          </ul>
                          <pre className="mt-2 text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                            <code>{`#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Serial.println("Scanner I2C");
}

void loop() {
  byte error, address;
  int nDevices = 0;
  
  Serial.println("Recherche de périphériques I2C...");
  
  for(address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("Périphérique I2C trouvé à l'adresse 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  
  if (nDevices == 0) {
    Serial.println("Aucun périphérique I2C trouvé");
  }
  
  delay(5000);
}`}</code>
                          </pre>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Capteur défectueux ou incompatible</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Testez le capteur sur un circuit simple</li>
                            <li>Vérifiez la compatibilité avec la tension d&apos;alimentation (3.3V vs 5V)</li>
                            <li>Vérifiez que vous utilisez la bonne bibliothèque pour le capteur</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Problèmes de connectivité</h2>
                
                <div className="space-y-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Le robot ne se connecte pas au WiFi</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Le robot ne parvient pas à se connecter au réseau WiFi</li>
                        <li>Déconnexions fréquentes</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">SSID ou mot de passe incorrect</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez les identifiants WiFi dans le code</li>
                            <li>Assurez-vous qu&apos;il n&apos;y a pas de caractères spéciaux problématiques</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Signal WiFi faible</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Rapprochez le robot du routeur</li>
                            <li>Envisagez l&apos;utilisation d&apos;une antenne WiFi externe</li>
                            <li>Vérifiez les interférences potentielles</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problème de configuration réseau</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Assurez-vous que votre routeur accepte de nouveaux appareils</li>
                            <li>Vérifiez que vous n&apos;avez pas atteint la limite d&apos;appareils connectés</li>
                            <li>Essayez de définir une adresse IP statique</li>
                          </ul>
                          <pre className="mt-2 text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                            <code>{`// Configuration d'IP statique
IPAddress local_IP(192, 168, 1, 184);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(8, 8, 8, 8);

if (!WiFi.config(local_IP, gateway, subnet, dns)) {
  Serial.println("Configuration IP statique échouée");
}

WiFi.begin(ssid, password);`}</code>
                          </pre>
                        </li>
                      </ol>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Problèmes de communication avec le serveur</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Le robot est connecté au WiFi mais ne communique pas avec le serveur</li>
                        <li>Messages WebSocket non envoyés ou reçus</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Adresse IP ou port incorrect</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez l&apos;adresse IP du serveur et le port dans le code</li>
                            <li>Assurez-vous que le serveur est bien démarré sur le port spécifié</li>
                            <li>Testez la connexion avec un client WebSocket simple</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Pare-feu bloquant les connexions</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez les paramètres du pare-feu sur le serveur</li>
                            <li>Autorisez les connexions entrantes sur le port utilisé</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Format de message incorrect</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez que les messages JSON sont correctement formatés</li>
                            <li>Ajoutez des logs détaillés pour voir les messages échangés</li>
                            <li>Utilisez un validateur JSON pour vérifier vos messages</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Problèmes logiciels</h2>
                
                <div className="space-y-6">
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Redémarrages ou crashs de l&apos;ESP32</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>L&apos;ESP32 redémarre aléatoirement</li>
                        <li>Le programme se bloque</li>
                        <li>Exceptions et erreurs dans la console série</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Problème d&apos;alimentation</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez que l&apos;alimentation est stable et suffisante</li>
                            <li>Ajoutez des condensateurs de découplage (100nF entre VCC et GND)</li>
                            <li>Utilisez une source d&apos;alimentation capable de fournir suffisamment de courant</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Dépassement de la mémoire</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Réduisez la taille des variables et des tampons</li>
                            <li>Évitez les grandes allocations de mémoire sur la pile</li>
                            <li>Surveillez l&apos;utilisation de la mémoire avec ESP.getFreeHeap()</li>
                          </ul>
                          <pre className="mt-2 text-xs bg-muted-foreground/20 p-2 rounded overflow-x-auto">
                            <code>{`void checkMemory() {
  Serial.print("Mémoire libre: ");
  Serial.println(ESP.getFreeHeap());
}

// Appelez régulièrement dans votre code
void loop() {
  checkMemory();
  // Votre code...
  delay(1000);
}`}</code>
                          </pre>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problème avec le Watchdog Timer</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Évitez les boucles bloquantes ou les délais trop longs</li>
                            <li>Utilisez yield() régulièrement pour les opérations longues</li>
                            <li>Ajustez les paramètres du watchdog si nécessaire</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-md bg-muted">
                    <h3 className="text-lg font-bold mb-2">Problèmes avec le LLM</h3>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Symptômes :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Le modèle ne répond pas ou répond lentement</li>
                        <li>Réponses incohérentes ou erreurs</li>
                        <li>Consommation excessive de ressources</li>
                      </ul>
                    </div>
                    
                    <div className="mb-4">
                      <p className="font-medium text-sm mb-2">Causes possibles et solutions :</p>
                      <ol className="ml-4 list-decimal space-y-2">
                        <li>
                          <p className="font-medium text-sm">Ressources insuffisantes</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez que votre serveur répond aux exigences minimales</li>
                            <li>Utilisez un modèle plus léger si nécessaire</li>
                            <li>Fermez les applications non essentielles pendant l&apos;exécution du LLM</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problèmes de configuration</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez les chemins vers les fichiers modèles</li>
                            <li>Vérifiez les paramètres d&apos;inférence (température, nombre de tokens, etc.)</li>
                            <li>Mettez à jour les bibliothèques et dépendances</li>
                          </ul>
                        </li>
                        <li>
                          <p className="font-medium text-sm">Problèmes de format de prompt</p>
                          <ul className="ml-4 list-disc text-sm">
                            <li>Vérifiez que vos prompts suivent le format attendu par le modèle</li>
                            <li>Ajustez la longueur et la structure des prompts</li>
                            <li>Testez vos prompts avec différentes formulations</li>
                          </ul>
                        </li>
                      </ol>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Maintenance préventive</h2>
                
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Conseils pour éviter les problèmes</h3>
                  
                  <div className="space-y-3">
                    <div>
                      <p className="font-medium text-sm mb-1">Maintenance régulière :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Vérifiez régulièrement toutes les connexions électriques</li>
                        <li>Nettoyez doucement les capteurs pour éliminer la poussière</li>
                        <li>Lubrifiez légèrement les pièces mobiles mécaniques si nécessaire</li>
                        <li>Vérifiez les niveaux de charge de la batterie avant utilisation</li>
                      </ul>
                    </div>
                    
                    <div>
                      <p className="font-medium text-sm mb-1">Mises à jour :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Mettez à jour régulièrement le firmware de l&apos;ESP32</li>
                        <li>Vérifiez les mises à jour des bibliothèques utilisées</li>
                        <li>Sauvegardez votre code avant chaque mise à jour importante</li>
                      </ul>
                    </div>
                    
                    <div>
                      <p className="font-medium text-sm mb-1">Bonnes pratiques :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Utilisez des logs détaillés pour détecter les problèmes précocement</li>
                        <li>Implémentez un système de récupération sur erreur</li>
                        <li>Testez chaque composant individuellement avant l&apos;intégration</li>
                        <li>Documentez toutes les modifications que vous apportez au système</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="mb-4 text-2xl font-bold tracking-tight">Ressources supplémentaires</h2>
                
                <div className="p-4 rounded-md bg-muted">
                  <h3 className="text-lg font-bold mb-2">Où obtenir de l&apos;aide</h3>
                  
                  <div className="space-y-3">
                    <div>
                      <p className="font-medium text-sm mb-1">Documentation :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Documentation de l&apos;ESP32 : <a href="#" className="text-primary hover:underline">esp32.com/docs</a></li>
                        <li>Documentation des capteurs et actionneurs utilisés</li>
                        <li>Référence de l&apos;API du protocole MCP</li>
                      </ul>
                    </div>
                    
                    <div>
                      <p className="font-medium text-sm mb-1">Forums et communautés :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Forum officiel ESP32 : <a href="#" className="text-primary hover:underline">esp32.com/viewforum.php?f=13</a></li>
                        <li>Subreddit r/esp32 : <a href="#" className="text-primary hover:underline">reddit.com/r/esp32</a></li>
                        <li>Discord du projet : <a href="#" className="text-primary hover:underline">discord.gg/robotmignon</a></li>
                      </ul>
                    </div>
                    
                    <div>
                      <p className="font-medium text-sm mb-1">Outils de diagnostic :</p>
                      <ul className="ml-4 list-disc text-sm">
                        <li>Analyseur logique pour les signaux I2C/SPI</li>
                        <li>Multimètre pour les vérifications électriques</li>
                        <li>Outils de profilage mémoire pour ESP32</li>
                        <li>Analyseur de paquets réseau pour déboguer la communication</li>
                      </ul>
                    </div>
                  </div>
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