senha = "1a238"
tamanho = len(senha)
def validarSenha(senha):
    if tamanho >= 8:
        if any(char.isdigit() for char in senha):
            return "Senha forte"
        else:
            return "Insira ao menos um número"
    else:
        return("Quantidade de caracteres inválida")
print(validarSenha(senha))