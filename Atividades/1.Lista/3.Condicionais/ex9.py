senha = input("Informe sua senha: ")

confirmarSenha = ""
while confirmarSenha != senha:
    confirmarSenha = input("Confirmar senha:")
    if confirmarSenha != senha:
        print("Senhas diferentes! Informe novamente.")
    
print("\nAcesso liberado")