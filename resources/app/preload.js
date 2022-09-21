const { contextBridge, ipcRenderer } = require('electron')

const API = {
    start: (args) => ipcRenderer.send('start', args),
    updateEmail: (args) => ipcRenderer.send('update', args),
    onResponse: (callback) => ipcRenderer.on("place-response", (event, args) => {
        callback(args)
    })
}

contextBridge.exposeInMainWorld('api', API)