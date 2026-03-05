import serial

import time
import mysql.connector
import re

def conexion_bluetooh(puerto="COM7", baudrate=9600):
    try:
        arduino = serial.Serial(puerto, baudrate, timeout=2)
        time.sleep(2)
        print("✅ Conexión exitosa a Bluetooth")
        return arduino
    except serial.SerialException:
        print("❌ No se pudo conectar a Bluetooth")
        return None

def leer_datos(dato_leer):
    try:
        if dato_leer and dato_leer.in_waiting > 0:
            dato = dato_leer.readline().decode().strip()
            print("📩 Dato recibido:", dato)

            if dato.startswith("luz:"):
                match = re.search(r'\d+', dato)
                if match:
                    numero = int(match.group())
                    print("💡 Luz:", numero)
                    return {"tipo": "luz", "valor": numero}
            
            elif dato.startswith("temp:"):
                match = re.search(r'\d+(\.\d+)?', dato)
                if match:
                    temperatura = int(match.group())
                    print("🌡️ Temperatura:", temperatura)
                    return {"tipo": "temperatura", "valor": temperatura}

            elif dato.startswith("hum:"):
                match = re.search(r'\d+(\.\d+)?', dato)
                if match:
                    humedad = int(match.group())
                    print("💧 Humedad:", humedad)
                    return {"tipo": "humedad", "valor": humedad}

            else:
                print("⚠️ Dato no reconocido")
                return None
    except Exception as e:
        print("❌ Error al leer datos:", e)
        return None

def conexion_base_mysql():
    try:
        conexion_base_datos = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="panta"
        )
        time.sleep(2)
        print("✅ Conexión exitosa a MySQL")
        return conexion_base_datos
    except mysql.connector.Error as e:
        print("❌ No se conectó a MySQL:", e)
        return None

# Conexiones
arduino = conexion_bluetooh()
conexion_mysql = conexion_base_mysql()

if arduino and conexion_mysql:
    cursor = conexion_mysql.cursor()
    while True:
        datos = leer_datos(arduino)
        if datos is not None:
            try:
                if datos["tipo"] == "luz":
                    consulta = "INSERT INTO sensor_luz (valor_luz) VALUES (%s)"
                    cursor.execute(consulta, (datos["valor"],))
                    print("💡 Valor de luz guardado:", datos["valor"])

                elif datos["tipo"] == "temperatura":
                    consulta = "INSERT INTO sensor_temperatura (valor_temp) VALUES (%s)"
                    cursor.execute(consulta, (datos["valor"],))
                    print("🌡️ Temperatura guardada:", datos["valor"])

                elif datos["tipo"] == "humedad":
                    consulta = "INSERT INTO sensor_humedad (valor_hum) VALUES (%s)"
                    cursor.execute(consulta, (datos["valor"],))
                    print("💧 Humedad guardada:", datos["valor"])

                conexion_mysql.commit()

            except mysql.connector.Error as e:
                print("❌ Error al guardar en MySQL:", e)

        time.sleep(1)
else:
    print("⛔ No se puede iniciar el programa: fallo en conexiones.")
