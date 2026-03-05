import pandas as pd
import os
import joblib
from prophet import Prophet
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:root@localhost/panta")


base_path = r"D:\visualcode\Peter\datos_guardados"

def actualizar_modelo(variable, nombre_archivo_csv, nombre_modelo_pkl):
    print(f"\n🔄 Procesando {variable}...")


    ruta_csv = os.path.join(base_path, nombre_archivo_csv)
    ruta_modelo = os.path.join(base_path, nombre_modelo_pkl)


    os.makedirs(base_path, exist_ok=True)

    if os.path.exists(ruta_csv):
        df_antiguos = pd.read_csv(ruta_csv)
    else:
        df_antiguos = pd.DataFrame(columns=["ds", "y"])

    df_nuevos = pd.read_sql(f"SELECT fecha, {variable} FROM sensor_completo ORDER BY fecha ASC", engine)
    df_nuevos = df_nuevos.rename(columns={"fecha": "ds", variable: "y"})

    df_total = pd.concat([df_antiguos, df_nuevos])
    df_total['ds'] = pd.to_datetime(df_total['ds']) 
    df_total = df_total.drop_duplicates().sort_values("ds")

    df_total = df_total.dropna(subset=["y"])

    if len(df_total) < 100:
        print("⚠️ Muy pocos datos para entrenar")
        return

    modelo = Prophet(daily_seasonality=True)
    modelo.fit(df_total)

    joblib.dump(modelo, ruta_modelo)
    df_total.to_csv(ruta_csv, index=False)
    print(f"✅ Modelo '{ruta_modelo}' entrenado y guardado con {len(df_total)} filas.")


actualizar_modelo("temperatura", "datos_temp.csv", "modelo_temp.pkl")
actualizar_modelo("humedad", "datos_humedad.csv", "modelo_humedad.pkl")
actualizar_modelo("valor_luz", "datos_luz.csv", "modelo_luz.pkl")
