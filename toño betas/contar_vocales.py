def contar_vocales(frase):
    vocales = "aeiouAEIOU"
    conteo = {v: frase.count(v) for v in vocales if v in frase}
    print("Cantidad de cada vocal:", conteo)

while True:
    frase = input("Ingresa una frase: ")
    contar_vocales(frase)
    
    continuar = input("¿Quieres continuar? (sí/no): ").strip().lower()
    if continuar not in ["si", "sí", "s", "yes", "y","Nz"]:
        print("Programa finalizado.")
        break
