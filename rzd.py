# coding=utf-8
from time import sleep

import pytest
import requests
import json

rzd_url = 'https://m.rzd.ru/timetable/public/ru?layer_id=5827'


def get_train_info(params):
    response1 = requests.post(rzd_url, params)
    params['rid'] = response1.json().get('RID')
    response2 = requests.post(rzd_url, params, cookies=response1.cookies)
    print(response2.json())
    return response2.json()


def get_free_places(response_data):
    print(response_data)
    free_places = {'Купе': 0, 'Люкс': 0, 'Плац': 0, 'Мягкий': 0}
    if response_data.get('tp') is not None:
        for cars in response_data['tp'][0]['list']:
            for car in cars['cars']:
                free_places[car['type']] += car['freeSeats']
    return free_places
