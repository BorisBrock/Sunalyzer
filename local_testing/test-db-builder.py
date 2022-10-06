from datetime import datetime, timedelta
import sqlite3
import math
from random import random


# Real time (24h) data
NUM_REAL_TIME_VALUES = 24*60  # 24h * 60 Minutes

global_ctr_produced = 0.0
global_ctr_consumed = 0.0
global_ctr_fed_in = 0.0


def update_counters():
    global global_ctr_produced
    global global_ctr_consumed
    global global_ctr_fed_in
    prod = random() * 10 + 1.0
    con = random() * 5 + 2.0
    fed = random() * 10 + 1.0
    if fed > prod:
        fed = prod * 0.5
    if con < prod - fed:
        con = (prod - fed) + 2.0
    global_ctr_produced += prod
    global_ctr_consumed += con
    global_ctr_fed_in += fed


# Helper function to insert new values into the DB
def insert_historical_values(
        _cursor,
        table_name,
        date_string,
        produced,
        consumed,
        fed_in):
    '''Helper function to insert new values into the DB.'''
    query = f"SELECT * FROM {table_name} WHERE date='{date_string}'"
    _cursor.execute(query)
    rows = _cursor.fetchall()

    if len(rows) == 0:
        # Create new row
        query = (f"INSERT INTO {table_name} VALUES ('{date_string}',"
                 f"{str(produced)}, {str(produced)}, "
                 f"{str(consumed)}, {str(consumed)}, "
                 f"{str(fed_in)}, {str(fed_in)})")
        _cursor.execute(query)
    else:
        # Update existing row
        query = (f"UPDATE {table_name} SET "
                 f"produced_b = {str(produced)}, "
                 f"consumed_b = {str(consumed)}, "
                 f"fed_in_b = {str(fed_in)} WHERE date='{date_string}'")
        _cursor.execute(query)


# Helper function to create a new DB
def create_new_db():
    '''Helper function to create a new DB.'''
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()

    # Historical data tables
    table_names = ["days", "months", "years", "all_time"]
    for name in table_names:
        query = (f"create table if not exists {name} ("
                 "date STRING PRIMARY KEY,"
                 "produced_a REAL, produced_b REAL,"
                 "consumed_a REAL, consumed_b REAL,"
                 "fed_in_a REAL, fed_in_b REAL)")
        cursor.execute(query)

    # Add initial all time row
    query = ("INSERT INTO all_time VALUES ('all_time',0,0,0,0,0,0)")
    cursor.execute(query)

    # Current data table
    query = ("create table if not exists current"
             "(date STRING PRIMARY KEY, "
             "produced REAL, consumed_grid REAL, "
             "consumed_pv REAL, consumed_total REAL, fed_in REAL)")
    cursor.execute(query)

    # Make sure table exists
    query = ("create table if not exists high_res "
             "(date STRING PRIMARY KEY, hrvalues STRING)")
    cursor.execute(query)

    # Real time data table
    query = ("create table if not exists real_time"
             "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
             "time STRING, produced REAL, consumed REAL, fed_in REAL)")
    cursor.execute(query)
    h = 0
    m = 0
    # Insert demo data
    for x in range(NUM_REAL_TIME_VALUES):  # 24h * 60 minutes
        p = math.sin(x*0.1) * 100.0 + 200.0
        c = 20.0 + (x % 100)
        f = random() * 100.0 + 100.0
        m = m + 1
        if m >= 60:
            m = 0
            h = h + 1
        mstr = str(m)
        if len(mstr) < 2:
            mstr = "0" + mstr
        query = (f"INSERT INTO real_time VALUES"
                 f"({str(x)}, '{str(h)}:{mstr}', '{str(p)}', '{str(c)}', '{str(f)}')")
        cursor.execute(query)

    connection.commit()
    connection.close()


def create_data(_date, _cursor, _is_a_call):
    global global_ctr_produced
    global global_ctr_consumed
    global global_ctr_fed_in

    # Time strings
    year_string = _date.strftime("%Y")
    month_string = year_string + "-" + _date.strftime("%m")
    day_string = month_string + "-" + _date.strftime("%d")

    # Capture daily data
    insert_historical_values(
        _cursor,
        "days",
        day_string,
        global_ctr_produced,
        global_ctr_consumed,
        global_ctr_fed_in)

    # Capture monthly data
    insert_historical_values(
        _cursor,
        "months", month_string,
        global_ctr_produced,
        global_ctr_consumed,
        global_ctr_fed_in)

    # Capture yearly data
    insert_historical_values(
        _cursor,
        "years",
        year_string,
        global_ctr_produced,
        global_ctr_consumed,
        global_ctr_fed_in)

    # Capture all time data
    insert_historical_values(
        _cursor,
        "all_time",
        "all_time",
        global_ctr_produced,
        global_ctr_consumed,
        global_ctr_fed_in)

    # High res data
    if _is_a_call:
        hrdata = ""
        for i in range(1440):
            prod = random() * 2 + 1
            con = random() * 0.5 + 0.1
            fed = prod - con
            m = i % 60
            h = i // 60
            tstr = str(h) + ":" + (str(m) if m > 9 else "0" + str(m))
            hrdata += f"[\"{tstr}\",{str(round(prod, 3))},{str(round(con, 3))},{str(round(fed, 3))}],"
        # Create new row
        query = (f"INSERT INTO high_res (date,hrvalues) "
                 f"VALUES ('{day_string}', '{hrdata}');")
        _cursor.execute(query)


# Main loop
def main():
    '''Main loop.'''
    num_days = 365 * 20
    td = timedelta(num_days)
    start_date = datetime.now() - td
    print(f"Starting to build data base at {start_date}")
    cur_date = start_date

    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()

    create_new_db()
    for i in range(num_days):
        cur_date = cur_date + timedelta(1)
        print(f"Creating data for {cur_date}")
        create_data(cur_date, cursor, True)  # A
        update_counters()
        create_data(cur_date, cursor, False)  # B

    connection.commit()
    connection.close()


# Main entry point of the application
if __name__ == "__main__":
    main()
