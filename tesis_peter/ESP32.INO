#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <Preferences.h>

// ===== Memoria NVS =====
Preferences prefs;

// ===== Servidor para modo configuración =====
WebServer server(80);

// ===== Variables WiFi =====
String ssidSaved = "";
String passSaved = "";

// ===== URL Firebase =====
String firebaseURL = "https://esp32-a9f92-default-rtdb.europe-west1.firebasedatabase.app/";

// ===== Variables de sensores =====
String temp = "--";
String tds  = "--";
String ph   = "--";
String ec   = "--";

// ===== Buffer Serial =====
String buffer = "";
bool leyendo = false;

// ===== LED =====
const int ledPin = 2; // Cambia según tu conexión
String ledState = "off";

// ===== Botón físico =====
const int botonPin = 4;

// =========================================================
//            HTML COMPLETO MODO CONFIGURACIÓN
// =========================================================
String htmlConfig = R"rawliteral(
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Configurar WiFi – ESP32</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
body {background: linear-gradient(135deg, #f8f9fa, #e9ecef);padding-top:3rem;padding-bottom:3rem;}
.card {border-radius:12px; box-shadow:0 6px 20px rgba(0,0,0,0.08); max-width:500px; margin:0 auto; border:none;}
.card-header {background:#495057; color:white; font-weight:600; font-size:1.25rem; text-align:center; border-radius:12px 12px 0 0 !important; padding:1.25rem;}
.form-label {font-weight:500;color:#495057;margin-top:1rem;}
.btn-primary {background-color:#28a745;border:none;padding:0.65rem;font-weight:600;}
.btn-primary:hover {background-color:#218838;}
</style>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header"><i class="bi bi-wifi"></i> Configurar Red WiFi – ESP32</div>
    <div class="card-body">
      <form action="/save" method="POST">
        <div class="mb-3">
          <label for="ssid" class="form-label"><i class="bi bi-reception-4 me-2"></i>Nombre de la red (SSID)</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-wifi"></i></span>
            <input type="text" id="ssid" name="ssid" class="form-control" placeholder="Ej: MiCasaWiFi" required>
          </div>
        </div>
        <div class="mb-4">
          <label for="pass" class="form-label"><i class="bi bi-shield-lock me-2"></i>Contraseña</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-key"></i></span>
            <input type="password" id="pass" name="pass" class="form-control" placeholder="••••••••" required>
            <button class="btn btn-outline-secondary" type="button" id="togglePass"><i class="bi bi-eye"></i></button>
          </div>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary"><i class="bi bi-save me-2"></i>Guardar y Reiniciar</button>
        </div>
      </form>
    </div>
  </div>
  <div class="text-center mt-4 text-muted small">
    El dispositivo se reiniciará automáticamente tras guardar.
  </div>
</div>
<script>
const toggleButton = document.getElementById('togglePass');
const passwordInput = document.getElementById('pass');
toggleButton.addEventListener('click', function() {
  const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput.setAttribute('type', type);
  this.innerHTML = type === 'password' ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
});
</script>
</body>
</html>
)rawliteral";

// =========================================================
//          Cargar credenciales guardadas
// =========================================================
void cargarWiFiGuardado() {
  prefs.begin("wifi", true);
  ssidSaved = prefs.getString("ssid", "");
  passSaved = prefs.getString("pass", "");
  prefs.end();
}

// =========================================================
//            Guardar nuevas credenciales WiFi
// =========================================================
void guardarWiFi(String ssid, String pass) {
  prefs.begin("wifi", false);
  prefs.putString("ssid", ssid);
  prefs.putString("pass", pass);
  prefs.end();
}

// =========================================================
//            Modo configuración – AP
// =========================================================
void iniciarModoConfig() {
  Serial.println("\n⚠ No se pudo conectar a WiFi");
  Serial.println("Iniciando modo configuración...");

  WiFi.softAP("ESP32_Config", "12345678");
  Serial.print("Accede a: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", []() {
    server.send(200, "text/html", htmlConfig);
  });

  server.on("/save", []() {
    String s = server.arg("ssid");
    String p = server.arg("pass");
    guardarWiFi(s, p);
    server.send(200, "text/plain", "Guardado! El ESP32 se reiniciará.");
    delay(1500);
    ESP.restart();
  });

  server.begin();

  while (true) server.handleClient();
}

// =========================================================
//                  Conectar al WiFi
// =========================================================
void conectarWiFi() {
  cargarWiFiGuardado();
  String ssidTry = ssidSaved.length() > 0 ? ssidSaved : "";
  String passTry = passSaved.length() > 0 ? passSaved : "";
  Serial.print("Conectando a: ");
  Serial.println(ssidTry);
  WiFi.begin(ssidTry.c_str(), passTry.c_str());
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("IP local: "); Serial.println(WiFi.localIP());
  } else {
    iniciarModoConfig();
  }
}

// =========================================================
//                  Enviar sensores a Firebase
// =========================================================
void enviarFirebase(String json) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = firebaseURL + "sensores.json";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.PUT(json);
    if (httpCode > 0) Serial.println("Sensores enviados OK");
    else Serial.println("Error enviando sensores: " + String(httpCode));
    http.end();
  }
}

// =========================================================
//                  Leer estado LED desde Firebase
// =========================================================
void leerLED() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = firebaseURL + "led/state.json";
    http.begin(url);
    int httpCode = http.GET();
    if (httpCode == 200) {
      String payload = http.getString();
      payload.replace("\"", "");
      if (payload != ledState) {
        ledState = payload;
        digitalWrite(ledPin, (ledState == "on") ? HIGH : LOW);
        Serial.println("LED actualizado desde Firebase: " + ledState);
      }
    } else {
      Serial.println("Error al leer LED: " + String(httpCode));
    }
    http.end();
  }
}

