import sqlite3
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags


conn = sqlite3.connect("sistemabiblioteca.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS AUTORES(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME TEXT NOT NULL)
 ''')
conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS CATEGORIAS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME TEXT NOT NULL)
''')
conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS LIVROS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITULO TEXT NOT NULL,
    AUTOR_ID INTEGER NOT NULL,
    CATEGORIA_ID INTEGER NOT NULL,
    ANO DATE NOT NULL,
    QUANTIDADE_DISPONIVEL INTEGER NOT NULL,
    FOREIGN KEY (AUTOR_ID) REFERENCES AUTORES(ID),
    FOREIGN KEY (CATEGORIA_ID) REFERENCES CATEGORIAS(ID))
''')
conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS EMPRESTIMOS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    LIVRO_ID INTEGER NOT NULL,
    DATA_EMPRESTIMO DATE NOT NULL,
    DEVOLVIDO BOOLEAN NOT NULL,
    FOREIGN KEY (LIVRO_ID) REFERENCES LIVROS(ID)) 
''')
conn.commit()



cursor.execute("SELECT COUNT(*) FROM AUTORES")
if cursor.fetchone()[0] == 0:
    autores_iniciais = [
        ('Ana Beatriz Lima',),
        ('Carlos Henrique Dias',),
        ('Fernanda Souza',),
        ('João Ricardo Martins',),
        ('Marina Duarte',),
        ('Lucas Ferreira',),
        ('Paula Cristina Lopes',),
        ('Rodrigo Azevedo',),
        ('Gabriela Tavares',),
        ('Bruno Mendes',)
    ]

    cursor.executemany("INSERT INTO AUTORES (NOME) VALUES (?)", autores_iniciais)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM CATEGORIAS")
if cursor.fetchone()[0] == 0:
    categorias_iniciais = [
        ('Mistério',),
        ('Ficção Científica',),
        ('Gastronomia',),
        ('Autoajuda',),
        ('Fantasia',),
        ('Tecnologia',),
        ('Romance',),
        ('Filosofia',),
        ('Aventura',),
        ('Terror',)
    ]

    cursor.executemany("INSERT INTO CATEGORIAS (NOME) VALUES (?)", categorias_iniciais)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM LIVROS")
if cursor.fetchone()[0] == 0:
    livros_iniciais = [
        ('O Mistério da Biblioteca Perdida',1,1,2015, 5),
        ('Aventuras no Espaço-Tempo',2,2,2018, 15),
        ('Culinária para Todos',3,3,2011, 4),
        ('O Poder da Mente',4,4,2022, 4),
        ('Histórias de Um Reino Esquecido',5,5,2013, 9),
        ('Guia Rápido de Programação Python',6,6,2017, 3),
        ('O Eco das Montanhas',7,7,2012, 1),
        ('Filosofia em Pílulas',8,8,2021, 1),
        ('O Caminho do Guerreiro',9,9,2012, 2),
        ('Contos de terror',10,10,1992, 2),


    ]

    cursor.executemany("INSERT INTO LIVROS (TITULO, AUTOR_ID, CATEGORIA_ID, ANO, QUANTIDADE_DISPONIVEL) VALUES (?,?,?,?,?)", livros_iniciais)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM EMPRESTIMOS")
if cursor.fetchone()[0] == 0:
    emprestimos_iniciais = [
        (1,'05-03-2015', True),
        (2,'04-02-2025', True),
        (3,'21-05-2025', False),
        (4,'09-01-2025', True),
        (5,'15-01-2025', True),
        (6,'04-02-2025', True),
        (7,'07-05-2025', False),
        (8,'21-04-2025', True),
        (9,'11-03-2025', True),
        (10,'12-02-2015', True)

    ]

    cursor.executemany("INSERT INTO EMPRESTIMOS (LIVRO_ID, DATA_EMPRESTIMO, DEVOLVIDO) VALUES (?,?,?)", emprestimos_iniciais)
    conn.commit()

cursor.execute("SELECT * FROM AUTORES")
autores = cursor.fetchall()
print(autores)

cursor.execute("SELECT * FROM CATEGORIAS")
categorias = cursor.fetchall()
print(categorias)

cursor.execute("SELECT * FROM LIVROS")
livros = cursor.fetchall()
print(livros)

st.subheader('Categoria de livros com autores', divider=True)
df = pd.read_sql_query('''
SELECT L.TITULO, A.NOME AS AUTOR, C.NOME AS CATEGORIA
    FROM LIVROS L
    INNER JOIN AUTORES A ON L.AUTOR_ID = A.ID 
    INNER JOIN CATEGORIAS C ON L.CATEGORIA_ID = C.ID;              
                       ''', conn)
st.dataframe(df)

st.subheader('Filtro de livros por ano de publicação.', divider=True)
df2 = pd.read_sql_query('''
SELECT * FROM EMPRESTIMOS''', conn)
st.dataframe(df2)

