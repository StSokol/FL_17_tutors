import json
import os.path
import data


def create_json_data(file_name):
    with open(file_name, "w") as f:
        json.dump(data.teachers, f)


def get_teachers(file_name):
    if not os.path.isfile(file_name):
        create_json_data(file_name)

    with open(file_name) as f:
        teachers = json.load(f)
    return teachers


def get_goals_old():
    return data.goals

def get_goals():
    goals = {"travel": {"route":"travel", "rus_name":"Для путешествий", "sign":"⛱"},
             "study": {"route":"study", "rus_name":"Для учебы", "sign":"🏫"},
             "work": {"route":"work", "rus_name":"Для работы",  "sign":"🏢"},
             "relocate": {"route":"relocate", "rus_name":"Для переезда",  "sign":"🚜"}}
    return goals


def get_rus_name_day_of_week(day_of_week):
    set_day = {"mon":"Понедельник","tue":"Вторник","wed":"Среда","thu":"Четверг",\
                "fri":"Пятница","sat":"Суббота","sun":"Воскресенье"}
    if day_of_week == 'all':
        return set_day
    elif day_of_week in set_day:
        return set_day[day_of_week]
    return ""


def get_bookings(file_name):
    if not os.path.isfile(file_name):
        with open(file_name, "w") as f:
            json.dump([], f)

    with open(file_name) as f:
        bookings = json.load(f)
    return bookings


def save_bookings(file_name, bookings):
    # сохранить bookings
    with open(file_name, "w") as f:
        json.dump(bookings, f)


def save_cli_request(file_name, client_request_for_tutor):
    # сохранить bookings
    with open(file_name, "w") as f:
        json.dump(client_request_for_tutor, f)