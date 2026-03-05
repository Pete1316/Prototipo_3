import wx
import serial
from pymongo import MongoClient
from datetime import datetime
import threading

class ArduinoApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Control LED, Luz y Movimiento", size=(320, 270))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.estado_label = wx.StaticText(panel, label="Estado del LED: Desconocido")
        self.estado_label.SetBackgroundColour("gray")
        self.estado_label.SetForegroundColour("white")
        self.estado_label.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(self.estado_label, flag=wx.EXPAND | wx.ALL, border=10)

        self.luz_label = wx.StaticText(panel, label="Nivel de luz: N/D")
        self.luz_label.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        vbox.Add(self.luz_label, flag=wx.EXPAND | wx.ALL, border=10)

        self.mov_label = wx.StaticText(panel, label="Nivel de movimiento: N/D")
        self.mov_label.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        vbox.Add(self.mov_label, flag=wx.EXPAND | wx.ALL, border=10)

        btn_on = wx.Button(panel, label="Encender LED")
        btn_off = wx.Button(panel, label="Apagar LED")
        btn_on.Bind(wx.EVT_BUTTON, self.encender_led)
        btn_off.Bind(wx.EVT_BUTTON, self.apagar_led)

        vbox.Add(btn_on, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(btn_off, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

        # Conexión a Arduino
        try:
            self.arduino = serial.Serial('COM7', 9600, timeout=1)  

            print("Conectado a Arduino.")
        except serial.SerialException:
            self.arduino = None
            wx.MessageBox("No se pudo conectar con Arduino en COM7", "Error", wx.OK | wx.ICON_ERROR)

        try:
            self.cliente = MongoClient("mongodb://localhost:27017")
            self.coleccion_comandos = self.cliente["arduino"]["comandos"]
            self.coleccion_luz = self.cliente["arduino"]["niveles_luz"]
            self.coleccion_movimiento = self.cliente["arduino"]["movimiento"]
            print("Conectado a MongoDB.")
        except Exception as e:
            print(" Error conectando a MongoDB:", e)

        self.valor_luz = None
        self.valor_mov = None

        # Hilo para lectura del puerto serial
        if self.arduino:
            self.hilo_lectura = threading.Thread(target=self.leer_serial, daemon=True)
            self.hilo_lectura.start()

        # Temporizador GUI
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.actualizar_gui, self.timer)
        self.timer.Start(1000)

    def guardar(self, coleccion, datos):
        try:
            coleccion.insert_one(datos)
            print(f"Guardado en MongoDB: {datos}")
        except Exception as e:
            print("Error guardando en MongoDB:", e)

    def enviar_comando(self, comando):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(comando.encode())
            self.arduino.flush()
            print(f" Enviado a Arduino: {comando.strip()}")
        else:
            wx.MessageBox("No conectado al Arduino", "Error", wx.OK | wx.ICON_ERROR)

    def encender_led(self, event):
        self.enviar_comando("$On\n")
        self.estado_label.SetLabel("Estado del LED: ENCENDIDO")
        self.estado_label.SetBackgroundColour("green")
        self.estado_label.Refresh()
        self.guardar(self.coleccion_comandos, {"accion": "ENCENDER", "fecha": datetime.now()})

    def apagar_led(self, event):
        self.enviar_comando("$Off\n")
        self.estado_label.SetLabel("Estado del LED: APAGADO")
        self.estado_label.SetBackgroundColour("red")
        self.estado_label.Refresh()
        self.guardar(self.coleccion_comandos, {"accion": "APAGAR", "fecha": datetime.now()})

    def leer_serial(self):
        while True:
            try:
                linea = self.arduino.readline().decode('utf-8').strip()
                if linea:
                    print(f"Recibido de Arduino: {linea}")

                if linea.startswith("luz:"):
                    valor = linea.split(":")[1]
                    try:
                        nivel = int(valor)
                        self.valor_luz = nivel
                        self.guardar(self.coleccion_luz, {
                            "nivel_luz": nivel,
                            "fecha": datetime.now()
                        })
                    except ValueError:
                        print("❗ Valor de luz no válido:", valor)

                elif linea.startswith("movimiento:"):
                    valor = linea.split(":")[1]
                    try:
                        nivel = int(valor)
                        self.valor_mov = nivel
                        self.guardar(self.coleccion_movimiento, {
                            "nivel_movimiento": nivel,
                            "fecha": datetime.now()
                        })
                    except ValueError:
                        print(" Valor de movimiento no válido:", valor)


            except Exception as e:
                print(" Error leyendo serial:", e)

    def actualizar_gui(self, event):
        if self.valor_luz is not None:
            self.luz_label.SetLabel(f"Nivel de luz: {self.valor_luz}")
        if self.valor_mov is not None:
            self.mov_label.SetLabel(f"Nivel de movimiento: {self.valor_mov}")

    def OnClose(self, event):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    ventana = ArduinoApp()
    app.MainLoop()
