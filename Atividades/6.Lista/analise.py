import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#Sexo	Dependentes	Educação	Estado Civil	
# Faixa Salarial Anual	Categoria Cartão	Meses como Cliente	
# Produtos Contratados	Inatividade 12m	Contatos 12m	Limite	Limite Consumido	
# Limite Disponível	Mudanças Transacoes_Q4_Q1	Valor Transacoes 12m	
# Qtde Transacoes 12m	Mudança Qtde Transações_Q4_Q1	Taxa de Utilização Cartão

sidebar = st.sidebar.selectbox("Visualizações sobre Análise de Clientes", ['Análise Descritiva Geral', 'Comportamento Financeiro e Uso do Cartão','Análise de Produtos e Serviços', 'Motivação e Satisfação do Cliente (indiretamente)', 'Segmentação de Clientes'])

df = pd.read_csv('clientes.csv', sep=',', encoding='latin1')
st.subheader("Todos os clientes")
st.dataframe(df)


if sidebar == 'Análise Descritiva Geral':
    st.subheader("Proporção de clientes Ativos X Cancelados")
    
    # Agrupa os dados
    proporcao = df['Categoria'].value_counts().reset_index()
    proporcao.columns = ['Categoria', 'Quantidade']
    
    # Cria o gráfico de pizza
    fig = px.pie(proporcao, values='Quantidade', names='Categoria',
                 title='Proporção de clientes Ativos x Cancelados')
    
    st.plotly_chart(fig, use_container_width=True)

    
#Perfil demográfico: idade, gênero, região, renda, etc. Há grupos com maior tendência a cancelar?
    st.subheader('Perfil demográfico: idade, gênero, região, renda, etc')
    fig = px.box(df, x='Categoria', y='Idade', points='all', title='Distribuição de Idade por Categoria')
    st.plotly_chart(fig, use_container_width=True)
    
    genero_categoria = df.groupby(['Sexo', 'Categoria']).size().reset_index(name='Quantidade')

    fig = px.bar(genero_categoria, x='Sexo', y='Quantidade', color='Categoria', barmode='group',
                title='Cancelamento por Gênero')
    st.plotly_chart(fig, use_container_width=True)
    st.write("Temos mais mulheres cancelando do que homens, portanto devemos ter uma abordagem diferente para nosso público feminino.")

#Tempo de relacionamento: quanto tempo em média os clientes ficam antes de cancelar? Clientes que cancelam logo após abrir o cartão são um sinal de problema na experiência inicial.



st.subheader("Clientes com cartões cancelados")
cancel_client = df[df['Categoria'] == 'Cancelado']
st.dataframe(cancel_client)
client_now = df[df['Categoria'] == 'Cliente']


#- Informações de renda e familiares
#- Meses inativos antes de cancelar
#- Categoria do cartão
#- Faixa salarial anual
#- Limite consumido e limite
#- Média de quantidade de transações no ano


st.subheader("Faixa salarial + limite consumido e quanto de limite possui dos cancelados")
st.write(cancel_client[['Faixa Salarial Anual', 'Categoria Cartão', 'Limite Consumido', 'Limite Disponível', 'Produtos Contratados', 'Valor Transacoes 12m', 'Qtde Transacoes 12m']])

st.subheader("Meses inativos antes de cancelar")

st.write(cancel_client.groupby('Inatividade 12m')['Meses como Cliente'])
st.write(cancel_client[['Inatividade 12m','Meses como Cliente']])

st.subheader("Idade média dos cancelados")
figIdade, ax = plt.subplots()
sns.histplot(data=df, x='Idade', hue='Categoria', kde=True, ax=ax)
st.pyplot(figIdade)

st.subheader("Dependentes")

figDep, ax = plt.subplots()
sns.boxplot(x='Categoria', y='Dependentes', data=df, ax=ax)
st.pyplot(figDep)
