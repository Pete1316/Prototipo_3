#include <SoftwareSerial.h>
#include <DHT.h>   // <---- librería DHT22
#include <ArduinoJson.h>

SoftwareSerial espSerial(2, 3); // RX, TX

// ===== Pines Sensores =====
#define TDS_PIN A1
#define PH_PIN A0
#define TEMP_PIN A2

// ===== DHT22 =====
#define DHTPIN 4        // Pin del DHT22FL
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== Sensor Nivel Agua =====
#define NIVEL_PIN 5     // Switch de nivel (2 cables)
#define NIVEL2_PIN 6


// ===== TDS =====
#define VREF 5.0
#define SCOUNT 30
int tdsBuffer[SCOUNT];
int tdsBufferTemp[SCOUNT];

String bufferRX = "";
bool leyendoIP = false;
String ipESP = "";


int tdsIndex = 0;
float tdsValue = 0;
float temperature = 25;


// ===== pH =====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

// ===== Factor EC =====
// ===== Referencias de agua =====
const int numAguas = 4; // 4 tipos de agua

// TDS ADC de referencia y TDS real en ppm
int tdsADCRef[numAguas] = {400, 600, 800, 1000}; // valores de prueba
float tdsPPMRef[numAguas] = {500, 1000, 1500, 2000}; // ppm reales

// pH ADC de referencia y pH real
int phADCRef[numAguas] = {948, 900, 850, 800}; // valores de ejemplo
float phRef[numAguas] = {6.0, 6.5, 7.0, 7.5}; // pH reales

// Agua seleccionada
int aguaSeleccionada = 0; // cambiar a 0,1,2 o 3 según el agua que quieras



void setup() {

  Serial.begin(9600);
  espSerial.begin(9600);

  dht.begin();               // Iniciar DHT22
  pinMode(NIVEL_PIN, INPUT); // Sensor de nivel agua
  pinMode(NIVEL2_PIN, INPUT);
  
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

int getMedianNum(int bArray[], int iFilterLen) {
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++) bTab[i] = bArray[i];

  for (int j = 0; j < iFilterLen - 1; j++) {
    for (int i = 0; i < iFilterLen - j - 1; i++) {
      if (bTab[i] > bTab[i + 1]) {
        int temp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = temp;
      }
    }
  }

  if (iFilterLen % 2 == 1) return bTab[(iFilterLen - 1) / 2];
  else return (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
}

void loop() {
  recibirDatosESP32(); 

  // ===== Sensores ADC =====
  temperature = leerTemperaturaADC();

  float ph = leerPH();
 int lecturaTDS = analogRead(TDS_PIN);
 float tds = calibrarTDS(lecturaTDS);
 float ec  = calibrarEC(lecturaTDS);





  // ===== DHT22 =====
  float dhtTemp = dht.readTemperature(); // °C
  float hum = dht.readHumidity();

  // ===== Sensor nivel agua =====
  int nivelAgua = digitalRead(NIVEL_PIN);  
  int nivelAgua1 = digitalRead(NIVEL2_PIN);
  // HIGH → Hay agua  
  // LOW  → No hay agua

  // ===== Crear JSON =====
  Serial.print("{\"temp\":");
  Serial.print(temperature, 1);
  Serial.print(",\"tds\":");
  Serial.print(tds, 0);
  Serial.print(",\"ph\":");
  Serial.print(ph, 2);
  Serial.print(",\"ec\":");
  Serial.print(ec, 0);
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
  espSerial.print(",\"tds\":");
  espSerial.print(tds, 0);
  espSerial.print(",\"ph\":");
  espSerial.print(ph, 2);
  espSerial.print(",\"ec\":");
  espSerial.print(ec, 0);
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
      DeserializationError error = deserializeJson(doc, bufferRX);

      if (!error && doc.containsKey("ip")) {
        ipESP = doc["ip"].as<String>();
        Serial.print("IP recibida del ESP32: ");
        Serial.println(ipESP);
      }

      bufferRX = "";
    }
    else if (leyendoIP) {
      bufferRX += c;
    }
  }
}

