import os
from bs4 import BeautifulSoup
import requests
import time

print('Put some skills that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def clear_posts():
    folder = 'posts'
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and file_path.endswith('.txt'):
                os.remove(file_path)

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_= 'clearfix job-bx wht-shd-bx')

    if not os.path.exists('posts'):
        os.makedirs('posts')

    for index, job in enumerate(jobs):
        company_name = job.find('h3', class_= 'joblist-comp-name').text.replace(' ', '')
        skills = job.find('span', class_ = 'srp-skills').text.replace('\n', ' ')
        published_date = job.find('span', class_ ='sim-posted').span.text
        more_info = job.header.h2.a['href']

        if unfamiliar_skill not in skills:
            with open(f'posts/{index}.txt', 'w') as f:

                f.write(f"Company Name: {company_name.strip()} \n")
                f.write(f"Required Skills: {skills.strip()} \n")
                f.write(f"Published Date: {published_date} \n")
                f.write(f"More Info: {more_info} \n")

                print(f'File Saved: {index}')

if __name__ == '__main__':
    while True:
        clear_posts()
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
