import requests
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
# готовим нужные данные
def get_info(raw_data, currency_code = None):
    data = [{'n':i,
            'name':note['name'],
            'alternate_url':note['alternate_url'],
            'salary':note['salary'],
            'employer':note['employer']['name'],
            'area':note['area']['name']} for i, note in enumerate(raw_data['items']) 
                                         if currency_code == None or currency_code == note['salary']['currency']]

    return data
# получаем список всех вакансий с указанными в задании ограничениями
def get_vacancies():
    # доступ к списку вакансий предоставляется и без авторизации пользователя\приложения
    headers = {'HH-User-Agent': 'api-test-agent'}
    url = 'https://api.hh.ru/vacancies'
    # получаем актуальный АЙДИ городов
    area_1 = get_area_id('Москва')
    area_2 = get_area_id('Санкт-Петербург')
    # пользуемся языком запросов, описанным в документации
    text = '(NAME:python) AND (DESCRIPTION: django OR flask)'
    
    params = {'area': [area_1, area_2],
              'text':text,
              'per_page': 100,
              'only_with_salary': True,
              'order_by':'publication_time'}

    raw_data = requests.get(url=url, headers=headers, params=params).json()

    return raw_data

# получаем "сырой" ответ
raw_data = get_vacancies()
# отрезаем ненужную информацию, отсеиваем неподходящие вакансии (которые не смогли отсеять через API) 
# ПЫСЫ: не нашел способа через get запрос получить только вакансии с ЗП в $
data = get_info(raw_data, 'USD')

with open(f'data.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)