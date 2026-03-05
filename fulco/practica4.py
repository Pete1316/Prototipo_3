import serial
import time
import mysql.connector
import re

def conexion_bluetooth(puerto="COM7", baudrate=9600):
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
                    return {"tipo": "temp", "valor": temperatura}

            elif dato.startswith("hum:"):
                match = re.search(r'\d+(\.\d+)?', dato)
                if match:
                    humedad = int(match.group())
                    print("💧 Humedad:", humedad)
                    return {"tipo": "hum", "valor": humedad}

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

# Variables para guardar valores temporales
ultimo_temp = None
ultima_hum = None
ultimo_luz = None

# Conexiones
arduino = conexion_bluetooth()
conexion_mysql = conexion_base_mysql()

if arduino and conexion_mysql:
    cursor = conexion_mysql.cursor()
    while True:
        datos = leer_datos(arduino)
        if datos is not None:
            # Guardar valores recibidos
            if datos["tipo"] == "temp" and datos["valor"] != -1:
                ultimo_temp = datos["valor"]
            elif datos["tipo"] == "hum" and datos["valor"] != -1:
                ultima_hum = datos["valor"]
            elif datos["tipo"] == "luz":
                ultimo_luz = datos["valor"]

            # Insertar sólo si se tienen los tres valores
            if (ultimo_temp is not None) and (ultima_hum is not None) and (ultimo_luz is not None):
                try:
                    consulta = """
                        INSERT INTO sensor_completo (temperatura, humedad, valor_luz)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(consulta, (ultimo_temp, ultima_hum, ultimo_luz))
                    conexion_mysql.commit()
                    print(f"📥 Datos guardados: temp={ultimo_temp}, hum={ultima_hum}, luz={ultimo_luz}")

                    # Resetear para recibir la siguiente tanda de datos
                    ultimo_temp = None
                    ultima_hum = None
                    ultimo_luz = None

                except mysql.connector.Error as e:
                    print("❌ Error al guardar en MySQL:", e)

        time.sleep(1)
else:
    print("⛔ No se puede iniciar el programa: fallo en conexiones.")
