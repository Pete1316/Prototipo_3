// ===============================
// VARIABLES GLOBALES
// ===============================
let ipESP32 = "";

// BOTONES
let Bomba_Agua, Ventilador, medicion, Automatico;

// ===============================
// CARGA INICIAL
// ===============================
window.onload = () => {

  // ---- IP ----
  ipESP32 = localStorage.getItem("ipESP32");
  if (!ipESP32) {
    ipESP32 = "192.168.0.102";
    localStorage.setItem("ipESP32", ipESP32);
  }

  document.getElementById("ipESP32").value = ipESP32;
  document.getElementById("ipActual").innerText = ipESP32;

  // ---- ENLAZAR BOTONES ----
  Automatico = document.getElementById("switch_Automatico");
  Bomba_Agua = document.getElementById("switch_Bomba");
  Ventilador = document.getElementById("switch_Ventilador");
  medicion   = document.getElementById("switch_Medicion");
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

  fetch(`http://${ipESP32}/datos`)
    .then(r => r.json())
    .then(d => {
            document.querySelectorAll(".temp").forEach(el => {
        el.innerText = d.temp;} );

        document.querySelectorAll(".hum").forEach(el => {
        el.innerText = d.hum;} );


      tds.innerText     = d.tds;
      ph.innerText      = d.ph;
      ec.innerText      = d.ec;
      dhtTemp.innerText = d.dhtTemp;
      hum.innerText     = d.hum;
    
      nivel.innerText   = d.nivel;
    })
    .catch(e => console.log(e));
}

// ===============================
// CONTROL DE ACTUADORES
// ===============================
function controlLED(accion) {

  fetch(`http://${ipESP32}/led/${accion}`);

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
  if (accion === "A") {
    Automatico.checked = true;
    setModoAutomatico(true);
  }

  if (accion === "B") {
    Automatico.checked = false;
    setModoAutomatico(false);
  }
}




function enviarDato(num) {
  const input = document.getElementById(`setTemp${num}`);
  const valor = input.value;

  if (valor === "") {
    alert("Ingrese un valor");
    return;
  }

  console.log(`Temperatura ${num}: ${valor} °C`);

  // ENVÍO AL ESP32
  fetch(`http://${ipESP32}/setTemp?canal=${num}&valor=${valor}`)
    .then(() => {
      alert(`Setpoint ${num} enviado: ${valor} °C`);
      input.value = ""; // opcional
    })
    .catch(err => {
      console.error(err);
      alert("Error al enviar");
    });
}

// ===============================
// REFRESCO
// ===============================
setInterval(actualizarDatos, 1000);
