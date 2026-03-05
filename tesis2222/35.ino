#include <SoftwareSerial.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
#include "GravityTDS.h"
SoftwareSerial espSerial(2, 3); // RX, TX

// ===== Pines Sensores =====
//======PIN DE TDS======
#define TDS_PIN A1
GravityTDS gravityTds;
//======PIN DE PH
#define PH_PIN A0

#define TEMP_PIN A2

// ===== DHT22 =====
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== Sensor Nivel Agua =====
#define NIVEL_PIN 5
#define NIVEL2_PIN 6

String bufferRX = "";
bool leyendoIP = false;
String ipESP = "";

float temperature = 25, tdsValue = 0;

// ===== pH =====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

void setup() {

  Serial.begin(9600);
  espSerial.begin(9600);

  dht.begin();
  pinMode(NIVEL_PIN, INPUT);
  pinMode(NIVEL2_PIN, INPUT);
  gravityTds.setPin(TDS_PIN);
  gravityTds.setAref(5.0);
  gravityTds.setAdcRange(1024);
  gravityTds.begin();
  Serial.println("Arduino listo para recibir IP del ESP32");
}

// ===== FUNCIONES =====

float leerPH() {
  int prom = 0;
  for (int i = 0; i < 20; i++) {
    prom += analogRead(PH_PIN);
    delay(10);
  }
  prom /= 20;

  float ph;
  if (prom <= m_7)
    ph = 4.01 + (prom - m_4) * (6.86 - 4.01) / (m_7 - m_4);
  else
    ph = 6.86 + (prom - m_7) * (9.18 - 6.86) / (m_9 - m_7);

  return ph;
}

float leerTemperaturaADC() {
  int valorADC = analogRead(TEMP_PIN);
  float R = 10000.0 * (1023.0 / valorADC - 1.0);
  float T = 1.0 / (1.0 / 298.15 + 1.0 / 3950.0 * log(R / 10000.0));
  return T - 273.15;
}

void loop() {
  recibirDatosESP32();

  // ===== Sensores =====
  temperature = leerTemperaturaADC();
  float ph = leerPH();

  // ===== DHT22 =====
  float dhtTemp = dht.readTemperature();
  float hum = dht.readHumidity();

  //======TDS=========
  gravityTds.setTemperature(temperature);
  gravityTds.update();
  tdsValue = gravityTds.getTdsValue();

  

  // ===== Nivel de agua =====
  int nivelAgua = digitalRead(NIVEL_PIN);
  int nivelAgua1 = digitalRead(NIVEL2_PIN);

  // ===== JSON =====
  Serial.print("{\"ppm\":");
  Serial.print(tdsValue);
  Serial.print(",\"temp\":");
  Serial.print(temperature, 1);
  Serial.print(",\"ph\":");
  Serial.print(ph, 2);
  Serial.print(",\"dhtTemp\":");
  Serial.print(dhtTemp, 1);
  Serial.print(",\"hum\":");
  Serial.print(hum, 1);
  Serial.print(",\"nivel\":");
  Serial.print(nivelAgua);
  Serial.print(",\"nivel1\":");
  Serial.print(nivelAgua1);
  Serial.println("}");

  // ===== Enviar al ESP32 =====
  espSerial.print("{\"temp\":");
  espSerial.print(temperature, 1);
  espSerial.print(",\"ph\":");
  espSerial.print(ph, 2);
  espSerial.print(",\"dhtTemp\":");
  espSerial.print(dhtTemp, 1);
  espSerial.print(",\"hum\":");
  espSerial.print(hum, 1);
  espSerial.print(",\"nivel\":");
  espSerial.print(nivelAgua);
  espSerial.print(",\"nivel1\":");
  espSerial.print(nivelAgua1);
  espSerial.println("}");

  delay(1000);
}

void recibirDatosESP32() {
  while (espSerial.available()) {
    char c = espSerial.read();

    if (c == '{') {
      bufferRX = "{";
      leyendoIP = true;
    }
    else if (c == '}' && leyendoIP) {
      bufferRX += "}";
      leyendoIP = false;

      StaticJsonDocument<100> doc;
      if (!deserializeJson(doc, bufferRX)) {
        if (doc.containsKey("ip")) {
          ipESP = doc["ip"].as<String>();
          Serial.print("IP recibida del ESP32: ");
          Serial.println(ipESP);
        }
      }
      bufferRX = "";
    }
    else if (leyendoIP) {
      bufferRX += c;
    }
  }
}
