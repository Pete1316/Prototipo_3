import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# 🔗 Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="panta"
)

# 📥 Cargar los datos desde la tabla sensor_luz
consulta = "SELECT id, valor_luz FROM sensor_luz ORDER BY id"
df = pd.read_sql(consulta, conexion)

# 📈 Entrenamiento del modelo de regresión lineal con todos los datos
X = df[['id']]
y = df['valor_luz']

modelo = LinearRegression()
modelo.fit(X, y)

# 🔮 Predecir los próximos 50 valores
ult_id = df['id'].max()
n_predicciones = 3000
futuros_ids = pd.DataFrame({'id': list(range(ult_id + 1, ult_id + n_predicciones + 1))})
predicciones = modelo.predict(futuros_ids)

# 🖨️ Mostrar predicciones
for i, val in enumerate(predicciones):
    print(f"Predicción para ID {futuros_ids['id'][i]}: {val:.2f}")

# 📊 Visualización combinada de datos reales y predicción
plt.scatter(X, y, label="Datos reales")
plt.plot(futuros_ids, predicciones, color='red', label="Predicción futura")
plt.xlabel("ID (Tiempo)")
plt.ylabel("Valor de luz")
plt.title("Predicción futura de valor_luz con regresión lineal")
plt.legend()
plt.grid(True)
plt.show()

# 🔚 Cerrar conexión
conexion.close()
