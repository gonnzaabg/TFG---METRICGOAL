const { app, BrowserWindow } = require("electron");

let mainWindow; // 👈 IMPORTANTE (global)

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadURL("https://tfg-metricgoal-bueno.onrender.com");
}

app.whenReady().then(createWindow);