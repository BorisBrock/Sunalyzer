import os
import time
import importlib
import signal
from os.path import exists
from datetime import date, datetime
import traceback

# Project imports
from config import Config
from database import Database
import version


# Real time (24h) data
NUM_REAL_TIME_VALUES = 24*60  # 24h * 60 Minutes
real_time_seconds_counter = 0
config = None
run = True


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
        # Create new row
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
def insert_current_values(
        db,
        produced,
        consumed_grid,
        consumed_pv,
        consumed_total,
        fed_in):
    '''Helper function to insert current values into the DB.'''
    rows = db.execute("SELECT * FROM current WHERE date='cur'")

    if len(rows) == 0:
        # Create day row
        query = (f"INSERT INTO current VALUES ('cur', "
                 f"{str(produced)}, {str(consumed_grid)}, "
                 f"{str(consumed_pv)}, {str(consumed_total)}, "
                 f"{str(fed_in)})")
        db.execute(query)
    else:
        # Update existing row
        query = (f"UPDATE current SET "
                 f"produced = {str(produced)}, "
                 f"consumed_grid = {str(consumed_grid)}, "
                 f"consumed_pv = {str(consumed_pv)}, "
                 f"consumed_total = {str(consumed_total)}, "
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
    table_names = ["days", "months", "years", "all_time"]
    for name in table_names:
        query = (f"create table if not exists {name} ("
                 "date STRING PRIMARY KEY,"
                 "produced_a REAL, produced_b REAL,"
                 "consumed_a REAL, consumed_b REAL,"
                 "fed_in_a REAL, fed_in_b REAL)")
        new_db.execute(query)

    # Add initial all time row
    query = ("INSERT INTO all_time VALUES ('all_time',0,0,0,0,0,0)")
    new_db.execute(query)

    # Current data table
    query = ("create table if not exists current"
             "(date STRING PRIMARY KEY, "
             "produced REAL, consumed_grid REAL, consumed_pv REAL, consumed_total REAL, fed_in REAL)")
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
def load_device_plugin(device_name):
    '''Loads the device class with the given name.'''
    module = importlib.import_module("devices." + device_name)
    class_ = getattr(module, device_name)
    device = class_(config)
    return device


# Sets the time zone environment variable
def set_time_zone(tz):
    '''Sets the time zone environment variable.'''
    if tz is None:
        print("Grabber: Warning: No time zone set")
    else:
        print(f"Grabber: Setting tme zone to {tz}")
        os.environ['TZ'] = tz
        time.tzset()
        print(f"Grabber: Time is now {time.strftime('%X %x %Z')}")


# Updates data in the data base
def update_data(device):
    '''Updates data in the data base.'''
    global real_time_seconds_counter

    # Download new data from the actual PV device
    device.update()

    # Open connection to data base
    db = Database("data/db.sqlite")

    # Time strings
    year_string = date.today().strftime("%Y")
    month_string = year_string + "-" + date.today().strftime("%m")
    day_string = month_string + "-" + date.today().strftime("%d")

    # Capture daily data
    insert_historical_values(
        db,
        "days",
        day_string,
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
        device.current_power_consumed_from_grid_kw,
        device.current_power_consumed_from_pv_kw,
        device.current_power_consumed_total_kw,
        device.current_power_fed_in_kw)

    # Also store the real time data
    real_time_seconds_counter = real_time_seconds_counter - \
        config.config_data['grabber']['interval_s']
    if real_time_seconds_counter <= 0:
        # Time string
        time_string = datetime.now().strftime("%H:%M")
        # Store in data base
        if config.verbose_logging:
            print((f"Grabber: capturing real time data({time_string}:"
                   f"{device.current_power_produced_kw}, "
                   f"{device.current_power_consumed_total_kw}, "
                   f"{device.current_power_fed_in_kw})"))

        insert_real_time_values(
            db,
            time_string,
            device.current_power_produced_kw,
            device.current_power_consumed_total_kw,
            device.current_power_fed_in_kw)

        real_time_seconds_counter = 60  # Reset counter to one minute


# This is called when SIGTERM is received
def handler_stop_signals(signum, frame):
    global run
    print("Grabber: SIGTERM/SIGINT received")
    run = False


# Main loop
def main():
    '''Main loop.'''
    global config
    global run

    # Set up signal handlers
    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    # Print version
    print(f"Starting Sunalyzer grabber version {version.get_version()}")

    # Read the configuration from disk
    try:
        print("Grabber: Reading backend configuration from config.yml")
        config = Config("data/config.yml")
    except Exception:
        exit()

    # Set time zone
    set_time_zone(config.config_data.get("time_zone"))

    # Dynamically load the device
    try:
        device_name = config.config_data['device']['type']
        print(f"Grabber: Loading device adapter '{device_name}'")
        device = load_device_plugin(device_name)
    except Exception:
        print("Grabber: Error: creating the device adapter failed")
        print(traceback.print_exc())
        exit()

    # Prepare the data base
    print("Grabber: Checking if data base exists")
    if not exists("data/db.sqlite"):
        print("Grabber: Data base does not exist. Creating new one")
        create_new_db()

    # Grabber main loop
    print("Grabber: Entering main loop")
    while run:
        if config.verbose_logging:
            time_string = datetime.now().strftime("%H:%M")
            print(f"Grabber: {time_string}: Updating device data")

        try:
            update_data(device)
        except Exception:
            print("Grabber: Error: updating data from device failed")
            print(traceback.print_exc())

        time.sleep(config.config_data['grabber']['interval_s'])

    # Exit
    print("Grabber: Exiting main loop")
    print("Grabber: Shutting down gracefully")


# Main entry point of the application
if __name__ == "__main__":
    main()
