#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <LiquidCrystal_I2C.h>
#include "RTClib.h"
#include "DHT.h"
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11);// RX, TX

// ==== CONFIGURACIÓN DE PANTALLAS ====
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD 16x2 I2C

// ==== PINES ====
#define PH_PIN A0
#define BUZZER_PIN 8
#define DHT_PIN 4
#define NIVEL_PIN 5
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);
RTC_DS3231 rtc;

// ==== CALIBRACIÓN SENSOR pH ====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);

  // ==== INICIALIZAR OLED ====
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("No se encontró la pantalla OLED"));
    while (1);
  }

  // ==== INICIALIZAR LCD ====
  lcd.init();
  lcd.backlight();

  // ==== INICIALIZAR RTC ====
  if (!rtc.begin()) {
    Serial.println("No se encuentra el RTC");
    while (1);
  }

  // rtc.adjust(DateTime(2025,11,1,12,00,0)); // <-- Descomentar para ajustar hora manualmente

  // ==== SENSORES ====
  dht.begin();
  pinMode(NIVEL_PIN, INPUT_PULLUP); // Nivel de agua: LOW = agua OK, HIGH = bajo nivel
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  // ==== MENSAJE DE INICIO ====
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Iniciando...");
  display.display();
  delay(2000);
}


void loop() {
  // ==== LECTURA DEL SENSOR DE pH ====
  int prom = 0;
  for (int i = 0; i < 20; i++) {
    prom += analogRead(PH_PIN);
    delay(50);
  }
  prom = prom / 20;

  float ph;
  if (prom <= m_7) {
    ph = 4.01 + (prom - m_4) * (6.86 - 4.01) / (m_7 - m_4);
  } else {
    ph = 6.86 + (prom - m_7) * (9.18 - 6.86) / (m_9 - m_7);
  }

  // ==== LECTURA SENSOR DHT22 ====
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

  // ==== LECTURA SENSOR DE NIVEL ====
  int nivel = digitalRead(NIVEL_PIN); // LOW = hay agua, HIGH = nivel bajoLHF

  // ==== FECHA Y HORA ====
  DateTime now = rtc.now();

  // ==== MOSTRAR EN OLED ====
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  // Fecha
  display.setCursor(0, 0);
  display.print(now.day()); display.print("/");
  display.print(now.month()); display.print("/");
  display.print(now.year());

  // Hora
  display.setCursor(0, 10);
  if (now.hour() < 10) display.print("0");
  display.print(now.hour()); display.print(":");
  if (now.minute() < 10) display.print("0");
  display.print(now.minute()); display.print(":");
  if (now.second() < 10) display.print("0");
  display.print(now.second());

  // pH
  display.setTextSize(2);
  display.setCursor(0, 25);
  display.print("pH: ");
  display.println(ph, 2);

  // Nivel de agua
  display.setTextSize(1);
  display.setCursor(0, 50);
  display.print("Nivel: ");
  if (nivel == LOW)
    display.print("OK");
  else
    display.print("BAJO!");

  display.display();

  // ==== MOSTRAR SOLO DHT22 EN LCD ====
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  if (isnan(temperatura)) lcd.print("--");
  else lcd.print(temperatura, 1);
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.print("Humedad: ");
  if (isnan(humedad)) lcd.print("--");
  else lcd.print(humedad, 1);
  lcd.print("%");

  // ==== ALARMAS ====
  bool alarmaPH = (ph > 8.0 || ph < 5.5);
  bool alarmaNivel = (nivel == HIGH);

  if (alarmaPH || alarmaNivel) {
    tone(BUZZER_PIN, 1000);
    delay(300);
    noTone(BUZZER_PIN);
    delay(300);
  } else {
    noTone(BUZZER_PIN);
  }

  // ==== SERIAL ====
  Serial.print("pH: "); Serial.print(ph, 2);
  Serial.print(" | Temp: "); Serial.print(temperatura);
  Serial.print(" | Hum: "); Serial.print(humedad);
  Serial.print(" | Nivel: ");
  Serial.println((nivel == LOW) ? "OK" : "BAJO");

  delay(1000);
  String mensaje = "pH: " + String(ph, 2) +
                 " | Temp: " + String(temperatura) +
                 " | Hum: " + String(humedad) +
                 " | Nivel: " + (nivel == LOW ? "OK" : "BAJO");

Serial.println(mensaje);
BTSerial.println(mensaje);   // ← Lo envía al HC-05

}