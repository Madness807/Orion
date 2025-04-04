#ifndef CONFIG_H
#define CONFIG_H

// Configuration Wi-Fi
#define WIFI_SSID "VotreSSID"
#define WIFI_PASSWORD "VotreMotDePasse"

// Configuration MCP (Model Context Protocol)
#define MCP_SERVER_IP "192.168.1.100"  // Adresse IP du NAS
#define MCP_SERVER_PORT 8080
#define ROBOT_ID "MignonBot1"

// Broches des capteurs
// Sons
#define PIN_BIG_SOUND 36
#define PIN_SMALL_SOUND 39

// Vision
#define PIN_ULTRASONIC_TRIG 23
#define PIN_ULTRASONIC_ECHO 22
#define PIN_PHOTORESISTOR 34
#define PIN_IR_RECEIVER 35

// Toucher
#define PIN_TAP 25
#define PIN_SHOCK 26
#define PIN_TOUCH 27
#define PIN_BUTTON 32

// Température
#define PIN_DHT11 4
#define PIN_DS18B20 5
#define PIN_ANALOG_TEMP 33

// Magnétisme
#define PIN_HALL 14
#define PIN_REED 12

// Humidité/Eau
#define PIN_WATER_LEVEL 13

// Proprioception (GY-521 utilise I2C)
#define PIN_SDA 21
#define PIN_SCL 22

// Expression
#define PIN_RGB_LED 15
#define PIN_BUZZER 2
#define PIN_LCD_SDA 21
#define PIN_LCD_SCL 22

// Moteurs
#define PIN_SERVO 18
#define PIN_MOTOR_A_IN1 19
#define PIN_MOTOR_A_IN2 16
#define PIN_MOTOR_B_IN1 17
#define PIN_MOTOR_B_IN2 5

// Fréquence de mise à jour (ms)
#define SENSOR_UPDATE_INTERVAL 1000
#define EMOTION_UPDATE_INTERVAL 2000
#define MCP_SEND_INTERVAL 5000

#endif // CONFIG_H
