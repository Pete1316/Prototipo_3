import numpy as np

def imprimir_tabla(tableau, iteracion):
    print(f"\n📊 Iteración {iteracion}")
    filas, cols = tableau.shape
    for i in range(filas):
        fila = ["{:<8.3f}".format(x) for x in tableau[i]]
        print(" | ".join(fila))


def simplex(c, A, b):
    """
    Método Simplex para maximización con impresión de tablas.
    c : coeficientes de la función objetivo (lista)
    A : matriz de restricciones (listas de listas)
    b : lado derecho de las restricciones (lista)
    """
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Número de restricciones y variables
    m, n = A.shape  

    # Agregar variables de holgura
    A = np.hstack([A, np.eye(m)])
    c = np.hstack([c, np.zeros(m)])

    # Crear la tabla inicial
    tableau = np.zeros((m+1, n+m+1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = -c

    # Imprimir tabla inicial
    imprimir_tabla(tableau, 0)

    iteracion = 1
    # Iteraciones del método
    while np.any(tableau[-1, :-1] < 0):
        # Columna pivote (la más negativa en la fila objetivo)
        col = np.argmin(tableau[-1, :-1])
        if np.all(tableau[:-1, col] <= 0):
            raise Exception("⚠️ Problema no acotado.")

        # Fila pivote (mínima razón b_i/a_ij)
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, col], 
                           out=np.full_like(tableau[:-1, -1], np.inf), 
                           where=tableau[:-1, col] > 0)
        row = np.argmin(ratios)

        # Normalizar fila pivote
        tableau[row, :] /= tableau[row, col]

        # Eliminar columna pivote en las demás filas
        for i in range(m+1):
            if i != row:
                tableau[i, :] -= tableau[i, col] * tableau[row, :]

        # Imprimir tabla de la iteración
        imprimir_tabla(tableau, iteracion)
        iteracion += 1

    # Solución
    solution = np.zeros(n+m)
    for i in range(m):
        pivot_col = np.where(tableau[i, :-1] == 1)[0]
        if len(pivot_col) == 1:
            solution[pivot_col[0]] = tableau[i, -1]

    z = tableau[-1, -1]
    return solution[:n], z


# ---------------- PRUEBA ----------------
# Max Z = 3x1 + 2x2
# Restricciones:
# 2x1 + x2 <= 18
# 2x1 + 3x2 <= 42
# 3x1 + 1x2 <= 24
# x1, x2 >= 0

c = [3, 2]
A = [[2, 1],
     [2, 3],
     [3, 1]]
b = [18, 42, 24]

sol, z = simplex(c, A, b)

print("\n✅ Solución óptima:")
print("x =", sol)
print("Z =", z)
