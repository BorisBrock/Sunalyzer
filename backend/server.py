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


# Converts the given rows to a CSV string
def rows_to_csv(rows):
    '''Converts the given rows to a CSV string.'''
    # Header
    csv = "date;production;consumption;feed_in\n"
    # Data
    for row in rows:
        csv += row[0]  # Date
        csv += ";"
        csv += str(row[2] - row[1])  # Production
        csv += ";"
        csv += str(row[4] - row[3])  # Consumption
        csv += ";"
        csv += str(row[6] - row[5])  # Feed-in
        csv += "\n"
    return csv


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
    try:
        # Gather parameters
        _table = request.args['table']
        _date = request.args.get('date', "")

        # Gather CSV contents
        rows = None
        db = Database("data/db.sqlite")

        # Build and execute query
        query = f"SELECT * FROM {_table}"
        if len(_date) > 0:
            query += f" WHERE date LIKE '{_date}%'"
        rows = db.execute(query)

        # Build file name
        file_name = (
            f"Sunalyzer_{_date}.csv" if len(_date) > 0
            else "Sunalyzer_All.csv")

        # Convert rows to CSV
        csv = rows_to_csv(rows)

        # Build HTML response
        response = make_response(csv)
        cd = f"attachment; filename={file_name}"
        response.headers["Content-Disposition"] = cd
        response.mimetype = "text/csv"
        return response

    except Exception:
        exception_string = traceback.print_exc()
        print("Server: Bad CSV request:")
        print(exception_string)
        data = {"state": "error", "message": exception_string}
        return json.dumps(data), 404


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
        "currently_produced_w": rows_cur[0][1] * 1000.0,  # kW -> W
        "currently_consumed_grid_w": rows_cur[0][2] * 1000.0,  # kW -> W
        "currently_consumed_pv_w": rows_cur[0][3] * 1000.0,  # kW -> W
        "currently_consumed_total_w": rows_cur[0][4] * 1000.0,  # kW -> W
        "currently_fed_in_w": rows_cur[0][5] * 1000.0,  # kW -> W
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
def get_json_data_statistics():
    '''Returns JSON response containing inverter statistics.'''
    # Date based data
    start_date = config.config_data['device']['start_date']
    num_days = (date.today() - start_date).days
    # Averages
    db = Database("data/db.sqlite")
    rows_all_time = db.execute("SELECT * FROM all_time")
    total_production_kwh = rows_all_time[0][2]
    average_production_kwhpd = total_production_kwh / num_days
    # Best day
    rows_best_day = db.execute(
        "SELECT date, MAX(produced_b-produced_a) AS produced_kwh FROM days")
    # Best month
    rows_best_month = db.execute(
        "SELECT date, MAX(produced_b-produced_a) AS produced_kwh FROM months")
    # Best year
    rows_best_year = db.execute(
        "SELECT date, MAX(produced_b-produced_a) AS produced_kwh FROM years")
    # Highest production
    rows_highest_prod = db.execute(
        "SELECT * FROM highscores WHERE type IS 'production'")
    # Assemble result data set
    data = {
        "state": "ok",
        "start_of_operation": str(start_date),
        "days_of_operation": num_days,
        "average_daily_production_kwh": average_production_kwhpd,
        "best_day_date": rows_best_day[0][0],
        "best_day_production_kwh": rows_best_day[0][1],
        "best_month_date": rows_best_month[0][0],
        "best_month_production_kwh": rows_best_month[0][1],
        "best_year_date": rows_best_year[0][0],
        "best_year_production_kwh": rows_best_year[0][1],
        "highest_production_w": rows_highest_prod[0][2] * 1000.0,
        "highest_production_date": rows_highest_prod[0][1],
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
def get_json_data_real_time(hours):
    '''Returns JSON response containing monthly data for a year.'''
    num_results = int(hours) * 60
    db = Database("data/db.sqlite")
    rows = db.execute(f"SELECT * FROM real_time "
                      f"ORDER BY ID DESC LIMIT {num_results}")
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

    # High resolution data (only for days)
    daily_high_res_data = ""
    if table == "days":
        rows = db.execute(f"SELECT * FROM high_res WHERE date='{search_date}'")
        if rows:
            hrdata = rows[0][1]
            if hrdata[-1] == ',':
                hrdata = hrdata[:-1]
            daily_high_res_data = "[" + hrdata + "]"

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
        "autarky": consumed_self_rel,
        "high_res": daily_high_res_data
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
            hours = request.args['h']
            data = get_json_data_real_time(hours)
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
        elif _type == "statistics":
            data = get_json_data_statistics()
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
        print("Server: Reading backend configuration from config.yml")
        config = Config("data/config.yml")
    except Exception:
        exit()

    # Start the web server
    app.run(
        host=config.config_data['server']['ip'],
        port=config.config_data['server']['port'])

    # Exit
    print("Server: Exiting main loop")
    print("Server: Shutting down gracefully")


# Main entry point of the application
if __name__ == "__main__":
    main()
