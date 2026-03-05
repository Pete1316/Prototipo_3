from scipy.optimize import linprog

# Coeficientes de la función objetivo (minimizar)
c = [-20, -15]

# Restricciones
A = [[3, 2],
     [1, 2]]

b = [18, 10]

# Límites inferiores
x0_bounds = (0, None)
x1_bounds = (0, None)

result = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds])

if result.success:
    x_opt = result.x
    Z_max = -result.fun  # Como minimizamos el negativo, invertimos signo para ganancia
    print(f"Mesas a producir: {x_opt[0]:.0f}")
    print(f"Sillas a producir: {x_opt[1]:.0f}")
    print(f"Ganancia máxima: ${Z_max:.2f}")
else:
    print("No se encontró solución óptima.")
