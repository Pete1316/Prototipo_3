const { app, BrowserWindow } = require("electron");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  win.setMenu(null);
  win.loadFile("index.html");

  // 🔥 evita que Electron pause Firebase
  win.on("minimize", () => {
    win.restore();
  });

  win.webContents.on("did-finish-load", () => {
    win.webContents.setZoomFactor(0.65);
    win.webContents.setVisualZoomLevelLimits(1, 1);
  });
}

// 🔥 CRÍTICO para tiempo real
app.commandLine.appendSwitch("disable-background-timer-throttling");
app.commandLine.appendSwitch("disable-renderer-backgrounding");
app.commandLine.appendSwitch("disable-backgrounding-occluded-windows");

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

