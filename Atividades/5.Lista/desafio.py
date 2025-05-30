import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dados_alunos_escola.csv', sep=',', encoding='utf-8')
coluna = st.sidebar.selectbox(
    "Escolha uma opção:",
   ['Estatísticas Descritivas','Filtros e Agrupamentos','Visualizações']
)

if coluna in ['Estatísticas Descritivas']:
    st.subheader(f"Média de Matemática, Português e Ciências", divider=True)
    st.write(df['nota_matematica'].mean())
    st.write(df['nota_portugues'].mean())
    st.write(df['nota_ciencias'].mean())
    st.subheader(f"Frequência média de aluno por série", divider=True)
    st.write(df.groupby('serie')['frequencia_%'].mean())

if coluna in ['Filtros e Agrupamentos']:
   #3. Filtre os alunos com frequência abaixo de 75% e calcule a média geral deles.
    filter = df[df['frequencia_%'] < 75]
    filter['media_geral'] = (filter['nota_matematica']+ filter['nota_portugues'] + filter['nota_ciencias'])/3
    st.subheader('Média geral alunos com frequência inferior a 75%', divider=True) 
    st.write(filter[['nome','serie','frequencia_%','media_geral']].round(2))
    #4. Use groupby para obter a nota média por cidade e matéria.
    st.subheader('Nota média por cidade e Matéria', divider=True) 
    st.write(df.groupby('cidade')[['nota_portugues','nota_matematica','nota_ciencias']].mean().round(2))
    #5 ------------------------------------
    st.subheader('Classificação de notas', divider=True) 
    df['media_geral'] = (df['nota_matematica']+ df['nota_portugues'] + df['nota_ciencias'])/3
    bins = [0, 3, 5.99999999, float('inf')]
    labels = ['Reprovado', 'Exame', 'Aprovado']
    df['Aprovacao'] = pd.cut(df['media_geral'], bins=bins, labels=labels)
    st.dataframe(df[['nome','serie','media_geral','Aprovacao']].round(2))
    #6 --------------------------------------
    st.subheader('Quantidade de notas menores que:', divider=True) 
    for materia in ['nota_portugues', 'nota_ciencias', 'nota_matematica']:
        menorq3 = df[df[materia] < 3].shape[0]
        menorq5 = df[df[materia] < 5].shape[0]
        menorq7 = df[df[materia] < 7].shape[0]
        menorq9 = df[df[materia] < 9].shape[0]
        igual10 = df[df[materia] == 10].shape[0]

        st.write(f'{materia} menor que 3: {menorq3}')
        st.write(f'{materia} menor que 5: {menorq5}')
        st.write(f'{materia} menor que 7: {menorq7}')
        st.write(f'{materia} menor que 9: {menorq9}')
        st.write(f'{materia} igual a 10: {igual10}')

    #11. Qual cidade tem a melhor nota em Matemática, português e ciências? E a Pior nota?
    for materia in ['nota_portugues', 'nota_ciencias', 'nota_matematica']:
        #pensei em usar filter pra ter um novo dicionario e depois disso só puxar a cidade com maior nota e pior
        st.write(f'{materia}, {df[['cidade',materia]].max()}')
if coluna in ['Visualizações']:
    st.subheader('Histograma das notas de todas as matérias:', divider=True) 
    plt.hist(df[['nota_ciencias','nota_matematica','nota_portugues']], bins=50) # qtd de barras
    plt.title("Distribuição de Notas")
    plt.xlabel("Notas")
    plt.ylabel("Frequência")
    st.pyplot(plt)
    
    st.subheader('Boxplot comparando notas de português por série:', divider=True) 
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='nota_portugues', y='serie',data=df, ax = ax)
    st.pyplot(fig)

    st.subheader('Boxplot comparando notas de Matemática por série:', divider=True) 
    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='nota_matematica', y='serie',data=df, ax = ax)
    st.pyplot(fig2)

    st.subheader('Boxplot comparando notas de Ciências por série:', divider=True) 
    fig3, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='nota_ciencias', y='serie',data=df, ax = ax)
    st.pyplot(fig3)

    st.subheader('Gráfico de barras com a quantidade de alunos por cidade:', divider=True) 
    alunos_por_cidade = df.groupby('cidade').size().reset_index(name='quantidade_alunos')

    st.subheader('Quantidade de alunos por cidade')
    st.bar_chart(data=alunos_por_cidade, x='cidade', y='quantidade_alunos')

    st.subheader('Gráfico de dispersão entre frequencia_% e nota por matéria:', divider=True) 
    df_melted = pd.melt(df, id_vars=['frequencia_%'], 
                    value_vars=['nota_ciencias', 'nota_portugues', 'nota_matematica'],
                    var_name='materia', value_name='nota')

    st.subheader('Gráfico de dispersão entre frequência e notas por matéria')

    fig4, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='frequencia_%', y='nota', hue='materia', data=df_melted, ax=ax)
    st.pyplot(fig4)



