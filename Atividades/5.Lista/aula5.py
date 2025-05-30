import streamlit as st
import pandas as pd
from vega_datasets import data

df = data.barley()

df = pd.read_csv('dados_estatistica_visualizacao.csv', sep=',', encoding='utf-8')
st.title("Painel de Análise de Funcionários")


coluna = st.sidebar.selectbox(
    "Escolha uma opção:",
   ['idade','salario','departamento','estado']
)

st.subheader(f"Estatisticas de {coluna}", divider=True)
st.dataframe(df)

if coluna in ['idade','salario']:
    st.subheader(f"Média de {coluna}", divider=True)
    st.write(df[coluna].mean())
    st.subheader(f"Mediana de {coluna}", divider=True)
    st.write(df[coluna].median())
    st.subheader(f"Variância {coluna}", divider=True)
    st.write(df[['idade','salario']].var())
    st.subheader(f"Amplitude de {coluna}", divider=True)
    st.write(df[['idade','salario']].max()-df[['idade','salario']].min())

if coluna in ['idade']:
    bins = [0, 25, 45, float('inf')]
    labels = ['Jovem', 'Adulto', 'Sênior']
    df['Faixa Etária'] = pd.cut(df['idade'], bins=bins, labels=labels)
    st.subheader(f"Categorizando a idade", divider=True)
    st.dataframe(df)

#3. Visualizações:
#*   Gráfico de barras com a distribuição por estado.
#*   Boxplot de salário por departamento.
#*   Gráfico de dispersão entre idade e salario, colorido por departamento.

st.subheader(f"Gráfico de barras com distribuição por {coluna}", divider=True)
st.bar_chart(df, x='idade', color="site", stack=False)



import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 12))
plt.subplot(3, 1, 1)
sns.countplot(x='estado', data=df)

plt.subplot(3, 1, 2)
sns.boxplot(x = 'departamento', y = 'salario', data=df)

plt.subplot(3, 1, 3)
sns.set_theme(style="ticks")
sns.scatterplot(x='idade', y='salario', hue='departamento', data=df)
plt.show()

