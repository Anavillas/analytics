with open("arquivo.txt", "w") as arquivo:
    arquivo.write("          maçã         \n")
    arquivo.write("          kiwi         \n")
    arquivo.write("          banana         \n")

with open("arquivo.txt", "r") as arquivo:

    vetor = [linha.strip() for linha in arquivo]

print(vetor)