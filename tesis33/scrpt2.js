// ===============================
// FIREBASE SDK v9 (MODULAR)
// ===============================
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-database.js";

// ===============================
// CONFIGURACIÓN FIREBASE
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
// REFERENCIA A SENSORES
// ===============================
const sensoresRef = ref(db, "sensores");

// ===============================
// ESCUCHA TIEMPO REAL
// ===============================
onValue(sensoresRef, (snapshot) => {
  if (!snapshot.exists()) return;

  const d = snapshot.val();

  // Agua
  document.getElementById("temp1").innerText   = d.waterTemp ?? "--";
  document.getElementById("temp2").innerText   = d.waterTemp ?? "--";

  // Sensores
  document.getElementById("tds").innerText     = d.tds ?? "--";
  document.getElementById("ph").innerText      = d.ph ?? "--";
  document.getElementById("ec").innerText      = d.ec ?? "--";
  document.getElementById("dhtTemp").innerText = d.dhtTemp ?? "--";
  document.getElementById("hum").innerText     = d.hum ?? "--";
  document.getElementById("nivel").innerText   = d.nivel ?? "--";

});
