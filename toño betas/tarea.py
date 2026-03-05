import customtkinter as ctk
from pymongo import MongoClient
import serial
from datetime import datetime

# Configuración inicial
ctk.set_appearance_mode("dark")      # "light" o "dark"
ctk.set_default_color_theme("blue")  # "green", "dark-blue", etc.

# Conexión a Arduino
arduino = serial.Serial('COM7', 9600)

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["arduino"]
coleccion = db["comandos"]

# Funciones
def encender_led():
    arduino.write(b"$On\n")
    estado_label.configure(text="LED ENCENDIDO", text_color="white", fg_color="green")
    guardar_comando("ENCENDER")

def apagar_led():
    arduino.write(b"$Off\n")
    estado_label.configure(text="LED APAGADO", text_color="white", fg_color="red")
    guardar_comando("APAGAR")

def guardar_comando(accion):
    datos = {
        "accion": accion,
        "fecha": datetime.now()
    }
    coleccion.insert_one(datos)

# Crear ventana principal
ventana = ctk.CTk()
ventana.geometry("400x300")
ventana.title("Control LED Profesional")

# Elementos de interfaz
estado_label = ctk.CTkLabel(ventana, text="ESTADO DEL LED", font=ctk.CTkFont(size=18, weight="bold"), fg_color="gray", corner_radius=10, width=300, height=40)
estado_label.pack(pady=20)

boton_on = ctk.CTkButton(ventana, text="Encender LED", command=encender_led, width=200)
boton_on.pack(pady=10)

boton_off = ctk.CTkButton(ventana, text="Apagar LED", command=apagar_led, width=200)
boton_off.pack(pady=10)

# Iniciar interfaz
ventana.mainloop()
