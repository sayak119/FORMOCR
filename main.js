// Modules to control application life and create native browser window
const { app, BrowserWindow, Menu } = require('electron')
const path = require('path')
const electron = require('electron')

function createWindow() {
  // Create the browser window.
  var screenElectron = electron.screen;
  var mainScreen = screenElectron.getPrimaryDisplay();
  //	var allScreens = screenElectron.getAllDisplays();
  var dimensions = mainScreen.size;

  const mainWindow = new BrowserWindow({
    width: dimensions.width,
    height: dimensions.height,
    icon: path.join(__dirname, '/Images/icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true
      //	preload: path.join(__dirname, 'renderer.js')
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  // Open the DevTools.
  //mainWindow.webContents.openDevTools()

  //To hide the menu bar.
  mainWindow.setMenuBarVisibility(false);

}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  app.quit()
})
  // In this file you can include the rest of your app's specific main process
  // code. You can also put them in separate files and require them here.

