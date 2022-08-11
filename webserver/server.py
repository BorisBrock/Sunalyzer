import json
import sqlite3
import yaml
from datetime import date
import traceback
from flask import Flask, request, send_from_directory


# Main Flask web server application
app = Flask(__name__)


@app.route('/')
# Serves the index.html
def get_index():
    '''Todo: add documentation.'''
    return send_from_directory("../site", "index.html")


@app.route('/<path:path>')
# Serves all other static files
def get_file(path):
    '''Todo: add documentation.'''
    return send_from_directory("../site", path)


def get_json_data_current():
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    # Current
    cur.execute("SELECT * FROM current")
    rows_cur = cur.fetchall()
    # All time
    cur.execute("SELECT * FROM all_time")
    rows_all = cur.fetchall()
    # Today
    day_string = str(date.today())
    cur.execute(f"SELECT * FROM days WHERE date='{day_string}'")
    rows_today = cur.fetchall()
    # Done
    con.commit()
    con.close()
    # Compute earnings
    price = float(config['prices']['price_per_grid_kwh'])
    revenue = float(config['prices']['revenue_per_fed_in_kwh'])
    earned_total = rows_all[0][6] * revenue
    saved_total = (rows_all[0][2] - rows_all[0][6]) * (price - revenue)
    earned_today = rows_today[0][6] * revenue
    saved_today = (rows_today[0][2] - rows_today[0][6]) * (price - revenue)
    # Build response data
    data = {
        "state": "ok",
        "currently_produced_kw": rows_cur[0][1],
        "currently_consumed_kw": rows_cur[0][2],
        "currently_fed_in_kw": rows_cur[0][3],
        "all_time_produced_kwh": rows_all[0][2],
        "all_time_consumed_kwh": rows_all[0][4],
        "all_time_fed_in_kwh": rows_all[0][6],
        "all_time_earned": (earned_total + saved_total),
        "today_produced_kwh": rows_today[0][2],
        "today_consumed_kwh": rows_today[0][4],
        "today_fed_in_kwh": rows_today[0][6],
        "today_earned": (earned_today + saved_today)
    }
    return json.dumps(data)


def get_json_data_dates():
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT min(date) FROM years")
    rows = cur.fetchall()
    con.commit()
    con.close()
    data = {
        "state": "ok",
        "year_min": rows[0][0],
        "year_max": int(date.today().strftime("%Y")),
    }
    return json.dumps(data)


def get_json_data_days_in_month(year_and_month):
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM days WHERE date LIKE '{year_and_month}%'")
    rows = cur.fetchall()
    con.commit()
    con.close()
    # Build results
    data = []
    for row in rows:
        data.append({
            "date": row[0],
            "produced": row[2] - row[1],
            "consumed": row[4] - row[3],
            "fed_in": row[6] - row[5]
            })
    return json.dumps(data)


def get_json_data_months_in_year(year):
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM months WHERE date LIKE '{year}%'")
    rows = cur.fetchall()
    con.commit()
    con.close()
    # Build results
    data = []
    for row in rows:
        data.append({
            "date": row[0],
            "produced": row[2] - row[1],
            "consumed": row[4] - row[3],
            "fed_in": row[6] - row[5]
            })
    return json.dumps(data)


def get_json_data_real_time():
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM real_time")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps(rows)


def get_json_data_history(table, search_date):
    '''Todo: add documentation.'''
    con = sqlite3.connect("../data/db.sqlite")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE date='{search_date}'")
    rows = cur.fetchall()
    con.commit()
    con.close()
    # Compute feed in
    consumed_self = rows[0][2] - rows[0][6]
    consumed_grid = rows[0][4] - consumed_self
    consumed_total = consumed_self + consumed_grid
    consumed_self_rel = (consumed_self / consumed_total) * 100.0
    consumed_grid_rel = (consumed_grid / consumed_total) * 100.0
    # Compute usage
    usage_fed_in_rel = rows[0][6] / rows[0][2] * 100.0
    usage_self_consumed_rel = consumed_self / rows[0][2] * 100.0
    # Compute earnings
    price = float(config['prices']['price_per_grid_kwh'])
    revenue = float(config['prices']['revenue_per_fed_in_kwh'])
    earned = rows[0][6] * revenue
    saved = (rows[0][2] - rows[0][6]) * (price - revenue)
    # Build response data
    data = {
        "state": "ok",
        "produced_kwh": rows[0][2],
        "consumed_total_kwh": rows[0][4],
        "consumed_from_pv_kwh": consumed_self,
        "consumed_from_grid_kwh": consumed_grid,
        "consumed_from_pv_percent": consumed_self_rel,
        "consumed_from_grid_percent": consumed_grid_rel,
        "usage_fed_in_kwh": rows[0][6],
        "usage_self_consumed_kwh": consumed_self,
        "usage_fed_in_percent": usage_fed_in_rel,
        "usage_self_consumed_percent": usage_self_consumed_rel,
        "earned_feedin": earned,
        "earned_savings": saved,
        "earned_total": (earned+saved),
    }
    return json.dumps(data)


# .../query?type=current
# .../query?type=dates
# .../query?type=historical&table=days&date=2022-08-03
@app.route("/query", methods=['GET'])
def handle_request():
    '''Todo: add documentation.'''
    try:
        _type = request.args['type']
        if _type == "current":
            print("Server: REST request for current data received")
            data = get_json_data_current()
            return data
        elif _type == "dates":
            print("Server: REST request for current dates")
            data = get_json_data_dates()
            return data
        elif _type == "historical":
            table = request.args['table']
            _date = request.args['date']
            print(
                f"Server: REST request for historical data received. Table: {table}, date: {_date}")
            data = get_json_data_history(table, _date)
            return data
        elif _type == "real_time":
            print("Server: REST request for real time data")
            data = get_json_data_real_time()
            return data
        elif _type == "days_in_month":
            print("Server: REST request for days in month")
            _month = request.args['date']
            data = get_json_data_days_in_month(_month)
            return data
        elif _type == "months_in_year":
            print("Server: REST request for months in year")
            _year = request.args['date']
            data = get_json_data_months_in_year(_year)
            return data
    except Exception:
        print(traceback.print_exc())
        data = {"state": "error"}
        return json.dumps(data)


# Main loop
def main():
    '''Todo: add documentation.'''

    # Read the configuration from disk
    try:
        print("Server: Reading backend configuration from config.yaml")
        with open("data/config.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except Exception:
        print("Server: Error: opening the configuration file failed")
        exit()

    # Start the web server
    if __name__ == '__main__':
        app.run(host=config['server']['ip'], port=config['server']['port'])


# Main entry point of the application
if __name__=="__main__":
    main()
