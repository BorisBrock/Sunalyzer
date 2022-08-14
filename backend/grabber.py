import time
import importlib
from os.path import exists
from datetime import date, datetime

# Project imports
from config import Config
from database import Database
import version

# pylint: disable=C0103


# Real time (24h) data
NUM_REAL_TIME_VALUES = 24*60  # 24h * 60 Minutes
has_real_time_data = False
real_time_seconds_counter = 0
last_real_time_produced = 0.0
last_real_time_consumed = 0.0
last_real_time_fed_in = 0.0
config = None


# Helper function to insert new values into the DB
def insert_historical_values(
        db,
        table_name,
        date_string,
        produced,
        consumed,
        fed_in):
    '''Helper function to insert new values into the DB.'''
    query = f"SELECT * FROM {table_name} WHERE date='{date_string}'"
    rows = db.execute(query)

    if len(rows) == 0:
        # Create day row
        query = (f"INSERT INTO {table_name} VALUES ('{date_string}',"
                 f"{str(produced)}, {str(produced)}, "
                 f"{str(consumed)}, {str(consumed)}, "
                 f"{str(fed_in)}, {str(fed_in)})")
        db.execute(query)
    else:
        # Update existing row
        query = (f"UPDATE {table_name} SET "
                 f"produced_b = {str(produced)}, "
                 f"consumed_b = {str(consumed)}, "
                 f"fed_in_b = {str(fed_in)} WHERE date='{date_string}'")
        db.execute(query)


# Helper function to insert current values into the DB
def insert_current_values(db, produced, consumed, fed_in):
    '''Helper function to insert current values into the DB.'''
    rows = db.execute("SELECT * FROM current WHERE date='cur'")

    if len(rows) == 0:
        # Create day row
        query = (f"INSERT INTO current VALUES ('cur', "
                 f"{str(produced)}, {str(consumed)}, {str(fed_in)})")
        db.execute(query)
    else:
        # Update existing row
        query = (f"UPDATE current SET "
                 f"produced = {str(produced)}, "
                 f"consumed = {str(consumed)}, "
                 f"fed_in = {str(fed_in)} "
                 f"WHERE date='cur'")
        db.execute(query)


# Helper function to insert new values into the DB
def insert_real_time_values(db, time_string2, produced, consumed, fed_in):
    '''Helper function to insert new values into the DB.'''
    # Insert new data
    query = (f"INSERT INTO real_time (time, produced, consumed, fed_in) "
             f"VALUES('{time_string2}', {produced}, {consumed}, {fed_in})")
    db.execute(query)
    # Limit data
    query = (f"DELETE FROM real_time WHERE ID IN ("
             f"SELECT ID FROM real_time "
             f"ORDER BY ID DESC "
             f"LIMIT -1 OFFSET {NUM_REAL_TIME_VALUES})")
    db.execute(query)


# Helper function to create a new DB
def create_new_db():
    '''Helper function to create a new DB.'''
    new_db = Database("data/db.sqlite")

    # Historical data tables
    table_names = ["days", "weeks", "months", "years", "all_time"]
    for name in table_names:
        query = (f"create table if not exists {name} ("
                 "date STRING PRIMARY KEY,"
                 "produced_a REAL, produced_b REAL,"
                 "consumed_a REAL, consumed_b REAL,"
                 "fed_in_a REAL, fed_in_b REAL)")
        new_db.execute(query)

    # Current data table
    query = ("create table if not exists current"
             "(date STRING PRIMARY KEY, "
             "produced REAL, consumed REAL, fed_in REAL)")
    new_db.execute(query)

    # Real time data table
    query = ("create table if not exists real_time"
             "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
             "time STRING, produced REAL, consumed REAL, fed_in REAL)")
    new_db.execute(query)
    # Insert null data
    for x in range(NUM_REAL_TIME_VALUES):  # 24h * 60 minutes
        query = (f"INSERT INTO real_time VALUES"
                 f"('{str(x)}', '...', '0.0', '0.0', '0.0')")
        new_db.execute(query)


