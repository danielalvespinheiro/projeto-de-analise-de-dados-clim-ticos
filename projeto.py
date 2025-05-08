import pandas as pd
import matplotlib.pyplot as plt

# FUNÇÃO UM
def variacaoTempPorDia(arqui):
    df = pd.read_csv(arqui, sep=";", decimal=",")
    df['Data'] = df['Data'].astype(str) # garantindo que o valor dessa coluna é string
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str).str.zfill(4) # garanto que o tipo é string e adiciono zeros a esquerda caso precise
    # crio uma nova coluna que se chama data_hora, aqui posso capturar os dadoas dia por dia
    df['Data_Hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora (UTC)'], format='%d/%m/%Y %H%M')
    # transforma a coluna Data_Hora no tipo hora, sim um tipo de dado
    df['Hora'] = df['Data_Hora'].dt.day
    media_por_hora_temperatura_ins = df.groupby('Hora')['Temp. Ins. (C)'].mean()
    media_por_hora_temperatura_max = df.groupby('Hora')['Temp. Max. (C)'].mean()
    media_por_hora_temperatura_min = df.groupby('Hora')['Temp. Min. (C)'].mean()
    # Gráfico
    plt.figure(figsize=(20, 10))
    plt.plot(media_por_hora_temperatura_ins.index, media_por_hora_temperatura_ins, marker='o', color='red', label='temperatura ins.')
    plt.plot(media_por_hora_temperatura_max.index, media_por_hora_temperatura_max, marker='.', color='green', label='temperatura max.')
    plt.plot(media_por_hora_temperatura_min.index, media_por_hora_temperatura_min, marker='>', color='blue', label='temperatura min.')
    plt.title('Temperatura média do dia passando 30 dias')
    plt.xlabel('Dia registrada')
    plt.ylabel('Temperatura (°C)')

    print("eixo x slim ",plt.xlim())
    print("eixo y slim ",plt.ylim())

    # variável para o comentário
    texto_explicativo = (
        "Faixas de temperatura para peixes:\n"
        "- 38-44°C: Redução de apetite e baixa resistência.\n"
        "- 26-30°C: Faixa de conforto.\n"
        "- 20-26°C: Consumo reduzido, crescimento lento.\n"
        "- 8-14°C: Crescimento muito lento, baixa tolerância ao manejo."
    )
    #12 é a posição x, e 31 a posição y
    plt.text(12.4, 31, texto_explicativo, fontsize=9, bbox=dict(facecolor='gray', alpha=0.5), color='black')
    plt.legend(loc='upper left', title='Média das temperaturas', fontsize='small')
    plt.grid(True)
    plt.xticks(range(1, 32))
    plt.tight_layout()
    plt.show()

# FUNÇÃO DOIS
# Analise da umidade
def variacaoUmidade(arqui):
    #tive que inicar novamente
    df = pd.read_csv(arqui, sep=";", decimal=",")
    # Substituir vírgulas por pontos e converter colunas numéricas
    df = df.replace(',', '.', regex=True)

    df['Data'] = df['Data'].astype(str) # garantindo que o valor dessa coluna é string
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str).str.zfill(4) # garanto que o tipo é string e adiciono zeros a esquerda caso precise
    df['Data_Hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora (UTC)'], format='%d/%m/%Y %H%M')
    df['Umi. Ins. (%)'] = pd.to_numeric(df['Umi. Ins. (%)'], errors='coerce')
    df['Umi. Max. (%)'] = pd.to_numeric(df['Umi. Max. (%)'], errors='coerce')
    df['Umi. Min. (%)'] = pd.to_numeric(df['Umi. Min. (%)'], errors='coerce')
    # apresento so as colunas de data_hora e umidade
    df = df[['Data_Hora', 'Umi. Ins. (%)', 'Umi. Max. (%)', 'Umi. Min. (%)']].dropna()
    df['Hora'] = df['Data_Hora'].dt.day

    mediaUmidadeIdeal = df.groupby('Hora')['Umi. Ins. (%)'].mean()
    mediaUmidadeMax = df.groupby('Hora')['Umi. Max. (%)'].mean()
    mediaUmidadeMin = df.groupby('Hora')['Umi. Min. (%)'].mean()

    # Gráfico
    plt.figure(figsize=(20, 10))
    plt.plot(mediaUmidadeIdeal.index, mediaUmidadeIdeal.values, label='Umidade Instantânea', color='blue', marker='s')
    plt.plot(mediaUmidadeMax.index, mediaUmidadeMax.values, label='Umidade Máxima', color='green', marker='o')
    plt.plot(mediaUmidadeMin.index, mediaUmidadeMin.values, label='Umidade Mínima', color='red', marker='x')

    # Faixa ideal de umidade (60% a 85%)
    plt.axhline(y=65, color='red', linestyle='--', label='Limite Inferior (65%)')
    plt.axhline(y=85, color='black', linestyle='--', label='Limite Superior (85%)')
    plt.title('Umidade Instantânea ao Longo do Tempo')
    plt.xlabel('Dia')
    plt.ylabel('Umidade (%)')
    plt.xticks(range(0, 32))

    # print(plt.xlim())
    # print(plt.ylim())

    # variável para o comentário
    texto_explicativo = (
        "Faixas de medida de umidade:\n"
        "- > 85%: crescimento de bactérias, aumento do risco de doenças e redução da reprodução.\n"
        "- 60% e 85%: ideal para a piscicultura, ambiente estável para os peixes\n"
        "- < 60% alta evaporação, variação de temperatura e concentração de sais\n"
    )

    #-1 é a posição x, e 28 a posição y
    plt.text(-0.25, 80.5, texto_explicativo, fontsize=9, bbox=dict(facecolor='gray', alpha=0.5), color='black')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# FUNÇÃO TRÊS
