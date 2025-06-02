lista = [1,2,3.1,'4','5',6.2,7.7,'8','9',False]
lista.append(True)
novos = [100, 200, 300]
lista.extend(novos)

lista.insert(2,'meio')

lista.remove(100)

popinho = lista.pop(3)
print(lista)
print(popinho)