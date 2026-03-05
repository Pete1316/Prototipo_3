texto = input("Ingresa una cadena de texto: ")
mayusculas = sum(1 for c in texto if c.isupper())

minusculas = sum(1 for c in texto if c.islower())

print(f"Letras mayúsculas: {mayusculas}")
print(f"Letras minúsculas: {minusculas}")
