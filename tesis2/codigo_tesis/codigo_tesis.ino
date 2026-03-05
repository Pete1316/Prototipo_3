Si funciona

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <LiquidCrystal_I2C.h>
#include "RTClib.h"
#include "DHT.h"
#include <SoftwareSerial.h>


SoftwareSerial BTSerial(10,11);
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD 16x2 I2C

#define PH_PIN A0
#define BUZZER_PIN 8
#define DHT_PIN 4
#define NIVEL_PIN_AGUA 5
#define DHT_TYPE DHT22

unsigned long ultimoEnvio = 0;
const unsigned long intervalo = 5000; 

DHT dht(DHT_PIN, DHT_TYPE);
RTC_DS3231 rtc;

// ==== CALIBRACIÓN SENSOR pH ====
int m_4 = 948;
int m_7 = 849;
int m_9 = 761;

void setup() {
  lcd.init();
  lcd.backlight();
  dht.begin(); // Si no se ubica no funciona el DHT
  //rtc.adjust(DateTime(2025,11,18,21,58,0));
  if (!rtc.begin()) {
    Serial.println("No se encuentra el RTC");
    while (1);
  }

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("No se encontró la pantalla OLED"));
    while (1);
  }
  

  //sensor nivel de agua
  pinMode(NIVEL_PIN_AGUA, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Iniciando...");
  display.display();
  Serial.begin(9600);
  BTSerial.begin(9600);
  delay(2000);


}
void loop() {
//Sensor de DHT22
  float temperatura = dht.readTemperature();
  float humedad =dht.readHumidity();
  int nivel = digitalRead(NIVEL_PIN_AGUA);
  String nivel_2;
  




//Sensor de pH
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
  



  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
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


  //Nivel de Agua
  display.setCursor(0, 50);
  display.print("Nivel;");
  if (nivel == LOW){
  display.print("OK");
  nivel_2 = "OK";
  } else{
  display.print("Bajo");
  nivel_2 = "Bajo";
  }
 

  //Pantalla OLED
  display.setCursor(0, 25);
  display.print("pH:");
  display.println(ph,2);





  display.display();



  //Pantalla LCD
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Temp:");
  if (isnan(temperatura)) lcd.print("--");
  else lcd.print(temperatura, 1);
  lcd.print("C");

  lcd.setCursor(0,1);
  lcd.print("Hum:");
  if (isnan(humedad)) lcd.print("--");
  else lcd.print(humedad, 1);
  lcd.print("%");

//Enviar Informacion mediante Bluetooth 
  if (millis() - ultimoEnvio > intervalo) {
    float ph_agua = ph;
    float temperatura_ambiente = temperatura;
    float humedad_ambiente = humedad;
    

    if(!isnan(ph_agua)){
    BTSerial.print("pH:");
    BTSerial.println(ph_agua);
    }
    if(!isnan(temperatura_ambiente)){
      BTSerial.print("Tem_AB");
      BTSerial.println(temperatura_ambiente);
    }
    if(!isnan(humedad_ambiente)){
      BTSerial.print("hum_AB");
      BTSerial.println(humedad_ambiente);
    }
      //Solo para datos String se agrega asi los otros son para numeros 
      BTSerial.print("Nivel_A");
      BTSerial.println(nivel_2);
    
  ultimoEnvio = millis();
  }
}


