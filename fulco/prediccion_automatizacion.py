import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.animation import FuncAnimation
from prophet import Prophet
from datetime import timedelta
import serial
import time
import re

# Conexión a MySQL con SQLAlchemy
usuario = "root"
clave = "root"
host = "localhost"
bd = "panta"
conexion_str = f"mysql+mysqlconnector://{usuario}:{clave}@{host}/{bd}"
engine = create_engine(conexion_str)

# Configura el puerto serial para Arduino (ajusta COM según tu sistema)
arduino = serial.Serial("COM7", 9600, timeout=2)
time.sleep(2)  # Esperar que se establezca conexión

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.5)

# Función para insertar datos en MySQL
def insertar_datos(temperatura, humedad, luz):
    try:
        with engine.connect() as conn:
            sql = """
                INSERT INTO sensor_completo (temperatura, humedad, valor_luz) 
                VALUES (%s, %s, %s)
            """
            conn.execute(sql, (temperatura, humedad, luz))
            conn.commit()
            print(f"✅ Datos guardados: Temp={temperatura}, Hum={humedad}, Luz={luz}")
    except Exception as e:
        print("Error al guardar en BD:", e)

# Leer datos seriales y guardar en BD
def leer_serial_y_guardar():
    if arduino.in_waiting > 0:
        try:
            linea = arduino.readline().decode('utf-8').strip()
            # Ejemplo esperado: "temp:28\nhum:65\nluz:450"
            # Leemos tres líneas consecutivas
            if linea.startswith("temp:"):
                temp = float(linea.split(":")[1])
                hum_line = arduino.readline().decode('utf-8').strip()
                luz_line = arduino.readline().decode('utf-8').strip()

                hum = float(hum_line.split(":")[1]) if hum_line.startswith("hum:") else None
                luz = float(luz_line.split(":")[1]) if luz_line.startswith("luz:") else None

                if temp is not None and hum is not None and luz is not None:
                    insertar_datos(temp, hum, luz)
        except Exception as e:
            print("Error leyendo serial:", e)

def preparar_datos(df, columna):
    df_pred = df[['fecha', columna]].rename(columns={'fecha': 'ds', columna: 'y'})
    return df_pred

def predecir(df_pred, periodo_dias=1):
    modelo = Prophet(daily_seasonality=True)
    modelo.fit(df_pred)
    futuro = modelo.make_future_dataframe(periods=int(periodo_dias * 24 * 6), freq='10min')
    forecast = modelo.predict(futuro)
    return forecast

def enviar_comando(comando):
    comando_bytes = f"{comando}\n".encode('utf-8')
    arduino.write(comando_bytes)
    print(f"📡 Enviado comando: {comando}")

def actualizar(frame):
    # Primero, leer y guardar datos nuevos
    leer_serial_y_guardar()

    consulta = "SELECT * FROM sensor_completo ORDER BY fecha DESC LIMIT 100"
    df = pd.read_sql(consulta, engine).sort_values(by="fecha")

    if len(df) < 10:
        print("⚠️ No hay suficientes datos para mostrar")
        return

    ahora = pd.Timestamp.now()
    futuro_30min = ahora + pd.Timedelta(minutes=30)

    # Temperatura
    df_temp = preparar_datos(df, 'temperatura')
    forecast_temp = predecir(df_temp, periodo_dias=0.5)

    ax1.clear()
    ax1.plot(df['fecha'], df['temperatura'], 'ro-', label="Temperatura real")
    ax1.plot(forecast_temp['ds'], forecast_temp['yhat'], 'r--', label="Predicción temperatura")
    ax1.set_title("Temperatura y Predicción")
    ax1.set_ylabel("°C")
    ax1.legend()
    ax1.grid(True)

    pred_temp_30min = forecast_temp.loc[(forecast_temp['ds'] - futuro_30min).abs().idxmin()]['yhat']

    # Humedad
    df_hum = preparar_datos(df, 'humedad')
    forecast_hum = predecir(df_hum, periodo_dias=0.5)

    ax2.clear()
    ax2.plot(df['fecha'], df['humedad'], 'bo-', label="Humedad real")
    ax2.plot(forecast_hum['ds'], forecast_hum['yhat'], 'b--', label="Predicción humedad")
    ax2.set_title("Humedad y Predicción")
    ax2.set_ylabel("%")
    ax2.legend()
    ax2.grid(True)

    pred_hum_30min = forecast_hum.loc[(forecast_hum['ds'] - futuro_30min).abs().idxmin()]['yhat']

    # Luz
    df_luz = preparar_datos(df, 'valor_luz')
    forecast_luz = predecir(df_luz, periodo_dias=0.5)

    ax3.clear()
    ax3.plot(df['fecha'], df['valor_luz'], 'mo-', label="Luz real")
    ax3.plot(forecast_luz['ds'], forecast_luz['yhat'], 'm--', label="Predicción luz")
    ax3.set_title("Luz y Predicción")
    ax3.set_ylabel("Intensidad")
    ax3.legend()
    ax3.grid(True)

    pred_luz_30min = forecast_luz.loc[(forecast_luz['ds'] - futuro_30min).abs().idxmin()]['yhat']

    # Automatización según predicciones

    # Temperatura (ventilador)
    if pred_temp_30min > 30:
        enviar_comando("$On")
    elif pred_temp_30min < 28:
        enviar_comando("$Off")

    # Humedad (bomba)
    if pred_hum_30min < 40:
        enviar_comando("$BombaOn")
    elif pred_hum_30min > 50:
        enviar_comando("$BombaOff")

    # Luz (lámpara)
    if pred_luz_30min < 300:
        enviar_comando("$LuzOn")
    elif pred_luz_30min > 500:
        enviar_comando("$LuzOff")

ani = FuncAnimation(fig, actualizar, interval=5000)  # Actualiza cada 5 segundos
plt.show()
