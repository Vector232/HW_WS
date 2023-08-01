import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

# В документации замеченно, что id могут поменяться в любой момент
# поэтому получаем актуальные id
def get_area_id(name):
    heders = {'HH-User-Agent': 'api-test-agent'}
    url = 'https://api.hh.ru/areas'
    
    data = requests.get(url=url, headers=heders).json()

    # with open(f'tree.json', 'w', encoding='UTF-8') as f:
    # json.dump(tree, f,  ensure_ascii=False, indent=4)

    for country in data:
        if country['name'] != 'Россия':
            continue
        
        for area in country['areas']:
            if area['name'] == name:
                return area['id']
              
    return '0'

def soupprocess(raw_data):

    return data


def get_vacancies():
    headers = {'HH-User-Agent': 'api-test-agent'}
    url = 'https://api.hh.ru/vacancies'

    area_1 = get_area_id('Москва')
    area_2 = get_area_id('Санкт-Петербург')

    params = {'area':area_1, 'area':area_2, 'salary': None, 'currency':'USD', 'text':'python', 'search_field': 'name'}

    raw_data = requests.get(url=url, headers=headers, params=params).json()

    data = soupprocess(raw_data)

    return data


raw_data = get_vacancies()

data = raw_data

with open(f'data.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)