from typing import Dict, Any

from flask import Flask, render_template, request, url_for
import local_tools
from random import sample

DATA_TEACHERS = "static/teachers.json"  # all tutors
DATA_BOOKINGS = "static/bookings.json"  # all bookings
DATA_CLIENT_REQUEST = "static/request.json"  # last request

app = Flask("__name__")

tutors = local_tools.get_teachers(DATA_TEACHERS)
goals = local_tools.get_goals()


@app.route('/')
def index(all_selected=None):
    # return "Here is a start page"
    if all_selected:  # не срабатывает
        selected_tutors = tutors
    else:
        # случайные 6 из списка
        selected_tutors = [tutors[i] for i in sample(range(len(tutors)), k=min(6, len(tutors)))]

    return render_template("index.html", goals=goals, tutors=selected_tutors)


@app.route("/goals/<goal>")
def app_goals(goal):
    # "- цели /goals/<goal>/  – здесь будет цель <goal>"
    if not goal or goal not in goals:
        goal = "travel"
    selected_tutors = [tutor for tutor in tutors if goal in tutor["goals"]]

    return render_template("goal.html", goal=goal, goals=goals, tutors=selected_tutors)


@app.route("/profiles")
def tutor_profile_0():
    return tutor_profile(0)


@app.route("/profiles/<int:tutor_id>")
def tutor_profile(tutor_id):
    # return " - профиля учителя /profiles/<id учителя>/ – здесь будет преподаватель <id учителя>"

    # TODO: надо найти объект по коду id  а не по номеру в списке:
    if (0 > tutor_id) or (tutor_id > len(tutors)):
        tutor_id = 0
    tutor = tutors[tutor_id]
    time_table = dict()
    time_table["days_of_week"] = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    time_table["time_slots"] = ["8:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
    time_table["name_of_days"] = local_tools.get_rus_name_day_of_week('all')
    time_table["open_days"] = {day: any(list(tutor["free"][day].values())) for day in time_table["days_of_week"]}
    return render_template("profile.html", tutor=tutor, goals=goals, time_table=time_table)


@app.route("/request")
def form_request_all():
    # TODO: как обойти этот редирект?
    return form_request('')


@app.route("/request/<goal>")
def form_request(goal):
    # return "- заявки на подбор /request/ – здесь будет заявка на подбор"
    if not goal:
        goal = "travel"
    return render_template("request.html", primary_goal=goal, goals=goals)


@app.route("/request_done", methods=["GET", "POST"])
def form_request_done():
    # "- принятой заявки на подбор /request_done/ – заявка на подбор отправлена"
    client_request_for_tutor = {"goal": request.form.get("goal"),
                                "time": request.form.get("time"),
                                "client_name": request.form.get("client_name"),
                                "client_phone": request.form.get("client_phone")}

    local_tools.save_cli_request(DATA_CLIENT_REQUEST, client_request_for_tutor)
    return render_template("request_done.html", goals=goals, cli_req=client_request_for_tutor)


@app.route("/booking/<int:tutor_id>/<day_of_week>/<time_slot>", methods=["GET", "POST"])
# @app.route("/booking", methods=["GET","POST"])
def form_tutor_booking(tutor_id, day_of_week, time_slot):
    # "- формы бронирования /booking/<id учителя>/ – здесь будет форма бронирования <id учителя>"
    slot_info: Dict[str, Any] = {
        "day_of_week": day_of_week, "day_rus_name": local_tools.get_rus_name_day_of_week(day_of_week), \
        "time_slot": time_slot
    }
    return render_template("booking.html", tutor=tutors[tutor_id], slot_info=slot_info)


@app.route("/booking_done", methods=["GET", "POST"])
def form_tutor_booking_done():
    # "- принятой заявки на подбор /booking_done/   – заявка отправлена"
    booking = {"tutor_id": request.form.get("tutor_id")}
    booking["day_of_week"] = request.form.get("day_of_week")
    booking["time_slot"] = request.form.get("time_slot")
    booking["client_name"] = request.form.get("client_name")
    booking["client_phone"] = request.form.get("client_phone")

    slot_info = {"day_of_week": request.form.get("day_of_week"), \
                 "day_rus_name": local_tools.get_rus_name_day_of_week(request.form.get("day_of_week")), \
                 "time_slot": request.form.get("time_slot")}
    response = request.form
    bookings = local_tools.get_bookings(DATA_BOOKINGS)
    bookings.append(booking)
    local_tools.save_bookings(DATA_BOOKINGS, bookings)
    # убрать время у препода
    tutors[int(booking["tutor_id"])]["free"][booking["day_of_week"]][booking["time_slot"]] = False
    # flash("Заявка успешно сохранена")
    return render_template("booking_done.html", booking=booking, slot_info=slot_info)


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(debug=False)
