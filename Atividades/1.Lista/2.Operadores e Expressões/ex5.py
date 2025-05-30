


option = 0
while option != 5:
    print("Informe dois números: ")
    x = int(input("X:"))
    y = int(input("y:"))
    print("Calculadora")
    print("Escolha uma operação:")
    print("1.Soma \n" \
    "2.Subtração\n" \
    "3.Multiplicação\n" \
    "4.Divisão\n" \
    "5.SAIR")
    option = int(input("Opção: "))

    if option == 1:
        soma = x + y
        print(soma)

    if option == 2:
        soma = x - y
        print(soma)

    if option == 3:
        soma = x * y
        print(soma)
        
    if option == 4:
        soma = x / y
        print(soma)
