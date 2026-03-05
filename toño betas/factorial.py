import wx
import serial
from pymongo import MongoClient
from datetime import datetime

# Conexión a Arduino
arduino = serial.Serial('COM7', 9600)

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
coleccion = cliente["arduino"]["comandos"]

# Función para guardar en la base de datos
def guardar(accion):
    coleccion.insert_one({"accion": accion, "fecha": datetime.now()})

# Ventana principal
class Ventana(wx.Frame):
    def __init__(self):
        super().__init__(None, title="LED Control", size=(250, 180))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.texto = wx.StaticText(panel, label="Estado del LED")
        self.texto.SetBackgroundColour("gray")
        self.texto.SetForegroundColour("white")
        self.texto.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(self.texto, flag=wx.EXPAND | wx.ALL, border=10)

        btn_on = wx.Button(panel, label="Encender")
        btn_off = wx.Button(panel, label="Apagar")
        btn_on.Bind(wx.EVT_BUTTON, self.encender)
        btn_off.Bind(wx.EVT_BUTTON, self.apagar)

        vbox.Add(btn_on, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(btn_off, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def encender(self, e):
        arduino.write(b"$On\n")
        self.texto.SetLabel("LED ENCENDIDO")
        self.texto.SetBackgroundColour("green")
        guardar("ENCENDER")

    def apagar(self, e):
        arduino.write(b"$Off\n")
        self.texto.SetLabel("LED APAGADO")
        self.texto.SetBackgroundColour("red")
        guardar("APAGAR")

# Ejecutar
if __name__ == "__main__":
    app = wx.App(False)
    Ventana()
    app.MainLoop()
