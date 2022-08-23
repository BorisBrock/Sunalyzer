import json
from datetime import date
import traceback
from flask import Flask, request, send_from_directory, make_response

# Project imports
from config import Config
from database import Database
import version


# Globals
config = None


# Main Flask web server application
app = Flask(__name__)


@app.route('/')
# Serves the index.html
def get_index():
    '''Serves the index.html.'''
    return send_from_directory("../site", "index.html")


@app.route('/<path:path>')
# Serves all other static files
def get_file(path):
    '''Serves all other static files.'''
    return send_from_directory("../site", path)


@app.route('/csv')
# Returns a .csv export from the database
def get_csv():
    '''Returns a .csv export from the database.'''
    csv = "Fooooo"
    response = make_response(csv)
    cd = "attachment; filename=fooo.csv"
    response.headers["Content-Disposition"] = cd
    response.mimetype = "text/csv"
    return response


# Returns JSON response containing current data
def get_json_data_current():
    '''Returns JSON response containing current data'''
    db = Database("data/db.sqlite")
    # Current
    rows_cur = db.execute("SELECT * FROM current")
    # All time
    rows_all = db.execute("SELECT * FROM all_time")
    produced_total = rows_all[0][2] - rows_all[0][1]
    consumed_total = rows_all[0][4] - rows_all[0][3]
    fed_in_total = rows_all[0][6] - rows_all[0][5]
    # Today
    day_string = str(date.today())
    rows_today = db.execute(f"SELECT * FROM days WHERE date='{day_string}'")
    produced_today = rows_today[0][2] - rows_today[0][1]
    consumed_today = rows_today[0][4] - rows_today[0][3]
    fed_in_today = rows_today[0][6] - rows_today[0][5]
    # Compute earnings
    price = float(config.config_data['prices']['price_per_grid_kwh'])
    revenue = float(config.config_data['prices']['revenue_per_fed_in_kwh'])
    earned_total = fed_in_total * revenue
    saved_total = (produced_total - fed_in_total) * (price - revenue)
    earned_today = fed_in_today * revenue
    saved_today = (produced_today - fed_in_today) * (price - revenue)
    # Build response data
    data = {
        "state": "ok",
        "currently_produced_kw": rows_cur[0][1],
        "currently_consumed_kw": rows_cur[0][2],
        "currently_fed_in_kw": rows_cur[0][3],
        "all_time_produced_kwh": produced_total,
        "all_time_consumed_kwh": consumed_total,
        "all_time_fed_in_kwh": fed_in_total,
        "all_time_earned": (earned_total + saved_total),
        "today_produced_kwh": produced_today,
        "today_consumed_kwh": consumed_today,
        "today_fed_in_kwh": fed_in_today,
        "today_earned": (earned_today + saved_today)
    }
    return json.dumps(data)


# Returns JSON response containing available years
def get_json_data_dates():
    '''Returns JSON response containing available years.'''
    db = Database("data/db.sqlite")
    rows = db.execute("SELECT min(date) FROM years")
    data = {
        "state": "ok",
        "year_min": rows[0][0],
        "year_max": int(date.today().strftime("%Y")),
    }
    return json.dumps(data)


# Returns JSON response containing history details
def get_json_data_history_details(table, date_search_string):
    '''Returns JSON response containing history details.'''
    db = Database("data/db.sqlite")
    if len(date_search_string) > 0:
        rows = db.execute(
            f"SELECT * FROM {table} WHERE date LIKE '{date_search_string}%'")
    else:
        rows = db.execute(
            f"SELECT * FROM {table}")
    # Build results
    data = []
    for row in rows:
        produced = row[2] - row[1]
        consumed = row[4] - row[3]
        fed_in = row[6] - row[5]
        data.append({
            "date": row[0],
            "produced_self": produced - fed_in,
            "produced_feed_in": fed_in,
            "consumed_from_pv": produced - fed_in,
            "consumed_from_grid": consumed - produced + fed_in
        })
    return json.dumps(data)


# Returns JSON response containing monthly data for a year
def get_json_data_real_time():
    '''Returns JSON response containing monthly data for a year.'''
    db = Database("data/db.sqlite")
    rows = db.execute("SELECT * FROM real_time")
    return json.dumps(rows)


# Returns JSON response containing historical data
def get_json_data_history(table, search_date):
    '''Returns JSON response containing historical data.'''
    db = Database("data/db.sqlite")
    rows = db.execute(f"SELECT * FROM {table} WHERE date='{search_date}'")
    # Compute data from sqlite columns
    produced = rows[0][2] - rows[0][1]
    consumed = rows[0][4] - rows[0][3]
    fed_in = rows[0][6] - rows[0][5]
    # Compute feed in
    consumed_self = produced - fed_in
    consumed_grid = consumed - consumed_self
    consumed_total = consumed_self + consumed_grid

    if consumed_total > 0:
        consumed_self_rel = (consumed_self / consumed_total) * 100.0
        consumed_grid_rel = (consumed_grid / consumed_total) * 100.0
    else:
        consumed_self_rel = 100.0
        consumed_grid_rel = 0.0

    # Compute usage
    if produced > 0:
        usage_fed_in_rel = fed_in / produced * 100.0
        usage_self_consumed_rel = consumed_self / produced * 100.0
    else:
        usage_fed_in_rel = 0.0
        usage_self_consumed_rel = 100.0

    # Compute earnings
    price = float(config.config_data['prices']['price_per_grid_kwh'])
    revenue = float(config.config_data['prices']['revenue_per_fed_in_kwh'])
    earned = fed_in * revenue
    saved = consumed_self * (price - revenue)
    # Build response data
    data = {
        "state": "ok",
        "produced_kwh": produced,
        "consumed_total_kwh": consumed,
        "consumed_from_pv_kwh": consumed_self,
        "consumed_from_grid_kwh": consumed_grid,
        "consumed_from_pv_percent": consumed_self_rel,
        "consumed_from_grid_percent": consumed_grid_rel,
        "usage_fed_in_kwh": fed_in,
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
# etc.
@app.route("/query", methods=['GET'])
def handle_request():
    '''Answers all query requests.'''
    try:
        _type = request.args['type']
        if config.verbose_logging:
            print(f"Server: REST request of type '{_type}' received")

        if _type == "current":
            data = get_json_data_current()
            return data
        elif _type == "dates":
            data = get_json_data_dates()
            return data
        elif _type == "historical":
            table = request.args['table']
            _date = request.args['date']
            if config.verbose_logging:
                print(f"  Request details: table: '{table}', date: {_date}")
            data = get_json_data_history(table, _date)
            return data
        elif _type == "real_time":
            data = get_json_data_real_time()
            return data
        elif _type == "days_in_month":
            _month = request.args['date']
            data = get_json_data_history_details("days", _month)
            return data
        elif _type == "months_in_year":
            _year = request.args['date']
            data = get_json_data_history_details("months", _year)
            return data
        elif _type == "years_in_all_time":
            data = get_json_data_history_details("years", "")
            return data

    except Exception:
        print("Server: Error:")
        print(traceback.print_exc())
        data = {"state": "error"}
        return json.dumps(data)


# Main loop
def main():
    '''Main loop.'''

    global config

    # Print version
    print(f"Starting Sunalyzer grabber version {version.get_version()}")

    # Read the configuration from disk
    try:
        print("Grabber: Reading backend configuration from config.yml")
        config = Config("data/config.yml")
    except Exception:
        exit()

    # Start the web server
    if __name__ == '__main__':
        app.run(
            host=config.config_data['server']['ip'],
            port=config.config_data['server']['port'])


# Main entry point of the application
if __name__ == "__main__":
    main()
