import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.animation import FuncAnimation

# 🔗 Conexión a la base de datos MySQL
usuario = "root"
clave = "root"
host = "localhost"
bd = "panta"
conexion_str = f"mysql+mysqlconnector://{usuario}:{clave}@{host}/{bd}"
engine = create_engine(conexion_str)


tiempos = []
temperaturas = []
humedades = []
luces = []

# 📊 Crear las figuras y subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))
plt.subplots_adjust(hspace=0.5)

# ⚙️ Función para actualizar los gráficos
def actualizar(frame):
    consulta = "SELECT * FROM sensor_completo ORDER BY id DESC LIMIT 20"
    df = pd.read_sql(consulta, engine).sort_values(by="id")

    tiempos.clear()
    temperaturas.clear()
    humedades.clear()
    luces.clear()

    for _, fila in df.iterrows():
        tiempos.append(fila["fecha"].strftime("%H:%M:%S"))
        temperaturas.append(fila["temperatura"])
        humedades.append(fila["humedad"])
        luces.append(fila["valor_luz"])

    # 📈 Gráfico de Temperatura
    ax1.clear()
    ax1.plot(tiempos, temperaturas, color='red', marker='o')
    ax1.set_title("Temperatura en Tiempo Real")
    ax1.set_ylabel("°C")
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True)

    # 💧 Gráfico de Humedad
    ax2.clear()
    ax2.plot(tiempos, humedades, color='blue', marker='o')
    ax2.set_title("Humedad en Tiempo Real")
    ax2.set_ylabel("%")
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True)

    # 💡 Gráfico de Luz
    ax3.clear()
    ax3.plot(tiempos, luces, color='orange', marker='o')
    ax3.set_title("Nivel de Luz en Tiempo Real")
    ax3.set_ylabel("Intensidad")
    ax3.set_xlabel("Hora")
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True)

# 🔁 Animación en tiempo real
ani = FuncAnimation(fig, actualizar, interval=2000)  # cada 2 segundos
plt.show()