def juncao_Temp_Umidade_Orvalho_Vento(arqui):
    # Carregar dados
    df = pd.read_csv(arqui, sep=";", decimal=",")
    # Substituir vírgulas por pontos e converter colunas numéricas
    df = df.replace(',', '.', regex=True)

    colunas_numericas = [
        'Temp. Ins. (C)', 'Temp. Max. (C)', 'Temp. Min. (C)',
        'Umi. Ins. (%)', 'Umi. Max. (%)', 'Umi. Min. (%)', 
        'Pto Orvalho Ins. (C)', 'Pto Orvalho Max. (C)', 'Vel. Vento (m/s)'
    ]

    # Conversão das colunas numéricas para tipo numérico
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Data'] = df['Data'].astype(str)
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str).str.zfill(4)
    df['Data_Hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora (UTC)'], format='%d/%m/%Y %H%M')
    df['Dia'] = df['Data_Hora'].dt.day

    # Agrupamentos para as colunas já existentes
    media_por_hora_temperatura_ins = df.groupby('Dia')['Temp. Ins. (C)'].mean()
    media_por_hora_temperatura_max = df.groupby('Dia')['Temp. Max. (C)'].mean()
    media_por_hora_temperatura_min = df.groupby('Dia')['Temp. Min. (C)'].mean()

    mediaUmidadeIdeal = df.groupby('Dia')['Umi. Ins. (%)'].mean()
    mediaUmidadeMax = df.groupby('Dia')['Umi. Max. (%)'].mean()
    mediaUmidadeMin = df.groupby('Dia')['Umi. Min. (%)'].mean()

    mediaPontoOrvalhoIns = df.groupby('Dia')['Pto Orvalho Ins. (C)'].mean()
    mediaPontoOrvalhoMax = df.groupby('Dia')['Pto Orvalho Max. (C)'].mean()
    mediaPontoOrvalhoMin = df.groupby('Dia')['Pto Orvalho Max. (C)'].mean()

    # Adicionando a nova coluna 'Vel. Vento (m/s)'
    mediaVelocidadeVento = df.groupby('Dia')['Vel. Vento (m/s)'].mean()

    # Gráfico com dois eixos Y
    fig, ax1 = plt.subplots(figsize=(12, 10))

    # Umidade
    ax1.plot(mediaUmidadeIdeal.index, mediaUmidadeIdeal, label='Umidade Inst.', color='red', marker='s')
    ax1.plot(mediaUmidadeMax.index, mediaUmidadeMax, label='Umidade Máx.', color='green', marker='s')
    ax1.plot(mediaUmidadeMin.index, mediaUmidadeMin, label='Umidade Mín.', color='blue', marker='s')
    ax1.axhline(y=65, color='salmon', linestyle='--', label='Limite Inf. (65%)')
    ax1.axhline(y=85, color='black', linestyle='--', label='Limite Sup. (85%)')
    ax1.set_ylabel('Umidade (%)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Temperatura
    ax2 = ax1.twinx()
    ax2.plot(media_por_hora_temperatura_ins.index, media_por_hora_temperatura_ins, label='Temp. Inst.', color='navy', marker='o')
    ax2.plot(media_por_hora_temperatura_max.index, media_por_hora_temperatura_max, label='Temp. Máx.', color='slateblue', marker='o')
    ax2.plot(media_por_hora_temperatura_min.index, media_por_hora_temperatura_min, label='Temp. Mín.', color='mediumpurple', marker='o')
    # Ponto de orvalho 
    ax2.plot(mediaPontoOrvalhoIns.index, mediaPontoOrvalhoIns, label='Pto Orvalho Ins. (C)', color='skyblue', marker='x')
    ax2.plot(mediaPontoOrvalhoMax.index, mediaPontoOrvalhoMax, label='Pto Orvalho Max. (C)', color='steelblue', marker='x')
    ax2.plot(mediaPontoOrvalhoMin.index, mediaPontoOrvalhoMin, label='Pto Orvalho Min. (C)', color='dodgerblue', marker='x')
    # Adicionando a velocidade do vento 
    ax2.plot(mediaVelocidadeVento.index, mediaVelocidadeVento, label='Vel. Vento (m/s)', color='cyan', marker='<')
    ax2.set_ylabel('Temp/ Pto. Orvalho/ Velo. Vento', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Legendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2 , labels_1 + labels_2, loc='lower left', fontsize='x-small', ncol=1)

    # Título e eixos
    plt.title('Variação de Umidade, Temperatura e Velocidade do Vent e Ponto de Orvalho')
    plt.xlabel('Hora do Dia')
    plt.xticks(range(0, 32))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analisar_radiacao_e_energia(arquivo, area_painel, eficiencia):
    # Leitura do arquivo com separador ponto e vírgula
    df = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    df = df.replace(',', '.', regex=True)

    # Converter colunas relevantes
    df['Radiacao (KJ/m²)'] = pd.to_numeric(df['Radiacao (KJ/m²)'], errors='coerce')
    df['Radiacao (kWh/m²)'] = df['Radiacao (KJ/m²)'] * 0.0002778

    # Preparar datas
    df['Data'] = df['Data'].astype(str)
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str).str.zfill(4)
    df['Data_Hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora (UTC)'], format='%d/%m/%Y %H%M', errors='coerce')
    df['Dia'] = df['Data_Hora'].dt.day

    # Agrupamentos
    media_radiacao = df.groupby('Dia')['Radiacao (KJ/m²)'].mean()
    df_diario = df.groupby('Dia')['Radiacao (kWh/m²)'].sum().reset_index()

    # Cálculo da energia gerada
    df_diario['Energia Gerada (kWh/dia)'] = df_diario['Radiacao (kWh/m²)'] * area_painel * eficiencia

    # --- GRÁFICO UNIFICADO COM DOIS EIXOS ---
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(media_radiacao.index, media_radiacao.values, color='orange', linewidth=2, label='Radiação Média (kJ/m²)')
    ax1.set_title('Radiação Solar e Energia Gerada por Dia', fontsize=16)
    ax1.set_xlabel('Dia do Mês')
    ax1.set_ylabel('Radiação Média (kJ/m²)', color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')

    ax2 = ax1.twinx()
    ax2.plot(df_diario['Dia'], df_diario['Energia Gerada (kWh/dia)'], color='green', linewidth=2, label='Energia Gerada (kWh/dia)')
    ax2.set_ylabel('Energia Gerada (kWh/dia)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    plt.xticks(range(1, 32))
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.4, 0.9), fontsize=12)
    plt.grid(True)
    plt.show()

    # Exibir tabela resumo
    print(df_diario[['Dia', 'Energia Gerada (kWh/dia)']])


# Parâmetros
arqui = 'dados_limpos.csv'
area_painel = 20  # Área dos painéis solares em m²
eficiencia = 0.80  # Eficiência do sistema

# Chamada da função

variacaoTempPorDia(arqui)
variacaoUmidade(arqui)
# Junção da temperatu, umidade, Pto Orvalho e vento
juncao_Temp_Umidade_Orvalho_Vento(arqui)

# Extra, analise da radição e geração de energia 
analisar_radiacao_e_energia(arqui, area_painel, eficiencia)