// ===============================
// VARIABLES GLOBALES
// ===============================
let ipESP32 = "";

// BOTONES
let Bomba_Agua, Ventilador, medicion, Automatico;

// FIREBASE
const firebaseSensoresURL = "https://esp32-a7ac9-default-rtdb.europe-west1.firebasedatabase.app/sensores.json";
const firebaseEstadoURL   = "https://esp32-a7ac9-default-rtdb.europe-west1.firebasedatabase.app//estado.json";

// ===============================
// CARGA INICIAL
// ===============================
window.onload = () => {

  // ---- IP ----
  ipESP32 = localStorage.getItem("ipESP32") || "192.168.0.102";
  document.getElementById("ipESP32").value = ipESP32;
  document.getElementById("ipActual").innerText = ipESP32;

  // ---- ENLAZAR BOTONES ----
  Automatico = document.getElementById("switch_Automatico");
  Bomba_Agua = document.getElementById("switch_Bomba");
  Ventilador = document.getElementById("switch_Ventilador");
  medicion   = document.getElementById("switch_Medicion");

  cargarEstado();           // <-- carga estado al inicio
  enlazarEventosBotones();  // <-- guarda cambios automáticamente
};

// ===============================
// MODO AUTOMÁTICO
// ===============================
function setModoAutomatico(activo) {
  Bomba_Agua.disabled = activo;
  Ventilador.disabled = activo;
  medicion.disabled   = activo;

  if (activo) {
    Bomba_Agua.checked = false;
    Ventilador.checked = false;
    medicion.checked   = false;
  }
}

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

  // Primero intento la ESP32 en la red local
  fetch(`http://${ipESP32}/datos`)
    .then(r => r.json())
    .then(d => actualizarInterfaz(d))
    .catch(err => {
      console.log("ESP32 local no disponible, consultando Firebase...", err);

      // Fallback a Firebase
      fetch(firebaseSensoresURL)
        .then(r => r.json())
        .then(d => actualizarInterfaz({
          temp: d.waterTemp,
          tds: d.tds,
          ph: d.ph,
          ec: d.ec,
          dhtTemp: d.dhtTemp,
          hum: d.hum,
          nivel: d.nivel
        }))
        .catch(e => console.log("Error Firebase:", e));
    });
}

// ===============================
// ACTUALIZAR INTERFAZ
// ===============================
function actualizarInterfaz(d) {
  document.querySelectorAll(".temp").forEach(el => el.innerText = d.temp);
  document.querySelectorAll(".hum").forEach(el => el.innerText = d.hum);

  document.getElementById("tds").innerText     = d.tds;
  document.getElementById("ph").innerText      = d.ph;
  document.getElementById("ec").innerText      = d.ec;
  document.getElementById("dhtTemp").innerText = d.dhtTemp;
  document.getElementById("hum").innerText     = d.hum;
  document.getElementById("nivel").innerText   = d.nivel;
}

// ===============================
// CONTROL DE ACTUADORES
// ===============================
function controlLED(accion) {
  // Solo control local si la ESP32 está disponible
  fetch(`http://${ipESP32}/led/${accion}`)
    .catch(e => console.log("No se pudo enviar comando al ESP32:", e));

  // ===== BOMBA =====
  if (accion === "on")  Bomba_Agua.checked = true;
  if (accion === "off") Bomba_Agua.checked = false;

  // ===== VENTILADOR =====
  if (accion === "on1")  Ventilador.checked = true;
  if (accion === "off1") Ventilador.checked = false;

  // ===== MEDICIÓN =====
  if (accion === "on2")  medicion.checked = true;
  if (accion === "off2") medicion.checked = false;

  // ===== MODO AUTOMÁTICO =====
  if (accion === "A") { Automatico.checked = true; setModoAutomatico(true); }
  if (accion === "B") { Automatico.checked = false; setModoAutomatico(false); }

  guardarEstado(); // <-- guardar cada cambio
}

// ===============================
// ENVIAR SETPOINTS
// ===============================
function enviarDato(num) {
  const input = document.getElementById(`setTemp${num}`);
  const valor = input.value;
  if (valor === "") { alert("Ingrese un valor"); return; }

  console.log(`Temperatura ${num}: ${valor} °C`);

  fetch(`http://${ipESP32}/setTemp?canal=${num}&valor=${valor}`)
    .then(() => {
      alert(`Setpoint ${num} enviado: ${valor} °C`);
      input.value = "";
    })
    .catch(err => {
      console.error(err);
      alert("Error al enviar al ESP32, intente en la red local");
    });
}

// ===============================
// ESTADO DE BOTONES
// ===============================
function guardarEstado() {
  const estado = {
    Bomba_Agua: Bomba_Agua.checked,
    Ventilador: Ventilador.checked,
    medicion: medicion.checked,
    Automatico: Automatico.checked
  };

  localStorage.setItem("estado_botones", JSON.stringify(estado));

  fetch(firebaseEstadoURL, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(estado)
  }).catch(e => console.log("No se pudo actualizar Firebase:", e));
}

function cargarEstado() {
  fetch(firebaseEstadoURL)
    .then(r => r.json())
    .then(estado => {
      if (estado) aplicarEstado(estado);
      else {
        const local = JSON.parse(localStorage.getItem("estado_botones"));
        if (local) aplicarEstado(local);
      }
    })
    .catch(err => {
      console.log("Error Firebase, cargando localStorage", err);
      const local = JSON.parse(localStorage.getItem("estado_botones"));
      if (local) aplicarEstado(local);
    });
}

function aplicarEstado(estado) {
  Bomba_Agua.checked = estado.Bomba_Agua;
  Ventilador.checked = estado.Ventilador;
  medicion.checked   = estado.medicion;
  Automatico.checked = estado.Automatico;

  setModoAutomatico(Automatico.checked);
}

// ===============================
// ENLAZAR EVENTOS BOTONES
// ===============================
function enlazarEventosBotones() {
  Bomba_Agua.addEventListener("change", guardarEstado);
  Ventilador.addEventListener("change", guardarEstado);
  medicion.addEventListener("change", guardarEstado);
  Automatico.addEventListener("change", () => {
    setModoAutomatico(Automatico.checked);
    guardarEstado();
  });
}

// ===============================
// REFRESCO AUTOMÁTICO
// ===============================
setInterval(actualizarDatos, 1000);
