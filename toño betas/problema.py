import wx
import serial
from pymongo import MongoClient
from datetime import datetime
import threading

class ArduinoApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Control LED", size=(300, 240))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.estado_led = wx.StaticText(panel, label="LED: Desconocido")
        self.nivel_luz = wx.StaticText(panel, label="Luz: N/D")
        self.nivel_mov = wx.StaticText(panel, label="Movimiento: N/D")

        sizer.Add(self.estado_led, flag=wx.ALL, border=5)
        sizer.Add(self.nivel_luz, flag=wx.ALL, border=5)
        sizer.Add(self.nivel_mov, flag=wx.ALL, border=5)

        btn_on = wx.Button(panel, label="Encender LED")
        btn_off = wx.Button(panel, label="Apagar LED")
        btn_on.Bind(wx.EVT_BUTTON, self.encender_led)
        btn_off.Bind(wx.EVT_BUTTON, self.apagar_led)

        sizer.Add(btn_on, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_off, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)
        self.Centre()
        self.Show()

        # Arduino y MongoDB
        try:
            self.arduino = serial.Serial('COM7', 9600, timeout=1)
        except:
            self.arduino = None
            wx.MessageBox("No se pudo conectar con Arduino", "Error")

        try:
            mongo = MongoClient("mongodb://localhost:27017")
            db = mongo["arduino"]
            self.cmds = db["comandos"]
            self.luz = db["luz"]
            self.mov = db["movimiento"]
        except:
            wx.MessageBox("No se pudo conectar a MongoDB", "Error")

        self.luz_valor = None
        self.mov_valor = None

        if self.arduino:
            threading.Thread(target=self.leer_datos, daemon=True).start()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.actualizar_gui, self.timer)
        self.timer.Start(1000)

    def encender_led(self, event):
        self.enviar_comando("$On\n")
        self.estado_led.SetLabel("LED: ENCENDIDO")
        self.cmds.insert_one({"accion": "ENCENDER", "hora": datetime.now()})

    def apagar_led(self, event):
        self.enviar_comando("$Off\n")
        self.estado_led.SetLabel("LED: APAGADO")
        self.cmds.insert_one({"accion": "APAGAR", "hora": datetime.now()})

    def enviar_comando(self, cmd):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(cmd.encode())

    def leer_datos(self):
        while True:
            try:
                linea = self.arduino.readline().decode().strip()
                if linea.startswith("luz:"):
                    valor = int(linea.split(":")[1])
                    self.luz_valor = valor
                    self.luz.insert_one({"valor": valor, "hora": datetime.now()})
                elif linea.startswith("movimiento:"):
                    valor = int(linea.split(":")[1])
                    self.mov_valor = valor
                    self.mov.insert_one({"valor": valor, "hora": datetime.now()})
            except:
                pass

    def actualizar_gui(self, event):
        if self.luz_valor is not None:
            self.nivel_luz.SetLabel(f"Luz: {self.luz_valor}")
        if self.mov_valor is not None:
            self.nivel_mov.SetLabel(f"Movimiento: {self.mov_valor}")

if __name__ == "__main__":
    app = wx.App(False)
    ArduinoApp()
    app.MainLoop()
