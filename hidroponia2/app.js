// ========= IMPORTAR FIREBASE =========
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";
import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged }
from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// ========= CONFIGURACIÓN FIREBASE =========
const firebaseConfig = {
  apiKey: "AIzaSyDzxgiVwirLRqNnLhyhIjPBijLv9kRDI-I",
  authDomain: "esp32-a9f92.firebaseapp.com",
  databaseURL: "https://esp32-a9f92-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "esp32-a9f92",
  storageBucket: "esp32-a9f92.appspot.com",
  messagingSenderId: "917386871044",
  appId: "1:917386871044:web:872db9ffa05fb85e7d5051"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth(app);

// ========= ELEMENTOS HTML =========
const loginDiv = document.getElementById("loginDiv");
const dataDiv = document.getElementById("dataDiv");
const loginError = document.getElementById("loginError");

// ========= LOGIN =========
document.getElementById("loginBtn").addEventListener("click", () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  loginError.textContent = "";

  signInWithEmailAndPassword(auth, email, password)
    .catch(error => {
      loginError.textContent = "Error: " + error.message;
    });
});

// ========= LOGOUT =========
document.getElementById("logoutBtn").addEventListener("click", () => {
  signOut(auth);
});

// ========= DETECTAR USUARIO ACTIVO =========
onAuthStateChanged(auth, user => {
  if (user) {
    loginDiv.style.display = "none";
    dataDiv.style.display = "block";

    leerDatosSensores();

  } else {
    loginDiv.style.display = "block";
    dataDiv.style.display = "none";
  }
});

// ========= LECTURA EN TIEMPO REAL =========
function leerDatosSensores() {
  const sensoresRef = ref(db, 'sensores');

  onValue(sensoresRef, snapshot => {
    const data = snapshot.val();
    if (!data) return;

    const temp = parseFloat(data.temp);
    const tds  = parseInt(data.tds);
    const ph   = parseFloat(data.ph);
    const ec   = parseInt(data.ec);

    document.getElementById("temp").textContent = temp.toFixed(1);
    document.getElementById("temp").className = (temp >= 20 && temp <= 26) ? "normal" : "alert";

    document.getElementById("tds").textContent = tds;
    document.getElementById("tds").className = (tds >= 400 && tds <= 800) ? "normal" : "alert";

    document.getElementById("ph").textContent = ph.toFixed(2);
    document.getElementById("ph").className = (ph >= 5.5 && ph <= 6.5) ? "normal" : "alert";

    document.getElementById("ec").textContent = ec;
    document.getElementById("ec").className = (ec >= 800 && ec <= 1500) ? "normal" : "alert";
  });
}
