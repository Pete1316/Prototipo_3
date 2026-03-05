#include <SoftwareSerial.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <math.h>

SoftwareSerial espSerial(2, 3); // RX, TX

// ===== Pines Sensores =====
#define TDS_PIN A1
#define PH_PIN A0
#define TEMP_PIN A2

// ===== DHT22 =====
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== Sensor Nivel =====
#define NIVEL_PIN 5
#define NIVEL2_PIN 6
#define BOMBA_PIN 11
#define MOTOR_IN1 10
#define MOTOR_IN4 9

String bufferRX = "";
bool leyendoIP = false;
String ipESP = "";

// ===== pH =====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

// ===== TDS / EC =====
float aref = 4.67;
float ecCalibration = 1.00;

float ec = 0;
unsigned int tds = 0;
float waterTemp = 0;

// ===== Control de lectura TDS =====
unsigned long lastTDSRead = 0;
const unsigned long tdsInterval = 10000; // 10 segundos

float ecFiltrado = 0;
unsigned int tdsFiltrado = 0;
unsigned long tiempoMotor = 0;
int estadoMotor = 0;


void setup() {
  Serial.begin(9600);
  espSerial.begin(9600);

  dht.begin();
  pinMode(TDS_PIN, INPUT);
  pinMode(NIVEL_PIN, INPUT);
  pinMode(NIVEL2_PIN, INPUT);
  pinMode(BOMBA_PIN, OUTPUT);
  pinMode(MOTOR_IN1,OUTPUT);
  pinMode(MOTOR_IN4,OUTPUT);


}

void motor_ciclo() {
  unsigned long ahora = millis();

  switch (estadoMotor) {

    case 0: // Gira sentido 1
      digitalWrite(MOTOR_IN1, HIGH);
      digitalWrite(MOTOR_IN4, LOW);
      tiempoMotor = ahora;
      estadoMotor = 1;
      break;

    case 1: // Espera 2 segundos
      if (ahora - tiempoMotor >= 2000) {
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN4, LOW);
        tiempoMotor = ahora;
        estadoMotor = 2;
      }
      break;

    case 2: // Pausa 1 segundo
      if (ahora - tiempoMotor >= 1000) {
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN4, HIGH);
        tiempoMotor = ahora;
        estadoMotor = 3;
      }
      break;

    case 3: // Espera 2 segundos
      if (ahora - tiempoMotor >= 2000) {
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN4, LOW);
        tiempoMotor = ahora;
        estadoMotor = 4;
      }
      break;

    case 4: // Pausa 1 segundo y reinicia ciclo
      if (ahora - tiempoMotor >= 1000) {
        estadoMotor = 0; // 🔁 vuelve a empezar
      }
      break;
  }
}


// ===== Temperatura NTC =====
float leerTemperaturaADC() {
  const float SERIES_RESISTOR = 10000.0;
  const float NOMINAL_RESISTANCE = 10000.0;
  const float NOMINAL_TEMPERATURE = 22.0;
  const float B_COEFFICIENT = 3950.0;

  int adcValue = analogRead(TEMP_PIN);
  float resistance = SERIES_RESISTOR / ((1023.0 / adcValue) - 1.0);

  float steinhart;
  steinhart = resistance / NOMINAL_RESISTANCE;
  steinhart = log(steinhart);
  steinhart /= B_COEFFICIENT;
  steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;

  return steinhart;
}

// ===== Lectura TDS filtrada =====
void actualizarTDS(float tempAgua) {
  const int muestras = 10;
  float sumaEc = 0;

  for (int i = 0; i < muestras; i++) {
    float rawEc = analogRead(TDS_PIN) * aref / 1024.0;
    float coefTemp = 1.0 + 0.02 * (tempAgua - 25.0);
    float ecTemp = (rawEc / coefTemp) * ecCalibration;
    sumaEc += ecTemp;
    delay(20);
  }

  ecFiltrado = sumaEc / muestras;

  tdsFiltrado = (133.42 * pow(ecFiltrado, 3)
               - 255.86 * pow(ecFiltrado, 2)
               + 857.39 * ecFiltrado) * 0.5;
}

// ===== pH =====
float leerPH() {
  int prom = 0;
  for (int i = 0; i < 20; i++) {
    prom += analogRead(PH_PIN);
    delay(10);
  }
  prom /= 20;

  if (prom <= m_7)
    return 4.01 + (prom - m_4) * (6.86 - 4.01) / (m_7 - m_4);
  else
    return 6.86 + (prom - m_7) * (9.18 - 6.86) / (m_9 - m_7);
}

void BOMBA(){
    int nivel = digitalRead(NIVEL_PIN);
    if (nivel == 1 ){
        digitalWrite(BOMBA_PIN, HIGH);
    }else{
        digitalWrite(BOMBA_PIN, LOW);
    }
}

void loop() {
  recibirDatosESP32();
  BOMBA();
  motor_ciclo();

  // Temperatura agua
  waterTemp = leerTemperaturaADC();

  // TDS cada 5 segundos
  if (millis() - lastTDSRead >= tdsInterval) {
    lastTDSRead = millis();
    actualizarTDS(waterTemp);
  }

  ec = ecFiltrado;
  tds = tdsFiltrado;

  float ph = leerPH();
  float dhtTemp = dht.readTemperature();
  float hum = dht.readHumidity();

  int nivelAgua = digitalRead(NIVEL_PIN);
  int nivelAgua1 = digitalRead(NIVEL2_PIN);

  // ===== Serial =====
  Serial.print("{\"waterTemp\":");
  Serial.print(waterTemp, 2);
  Serial.print(",\"tds\":");
  Serial.print(tds);
  Serial.print(",\"ec\":");
  Serial.print(ec, 3);
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

  delay(10);
}

void recibirDatosESP32() {
  while (espSerial.available()) {
    char c = espSerial.read();
    if (c == '{') {
      bufferRX = "{";
      leyendoIP = true;
    } else if (c == '}' && leyendoIP) {
      bufferRX += "}";
      leyendoIP = false;
      bufferRX = "";
    } else if (leyendoIP) {
      bufferRX += c;
    }
  }
}
