// firebase-messaging-sw.js
importScripts("https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js");

const firebaseConfig = {
  apiKey: "AIzaSyBXAal12oFlxKZ81PlaDNnar_y2-DiZRlU",
  authDomain: "esp32-a7ac9.firebaseapp.com",
  projectId: "esp32-a7ac9",
  storageBucket: "esp32-a7ac9.firebasestorage.app",
  messagingSenderId: "312730525959",
  appId: "1:312730525959:web:dae44f28a4149dcee165a2"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Opcional: manejar notificaciones en segundo plano
messaging.onBackgroundMessage((payload) => {
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.icon || "/icon-192.png",
    badge: "/icon-72.png"
  };
  self.registration.showNotification(notificationTitle, notificationOptions);
});