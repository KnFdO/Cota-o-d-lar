import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
link = 'https://www.aasp.org.br/suporte-profissional/indices-economicos/mensal/dolar/'
data = requests.get(link).text
soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
df = pd.DataFrame(columns=[])
for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')
    x = list()
    if columns:
        ano = columns[0].text.strip(' ')
        janeiro = columns[1].text.strip(' ')
        fevereiro = columns[2].text.strip(' ')
        marco = columns[3].text.strip(' ')
        abril = columns[4].text.strip(' ')
        maio = columns[5].text.strip(' ')
        junho = ' '
        julho = ' '
        agosto = ' '
        setembro = ' '
        outubro = ' '
        novembro = ' '
        dezembro = ' '
        if len(columns) > 6:
            junho = columns[6].text.strip(' ')
            julho = columns[7].text.strip(' ')
            agosto = columns[8].text.strip(' ')
            setembro = columns[9].text.strip(' ')
            outubro = columns[10].text.strip(' ')
            novembro = columns[11].text.strip(' ')
            dezembro = columns[12].text.strip(' ')
        df = pd.concat([df, pd.DataFrame.from_records([{'ano': ano, 'janeiro': janeiro, 'fevereiro': fevereiro,
                                                        'marco': marco, 'abril': abril, 'maio': maio, 'junho': junho,
                                                        'julho': julho, 'agosto': agosto, 'setembro': setembro,
                                                        'outubro': outubro, 'novembro': novembro,
                                                        'dezembro': dezembro}])])
df.head(20)
df.dropna()


def limpar_coluna(coluna):
    coluna = [x.replace('.', '') for x in coluna]
    coluna = [x.replace(',', '.') for x in coluna]
    return coluna


colunas_meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
                 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
for mes in colunas_meses:
    df[mes] = limpar_coluna(df[mes])
a = np.array(df)
a = np.where(a == '', 0, a)
a = np.where(a == ' ', 0, a)
a[:, 0] = a[:, 0].astype(int)
a[:, 1:] = a[:, 1:].astype(float)
count = 0
soma_dict = dict()
for x in a:
    count += 1
    if count == 10:
        key = x[0]
        soma = np.sum(x[7:])
        soma_dict[key] = soma/6
    elif count > 10:
        if count < 39:
            if count == 22:
                key = x[0]
                soma = np.sum(x[1:8]) + 2.1480 + np.sum(x[9:])
                soma_dict[key] = soma / 12
            else:
                key = x[0]
                soma = np.sum(x[1:])
                soma_dict[key] = soma/12
        else:
            key = x[0]
            soma = np.sum(x[1:])
            soma_dict[key] = soma / 11
keys = list(soma_dict.keys())
values = list(soma_dict.values())
plt.bar(keys, values, color='red')
plt.xlabel('Ano')
plt.ylabel('Dólar')
plt.title('Média anual da cotação do Dólar em Real')
plt.show()
