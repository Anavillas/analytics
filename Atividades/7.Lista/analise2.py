import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# st.set_option('deprecation.showPyplotGlobalUse', False)  # <-- comente ou apague essa linha
st.title("Análise Estatística: Fatores que Influenciam a Expectativa de Vida (OMS)")

# --- 1. Carregar e tratar os dados ---
@st.cache_data
def load_data():
    df = pd.read_csv('analise2/Life_Expectancy_Data.csv', encoding='latin1')
    # Padronizar colunas
    df.columns = df.columns.str.strip()
    # Remover linhas com muitos dados faltantes
    df = df.dropna(thresh=15)
    # Preencher valores numéricos faltantes com média por país (mais apropriado)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    for country in df['Country'].unique():
        idx = df['Country'] == country
        df.loc[idx, numeric_cols] = df.loc[idx, numeric_cols].fillna(df.loc[idx, numeric_cols].mean())
    # Remover linhas ainda com NaN
    df = df.dropna()
    # Converter status para categoria
    df['Status'] = df['Status'].astype('category')
    return df

df = load_data()
st.sidebar.write(f"Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")

# Sidebar para navegação
questao = st.sidebar.selectbox("Selecione a questão para análise:", [
    "1. Fatores que afetam a Expectativa de Vida",
    "2. Gastos com saúde e Expectativa de Vida < 65",
    "3. Mortalidade infantil e adulta vs Expectativa de Vida",
    "4. Hábitos de vida e Expectativa de Vida",
    "5. Impacto da Escolaridade",
    "6. Consumo de álcool",
    "7. Densidade populacional",
    "8. Cobertura de imunização"
])

# 1. Fatores que afetam a expectativa de vida
if questao == "1. Fatores que afetam a Expectativa de Vida":
    st.header("1. Quais fatores afetam a Expectativa de Vida?")
    st.write("""
    Analisamos a correlação entre variáveis numéricas para identificar quais fatores
    têm maior impacto na expectativa de vida.
    """)
    
    corr = df.select_dtypes(include=np.number).corr()['Life expectancy'].sort_values(ascending=False)
    st.write("Correlação das variáveis numéricas com Expectativa de Vida:")
    st.dataframe(corr)

    st.write("Mapa de calor da correlação entre as principais variáveis:")
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    st.pyplot(plt)

    st.write("""
    Observação: Variáveis com correlação positiva alta indicam que aumentos nelas estão
    associados a aumento da expectativa de vida, enquanto correlações negativas indicam
    o contrário.
    """)

# 2. Gastos com saúde para países com expectativa < 65
elif questao == "2. Gastos com saúde e Expectativa de Vida < 65":
    st.header("2. Gastos com saúde em países com Expectativa de Vida menor que 65")
    
    low_life = df[df['Life expectancy'] < 65]
    high_life = df[df['Life expectancy'] >= 65]

    st.write(f"Países com expectativa < 65: {low_life['Country'].nunique()} países")
    st.write(f"Países com expectativa >= 65: {high_life['Country'].nunique()} países")
    
    fig = plt.figure(figsize=(10, 5))
    sns.kdeplot(low_life['percentage expenditure'], label='Vida < 65', shade=True)
    sns.kdeplot(high_life['percentage expenditure'], label='Vida >= 65', shade=True)
    plt.xlabel('Porcentagem de Gastos com Saúde')
    plt.title('Distribuição dos Gastos com Saúde')
    plt.legend()
    st.pyplot(fig)

    st.write("""
    Países com expectativa de vida menor tendem a ter gastos com saúde mais baixos em média.
    Isso sugere que aumentar os gastos pode ajudar na melhora da expectativa, mas outros fatores
    também são importantes.
    """)

# 3. Mortalidade infantil e adulta vs expectativa
elif questao == "3. Mortalidade infantil e adulta vs Expectativa de Vida":
    st.header("3. Impacto das taxas de mortalidade infantil e adulta")

    st.write("Gráfico: Mortalidade infantil x Expectativa de Vida")
    fig1 = px.scatter(df, x='infant deaths', y='Life expectancy', color='Status',
                      title='Mortalidade infantil vs Expectativa de Vida',
                      labels={'infant deaths':'Mortalidade Infantil','Life expectancy':'Expectativa de Vida'})
    st.plotly_chart(fig1)

    st.write("Gráfico: Mortalidade adulta x Expectativa de Vida")
    fig2 = px.scatter(df, x='Adult Mortality', y='Life expectancy', color='Status',
                      title='Mortalidade adulta vs Expectativa de Vida',
                      labels={'Adult Mortality':'Mortalidade Adulta','Life expectancy':'Expectativa de Vida'})
    st.plotly_chart(fig2)

    st.write("""
    Observa-se que taxas elevadas de mortalidade infantil e adulta estão associadas a menor expectativa de vida.
    Essas variáveis são indicadores críticos da saúde populacional.
    """)

