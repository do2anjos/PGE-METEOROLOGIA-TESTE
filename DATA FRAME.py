import pandas as pd

# Função para filtrar os dados por mês específico
def filtrar_dados_por_mes(data, data_especifica, nome_coluna_data):
    # Converte a coluna de data para o formato de data do pandas
    data[nome_coluna_data] = pd.to_datetime(data[nome_coluna_data], format='%d/%m/%Y')
    data_especifica = pd.to_datetime(data_especifica, format='%d/%m/%Y')
    primeiro_dia_mes = data_especifica.replace(day=1)
    ultimo_dia_mes = primeiro_dia_mes + pd.offsets.MonthEnd(0)
    return data[(data[nome_coluna_data] >= primeiro_dia_mes) & (data[nome_coluna_data] <= ultimo_dia_mes)].copy()

# Função para limpar os dados, convertendo as colunas de temperatura e umidade para valores numéricos
def limpar_dados(dataframe):
    dataframe = dataframe.copy()  # Cria uma cópia do dataframe

    colunas_temperatura = [
        'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
        'TEMPERATURA DO PONTO DE ORVALHO (°C)',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)'
    ]

    colunas_umidade = [
        'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
        'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'
    ]

    # Verifica se as colunas estão presentes no DataFrame antes de aplicar a conversão
    colunas_presentes = list(dataframe.columns)
    colunas_temperatura_presentes = [coluna for coluna in colunas_temperatura if coluna in colunas_presentes]
    colunas_umidade_presentes = [coluna for coluna in colunas_umidade if coluna in colunas_presentes]

    # Converte as colunas de temperatura e umidade para valores numéricos, com erros sendo substituídos por NaN
    dataframe.loc[:, colunas_temperatura_presentes + colunas_umidade_presentes] = dataframe.loc[:, colunas_temperatura_presentes + colunas_umidade_presentes].apply(pd.to_numeric, errors='coerce')

    return dataframe

# Função para adicionar colunas indicando se a temperatura está acima de 28°C ou não
def adicionar_coluna_acima_de_28(dataframe):
    dataframe = dataframe.copy()  # Cria uma cópia do dataframe

    colunas_temperatura = [
        'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
        'TEMPERATURA DO PONTO DE ORVALHO (°C)',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)'
    ]

    colunas_umidade = [
        'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
        'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'
    ]

    # Itera sobre as colunas de temperatura e umidade
    for coluna in colunas_temperatura:
        # Cria o nome da nova coluna indicando se a temperatura está acima de 28°C
        nome_coluna_acima_de_28 = f"{coluna} - Acima de 28"
        # Adiciona uma nova coluna ao dataframe com valores booleanos indicando se a temperatura está acima de 28°C
        dataframe[nome_coluna_acima_de_28] = dataframe[coluna] > 28

    return dataframe

# Função principal
def main():
    arquivo_csv = 'C:\\Users\\anjos\\Desktop\\Meteorologia\\INMET01-01-2023_A_31-05-2023.CSV'

    # Lê o arquivo CSV e armazena as informações em um DataFrame
    informacoes_csv = pd.read_csv(arquivo_csv, delimiter=';', encoding='latin-1', skiprows=9, decimal=',')

    nome_coluna_data = 'DATA'

    while True:
        print("Escolha uma opção:")
        print("1. Filtrar dados por mês específico")
        print("2. Sair")

        opcao = input("Opção: ")

        if opcao == '1':
            # Solicita a data específica ao usuário
            data_especifica = input("Digite a data no formato dd/mm/yyyy ou dd-mm-yyyy: ")

            # Filtra os dados do DataFrame para o mês específico
            dados_filtrados = filtrar_dados_por_mes(informacoes_csv, data_especifica, nome_coluna_data)

            if dados_filtrados.empty:
                print("Não há datas encontradas.")
                continue

            # Limpa os dados do DataFrame
            dados_limpos = limpar_dados(dados_filtrados)
            # Adiciona colunas indicando se a temperatura está acima de 28°C ou não
            dados_com_coluna_acima_de_28 = adicionar_coluna_acima_de_28(dados_limpos)

            colunas_temperatura = [
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
                'TEMPERATURA DO PONTO DE ORVALHO (°C)',
                'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
                'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
                'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
                'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)'
            ]

            colunas_umidade = [
                'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
                'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'
            ]

            # Calcula e exibe as estatísticas das colunas de temperatura e umidade
            for coluna in colunas_temperatura + colunas_umidade:
                temperatura_media = dados_limpos[coluna].mean()
                temperatura_minima = dados_limpos[coluna].min()
                temperatura_maxima = dados_limpos[coluna].max()

                print(f"\n{coluna}")
                print(f"Média: {temperatura_media:.2f}")
                print(f"Temperatura mínima: {temperatura_minima:.2f}")
                print(f"Temperatura máxima: {temperatura_maxima:.2f}")

            # Obtém a temperatura máxima no dia 10/01/2023
            data_especifica = pd.to_datetime(data_especifica, format='%d/%m/%Y')
            temperatura_maxima_dia_10_01_2023 = dados_limpos.loc[dados_limpos[nome_coluna_data] == data_especifica, 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].values[0]
            print(f"\nTemperatura máxima no dia 10/01/2023: {temperatura_maxima_dia_10_01_2023:.2f}")

            print("\nDias com temperatura acima de 28°C:")
            for coluna in colunas_temperatura:
                nome_coluna_acima_de_28 = f"{coluna} - Acima de 28"
                datas_acima_de_28 = dados_com_coluna_acima_de_28.loc[
                    dados_com_coluna_acima_de_28[nome_coluna_acima_de_28], nome_coluna_data]
                datas_unicas = datas_acima_de_28.drop_duplicates()

                print(f"\nDias com temperatura acima de 28°C - {coluna}:")
                if datas_unicas.empty:
                    print("Não há datas encontradas.")
                else:
                    datas_formatadas = datas_unicas.dt.strftime('%d/%m/%Y')
                    print(datas_formatadas.to_string(index=False))

            # Obtém as datas da primeira e última leitura dos dados
            primeira_data_leitura = dados_limpos[nome_coluna_data].min()
            ultima_data_leitura = dados_limpos[nome_coluna_data].max()
            print(f"\nData da primeira leitura dos dados: {primeira_data_leitura.strftime('%d/%m/%Y')}")
            print(f"Data da última leitura dos dados: {ultima_data_leitura.strftime('%d/%m/%Y')}")

        elif opcao == '2':
            break

        else:
            print("Opção inválida. Digite novamente.")

if __name__ == '__main__':
    main()
1