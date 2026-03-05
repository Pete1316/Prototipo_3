import serial
import time
import mysql.connector
import re

def conexion_bluetooth():
    try:
        arduino = serial.Serial("COM7", 9600, timeout=2)
        time.sleep(2)
        print("✅ Conexión Bluetooth exitosa")
        return arduino
    except:
        print("❌ Error en conexión Bluetooth")
        return None

def conexion_mysql():
    try:
        con = mysql.connector.connect(
            host="localhost", user="root", password="root", database="panta"
        )
        print("✅ Conexión MySQL exitosa")
        return con
    except:
        print("❌ Error en conexión MySQL")
        return None

def leer_datos(serial_bt):
    if serial_bt.in_waiting > 0:
        linea = serial_bt.readline().decode().strip()
        print("📩 Recibido:", linea)
        match = re.match(r'(temp|hum|luz):([\d\.]+)', linea)
        if match:
            return match.group(1), float(match.group(2))
    return None, None

# Inicialización
arduino = conexion_bluetooth()
db = conexion_mysql()
cursor = db.cursor()

ultimo_temp = None
ultima_hum = None
ultimo_luz = None

while arduino and db:
    tipo, valor = leer_datos(arduino)
    if tipo == "temp":
        ultimo_temp = valor
    elif tipo == "hum":
        ultima_hum = valor
    elif tipo == "luz":
        ultimo_luz = valor

    if ultimo_temp and ultima_hum and ultimo_luz:
        try:
            cursor.execute(
                "INSERT INTO sensor_completo (temperatura, humedad, valor_luz) VALUES (%s, %s, %s)",
                (ultimo_temp, ultima_hum, ultimo_luz),
            )
            db.commit()
            print(f"✅ Guardado: T={ultimo_temp} H={ultima_hum} L={ultimo_luz}")
            ultimo_temp = ultima_hum = ultimo_luz = None
        except Exception as e:
            print("❌ Error al guardar:", e)

    time.sleep(1)
