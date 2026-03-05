import serial
import mysql.connector
from datetime import datetime
import time

# Conexión a MySQL
def conexion_mysql():
    try:
        conexion_base_datos = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="planta_1"
        )
        print("✅ MYSQL CONECTADA")
        return conexion_base_datos
    except mysql.connector.Error as err:
        print(f"❌ ERROR CON MYSQL: {err}")
        return None

# Conexión al módulo Bluetooth (Arduino)
def conexion_arduino(puerto="COM7", baudrate=9600): 
    try:
        arduino = serial.Serial(puerto, baudrate, timeout=2)
        print("✅ Bluetooth conectado")
        time.sleep(2)  # Esperar que Arduino se reinicie y comience a enviar datos
        return arduino
    except serial.SerialException as err:
        print(f"❌ ERROR CON BLUETOOTH: {err}")
        return None

# Función principal que escucha datos y guarda en la base
def bluetooth_conectado(): 
    arduino = conexion_arduino()
    base_datos = conexion_mysql()
    
    if arduino is None or base_datos is None:
        print("❌ No se pudo establecer conexión con Arduino o MySQL.")
        return

    cursor = base_datos.cursor()

    try:
        while True:
            if arduino.in_waiting:
                valor = arduino.readline().decode('utf-8').strip()
                print(f"📥 Dato recibido: {valor}")

                if valor.startswith("luz:"):
                    valor_numero = valor.split(":")[1]
                    try:
                        nivel = int(valor_numero)
                    except ValueError:
                        print(f"⚠️ Valor no válido para nivel de luz: {valor_numero}")
                        continue

                    try:
                        cursor.execute(
                            "INSERT INTO nivel_luz (id_nivel_luz) VALUES (%s)", (valor)
                        )db.commit()
                        print("✅ Dato guardado en la base de datos")
                    except Exception as err:
                        print(f"❌ Error al insertar en la base: {err}")
                else:
                    print("⚠️ Dato recibido no válido:",valor)
            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n⛔ Programa detenido por el usuario")

    finally:
        if arduino and arduino.is_open:
            arduino.close()
            print("🔌 Bluetooth cerrado")
        if base_datos:
            base_datos.close()
            print("🗃️ MySQL desconectado")

if __name__ == "__main__":
    bluetooth_conectado()
