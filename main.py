# coding=utf-8
from flask import Flask
from flask import render_template
import rzd
import datetime
from datetime import timedelta

app = Flask(__name__)
app.debug = True
today = datetime.date.today()

params = {
        "tfl": "3",  # 3 - Поезда и электрички, 2 - электрички, 1 - поезда
        "actorType": "mobile_user",  # Агент, отправивший запрос
        "st0": "АДЛЕР",
        "code0": "2064150",  # Код станции прибытия
        "st1": "Москва",
        "code1": "2000000",  # Код станции отправления
        "dir": "0",  # 0 - в один конец, 1 - туда и обратно
        "checkSeats": "1"  # 1 - если остались билеты, 0 - все поезда
}



def set_search_date(addDay=False):
    global today
    if addDay is True:
        today += timedelta(days=1)
    search_start_date = today.strftime('%d.%m.%Y')
    return search_start_date


def get_trains(date):
    params['dt0'] = set_search_date()
    params['dt1'] = set_search_date()
    response = rzd.get_train_info(params)
    free_places = rzd.get_free_places(response)
    free_places['date'] = date
    return free_places


@app.route("/")
def get_today_trains(response=None):
    global today
    today = datetime.date.today()
    date = set_search_date(False)
    free_places = get_trains(date)
    print(free_places)
    return render_template('rzd.html',
                           date=free_places['date'],
                           k=free_places['Купе'],
                           l=free_places['Люкс'],
                           p=free_places['Плац'],
                           m=free_places['Мягкий']
                           )

@app.route("/next")
def get_next_day_trains(response=None):
    date = set_search_date(True)
    free_places = get_trains(date)
    return render_template('rzd.html',
                           date=free_places['date'],
                           k=free_places['Купе'],
                           l=free_places['Люкс'],
                           p=free_places['Плац'],
                           m=free_places['Мягкий']
                           )

if __name__ == "__main__":
    app.run()
