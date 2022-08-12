import time
import importlib
from os.path import exists
from datetime import date, datetime

# Project imports
from config import Config
from database import Database

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
        query = f"""INSERT INTO {table_name} VALUES ('{date_string}',
        {str(produced)}, {str(produced)}, {str(consumed)}, {str(consumed)},
        {str(fed_in)}, {str(fed_in)})"""
        db.execute(query)
    else:
        # Update existing row
        db.execute(
            f"""UPDATE {table_name} SET
            produced_b = {str(produced)}, consumed_b = {str(consumed)},
            fed_in_b = {str(fed_in)} WHERE date='{date_string}'""")


# Helper function to insert current values into the DB
def insert_current_values(db, produced, consumed, fed_in):
    '''Helper function to insert current values into the DB.'''
    rows = db.execute("SELECT * FROM current WHERE date='cur'")

    if len(rows) == 0:
        # Create day row
        query = f"""INSERT INTO current VALUES ('cur',
        {str(produced)}, {str(consumed)}, {str(fed_in)})"""
        db.execute(query)
    else:
        # Update existing row
        db.execute(
            f"""UPDATE current SET produced = {str(produced)},
            consumed = {str(consumed)}, fed_in = {str(fed_in)} WHERE date='cur'""")


# Helper function to insert new values into the DB
def insert_real_time_values(db, time_string2, produced, consumed, fed_in):
    '''Helper function to insert new values into the DB.'''
    # Insert new data
    query = f"""INSERT INTO real_time (time, produced, consumed, fed_in) VALUES
        ('{time_string2}', {produced}, {consumed}, {fed_in})"""
    db.execute(query)
    # Limit data
    query = f"""DELETE FROM real_time WHERE ID IN (
        SELECT ID FROM real_time
        ORDER BY ID DESC
        LIMIT -1 OFFSET {NUM_REAL_TIME_VALUES})"""
    db.execute(query)


# Helper function to create a new DB
def create_new_db():
    '''Helper function to create a new DB.'''
    new_db = Database("data/db.sqlite")

    # Historical data tables
    table_names = ["days", "weeks", "months", "years", "all_time"]
    for name in table_names:
        new_db.execute(f"""create table if not exists {name} (
            date STRING PRIMARY KEY,
            produced_a REAL, produced_b REAL,
            consumed_a REAL, consumed_b REAL,
            fed_in_a REAL, fed_in_b REAL)""")

    # Current data table
    new_db.execute("""create table if not exists current
                (date STRING PRIMARY KEY, produced REAL, consumed REAL, fed_in REAL)""")

    # Real time data table
    new_db.execute("""create table if not exists real_time
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                time STRING, produced REAL, consumed REAL, fed_in REAL)""")
    # Insert null data
    for x in range(NUM_REAL_TIME_VALUES):  # 24h * 60 minutes
        query = f"INSERT INTO real_time VALUES ('{str(x)}', '...', '0.0', '0.0', '0.0')"
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
        week_string = date.today().strftime("%Y") + "-" + date.today().strftime("%V")
        insert_historical_values(
            db,
            "weeks",
            week_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture monthly data
        month_string = date.today().strftime("%Y") + "-" + date.today().strftime("%m")
        insert_historical_values(
            db,
            "months", month_string,
            device.total_energy_produced_kwh,
            device.total_energy_consumed_kwh,
            device.total_energy_fed_in_kwh)

        # Capture yearly data
        year_string = date.today().strftime("%Y")
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
                    print(f"""Grabber: capturing real time data ({time_string}:
                        {d_produced}, {d_consumed}, {d_fed_in})""")
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
