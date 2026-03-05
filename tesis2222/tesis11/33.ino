#include <WiFi.h>
#include <Wire.h>
#include <WebServer.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>
#include <ESPmDNS.h>   // <---- AGREGADO (mDNS)

// ===== Configuración WiFi =====
const char* ssid     = "Manantial Azul Invitados";
const char* password = "1316444403";

// ===== Variables de sensores =====
float temp = 0;
float tds  = 0;
float ph   = 0;
float ec   = 0;
float dhtTemp = 0;
float hum = 0;
int nivel = 0;
int modo = 0;
int setpoint1 = 0;
int setpoint2 = 0;
float histeresis = 1.0; // 1 grado

int pantalla = 0;
const int boton = 14;
LiquidCrystal_I2C lcd(0x27, 16, 2); // Dirección I2C, 16 columnas, 2 filas
int ultimoEstado = HIGH; // Último estado del botón
unsigned long ultimoTiempo = 0;
const unsigned long debounce = 525; // Tiempo de debounce en ms

bool ventiladorManual = false;
bool bonbaManual= false;

// ===== Pines de LEDs =====
const int ledPin  = 2;   // Bomba agua
const int ledPin1 = 4;   // Ventilador
const int ledPin2 = 5;   // pH
const int ledPin3 = 12;

// ===== Servidor web en puerto 80 =====
WebServer server(80);

// ===== Buffer para datos Arduino =====
String buffer = "";
bool leyendo = false;

void setup() {
  // Inicializar LEDs
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);

  pinMode(boton, INPUT_PULLUP); // Resistencia interna pull-up
  lcd.init();       
  lcd.backlight();  
  lcd.setCursor(0, 0);
  lcd.print("Presiona boton");

  Serial.begin(9600);

  // Inicializar Serial2
  Serial2.begin(9600, SERIAL_8N1, 32, 35);

  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // ===== RUTAS DEL SERVIDOR =====
  server.on("/datos", HTTP_GET, []() {
    String json = "{";
    json += "\"temp\":" + String(temp) + ",";
    json += "\"tds\":"  + String(tds)  + ",";
    json += "\"ph\":"   + String(ph)   + ",";
    json += "\"ec\":"   + String(ec)   + ",";
    json += "\"dhtTemp\":"   + String(dhtTemp)   + ",";
    json += "\"hum\":"   + String(hum)   + ",";
    json += "\"nivel\":"   + String(nivel);
    json += "}";
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "application/json", json);
  });

  server.on("/led/on", HTTP_GET, []() {
    digitalWrite(ledPin, HIGH);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 1 ENCENDIDO");
  });

  server.on("/led/off", HTTP_GET, []() {
    digitalWrite(ledPin, LOW);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 1 APAGADO");
  });

  server.on("/led/on1", HTTP_GET, []() {
    digitalWrite(ledPin1, HIGH);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 2 ENCENDIDO");
  });

  server.on("/led/off1", HTTP_GET, []() {
    digitalWrite(ledPin1, LOW);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 2 APAGADO");
  });

  server.on("/led/on2", HTTP_GET, []() {
    digitalWrite(ledPin2, HIGH);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 3 ENCENDIDO");
  });

  server.on("/led/off2", HTTP_GET, []() {
    digitalWrite(ledPin2, LOW);
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "LED 3 APAGADO");
  });

  server.on("/led/A", HTTP_GET, [](){
    modo = 0;
    server.send(200, "text/plain", "AUTO ON");
  });

  server.on("/led/B", HTTP_GET, [](){    
    modo = 1;
    digitalWrite(ledPin1, LOW);
    server.send(200, "text/plain", "AUTO OFF");
  });

  server.on("/setTemp", HTTP_GET, []() {
    if (!server.hasArg("canal") || !server.hasArg("valor")) {
      server.send(400, "text/plain", "Faltan parametros");
      return;
    }

    int canal = server.arg("canal").toInt();
    int valor = server.arg("valor").toInt();

    if (canal == 1) {
      setpoint1 = valor;
      Serial.println("Dato1");
      Serial.println(setpoint1);
    }
    else if (canal == 2) {
      setpoint2 = valor;
      Serial.println("Dato2");
      Serial.println(setpoint2);
    }

    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

void loop() {
  server.handleClient();
  recibirDatosArduino();
  tipo_Automatico_Manual();
  contar_boton();
  actualizar_LCD();
}

void tipo_Automatico_Manual(){
  switch (modo) {
    case 0:  // AUTOMÁTICO
      if (temp > setpoint1 ) {
        digitalWrite(ledPin1, HIGH);
      } else {
        digitalWrite(ledPin1, LOW);
      }
      if (hum > setpoint2) {
        digitalWrite(ledPin, HIGH);
      } else {
        digitalWrite(ledPin, LOW);
      }
      break;

    case 1:  // MANUAL
      // El ventilador se controla solo desde la web
      break;
  }
}

// ===== Función para recibir datos desde Arduino =====
void recibirDatosArduino() {
  while (Serial2.available() > 0) {
    char c = Serial2.read();

    if (c == '{') {
      buffer = "{";
      leyendo = true;
    }
    else if (c == '}' && leyendo) {
      buffer += "}";
      leyendo = false;

      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, buffer);

      if (!error) {
        temp = doc["temp"];
        tds  = doc["tds"];
        ph   = doc["ph"];
        ec   = doc["ec"];
        dhtTemp = doc["dhtTemp"];
        hum = doc["hum"];
        nivel = doc["nivel"];
      }

      buffer = "";
    }
    else if (leyendo) {
      buffer += c;
    }
  }
}

void contar_boton() {
  int estadoActual = digitalRead(boton);

  if (estadoActual == LOW && ultimoEstado == HIGH && (millis() - ultimoTiempo) > debounce) {
    pantalla++;
    if (pantalla > 4) pantalla = 1;
    ultimoTiempo = millis();
  }

  ultimoEstado = estadoActual;
}

void actualizar_LCD() {
  switch(pantalla) {
    case 1:
      lcd.setCursor(0,0);
      lcd.print("IP:                              "); // limpia toda la línea
      lcd.setCursor(0,1);
      lcd.print(WiFi.localIP().toString() + "                   "); // limpia resto de línea
      break;
    case 2:
      lcd.setCursor(0,0);
      lcd.print("Temperatura:                         "); // limpia toda la línea
      lcd.setCursor(0,1);
      lcd.print(String(temp) + "                            "); // limpia resto de línea
      break;
    case 3:
      lcd.setCursor(0,0);
      lcd.print("Humedad:        "); // limpia toda la línea
      lcd.setCursor(0,1);
      lcd.print(String(hum) + "        "); // limpia resto de línea
      break;
    case 4:
      lcd.setCursor(0,0);
      lcd.print("pH:              "); // limpia toda la línea
      lcd.setCursor(0,1);
      lcd.print(String(ph) + "        "); // limpia resto de línea
      break;
  }
}