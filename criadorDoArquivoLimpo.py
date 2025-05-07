import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('INMET_01_01_2024_A_01_06_2024_generatedBy_react-csv.csv', delimiter=';', encoding='UTF-8')

valoresVazios = df.isnull().sum()
print(valoresVazios)

# apagar valores vazios
df.fillna(0, inplace=False)

# apaga as linhs vazias
df = df.dropna()

print(df)
# Salvar o resultado em um novo arquivo
df.to_csv("dados_limpos.csv", sep=";", index=False)