import streamlit as st
import hashlib
import sqlite3
import pandas as pd

conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

# Criação das tabelas
cursor.executescript("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER,
    sexo TEXT,
    email TEXT,
    telefone TEXT,
    plano_id INTEGER,
    instrutor_id INTEGER,
    treino_id INTEGER,
    FOREIGN KEY (plano_id) REFERENCES planos(id),
    FOREIGN KEY (instrutor_id) REFERENCES instrutores(id),
    FOREIGN KEY (treino_id) REFERENCES treinos(id)
);

CREATE TABLE IF NOT EXISTS instrutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    especialidade TEXT
);

CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    preco_mensal REAL,
    duracao_meses INTEGER
);

CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    grupo_muscular TEXT
);

CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    instrutor_id INTEGER,
    plano_id INTEGER,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (instrutor_id) REFERENCES instrutores(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);

CREATE TABLE IF NOT EXISTS treino_exercicio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id INTEGER,
    treino TEXT,
    exercicio_id INTEGER,
    exercicio TEXT,
    series INTEGER,
    repeticoes INTEGER,
    FOREIGN KEY (treino_id) REFERENCES treinos(id),
    FOREIGN KEY (exercicio_id) REFERENCES exercicios(id)
);

CREATE TABLE IF NOT EXISTS pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    plano_id INTEGER,
    valor_pago REAL,
    data_pagamento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);