# 4. Hábitos de vida
elif questao == "4. Hábitos de vida e Expectativa de Vida":
    st.header("4. Expectativa de Vida e hábitos de vida (álcool, IMC, gastos)")

    cols = ['Alcohol', 'BMI', 'percentage expenditure']
    for col in cols:
        st.write(f"Gráfico: {col} x Expectativa de Vida")
        fig = px.scatter(df, x=col, y='Life expectancy', color='Status',
                         labels={col: col, 'Life expectancy':'Expectativa de Vida'},
                         trendline='ols')
        st.plotly_chart(fig)

    st.write("""
    As relações são variadas: por exemplo, maior consumo de álcool tende a estar associado a menor expectativa,
    enquanto maior BMI e gastos com saúde mostram tendências positivas até certo ponto.
    """)

# 5. Escolaridade
elif questao == "5. Impacto da Escolaridade":
    st.header("5. Impacto da escolaridade na Expectativa de Vida")

    fig = px.scatter(df, x='Schooling', y='Life expectancy', color='Status',
                     labels={'Schooling':'Anos de escolaridade','Life expectancy':'Expectativa de Vida'},
                     trendline='ols')
    st.plotly_chart(fig)

    st.write("""
    A escolaridade tem forte correlação positiva com a expectativa de vida,
    indicando que educação é um fator chave para saúde e longevidade.
    """)

# 6. Consumo de álcool
elif questao == "6. Consumo de álcool":
    st.header("6. Consumo de álcool e Expectativa de Vida")

    fig = px.box(df, x='Status', y='Alcohol', points='all',
                 labels={'Alcohol':'Consumo de Álcool', 'Status':'Status do País'},
                 title='Consumo de álcool por status do país')
    st.plotly_chart(fig)

    st.write("""
    Observa-se que países em desenvolvimento tendem a apresentar menor consumo médio de álcool,
    porém, o impacto direto na expectativa deve ser analisado em conjunto com outros fatores.
    """)

# 7. Densidade populacional
elif questao == "7. Densidade populacional":
    st.header("7. Densidade populacional e Expectativa de Vida")

    # Criar coluna log população para melhor visualização
    df['Population_log'] = df['Population'].apply(lambda x: np.log(x) if x > 0 else 0)

    fig = px.scatter(df, x='Population_log', y='Life expectancy', color='Status',
                     labels={'Population_log':'Log da População', 'Life expectancy':'Expectativa de Vida'},
                     trendline='ols')
    st.plotly_chart(fig)

    st.write("""
    Não há uma relação direta clara entre população e expectativa de vida. Países muito populosos podem apresentar
    diferentes níveis de expectativa, sugerindo que densidade isoladamente não explica a variação.
    """)

# 8. Cobertura de imunização
elif questao == "8. Cobertura de imunização":
    st.header("8. Impacto da cobertura de imunização na Expectativa de Vida")

    imunizacoes = ['Hepatitis B', 'Measles', 'Polio', 'Diphtheria']
    for vac in imunizacoes:
        st.write(f"Gráfico: Cobertura de {vac.strip()} vs Expectativa de Vida")
        fig = px.scatter(df, x=vac, y='Life expectancy', color='Status',
                         labels={vac: f'Cobertura {vac.strip()}', 'Life expectancy':'Expectativa de Vida'},
                         trendline='ols')
        st.plotly_chart(fig)

    st.write("""
    A cobertura de imunização apresenta correlação positiva com a expectativa de vida,
    indicando que países com maiores taxas de vacinação tendem a ter populações mais saudáveis
    e maior longevidade.
    """)

# Rodapé
st.markdown("---")
st.markdown("Projeto baseado em dados do Observatório Global da Saúde da OMS e dados econômicos da ONU.")

