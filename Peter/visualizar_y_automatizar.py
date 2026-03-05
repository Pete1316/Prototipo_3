import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import joblib
from sqlalchemy import create_engine
import serial
import time
import signal
import sys
import atexit
from tabulate import tabulate
import os
import random

base_path = r"D:\visualcode\Peter\datos_guardados"

def cargar_modelo(nombre_modelo):
    ruta = os.path.join(base_path, nombre_modelo)
    if not os.path.exists(ruta):
        print(f"❌ Modelo no encontrado: {ruta}")
        sys.exit(1)
    return joblib.load(ruta)

modelo_temp = cargar_modelo("modelo_temp.pkl")
modelo_hum = cargar_modelo("modelo_humedad.pkl")
modelo_luz = cargar_modelo("modelo_luz.pkl")

engine = create_engine("mysql+mysqlconnector://root:root@localhost/panta")


try:
    bt = serial.Serial("COM7", 9600, timeout=1)
    time.sleep(2)
    modo_simulado = False
    print("✅ Puerto serial abierto: modo normal")
except Exception as e:
    print(f"⚠️ No se pudo abrir puerto serial: {e}")
    print("🔄 Usando modo simulado (sin Arduino)")
    modo_simulado = True

datos_acumulados = []
contador_guardado = 0  

def enviar_comando(comando):
    if modo_simulado:
        print(f"📡 (Simulado) Comando enviado: {comando}")
        return
    print(f"📡 Enviando comando: {comando}")
    try:
        bt.write((comando + "\n").encode())
    except Exception as e:
        print(f"⚠️ Error enviando comando: {e}")

def automatizar(nombre, prediccion, umbral, comando_on, comando_off, acciones):
    valor_predicho = prediccion['yhat'].iloc[-1]
    if valor_predicho > umbral:
        acciones.append([nombre.upper(), f"{valor_predicho:.2f}", "ALTA", comando_on])
        enviar_comando(comando_on)
    else:
        acciones.append([nombre.upper(), f"{valor_predicho:.2f}", "NORMAL", comando_off])
        enviar_comando(comando_off)

def guardar_datos_mysql(df):
    try:
        with engine.begin() as conexion:
            df.to_sql('sensor_completo', conexion, if_exists='append', index=False)
        print("✅ Datos guardados en MySQL")
    except Exception as e:
        print(f"❌ Error al guardar datos en MySQL: {e}")

def apagar_todo():
    print("\n🔌 Cerrando programa... apagando todos los dispositivos.")
    try:
        enviar_comando("FAN_OFF")
        enviar_comando("DESHUM_OFF")
        enviar_comando("LED_OFF")
        if not modo_simulado and bt.is_open:
            bt.close()
    except Exception as e:
        print(f"⚠️ Error al apagar: {e}")

atexit.register(apagar_todo)

def cerrar_programa(signal_received, frame):
    apagar_todo()
    sys.exit(0)

signal.signal(signal.SIGINT, cerrar_programa)
signal.signal(signal.SIGTERM, cerrar_programa)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.5)

def actualizar(frame):
    global datos_acumulados, contador_guardado
    acciones = []

    temp = None
    hum = None
    luz = None

    if not modo_simulado:

        lineas_leidas = 0
        while bt.in_waiting and lineas_leidas < 10:
            try:
                linea = bt.readline().decode().strip()
            except Exception as e:
                print(f"⚠️ Error leyendo serial: {e}")
                break

            if linea.startswith("Temp:"):
                try:
                    temp = float(linea.split(":")[1])
                except:
                    temp = None
            elif linea.startswith("Hum:"):
                try:
                    hum = float(linea.split(":")[1])
                except:
                    hum = None
            elif linea.startswith("luz:"):
                try:
                    luz = float(linea.split(":")[1])
                except:
                    luz = None

            if temp is not None and hum is not None and luz is not None:
                fecha_actual = pd.Timestamp.now()
                datos_acumulados.append({
                    'fecha': fecha_actual,
                    'temperatura': temp,
                    'humedad': hum,
                    'valor_luz': luz
                })
            lineas_leidas += 1

    else:

        fecha_actual = pd.Timestamp.now()
        temp = 25 + random.uniform(-2, 2)      
        hum = 60 + random.uniform(-10, 10)    
        luz = 800 + random.uniform(-200, 200)  
        datos_acumulados.append({
            'fecha': fecha_actual,
            'temperatura': temp,
            'humedad': hum,
            'valor_luz': luz
        })

    if len(datos_acumulados) > 0:
        contador_guardado += 1
        if contador_guardado >= 5:
            df_nuevo = pd.DataFrame(datos_acumulados)
            guardar_datos_mysql(df_nuevo)
            datos_acumulados = []
            contador_guardado = 0

    try:
        df = pd.read_sql("SELECT * FROM sensor_completo ORDER BY fecha DESC LIMIT 100", engine)
        df = df.sort_values(by="fecha")
    except Exception as e:
        print(f"⚠️ Error leyendo base de datos: {e}")
        return

    if len(df) < 10:
        print("⚠️ No hay suficientes datos para predecir.")
        return


    df_temp = df[['fecha', 'temperatura']].rename(columns={'fecha': 'ds', 'temperatura': 'y'})
    futuro_temp = modelo_temp.make_future_dataframe(periods=6, freq='10min')
    forecast_temp = modelo_temp.predict(futuro_temp)

    ax1.clear()
    ax1.plot(df_temp['ds'], df_temp['y'], 'ro-', label="Real")
    ax1.plot(forecast_temp['ds'], forecast_temp['yhat'], 'r--', label="Predicción")
    ax1.set_title("Temperatura")
    ax1.legend()
    ax1.grid(True)

    automatizar("temperatura", forecast_temp, 30, "FAN_ON", "FAN_OFF", acciones)


    df_hum = df[['fecha', 'humedad']].rename(columns={'fecha': 'ds', 'humedad': 'y'})
    futuro_hum = modelo_hum.make_future_dataframe(periods=6, freq='10min')
    forecast_hum = modelo_hum.predict(futuro_hum)

    ax2.clear()
    ax2.plot(df_hum['ds'], df_hum['y'], 'bo-', label="Real")
    ax2.plot(forecast_hum['ds'], forecast_hum['yhat'], 'b--', label="Predicción")
    ax2.set_title("Humedad")
    ax2.legend()
    ax2.grid(True)

    automatizar("humedad", forecast_hum, 70, "DESHUM_ON", "DESHUM_OFF", acciones)


    df_luz = df[['fecha', 'valor_luz']].rename(columns={'fecha': 'ds', 'valor_luz': 'y'})
    futuro_luz = modelo_luz.make_future_dataframe(periods=6, freq='10min')
    forecast_luz = modelo_luz.predict(futuro_luz)

    ax3.clear()
    ax3.plot(df_luz['ds'], df_luz['y'], 'mo-', label="Real")
    ax3.plot(forecast_luz['ds'], forecast_luz['yhat'], 'm--', label="Predicción")
    ax3.set_title("Luz")
    ax3.legend()
    ax3.grid(True)

    automatizar("luz", forecast_luz, 900, "LED_ON", "LED_OFF", acciones)

    print("\n📊 ACCIONES EN ESTE CICLO:")
    print(tabulate(acciones, headers=["SENSOR", "PREDICCIÓN", "ESTADO", "ACCIÓN"], tablefmt="fancy_grid"))

ani = FuncAnimation(fig, actualizar, interval=60000)
plt.show()