""")
conn.commit()

clientes = pd.read_csv("Atividades/9.Lista/clientes_academia.csv")
instrutores = pd.read_csv("Atividades/9.Lista/instrutores.csv")
planos = pd.read_csv("Atividades/9.Lista/planos.csv")
exercicios = pd.read_csv("Atividades/9.Lista/exercicios.csv")
pagamentos = pd.read_csv("Atividades/9.Lista/pagamento_clientes.csv")
treino_exercicio = pd.read_csv("Atividades/9.Lista/ptreino_exercicios.csv")

clientes.to_sql("clientes", conn, if_exists="append", index=False)
instrutores.to_sql("instrutores", conn, if_exists="append", index=False)
planos.to_sql("planos", conn, if_exists="append", index=False)
exercicios.to_sql("exercicios", conn, if_exists="append", index=False)
pagamentos.to_sql("pagamentos", conn, if_exists="append", index=False)
treino_exercicio.to_sql("treino_exercicio", conn, if_exists="append", index=False)

# Criação da tabela e cadastro inicial
def criar_tabela():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Usuário já existe.")
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_login(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result


def main():
    st.title("Gym Login")
    username = st.text_input("Usuário:")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if verificar_login(username, password):
            st.session_state['logado'] = True
            st.session_state['usuario'] = username
            st.success(f"Bem-vindo, {username}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos!")

def buscar_usuarios_dict():
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM clientes")
    resultado = cursor.fetchall()
    conn.close()
    return {nome: id for id, nome in resultado}

def buscar_instrutor_dict():
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM instrutores")
    resultado = cursor.fetchall()
    conn.close()
    return {nome: id for id, nome in resultado}


def buscar_exercicio_dict():
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM exercicios")
    resultado = cursor.fetchall()
    conn.close()
    return {nome: id for id, nome in resultado}


def tela_principal():
    st.sidebar.subheader(f"Bem-vindo, {st.session_state['usuario']}!")
    opcao = st.sidebar.selectbox("Escolha uma opção:", ['Cadastro'])

    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.session_state['usuario'] = ""
        st.experimental_rerun()
    st.subheader("Auxiliares de Busca:")
    
    usuarios_dict = buscar_usuarios_dict()
    nomes_disponiveis = list(usuarios_dict.keys())

    nome_digitado = st.text_input("Pesquisar ID por nome de usuário:", key="buscar_usuario")

    sugestoes = [nome for nome in nomes_disponiveis if nome_digitado.lower() in nome.lower()]

    if nome_digitado:
            if nome_digitado in usuarios_dict:
                st.success(f"ID do usuário: {usuarios_dict[nome_digitado]}")
            elif sugestoes:
                st.info("Possível usuário que está sendo buscado")
                for sugestao in sugestoes:
                    st.write(f"Usuário: {sugestao}")
            else:
                st.warning("Usuário não encontrado.")

    instrutores_dict = buscar_instrutor_dict()
    nomes_disponiveis_inst = list(instrutores_dict.keys())
    instrutor = st.text_input("Buscar ID por nome de instrutor:", key="buscar_instrutor")
    sugestoesinst = [nome for nome in nomes_disponiveis_inst if instrutor.lower() in nome.lower()]
    if instrutor:
        if instrutor in instrutores_dict:
            st.success(f"ID do instrutor: {instrutores_dict[instrutor]}")
        elif sugestoesinst:
            st.info("Possível instrutor que está sendo buscado")
            for sugestao in sugestoesinst:
                st.write(f"Instrutor: {sugestao}")
        else:
                st.warning("Instrutor não encontrado")
    exercicio_dict = buscar_exercicio_dict()
    exercicios_disponiveis_inst = list(exercicio_dict.keys())
    exercicio = st.text_input("Buscar ID por nome do exercício:", key="buscar_exercicio")

    sugestoesex = [nome for nome in exercicios_disponiveis_inst if exercicio.lower() in nome.lower()]
    if exercicio:
        if exercicio in exercicio_dict:
            st.success(f"ID do exercício: {exercicio_dict[exercicio]}")
        elif sugestoesex:
            st.info("Possível exercício que está sendo buscado")
            for sugestao in sugestoesex:
                st.write(f"Exercício: {sugestao}")
        else:
                st.warning("Exercício não encontrado")

    st.subheader("Opções de Cadastro", divider=True)
    if opcao == 'Cadastro':
        sidebarc = st.selectbox("Escolha uma opção de Cadastro:", ['Clientes', 'Pagamentos', 'Treinos', 'Exercícios em Treino'])

        if sidebarc == 'Clientes':
            nome = st.text_input("Nome:")
            idade = st.number_input("Idade:", min_value=0)
            sexo = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"])
            email = st.text_input("Email:")
            telefone = st.text_input("Telefone:")
            plano_id = st.text_input("ID do Plano:")
            instrutor_id = st.text_input("ID do Instrutor:")
            treino_id = st.text_input("ID do Treino:")
            if st.button("Cadastrar Cliente"):
                cursor.execute("INSERT INTO clientes (nome, idade, sexo, email, telefone, plano_id, instrutor_id, treino_id) VALUES (?,?,?,?,?,?,?,?)", (nome, idade, sexo, email, telefone, plano_id, instrutor_id, treino_id))
                conn.commit()
                st.success("Cliente cadastrado com sucesso!")

        elif sidebarc == 'Pagamentos':
            cliente_id = st.text_input("ID Cliente:")
            plano_id = st.text_input("ID do Plano:")
            valor_pago = st.number_input("Valor Pago:")
            data_pagamento = st.date_input("Data de Pagamento:")
            if st.button("Registrar Pagamento"):
                cursor.execute("INSERT INTO pagamentos (cliente_id, plano_id, valor_pago, data_pagamento) VALUES (?,?,?,?)", (cliente_id, plano_id, valor_pago, data_pagamento))
                conn.commit()
                st.success("Pagamento registrado com sucesso!")

        elif sidebarc == 'Treinos':
            cliente_id = st.text_input("ID Cliente:")
            instrutor_id = st.text_input("ID do Instrutor:")
            plano_id = st.text_input("ID do Plano:")
            data_inicio = st.date_input("Início de Treino:")
            data_fim = st.date_input("Término de Treino:")
            if st.button("Cadastrar Treino"):
                cursor.execute("INSERT INTO treinos (cliente_id, instrutor_id, plano_id, data_inicio, data_fim) VALUES (?,?,?,?,?)", (cliente_id, instrutor_id, plano_id, data_inicio, data_fim))
                conn.commit()
                st.success("Treino cadastrado com sucesso!")

        elif sidebarc == 'Exercícios em Treino':
            treino_id = st.text_input("ID do Treino:")
            treino_nome = st.text_input("Nome do Treino:")
            exercicio_id = st.text_input("ID do Exercício:")
            exercicio_nome = st.text_input("Nome do Exercício:")
            series = st.number_input("Séries:", min_value=1)
            repeticoes = st.number_input("Repetições:", min_value=1)
            if st.button("Cadastrar Exercício no Treino"):
                cursor.execute("INSERT INTO treino_exercicio (treino_id, treino, exercicio_id, exercicio, series, repeticoes) VALUES (?,?,?,?,?,?)", (treino_id, treino_nome, exercicio_id, exercicio_nome, series, repeticoes))
                conn.commit()
                st.success("Exercício adicionado ao treino com sucesso!")

criar_tabela()

if 'logado' not in st.session_state:
    st.session_state['logado'] = False
    st.session_state['usuario'] = ""

if st.session_state['logado']:
    tela_principal()
else:
    main()