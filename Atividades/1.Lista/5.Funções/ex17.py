n1 = float(input("Informe o primeiro número: "))
n2 = float(input("Informe o segundo número: "))
x = 0
def maior(n1,n2):
    if n1 >n2:
        return n1
    if n2 > n1:
        return n2
    else:
        return "Iguais"
    
print(maior(n1,n2))