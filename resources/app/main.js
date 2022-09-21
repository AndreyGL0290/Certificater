const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

let mainWindow

function createWindow () {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'preload.js')
        }
    })
    mainWindow.loadFile('Web\\HomePage.html');
    mainWindow.on('closed', function () {
        mainWindow = null
    })
}

app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {  
    if (mainWindow === null) createWindow()
})

ipcMain.on("start", (event, args) => {
    var executable = require("child_process").execFile("main.exe", [...args]);
    console.log("smth")
    executable.stdout.on("data", function (data) {
        console.log(data)
        event.sender.send("place-response", data)
    });

    executable.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        console.log(`stderr: ${data}`);
    });

    executable.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });

    // ДЛЯ РАЗРАБОТКИ

    // let options = {
    //     mode: "text",
    //     pythonPath: "C:\\Users\\Андрей\\AppData\\Local\\Programs\\Python\\Python39\\python.exe",
    //     args: [...args]
    // }
    // const { PythonShell } = require("python-shell")
    // PythonShell.run("py\\main.py", options, (err, data) => {
    //     if (err) throw err;
    //     // Отправляем полученные данные
    //     event.sender.send("place-response", data)
    // });
});

ipcMain.on("update", (event, args) => {
    var executable = require("child_process").execFile("update_email.exe", [...args]);

    executable.stdout.on("data", function (data) {
        console.log(data)
        event.sender.send("place-response", data)
    });

    executable.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        console.log(`stderr: ${data}`);
    });

    executable.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });

    // ДЛЯ РАЗРАБОТКИ

    // let options = {
    //     mode: "text",
    //     pythonPath: "C:\\Users\\Андрей\\AppData\\Local\\Programs\\Python\\Python39\\python.exe",
    //     args: [...args]
    // }

    // const { PythonShell } = require("python-shell")
    // PythonShell.run("py\\update_email.py", options, (err, response) => {
    //     if (err) throw err;
    //     // Отправляем полученные данные
    //     event.sender.send("place-response", data)
    // });
});