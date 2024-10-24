import os 
from bs4 import BeautifulSoup ##importando biblioteca bs4
import requests
import time

print('Put some skills that you are not familiar with') 
unfamiliar_skill = input('>') ##filtro para requisitos não atendidos
print(f'Filtering out {unfamiliar_skill}')

def clear_posts(): ##função para limpar os posts antigos dos txts
    folder = 'posts'
    if os.path.exists(folder): ##condição
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename) ##encontrar o diretorio
            if os.path.isfile(file_path) and file_path.endswith('.txt'): ##se existir e terminar em txt será excluído
                os.remove(file_path) ##remoção

def find_jobs(): ##função para encontrar os empregos

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=Python&txtLocation=').text ##acessando um link
    soup = BeautifulSoup(html_text, 'lxml') ##usando biblioteca para acessar o html de forma organizada
    jobs = soup.find_all('li', class_= 'clearfix job-bx wht-shd-bx') ##find_all para printar tudo, senão printaria somente o primeiro

    if not os.path.exists('posts'): 
        os.makedirs('posts')

    for index, job in enumerate(jobs): ##iteração para encontrar as características que queremos 
        company_name = job.find('h3', class_= 'joblist-comp-name').text.replace(' ', '') ##class faz parte do html e ajuda para organizá-lo
        skills = job.find('span', class_ = 'srp-skills').text.replace('\n', ' ') ##replace para organizar 
        published_date = job.find('span', class_ ='sim-posted').span.text ##span, h3, h2 são tags para organizar o html e são associados ao texto
        more_info = job.header.h2.a['href'] 

        if unfamiliar_skill not in skills: ##usando o filtro para printarmos somente os que nos satisfazem
            with open(f'posts/{index}.txt', 'w') as f: ##'w' para escrever o arquivo e definindo a variavel para f

                f.write(f"Company Name: {company_name.strip()} \n") 
                f.write(f"Required Skills: {skills.strip()} \n")
                f.write(f"Published Date: {published_date} \n")
                f.write(f"More Info: {more_info} \n")

                print(f'File Saved: {index}')

if __name__ == '__main__': ##rodar o código
    while True:
        clear_posts() ##uso das funções
        find_jobs() 
        time_wait = 10 ##tempo de espera
        print(f'Waiting {time_wait} minutes...') ##tempo mostrado enquanto são printados os txts
        time.sleep(time_wait * 60)
