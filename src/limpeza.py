import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## --- importando os arquivos em CSV de uma pasta
from pathlib import Path # aqui a gente ja descreve o caminho certo com o 'path'

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data' 

dados = pd.read_csv(
    DATA_DIR / 'impacto_ambiental_brasil.csv',
    parse_dates=['ano']
)

## aqui vamos visulizar como estao os dados
print('\nimprimindo as 5 primeiras linhas\n')
print(dados.head())

print('\nimprimindo as info de cada coluna de dados\n')
dados.info()

print("\n--- Estatísticas descritivas para colunas numéricas ---\n")
# Usamos o describe() para ter uma noção inicial. 
print(dados.describe())

print('\nimprimindo valores ausentes\n')
print(dados.isna().sum())

# verificando valores duplicados
print("\n--- Verificando a presença de registros duplicados ---\n")
print(f'Numero de linhas duplicadas: {dados.duplicated().sum()}')

## --- Parte 3 - Limpeza e pre-processamento de dados  ---
print('\n--- Parte 3 - Limpeza e pre-processamento de "dados_limpo"  ---\n')

##  Copiando o DataFrame para manter o original intacto
dados_limpo = dados.copy()

## transformando tipo de dados 'ano' para int64
dados_limpo['ano'] = dados_limpo['ano'].dt.year.astype('int64')

print('\nimprimindo pra ver se deu certo\n')
dados.info()
print(dados_limpo.head())

## --- 1 Corrigindo Tipos de Dados ---
print("Corrigindo tipos de dados...")

# Removendo estados ausentes
dados_limpo = dados_limpo.dropna(subset='estado')

# Removendo 'area_desmatada_km2' (remover linhas)
dados_limpo = dados_limpo.dropna(subset='area_desmatada_km2')

# Removendo valores ausentes de 'emissao_co2_ton'
mediana_co2 = dados_limpo['emissao_co2_ton'].median()
dados_limpo['emissao_co2_ton'] = dados_limpo['emissao_co2_ton'].fillna(mediana_co2)

# Removendo valores ausente em 'fonte_dado' e substituindo pr 'Desconhecido'
dados_limpo['fonte_dado'] = dados_limpo['fonte_dado'].fillna('Desconhecido')

print('\nimprimindo valores ausentes\n')
print(dados_limpo.isna().sum())
print(dados_limpo.shape)

# # tratando valores outliers
# print("Tratando outliers...")
# sns.boxplot(y = dados_limpo['area_desmatada_km2'])
# plt.title('Boxplot de area desmatada (Antes de tratar outlier)')
# plt.show()

# print("Tratando outliers...")
# sns.boxplot(y = dados_limpo['emissao_co2_ton'])
# plt.title('Boxplot de pemissao CO2 (Antes de tratar outlier)')
# plt.show()

# Uma abordagem comum é remover valores que estão além de 3 desvios padrão da média.
limite_emissao = dados_limpo['emissao_co2_ton'].mean() + 3 * dados_limpo['emissao_co2_ton'].std()
dados_limpo = dados_limpo[dados_limpo['emissao_co2_ton'] < limite_emissao]

# print("Tratando outliers...")
# sns.boxplot(y = dados_limpo['emissao_co2_ton'])
# plt.title('Boxplot de pemissao CO2 (Antes de tratar outlier)')
# plt.show()

# print("Tratando outliers...")
# sns.boxplot(y = dados_limpo['area_reflorestada_km2'])
# plt.title('Boxplot de area reflorestada (Antes de tratar outlier)')
# plt.show()

## criando nova planilha de desmatamento anual por estado
desmatamento_anual_estado = (
    dados_limpo
    .dropna(subset=['area_desmatada_km2'])
    .groupby(['ano', 'estado'])['area_desmatada_km2']
    .sum()
    .reset_index(name='desmatamento_total_km2')
)
print('\nDesmatamento Anual por Estado\n')
print(desmatamento_anual_estado)

## criando nova planilha de desmatamento total ao longo do ano
desmatamento_total_ano = (
    desmatamento_anual_estado.groupby('ano', as_index=False)
    .agg(desmatamento_total_km2=('desmatamento_total_km2', 'sum'))
)

print('\nDesmatamento total por Ano\n')
print(desmatamento_total_ano)

## criando nova planilha de ranking dos estados que mais desmatam
ranking_desmatamento_estado = (
    desmatamento_anual_estado
    .groupby('estado', as_index=False)
    .agg(desmatamento_total_km2=('desmatamento_total_km2', 'sum'))
    .sort_values(by='desmatamento_total_km2', ascending=False)

)

# #quantos dados unicos tem em 'estado'
# print(dados_limpo['estado'].unique())


## 04 --- há relação entre desmatamento, reflorestamento e emissão de CO₂?
## --- descobrir o reflorestamento por ano/estado 
## --- descobrir o desmatamento por ano/estado
## --- descobrir a emissao co2 por ano/estado

## criando planilha de 'reflorestamento_por_ano'
print('\nReflorestamento Anual por Estado\n')

