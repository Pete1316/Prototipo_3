
// ===== Pines =====
#define TDS_PIN A1
#define PH_PIN A0
#define TEMP_PIN A2
#define FOCO_PIN 7

// ===== TDS =====
#define VREF 5.0
#define SCOUNT 30
int tdsBuffer[SCOUNT];
int tdsBufferTemp[SCOUNT];
int tdsIndex = 0;
float tdsValue = 0;
float temperature = 25;

// ===== pH =====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

// ===== Factor EC =====
#define TDS_FACTOR 0.5

void setup() {
  pinMode(FOCO_PIN, OUTPUT);
  Serial.begin(9600);   // IMPORTANTE: mismo baud que ESP32
}

// ===== Funciones =====
float leerTDS() {
  int lectura = analogRead(TDS_PIN);
  tdsBuffer[tdsIndex++] = lectura;
  if (tdsIndex >= SCOUNT) tdsIndex = 0;

  for (int i = 0; i < SCOUNT; i++) tdsBufferTemp[i] = tdsBuffer[i];

  int temp = getMedianNum(tdsBufferTemp, SCOUNT);
  float voltaje = temp * VREF / 1024.0;
  float compensado = voltaje / (1.0 + 0.02 * (temperature - 25.0));

  tdsValue = (133.42 * compensado * compensado * compensado
            - 255.86 * compensado * compensado
            + 857.39 * compensado) * 0.5;

  return tdsValue;
}

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

float leerTemperatura() {
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


  digitalWrite(FOCO_PIN, HIGH);
  delay(1000);
  digitalWrite(FOCO_PIN, LOW);
  delay(1000);
  temperature = leerTemperatura();
  float tds = leerTDS();
  float ph = leerPH();
  float ec = tds / TDS_FACTOR;

  // ===== Enviar al ESP32 en formato JSON =====
  Serial.print("{\"temp\":");
  Serial.print(temperature, 1);
  Serial.print(",\"tds\":");
  Serial.print(tds, 0);
  Serial.print(",\"ph\":");
  Serial.print(ph, 2);
  Serial.print(",\"ec\":");
  Serial.print(ec, 0);
  Serial.println("}");
  
  delay(1000);
}