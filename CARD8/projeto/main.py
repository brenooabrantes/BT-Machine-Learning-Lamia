import os
from bs4 import BeautifulSoup  #Biblioteca para análise de documentos HTML
import requests
import time

#Solicita ao usuario que insira habilidades desconhecidas para serem filtradas
print('Put some skills that you are not familiar with')
unfamiliar_skill = input('>')  #Entrada do usuario
print(f'Filtering out {unfamiliar_skill}')  #Mostra o filtro aplicado

#Função para excluir arquivos de postagens antigos
def clear_posts():
    folder = 'posts'  #Diretório que armazena as postagens
    if os.path.exists(folder):  #Verifica se o diretório existe
        for filename in os.listdir(folder):  #Itera sobre arquivos na pasta
            file_path = os.path.join(folder, filename)  #Cria caminho completo
            if os.path.isfile(file_path) and file_path.endswith('.txt'):  #Confirma que é um arquivo .txt
                os.remove(file_path)  #Remove o arquivo

#Função para encontrar e salvar vagas de emprego
def find_jobs():
    #Requisição à URL para obter a página HTML com vagas
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')  #Analisa o HTML usando lxml
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  #Localiza todas as vagas listadas

    #Cria o diretório 'posts' se ele não existir
    if not os.path.exists('posts'):
        os.makedirs('posts')

    #Itera pelas vagas encontradas
    for index, job in enumerate(jobs):
        company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')  #Extrai o nome da empresa
        skills = job.find('span', class_='srp-skills').text.replace('\n', ' ')  #Extrai as habilidades requeridas
        published_date = job.find('span', class_='sim-posted').span.text  #Extrai a data de publicação
        more_info = job.header.h2.a['href']  #Link com mais detalhes da vaga

        #Condição para filtrar vagas de acordo com habilidades
        if unfamiliar_skill not in skills:
            with open(f'posts/{index}.txt', 'w') as f:  # ria um arquivo .txt para cada vaga filtrada
                #Escreve as informações no arquivo
                f.write(f"Company Name: {company_name.strip()} \n")
                f.write(f"Required Skills: {skills.strip()} \n")
                f.write(f"Published Date: {published_date} \n")
                f.write(f"More Info: {more_info} \n")
                print(f'File Saved: {index}')
                #Confirmação de salvamento do arquivo

#Execução principal do código com loop
if __name__ == '__main__':
    while True:
        clear_posts()  #Remove arquivos de postagens antigos
        find_jobs()  #Coleta e salva novas vagas
        time_wait = 10  #Intervalo de espera em minutos
        print(f'Waiting {time_wait} minutes...')  #Exibe o tempo de espera
        time.sleep(time_wait * 60)  #Pausa o código pelo tempo definido

        #Testes feitos na pasta testes onde realizo filtragem das skills django, css e html.