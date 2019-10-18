# coding=utf-8
import json

import rzd


class TestClass:
    def test_get_free_places(self):
        with open('response.json') as json_file:
            response_data = json.load(json_file)
        free_places = rzd.get_free_places(response_data)
        print(free_places)
        assert free_places['Купе'] == 5
        assert free_places['Люкс'] == 10
        assert free_places['Плац'] == 13
        assert free_places['Мягкий'] == 12