import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# --- Leitura dos dados prontos
dados = pd.read_csv(DATA_DIR / 'dados_limpos.csv')

# ===============================
# 1️ AGREGAÇÕES
# ===============================

analitico_ano_estado = (
    dados
    .groupby(['ano', 'estado'], as_index=False)
    .agg(
        desmatamento_km2=('area_desmatada_km2', 'sum'),
        reflorestamento_km2=('area_reflorestada_km2', 'sum'),
        emissao_co_ton=('emissao_co2_ton', 'sum')
    )
)

# --- Total anual
analitico_ano = (
    analitico_ano_estado
    .groupby('ano', as_index=False)
    .agg(
        desmatamento_km2=('desmatamento_km2', 'sum'),
        reflorestamento_km2=('reflorestamento_km2', 'sum'),
        emissao_co_ton=('emissao_co_ton', 'sum')
    )
)

# ===============================
# 2️ GRÁFICOS
# ===============================

# Tendência do desmatamento
analitico_ano.plot(
    x='ano',
    y='desmatamento_km2',
    kind='line',
    marker='o',
    legend=False
)
plt.title('Desmatamento total por ano')
plt.xlabel('Ano')
plt.ylabel('km²')
plt.grid(True)
plt.show()

# Scatter: Desmatamento x CO₂
sns.scatterplot(
    data=analitico_ano,
    x='desmatamento_km2',
    y='emissao_co_ton'
)
plt.title('Desmatamento vs Emissão de CO₂')
plt.show()

# Scatter: Reflorestamento x CO₂
sns.scatterplot(
    data=analitico_ano,
    x='reflorestamento_km2',
    y='emissao_co_ton'
)
plt.title('Reflorestamento vs Emissão de CO₂')
plt.show()

# ===============================
# 3️ CORRELAÇÃO
# ===============================

correlacao = analitico_ano[
    ['desmatamento_km2', 'reflorestamento_km2', 'emissao_co_ton']
].corr()

sns.heatmap(correlacao, annot=True, cmap='coolwarm')
plt.title('Correlação entre variáveis ambientais')
plt.show()
