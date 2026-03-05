import serial
from pymongo import MongoClient
from datetime import datetime
import time

def conectar_arduino(puerto='COM7', baudrate=9600):
    try:
        arduino = serial.Serial(puerto, baudrate, timeout=1)
        print("✅ Conectado a Arduino en", puerto)
        time.sleep(2)
        return arduino
    except Exception as e:
        print("❌ No se pudo conectar con Arduino:", e)
        return None

def enviar_comando(arduino, comando):
    if arduino and arduino.is_open:
        arduino.write(comando.encode())
        arduino.flush()
        print(f"📤 Comando enviado a Arduino: {comando.strip()}")
    else:
        print("❌ Arduino no está conectado.")

def main():
    cliente = MongoClient("mongodb://localhost:27017")
    db = cliente["arduino"]
    coleccion = db["sensores"]

    arduino = conectar_arduino('COM7')

    while True:
        if arduino and arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').strip()
            print(f"📥 Datos recibidos: {linea}")

            try:
                partes = linea.split(',')
                datos = {}

                # Validar formato y valores numéricos
                valido = True
                for parte in partes:
                    if ':' not in parte:
                        valido = False
                        break
                    clave, valor = parte.split(':', 1)
                    valor = valor.strip()
                    try:
                        if '.' in valor:
                            _ = float(valor)
                        else:
                            _ = int(valor)
                    except:
                        valido = False
                        break

                if valido:
                    for parte in partes:
                        clave, valor = parte.split(':', 1)
                        valor = valor.strip()
                        if '.' in valor:
                            datos[clave] = float(valor)
                        else:
                            datos[clave] = int(valor)

                    datos["fecha"] = datetime.now()
                    coleccion.insert_one(datos)
                    print(f"💾 Datos guardados: {datos}")

                    # Obtener últimos 10 registros de luz para analizar promedio
                    ultimos = list(coleccion.find().sort("fecha", -1).limit(1000))
                    valores_luz = [doc.get("luz", 9999) for doc in ultimos if "luz" in doc]
                    if valores_luz:
                        promedio_luz = sum(valores_luz) / len(valores_luz)
                        print(f"📊 Promedio últimos 10 valores luz: {promedio_luz:.2f}")

                        # Decisión basada en promedio
                        if promedio_luz < 200:
                            enviar_comando(arduino, "$On\n")
                            print("💡 LED ENCENDIDO por baja luz promedio")
                        else:
                            enviar_comando(arduino, "$Off\n")
                            print("🌙 LED APAGADO por luz promedio suficiente")
                    else:
                        print("⚠️ No hay datos suficientes de luz para hacer promedio")
                else:
                    print("⚠️ Línea ignorada, formato no válido o valor no numérico")

            except Exception as e:
                print(f"⚠️ Error procesando datos: {e}")

        time.sleep(1)

if __name__ == "__main__":
    main()
