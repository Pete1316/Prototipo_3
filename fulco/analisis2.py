import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.animation import FuncAnimation
from prophet import Prophet
from datetime import timedelta


usuario = "root"
clave = "root"
host = "localhost"
bd = "panta"
conexion_str = f"mysql+mysqlconnector://{usuario}:{clave}@{host}/{bd}"
engine = create_engine(conexion_str)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.5)

def preparar_datos(df, columna):
    df_pred = df[['fecha', columna]].rename(columns={'fecha': 'ds', columna: 'y'})
    return df_pred

def predecir(df_pred, periodo_dias=1):
    modelo = Prophet(daily_seasonality=True)
    modelo.fit(df_pred)
    futuro = modelo.make_future_dataframe(periods=int(periodo_dias * 24 * 6), freq='10min')
    forecast = modelo.predict(futuro)
    return forecast

def actualizar(frame):
    consulta = "SELECT * FROM sensor_completo ORDER BY fecha DESC LIMIT 100"
    df = pd.read_sql(consulta, engine).sort_values(by="fecha")

    if len(df) < 10:
        print("⚠️ No hay suficientes datos para mostrar")
        return


    df_temp = preparar_datos(df, 'temperatura')
    forecast_temp = predecir(df_temp, periodo_dias=0.5)

    ax1.clear()
    ax1.plot(df['fecha'], df['temperatura'], 'ro-', label="Temperatura real")
    ax1.plot(forecast_temp['ds'], forecast_temp['yhat'], 'r--', label="Predicción temperatura")
    ax1.set_title("Temperatura y Predicción")
    ax1.set_ylabel("°C")
    ax1.legend()
    ax1.grid(True)

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

ani = FuncAnimation(fig, actualizar, interval=5000)
plt.show()