# Loads the device class with the given name
def load_devie_plugin(device_name):
    '''Loads the device class with the given name.'''
    module = importlib.import_module("devices." + device_name)
    class_ = getattr(module, device_name)
    device = class_(config)
    return device


# Main loop
def main():
    '''Main loop.'''
    global has_real_time_data
    global real_time_seconds_counter
    global last_real_time_produced
    global last_real_time_consumed
    global last_real_time_fed_in
    global config

    # Print version
    print(f"Starting Sunalyzer grabber version {version.get_version()}")

    # Read the configuration from disk
    try:
        print("Grabber: Reading backend configuration from config.yml")
        config = Config("data/config.yml")
    except Exception:
        exit()

    # Dynamically load the device
    try:
        device_name = config.config_data['grabber']['device']
        print(f"Grabber: Loading device adapter '{device_name}'")
        device = load_devie_plugin(device_name)
    except Exception:
        print("Grabber: Error: creating the device adapter failed")
        exit()

    # Prepare the data base
    print("Grabber: Checking if data base exists")
    if not exists("data/db.sqlite"):
        print("Grabber: Data base does not exist. Creating new one")
        create_new_db()

    # Grabber main loop
    print("Grabber: Entering main loop")
    while True:
        if config.verbose_logging:
            print("Grabber: Updating device data")

        # Download new data from the actual PV device
        device.update()

        # Open connection to data base
        db = Database("data/db.sqlite")

        # Time strings
        year_string = date.today().strftime("%Y")
        week_string = year_string + "-" + date.today().strftime("%V")
        month_string = year_string + "-" + date.today().strftime("%m")

        # Capture daily data
        day_string = str(date.today())
        insert_historical_values(
            db,
            "days",
            day_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture weekly data
        insert_historical_values(
            db,
            "weeks",
            week_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture monthly data
        insert_historical_values(
            db,
            "months", month_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture yearly data
        insert_historical_values(
            db,
            "years",
            year_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture all time data
        insert_historical_values(
            db,
            "all_time",
            "all_time",
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Also store the current values
        insert_current_values(
            db,
            device.current_power_produced_kw,
            device.current_power_consumed_kw,
            device.current_power_fed_in_kw)

        # Also store the real time data
        real_time_seconds_counter = real_time_seconds_counter - \
            config.config_data['grabber']['interval_s']
        if real_time_seconds_counter <= 0:
            if has_real_time_data:
                # Compute deltas
                d_produced = device.total_energy_produced_kwh - last_real_time_produced
                d_consumed = device.total_energy_consumed_kwh - last_real_time_consumed
                d_fed_in = device.total_energy_fed_in_kwh - last_real_time_fed_in
                # Update values
                last_real_time_produced = device.total_energy_produced_kwh
                last_real_time_consumed = device.total_energy_consumed_kwh
                last_real_time_fed_in = device.total_energy_fed_in_kwh
                # Time string
                time_string = datetime.now().strftime("%H:%M")
                # Store in data base
                if config.verbose_logging:
                    print((f"Grabber: capturing real time data({time_string}:"
                           f"{d_produced}, {d_consumed}, {d_fed_in})"))
                insert_real_time_values(
                    db,
                    time_string,
                    d_produced,
                    d_consumed,
                    d_fed_in)
            else:
                # One time initialization
                last_real_time_produced = device.total_energy_produced_kwh
                last_real_time_consumed = device.total_energy_consumed_kwh
                last_real_time_fed_in = device.total_energy_fed_in_kwh

            has_real_time_data = True
            real_time_seconds_counter = 60  # Reset counter to one minute

        time.sleep(config.config_data['grabber']['interval_s'])


# Main entry point of the application
if __name__ == "__main__":
    main()
