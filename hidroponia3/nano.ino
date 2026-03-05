#include <SoftwareSerial.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <math.h>
#include <Servo.h>

SoftwareSerial espSerial(2, 3); // RX, TX

// ===== Pines Sensores =====
#define TDS_PIN A1
#define PH_PIN A0
#define TEMP_PIN A2tT

// ===== DHT22 =====
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== Sensor Nivel y Actuadores =====
#define NIVEL_PIN 5

#define BOMBA_PIN 11

// ===== SERVO SG90 =====
#define SERVO_PIN 9
#define SERVO_MIN 5          // evita vibración
#define SERVO_MAX 175        // evita vibración
#define SERVO_STEP 1
#define SERVO_DELAY 166      // 30 segundos para 180°

Servo miServo;
int anguloServo = SERVO_MIN;
bool subiendo = true;
unsigned long lastServoMove = 0;
#define SERVO_PAUSA_ARRIBA 30000  // 30 segundos en 180°
#define SERVO_PAUSA_ABAJO 30000   // 30 segundos en 0°

bool enPausaArriba = false;
bool enPausaAbajo = false;

unsigned long pausaArribaInicio = 0;
unsigned long pausaAbajoInicio = 0;


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

// ===== Control TDS =====
unsigned long lastTDSRead = 0;
const unsigned long tdsInterval = 10000;

// ===== SETUP =====
void setup() {
  Serial.begin(9600);
  espSerial.begin(9600);

  dht.begin();

  pinMode(TDS_PIN, INPUT);
  pinMode(NIVEL_PIN, INPUT);
  
  pinMode(BOMBA_PIN, OUTPUT);

  miServo.attach(SERVO_PIN);
  miServo.write(anguloServo);
}

// ===== MOVIMIENTO SERVO 30s 0↔180 =====
void moverServo() {

  // ⏸️ Pausa en 180°
  if (enPausaArriba) {
    if (millis() - pausaArribaInicio >= SERVO_PAUSA_ARRIBA) {
      enPausaArriba = false;
      subiendo = false; // empezar a bajar
    }
    return;
  }

  // ⏸️ Pausa en 0°
  if (enPausaAbajo) {
    if (millis() - pausaAbajoInicio >= SERVO_PAUSA_ABAJO) {
      enPausaAbajo = false;
      subiendo = true; // empezar a subir
    }
    return;
  }

  // Movimiento normal
  if (millis() - lastServoMove >= SERVO_DELAY) {
    lastServoMove = millis();

    if (subiendo) {
      anguloServo += SERVO_STEP;

      if (anguloServo >= SERVO_MAX) {
        anguloServo = SERVO_MAX;
        miServo.write(anguloServo);

        // activar pausa en 180°
        enPausaArriba = true;
        pausaArribaInicio = millis();
        return;
      }

    } else {
      anguloServo -= SERVO_STEP;

      if (anguloServo <= SERVO_MIN) {
        anguloServo = SERVO_MIN;
        miServo.write(anguloServo);

        // activar pausa en 0°
        enPausaAbajo = true;
        pausaAbajoInicio = millis();
        return;
      }
    }

    miServo.write(anguloServo);
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

  float steinhart = resistance / NOMINAL_RESISTANCE;
  steinhart = log(steinhart);
  steinhart /= B_COEFFICIENT;
  steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;

  return steinhart;
}

// ===== TDS =====
void actualizarTDS(float tempAgua) {
  float sumaEc = 0;

  for (int i = 0; i < 10; i++) {
    float rawEc = analogRead(TDS_PIN) * aref / 1024.0;
    float coefTemp = 1.0 + 0.02 * (tempAgua - 25.0);
    sumaEc += (rawEc / coefTemp) * ecCalibration;
    delay(20);
  }

  ec = sumaEc / 10;

  tds = (133.42 * pow(ec, 3)
       - 255.86 * pow(ec, 2)
       + 857.39 * ec) * 0.5;
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

// ===== BOMBA =====
void BOMBA() {
  digitalWrite(BOMBA_PIN, digitalRead(NIVEL_PIN));
}

// ===== LOOP =====
void loop() {
  BOMBA();
  moverServo();

  waterTemp = leerTemperaturaADC();

  if (millis() - lastTDSRead >= tdsInterval) {
    lastTDSRead = millis();
    actualizarTDS(waterTemp);
  }

  Serial.print("{\"waterTemp\":");
  Serial.print(waterTemp, 2);
  Serial.print(",\"tds\":");
  Serial.print(tds);
  Serial.print(",\"ec\":");
  Serial.print(ec, 3);
  Serial.print(",\"ph\":");
  Serial.print(leerPH(), 2);
  Serial.print(",\"dhtTemp\":");
  Serial.print(dht.readTemperature(), 1);
  Serial.print(",\"hum\":");
  Serial.print(dht.readHumidity(), 1);
  Serial.print(",\"nivel\":");
  Serial.print(digitalRead(NIVEL_PIN));
  Serial.println("}");

  delay(10);
}
