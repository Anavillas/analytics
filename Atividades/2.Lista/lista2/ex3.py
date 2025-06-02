preco = [356.5, 2213.4,1231.0, 412.231, 321.3,1216.5, 1313.4,4231.0, 462.231, 521.3]
desconto = []
for i in range(1,10):
    i = round(preco[i] * 0.1, 2)
    desconto.append(i)

print(desconto)