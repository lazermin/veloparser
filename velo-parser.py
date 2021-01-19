import requests
from bs4 import BeautifulSoup
import csv


'''Парсер информации о продаже велосипедов на avito'''
URL = 'https://www.avito.ru/moskva/velosipedy'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0', 'Accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-body-NPl6W')
    velo = []
    for item in items:
        velo.append(dict(title=item.find('span', class_='title-root-395AQ').get_text(strip=True),
                         price=item.find('span', class_='price-text-1HrJ_').get_text(strip=True),
                         adres=item.find('div').find_next('span', class_='geo-icons-agBYC').find_next('span').get_text(strip=True),
                         date=item.find('div').find_next('div', class_='iva-item-dateStep-pZ3hT').find_next('span').get_text(strip=True),
                         ))
    return velo


# Сохранение в файл csv
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Цена', 'Адрес', 'Дата'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['adres'], item['date']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        save_file(get_content(html.text), 'velo.csv')
        for key in get_content(html.text):
            print(key['title'] + '; Цена: ' + key['price'] + '; Адрес: ' + key['adres'] + '; Дата : ' + key['date'])
    else:
        print('Error!')


parse()
