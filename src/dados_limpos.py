import pandas as pd
from pathlib import Path

# --- Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# --- Leitura
dados = pd.read_csv(
    DATA_DIR / 'impacto_ambiental_brasil.csv',
    parse_dates=['ano']
)

# --- Diagnóstico inicial
print(dados.info())
print(dados.isna().sum())

# --- Cópia segura
dados_limpo = dados.copy()

# --- Conversão de tipo
dados_limpo['ano'] = dados_limpo['ano'].dt.year.astype('int64')

# --- Limpeza de valores ausentes
dados_limpo = dados_limpo.dropna(subset=['estado'])
dados_limpo = dados_limpo.dropna(subset=['area_desmatada_km2'])

mediana_co2 = dados_limpo['emissao_co2_ton'].median()
dados_limpo['emissao_co2_ton'] = dados_limpo['emissao_co2_ton'].fillna(mediana_co2)

dados_limpo['fonte_dado'] = dados_limpo['fonte_dado'].fillna('Desconhecido')

# --- Tratamento simples de outliers (CO₂)
limite_emissao = (
    dados_limpo['emissao_co2_ton'].mean()
    + 3 * dados_limpo['emissao_co2_ton'].std()
)

dados_limpo = dados_limpo[dados_limpo['emissao_co2_ton'] < limite_emissao]

# --- Validação final
print(dados_limpo.info())
print(dados_limpo.isna().sum())

# --- Saída padronizada
dados_limpo.to_csv(DATA_DIR / 'dados_limpos.csv', index=False)

print('✔ Dados limpos salvos em data/dados_limpos.csv')
