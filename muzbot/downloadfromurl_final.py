import requests
from bs4 import BeautifulSoup
import os


def reg_href(div):
    start_index = div.find('href="') + len('href="')
    end_index = div.find('"', start_index)
    href_content = div[start_index:end_index]
    return href_content


def parse_response(user_response):
    song_response = user_response.replace(" ", "%20")
    base = "https://mp3party.net"
    baze_url = "https://mp3party.net/search?q=" + song_response
    html = requests.get(baze_url)
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    download_links = soup.find_all('div', {"class": "track song-item"})
    print(baze_url)

    for link in download_links:
        for j_line in str(link).split("\n"):
            if j_line.startswith("<a"):
                href_content = reg_href(j_line)
                print(base + href_content)
                result = (get_download_url(base + href_content), user_response)
                print(result[0])
                download_file(url=result[0], filename=result[1] + ".mp3")

        break


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        folder = "music"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Файл {filename} успешно скачан в папку {folder}.")
    else:
        print("Не удалось скачать файл.")


def get_download_url(url):
    l_html = requests.get(url)
    l_html = l_html.text
    l_soup = BeautifulSoup(l_html, 'html.parser')
    l_download_link = l_soup.find_all('div', {"id": "download"})
    for div_line in str(l_download_link).split("\n"):
        return reg_href(div_line)


import os

# Укажите путь к папке, которую вы хотите просканировать
folder_path = r'C:\Users\wowbg\PycharmProjects\pythonProject3\muzbot\music'

# Проходим по всем файлам в папке
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        print(file_path.split("\\")[-1])