// =========================================================
//                  Actualizar LED a Firebase
// =========================================================
void actualizarLEDFirebase(String estado) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = firebaseURL + "led.json";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    String json = "{\"state\":\"" + estado + "\"}";
    int httpCode = http.PUT(json);
    if (httpCode == 200 || httpCode == 204) {
      ledState = estado;
      digitalWrite(ledPin, (estado == "on") ? HIGH : LOW);
      Serial.println("LED enviado a Firebase: " + estado);
    } else {
      Serial.println("Error enviando LED a Firebase: " + String(httpCode));
    }
    http.end();
  }
}

// =========================================================
//                  SETUP PRINCIPAL
// =========================================================
void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  pinMode(botonPin, INPUT_PULLUP);

  conectarWiFi();
}

// =========================================================
//                  LOOP PRINCIPAL
// =========================================================
void loop() {
  // ===== Leer Serial de sensores =====
  while (Serial2.available()) {
    char c = Serial2.read();
    if (c == '{') { buffer = "{"; leyendo = true; } 
    else if (c == '}' && leyendo) {
      buffer += "}"; leyendo = false;
      Serial.println("JSON recibido: " + buffer);

      int i1 = buffer.indexOf("\"temp\":");
      int i2 = buffer.indexOf(",", i1);
      temp = buffer.substring(i1 + 7, i2);

      i1 = buffer.indexOf("\"tds\":");
      i2 = buffer.indexOf(",", i1);
      tds = buffer.substring(i1 + 6, i2);

      i1 = buffer.indexOf("\"ph\":");
      i2 = buffer.indexOf(",", i1);
      ph = buffer.substring(i1 + 5, i2);

      i1 = buffer.indexOf("\"ec\":");
      i2 = buffer.indexOf("}", i1);
      ec = buffer.substring(i1 + 5, i2);

      buffer = "";

      String jsonFirebase = "{\"temp\":" + temp + ",\"tds\":" + tds + ",\"ph\":" + ph + ",\"ec\":" + ec + "}";
      enviarFirebase(jsonFirebase);
    } 
    else if (leyendo) buffer += c;
  }

  // ===== Leer LED desde Firebase =====
  leerLED();

  // ===== Leer botón físico =====
  if (digitalRead(botonPin) == LOW) { // pulsado
    String nuevoEstado = (ledState == "on") ? "off" : "on";
    actualizarLEDFirebase(nuevoEstado);
    delay(500); // debounce
  }

  delay(500); // evitar saturar Firebase
}


