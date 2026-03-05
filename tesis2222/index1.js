// ===============================
// VARIABLES GLOBALES
// ===============================
let ipESP32 = "";

// BOTONES
let btnOn, btnOff;
let btnOn1, btnOff1;
let btnOn2, btnOff2;
let btnOn3, btnOff3;

// SENSORES
let temp, tds, ph, ec, dhtTemp, hum, nivel;

// ===============================
// CARGA INICIAL
// ===============================
window.onload = () => {

  // ---- IP ----
  ipESP32 = localStorage.getItem("ipESP32") || "192.168.0.102";
  localStorage.setItem("ipESP32", ipESP32);

  document.getElementById("ipESP32").value = ipESP32;
  document.getElementById("ipActual").innerText = ipESP32;

  // ---- BOTONES ----
  btnOn  = document.getElementById("B1");
  btnOff = document.getElementById("B2");

  btnOn1  = document.getElementById("B3");
  btnOff1 = document.getElementById("B4");

  btnOn2  = document.getElementById("B5");
  btnOff2 = document.getElementById("B6");

  btnOn3  = document.getElementById("B7");
  btnOff3 = document.getElementById("B8");

  // ---- SENSORES ----
  temp    = document.getElementById("temp");
  tds     = document.getElementById("tds");
  ph      = document.getElementById("ph");
  ec      = document.getElementById("ec");
  dhtTemp = document.getElementById("dhtTemp");
  hum     = document.getElementById("hum");
  nivel   = document.getElementById("nivel");
};

// ===============================
// GUARDAR IP
// ===============================
function guardarIP() {
  const nuevaIP = document.getElementById("ipESP32").value.trim();
  if (nuevaIP.length < 7) return alert("IP no válida");

  ipESP32 = nuevaIP;
  localStorage.setItem("ipESP32", ipESP32);
  document.getElementById("ipActual").innerText = ipESP32;

  alert("IP guardada correctamente");
}

// ===============================
// ACTUALIZAR SENSORES
// ===============================
function actualizarDatos() {
  if (!ipESP32) return;

  fetch(`http://${ipESP32}/datos`)
    .then(r => r.json())
    .then(d => {
      temp.innerText    = d.temp ?? "--";
      tds.innerText     = d.tds ?? "--";
      ph.innerText      = d.ph ?? "--";
      ec.innerText      = d.ec ?? "--";
      dhtTemp.innerText = d.dhtTemp ?? "--";
      hum.innerText     = d.hum ?? "--";
      nivel.innerText   = d.nivel ?? "--";
    })
    .catch(e => console.log("ESP32 offline"));
}

// ===============================
// CONTROL DE ACTUADORES
// ===============================
function controlDispositivo(dispositivo, estado) {

  const accion = estado ? "on" : "off";

  fetch(`http://${ipESP32}/${dispositivo}/${accion}`)
    .then(res => res.text())
    .then(data => console.log(`${dispositivo}: ${data}`))
    .catch(err => console.error("Error ESP32:", err));
}

// ===============================
// REFRESCO AUTOMÁTICO
// ===============================
setInterval(actualizarDatos, 1000);