st.subheader('Quantidade total de livros, de empréstimos e devolvidos.')
df3 = pd.read_sql_query(''' 
SELECT
  (SELECT COUNT(*) FROM LIVROS) AS TOTAL_LIVROS,
  (SELECT COUNT(*) FROM EMPRESTIMOS) AS QTD_EMPRESTIMOS,
  (SELECT COUNT(*) FROM EMPRESTIMOS WHERE DEVOLVIDO = 1) AS QTD_DEVOLVIDOS;
''', conn)
st.dataframe(df3)

st.subheader('Número de livros por caregoria')
df4 = pd.read_sql_query('''
SELECT 
    C.NOME AS CATEGORIA, 
    COUNT(L.ID) AS TOTAL_LIVROS
FROM LIVROS L
JOIN CATEGORIAS C ON L.CATEGORIA_ID = C.ID
GROUP BY C.NOME
ORDER BY TOTAL_LIVROS DESC
''', conn)

st.dataframe(df4)

st.subheader('Formulário para registrar empréstimo ou livro')
selectReOrEm = st.selectbox('Opção',['Escolha uma opção','Registrar','Emprestar'])

if selectReOrEm == 'Registrar':
    titulo = st.text_input('Título do livro:')
    autor = st.text_input('Autor ID:')
    categoria = st.text_input('Categoria:')
    ano = st.text_input('Ano de Lançamento:') 
    qtd = st.text_input('Quantidade disponível:')
    cursor.execute("INSERT INTO LIVROS (TITULO, AUTOR_ID, CATEGORIA_ID, ANO, QUANTIDADE_DISPONIVEL) VALUES (?,?,?,?,?)", (titulo, autor, categoria, ano, qtd))
    conn.commit()
    st.dataframe(df)


if selectReOrEm == 'Emprestar':
    livro = st.text_input('Insira o ID do livro para emprestar:')
    cursor.execute("UPDATE EMPRESTIMOS SET DATA_EMPRESTIMO = CURRENT_DATE, DEVOLVIDO = 0 WHERE ID = ?", (livro,))
    conn.commit()
    if cursor.rowcount == 0:
            st.warning('Empréstimo não encontrado para o ID informado.')
    else:
            st.success('Empréstimo atualizado com sucesso!')
    df5 = pd.read_sql_query('''SELECT * FROM EMPRESTIMOS''', conn)
    st.dataframe(df5)

selectAut = st.selectbox('Opção para Autor',['Escolha uma opção','Editar','Deletar'])

if selectAut == 'Editar':
    id = st.text_input('Insira o ID do autor a ser alterado:')
    autor = st.text_input('Insira o novo nome:')
    cursor.execute("UPDATE AUTORES SET NOME = ? WHERE ID = ?",(autor, id))
    conn.commit()

    df6 = pd.read_sql_query('''SELECT * FROM AUTORES''', conn)
    st.dataframe(df6)

if selectAut == 'Deletar':
    id = st.text_input('Insira o ID do autor:')
    cursor.execute("DELETE FROM AUTORES WHERE ID=?",(id,))
    conn.commit()
    
    df6 = pd.read_sql_query('''SELECT * FROM AUTORES''', conn)
    st.dataframe(df6)

selectLiv = st.selectbox('Opção para Livros',['Escolha uma opção','Editar','Deletar'])

if selectLiv == 'Deletar':
    id = st.text_input('Insira o ID do livro:')
    cursor.execute("DELETE FROM AUTORES WHERE ID=?",(id,))
    conn.commit()
    
    df6 = pd.read_sql_query('''SELECT * FROM LIVROS''', conn)
    st.dataframe(df6)

if selectLiv == 'Editar':
    id = st.text_input('Insira o ID do livro a ser alterado:')
    titulo = st.text_input('Título novo:')
    categoria = st.text_input('Categoria ID:')
    qtd = st.text_input('Quantidade:')
    cursor.execute("UPDATE LIVROS SET TITULO = ?, CATEGORIA_ID = ?, QUANTIDADE_DISPONIVEL = ? WHERE ID = ?", (titulo, categoria, qtd, id,))
    conn.commit()

    df6 = pd.read_sql_query('''SELECT * FROM LIVROS''', conn)
    st.dataframe(df6)


st.subheader('FORMULÁRIOS DE LIVROS', divider=True)
def buscar_autores():
    cursor.execute("SELECT nome FROM autores")
    return [r[0] for r in cursor.fetchall()]

def adicionar_autor(nome):
    cursor.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
    conn.commit()

st.title("Autocomplete com streamlit-tags")

# Busca todos autores do banco para sugestões
lista_autores = buscar_autores()

# Input com sugestões e possibilidade de adicionar novo
autores_selecionados = st_tags(
    label='Digite ou selecione autores (pressione Enter para adicionar)',
    text='',
    value=[],
    suggestions=lista_autores,
    maxtags=5,
    key='tags1'
)

st.write("Autores escolhidos:", autores_selecionados)

# Adiciona novos autores ao banco, se ainda não existirem
novos_autores = [a for a in autores_selecionados if a not in lista_autores]

if novos_autores:
    if st.button(f"Adicionar {len(novos_autores)} autor(es) novo(s) no banco"):
        for autor in novos_autores:
            adicionar_autor(autor)
        st.success(f"Autores {', '.join(novos_autores)} adicionados!")