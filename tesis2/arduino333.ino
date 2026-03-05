#include <SoftwareSerial.h>
#include "DHT.h"

// PINS
#define LED_PIN A5
#define LUZ_PIN A0
#define DHTPIN 2              // Pin digital conectado al DHT22
#define DHTTYPE DHT22         // Tipo de sensor DHT

// Nuevos pines para actuadores
#define FAN_PIN 3
#define DESHUM_PIN 4

// Inicializaciones
SoftwareSerial BTSerial(10, 11); // RX, TX
DHT dht(DHTPIN, DHTTYPE);
unsigned long ultimoEnvio = 0;
const unsigned long intervalo = 5000; // 5 segundos

void setup() {
  pinMode(LUZ_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(DESHUM_PIN, OUTPUT);

  // Apagar actuadores al inicio
  digitalWrite(LED_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(DESHUM_PIN, LOW);

  BTSerial.begin(9600);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Control de actuadores vía Bluetooth
  if (BTSerial.available()) {
    String command = BTSerial.readStringUntil('\n');
    command.trim();

    Serial.print("Comando recibido: ");
    Serial.println(command);

    if (command == "LED_ON") {
      digitalWrite(LED_PIN, HIGH);
    } else if (command == "LED_OFF") {
      digitalWrite(LED_PIN, LOW);

    } else if (command == "FAN_ON") {
      digitalWrite(FAN_PIN, HIGH);
    } else if (command == "FAN_OFF") {
      digitalWrite(FAN_PIN, LOW);

    } else if (command == "DESHUM_ON") {
      digitalWrite(DESHUM_PIN, HIGH);
    } else if (command == "DESHUM_OFF") {
      digitalWrite(DESHUM_PIN, LOW);
    }
  }

  // Enviar datos por Bluetooth cada 5 segundos
  if (millis() - ultimoEnvio > intervalo) {
    float temperatura = dht.readTemperature();
    float humedad = dht.readHumidity();
    int nivelLuz = analogRead(LUZ_PIN);

    if (!isnan(temperatura)) {
      BTSerial.print("temp:");
      BTSerial.println(temperatura);
    }

    if (!isnan(humedad)) {
      BTSerial.print("hum:");
      BTSerial.println(humedad);
    }

    BTSerial.print("luz:");
    BTSerial.println(nivelLuz);

    // Monitoreo en Serial
    Serial.print("Temp: ");
    Serial.println(temperatura);
    Serial.print("Hum: ");
    Serial.println(humedad);
    Serial.print("Luz: ");
    Serial.println(nivelLuz);

    ultimoEnvio = millis();
  }
}

