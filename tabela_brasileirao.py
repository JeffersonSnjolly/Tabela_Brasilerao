from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd 
import sqlite3


#CONEXÃO COM O BANCO
connect = sqlite3.connect('meu_banco.db')



url = "https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/2025"
service = Service()
option = webdriver.ChromeOptions()

drive = webdriver.Chrome(service=service, options=option)


drive.get(url)
time.sleep(3)

#TIRANDO O POPUP!
drive.find_element(By.XPATH, '//*[@id="body"]/div[6]/div/button[2]').click()

tabela = drive.find_element(By.XPATH,'//*[@id="body"]/section[1]/div/div/div[2]/table')
# linhas  = tabela.find_elements(By.TAG_NAME, 'tr') Melhor Jeito
linhas = drive.find_elements(By.TAG_NAME,'tr')[:21] #tbm funciona
novas_colunas = linhas[0].text.replace('\n',' ').split()

dados =[]
for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, 'td')
    if colunas:
        dados.append([coluna.text.replace('\n',' ') for coluna in colunas])
        
df = pd.DataFrame(dados, columns=novas_colunas)
#LIMPANDO OS DADOS
df['Classificação'] = df['Classificação'].str.replace('0','', regex=False).str.replace('+','', regex=False).str.replace('-','', regex=False)
df['Classificação'] = df['Classificação'].str.replace('1 1 Corinthians', '10 Corinthians', regex=False).str.replace('11 1 Grêmio', '11 Grêmio', regex=False).str.replace('12 2 Red Bull Bragantino', '12 Red Bull Bragantino', regex=False)
df['Classificação'] = df['Classificação'].str.replace('13 2 Atlético Mineiro Saf', '13 Atlético Mineiro Saf', regex=False).str.replace('14 1 Ceará', '14 Ceará', regex=False).str.replace('15 1 Internacional', '15 Internacional', regex=False)
df['Classificação'] = df['Classificação'].str.replace('18 1 Fortaleza Ec Saf', '18 Fortaleza Ec Saf', regex=False).str.replace('19 1 Juventude', '19 Juventude', regex=False).str.replace(' 2 Sport', '20 Sport', regex=False)

#COLUNAS FINAIS
df = df[['Classificação', 'PTS', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', 'CA',
    'CV', '%',]]

#SUBINDO NO BANCO
df.to_sql('tabela_brasileirao', if_exists='replace',index=False, con=connect)
