// miArchivo.js
console.log("JS cargado ✔");

// ===============================
// IMPORTS FIREBASE
// ===============================
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getDatabase, ref, onValue, set } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-database.js";

// ===============================
// CONFIG FIREBASE
// ===============================
const firebaseConfig = {
  apiKey: "AIzaSyBXAal12oFlxKZ81PlaDNnar_y2-DiZRlU",
  authDomain: "esp32-a7ac9.firebaseapp.com",
  databaseURL: "https://esp32-a7ac9-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "esp32-a7ac9",
  storageBucket: "esp32-a7ac9.firebasestorage.app",
  messagingSenderId: "312730525959",
  appId: "1:312730525959:web:dae44f28a4149dcee165a2"
};

// ===============================
// INIT FIREBASE
// ===============================
const app = initializeApp(firebaseConfig);
const db  = getDatabase(app);

// ===============================
// VARIABLES GLOBALES
// ===============================
let ipESP32 = localStorage.getItem("ipESP32") || "192.168.0.109";
let phAltoNotificado = false;

// ===============================
// CONTROL DE BOMBA
// ===============================
export function controlBomba(estado) {
  // Guardar estado en Firebase
  set(ref(db, "bombas/bomba1"), estado)
    .catch(e => console.log("No se pudo actualizar Firebase:", e));

  // Enviar comando al ESP32 si está en la red local
  fetch(`http://${ipESP32}/led/${estado ? "on" : "off"}`)
    .catch(e => console.log("ESP32 no disponible:", e));
}

// ===============================
// ESTADO LOCAL
// ===============================
export function guardarEstadoBomba(estado) {
  localStorage.setItem("estado_bomba", JSON.stringify({ Bomba_Agua: estado }));
  controlBomba(estado);
}

export function cargarEstadoBomba() {
  const local = JSON.parse(localStorage.getItem("estado_bomba"));
  return local ? local.Bomba_Agua : false;
}

// ===============================
// LECTURA DE SENSORES FIREBASE
// ===============================
export function escucharSensores(callback) {
  const sensoresRef = ref(db, "sensores");
  onValue(sensoresRef, snapshot => {
    const d = snapshot.val();
    if (!d) return;
    callback(d);

    // Notificación si el pH es alto
    if (d.ph > 6.5 && !phAltoNotificado) {
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("⚠️ Alerta pH", { body: `El pH está alto: ${d.ph}` });
        phAltoNotificado = true;
      }
    } else if (d.ph <= 6.5) {
      phAltoNotificado = false;
    }
  });
}

// ===============================
// INICIALIZACIÓN DE NOTIFICACIONES
// ===============================
export function initNotificaciones() {
  if ("Notification" in window) Notification.requestPermission();
}

// ===============================
// IP ESP32
// ===============================
export function setIP(ip) {
  ipESP32 = ip;
  localStorage.setItem("ipESP32", ip);
}
export function getIP() {
  return ipESP32;
}
