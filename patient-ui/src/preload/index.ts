import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  getCameraPermission: () => ipcRenderer.invoke("get-camera-permission"),
});