reflorestamento_anual_estado = (
    dados_limpo
    .dropna(subset=['area_reflorestada_km2'])
    .groupby(['ano','estado'])['area_reflorestada_km2']
    .sum()
    .reset_index(name='reflorestamento_anual_km2')

)
print(reflorestamento_anual_estado)

## criando nova planilha de reflorestamento total ao longo do ano
print('\nRefloresmatamento total por Ano\n')

reflorestamento_total_ano = (
    reflorestamento_anual_estado.groupby('ano', as_index=False)
    .agg(reflorestamento_anual_km2=('reflorestamento_anual_km2', 'sum'))
)

print(reflorestamento_total_ano)

## criando planilha de ranking dos reflorestamento por estados
print('\nRanking de refloresmatamento por estado\n')

ranking_reflorestamento_estado = (
    reflorestamento_anual_estado
    .groupby('estado', as_index=False)
    .agg(reflorestamento_anual_km2=('reflorestamento_anual_km2', 'sum'))
    .sort_values(by='reflorestamento_anual_km2', ascending=False)
)

print(ranking_reflorestamento_estado)

## criando planilha de emissao de CO2
print('\nEmissao CO2 Anual\n')

emissao_co2_anual_estado = (
    dados_limpo
    .dropna(subset=['emissao_co2_ton'])
    .groupby(['ano', 'estado'])['emissao_co2_ton']
    .sum()
    .reset_index(name='emissao_co2_ton_total')
)

print(emissao_co2_anual_estado)

## criando nova planilha de emissao co2 ao longo do ano
print('\nEmissao de CO2 tota por ano\n')

emissao_co2_total_ano = (
    emissao_co2_anual_estado.groupby('ano', as_index=False)
    .agg(emissao_co2_ton_total=('emissao_co2_ton_total', 'sum'))    
)

print(emissao_co2_total_ano)

## criando nova planilha de ranking de emissão de co2 por estado
print('\nRanking de Emissão de CO2 por estado\n')

ranking_emissao_co2_estado = (
    emissao_co2_anual_estado
    .groupby('estado', as_index=False)
    .agg(emissao_co2_ton_total=('emissao_co2_ton_total', 'sum'))
    .sort_values(by='emissao_co2_ton_total', ascending=False)
)

print(ranking_emissao_co2_estado)

## juntando objetos em uma planilha
print('\Periodo analitoco ano e estado\n')

analitico_ano_estado = (
    dados_limpo
    .groupby(['ano'], as_index=False)
    .agg(
        desmatamento_km2=('area_desmatada_km2', 'sum'),
        reflorestamento_km2=('area_reflorestada_km2', 'sum'),
        emissao_co_ton=('emissao_co2_ton', 'sum')
    )
)

print(analitico_ano_estado)

# Gráfico 1: Tendência de Desmatamento nos Últimos 14 Anos
desmatamento_total_ano.plot(
    x='ano',
    y='desmatamento_total_km2',
    kind='line',
    marker='.',
    linestyle='-',
    legend=False
)

plt.title('Tendência de Desmatamento nos Últimos 14 Anos')
plt.xlabel('Ano')
plt.ylabel('Desmatamento total (km²)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico 2: Ranking de desmatamento por estado
ranking_desmatamento_estado.plot(
    kind='barh',
    x='estado',
    y='desmatamento_total_km2',
    color='salmon',
    legend=False
)

plt.title('Ranking de desmatamento por estado de 2010 a 2024')
plt.xlabel('Desmatamento total (km²)')
plt.ylabel('Estado')
plt.gca().invert_yaxis()
plt.show()

# Gráfico 3: Ranking de reflorestamento por estado
ranking_reflorestamento_estado.plot(
    kind='barh',
    x='estado',
    y='desmatamento_total_km2',
    color='salmon',
    legend=False
)

plt.title('Ranking de Reflorestamento por Estado de 2010 a 2024')
plt.xlabel('Desmatamento total (km²)')
plt.ylabel('Estado')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

##  criando grafico de dispersão para analisar Desmatamento x Emissao CO²
sns.scatterplot(
    data=analitico_ano_estado,
    x='desmatamento_km2',
    y='emissao_co_ton'
)
plt.title('Desmatamento vs Emissão de CO₂')
plt.tight_layout()
plt.show()

##  criando grafico de dispersão para analisar Desmatamento x Emissao CO²
sns.scatterplot(
    data=analitico_ano_estado,
    x='reflorestamento_km2',
    y='emissao_co_ton'
)
plt.title('Reflorestamento vs Emissão de CO₂')
plt.tight_layout()
plt.show()

## correlação entre desmatamento, reflorestamento e CO²
correlacao = analitico_ano_estado[
    ['desmatamento_km2', 'reflorestamento_km2', 'emissao_co_ton']
].corr()

sns.heatmap(
    correlacao,
    annot=True,
    cmap='coolwarm'
)
plt.title('Correlação entre Desmatamento, Reflorestamento e CO₂')
plt.tight_layout()
plt.show()

