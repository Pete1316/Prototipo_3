def numero1 ():
    fo = []
    r = []

    for i in range (1, 4):
        a =(int(input(f"Valor de X1 ")))
        if a == 0:
            a = 1
        b =(int(input(f"Valor de X2 ")))
        if b == 0:
            b = 1
        fo.extend([a,b])
    
    for i in range (0,2):
        c =(int(input(f"Valor R{i+1} ")))
        r.extend([c])
    return fo, r
def pigote (fo,r):

    # Encontrar fila
    if fo[0] > fo[1]:
        r1 = r[0]/fo[2]
        r2 = r[1]/fo[4]
        if r1 < r2:
            return r1, fo[2]
        else:
            return r2, fo[4]
        
    else:
        r1 = r [0]/fo [3]
        r2 = r [1]/fo[5]
        if r2 < r1:
            return r2, fo[5]
        else:
            return r1, fo[3]


fo,r = numero1()

resultado, Elemento_pigote = pigote(fo,r) ##Valor del retur que son 2 

print (f"Z = {fo[0]} X1 + {fo[1]} X2")
print (f"     {fo[2]} X1 +  {fo [3]} X2 <= {r[0]}")
print (f"     {fo[4]} X1 +  {fo [5]} X2 <= {r[1]}")

print(resultado)
print(Elemento_pigote)
