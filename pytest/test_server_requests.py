import json
import logging
import sqlite3
from types import SimpleNamespace

import pytest

import server


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    connection = sqlite3.connect(data_dir / "db.sqlite")
    connection.executescript(
        """
        CREATE TABLE days (
            date TEXT PRIMARY KEY,
            produced_a REAL, produced_b REAL,
            consumed_a REAL, consumed_b REAL,
            fed_in_a REAL, fed_in_b REAL
        );
        CREATE TABLE months (
            date TEXT PRIMARY KEY,
            produced_a REAL, produced_b REAL,
            consumed_a REAL, consumed_b REAL,
            fed_in_a REAL, fed_in_b REAL
        );
        CREATE TABLE years (
            date TEXT PRIMARY KEY,
            produced_a REAL, produced_b REAL,
            consumed_a REAL, consumed_b REAL,
            fed_in_a REAL, fed_in_b REAL
        );
        CREATE TABLE all_time (
            date TEXT PRIMARY KEY,
            produced_a REAL, produced_b REAL,
            consumed_a REAL, consumed_b REAL,
            fed_in_a REAL, fed_in_b REAL
        );
        CREATE TABLE real_time (
            ID INTEGER PRIMARY KEY,
            time TEXT,
            produced REAL,
            consumed REAL,
            fed_in REAL
        );
        CREATE TABLE high_res (date TEXT PRIMARY KEY, hrvalues TEXT);
        """
    )
    rows = (
        ("days", "2026-07-24", 10, 15, 20, 24, 3, 4),
        ("months", "2026-07", 100, 150, 200, 240, 30, 40),
        ("years", "2026", 1000, 1500, 2000, 2400, 300, 400),
        ("all_time", "all_time", 1000, 1500, 2000, 2400, 300, 400),
    )
    for table, *values in rows:
        connection.execute(
            f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?)",
            values,
        )
    connection.execute(
        "INSERT INTO high_res VALUES (?, ?)",
        ("2026-07-24", '["12:00",1.0,0.5,0.2],'),
    )
    connection.executemany(
        "INSERT INTO real_time VALUES (?, ?, ?, ?, ?)",
        [
            (1, "12:00", 1.0, 0.5, 0.2),
            (2, "12:01", 1.1, 0.6, 0.3),
        ],
    )
    connection.commit()
    connection.close()

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        server,
        "config",
        SimpleNamespace(
            config_data={
                "prices": {
                    "price_per_grid_kwh": 0.30,
                    "revenue_per_fed_in_kwh": 0.10,
                }
            }
        ),
    )
    server.app.config.update(TESTING=True)
    return server.app.test_client()


def test_daily_history_preserves_public_response(client):
    response = client.get(
        "/query",
        query_string={
            "type": "historical",
            "table": "days",
            "date": "2026-07-24",
        },
    )

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        "state": "ok",
        "produced_kwh": 5.0,
        "consumed_total_kwh": 4.0,
        "consumed_from_pv_kwh": 4.0,
        "consumed_from_grid_kwh": 0.0,
        "consumed_from_pv_percent": 100.0,
        "consumed_from_grid_percent": 0.0,
        "usage_fed_in_kwh": 1.0,
        "usage_self_consumed_kwh": 4.0,
        "usage_fed_in_percent": 20.0,
        "usage_self_consumed_percent": 80.0,
        "earned_feedin": 0.1,
        "earned_savings": 0.7999999999999999,
        "earned_total": 0.8999999999999999,
        "autarky": 100.0,
        "high_res": '[["12:00",1.0,0.5,0.2]]',
    }


@pytest.mark.parametrize(
    "table",
    ["sqlite_master", "days WHERE 1=1 --"],
)
def test_historical_query_rejects_unsupported_table(client, table):
    response = client.get(
        "/query",
        query_string={
            "type": "historical",
            "table": table,
            "date": "2026-07-24",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "unsupported table",
    }


def test_historical_query_rejects_sql_shaped_date(client):
    response = client.get(
        "/query",
        query_string={
            "type": "historical",
            "table": "days",
            "date": "2026-07-24' OR '1'='1",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "invalid date",
    }


@pytest.mark.parametrize(
    ("table", "date_value", "expected_production"),
    [
        ("months", "2026-07", 50.0),
        ("years", "2026", 500.0),
        ("all_time", "all_time", 500.0),
    ],
)
def test_monthly_yearly_and_all_time_history_preserve_public_response(
    client,
    table,
    date_value,
    expected_production,
):
    response = client.get(
        "/query",
        query_string={
            "type": "historical",
            "table": table,
            "date": date_value,
        },
    )

    assert response.status_code == 200
    body = json.loads(response.get_data(as_text=True))
    assert set(body) == {
        "state",
        "produced_kwh",
        "consumed_total_kwh",
        "consumed_from_pv_kwh",
        "consumed_from_grid_kwh",
        "consumed_from_pv_percent",
        "consumed_from_grid_percent",
        "usage_fed_in_kwh",
        "usage_self_consumed_kwh",
        "usage_fed_in_percent",
        "usage_self_consumed_percent",
        "earned_feedin",
        "earned_savings",
        "earned_total",
        "autarky",
        "high_res",
    }
    assert body["state"] == "ok"
    assert body["produced_kwh"] == expected_production
    assert body["high_res"] == ""


@pytest.mark.parametrize(
    ("table", "date_value"),
    [
        ("days", "2026-02-30"),
        ("days", "2026-7-24"),
        ("months", "2026-13"),
        ("months", "2026-7"),
        ("years", "26"),
        ("years", "202A"),
        ("years", "٢٠٢٦"),
        ("all_time", "2026"),
        ("all_time", "all_time' OR '1'='1"),
    ],
)
def test_historical_query_rejects_malformed_or_impossible_dates(
    client,
    table,
    date_value,
):
    response = client.get(
        "/query",
        query_string={
            "type": "historical",
            "table": table,
            "date": date_value,
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "invalid date",
    }


@pytest.mark.parametrize(
    ("query_type", "date_value", "expected_body"),
    [
        (
            "days_in_month",
            "2026-07",
            {
                "date": "2026-07-24",
                "produced_self": 4.0,
                "produced_feed_in": 1.0,
                "consumed_from_pv": 4.0,
                "consumed_from_grid": 0.0,
            },
        ),
        (
            "months_in_year",
            "2026",
            {
                "date": "2026-07",
                "produced_self": 40.0,
                "produced_feed_in": 10.0,
                "consumed_from_pv": 40.0,
                "consumed_from_grid": 0.0,
            },
        ),
        (
            "years_in_all_time",
            None,
            {
                "date": "2026",
                "produced_self": 400.0,
                "produced_feed_in": 100.0,
                "consumed_from_pv": 400.0,
                "consumed_from_grid": 0.0,
            },
        ),
    ],
)
def test_history_detail_queries_preserve_public_response(
    client,
    query_type,
    date_value,
    expected_body,
):
    query_string = {"type": query_type}
    if date_value is not None:
        query_string["date"] = date_value

    response = client.get("/query", query_string=query_string)

    assert response.status_code == 200
    body = json.loads(response.get_data(as_text=True))
    assert body == [expected_body]


@pytest.mark.parametrize(
    ("query_type", "date_value"),
    [
        ("days_in_month", "2026-13"),
        ("days_in_month", "2026-07' OR '1'='1"),
        ("months_in_year", "26"),
        ("months_in_year", "2026' OR '1'='1"),
    ],
)
def test_history_detail_queries_reject_invalid_dates(
    client,
    query_type,
    date_value,
):
    response = client.get(
        "/query",
        query_string={"type": query_type, "date": date_value},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "invalid date",
    }


@pytest.mark.parametrize(
    ("table", "date_value", "expected_row"),
    [
        ("days", "", "2026-07-24;5.0;4.0;1.0"),
        ("days", "2026", "2026-07-24;5.0;4.0;1.0"),
        ("days", "2026-07", "2026-07-24;5.0;4.0;1.0"),
        ("days", "2026-07-24", "2026-07-24;5.0;4.0;1.0"),
        ("months", "", "2026-07;50.0;40.0;10.0"),
        ("months", "2026", "2026-07;50.0;40.0;10.0"),
        ("months", "2026-07", "2026-07;50.0;40.0;10.0"),
        ("years", "", "2026;500.0;400.0;100.0"),
        ("years", "2026", "2026;500.0;400.0;100.0"),
    ],
)
def test_csv_export_preserves_supported_tables_and_date_prefixes(
    client,
    table,
    date_value,
    expected_row,
):
    response = client.get(
        "/csv",
        query_string={"table": table, "date": date_value},
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert response.headers["Content-Disposition"] == (
        f"attachment; filename=Sunalyzer_{date_value}.csv"
        if date_value
        else "attachment; filename=Sunalyzer_All.csv"
    )
    lines = response.get_data(as_text=True).splitlines()
    assert lines == [
        "date;production;consumption;feed_in",
        expected_row,
    ]


@pytest.mark.parametrize(
    "table",
    ["sqlite_master", "days WHERE 1=1 --"],
)
def test_csv_export_rejects_unsupported_or_sql_shaped_tables(client, table):
    response = client.get(
        "/csv",
        query_string={"table": table},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "unsupported table",
    }


@pytest.mark.parametrize(
    ("table", "date_value"),
    [
        ("days", "2026-02-30"),
        ("days", "2026-13"),
        ("days", "2026-7"),
        ("days", "2026' OR '1'='1"),
        ("months", "2026-13"),
        ("months", "2026-07-24"),
        ("months", "2026' OR '1'='1"),
        ("years", "2026-07"),
        ("years", "2026' OR '1'='1"),
    ],
)
def test_csv_export_rejects_invalid_date_prefixes(client, table, date_value):
    response = client.get(
        "/csv",
        query_string={"table": table, "date": date_value},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "invalid date",
    }


@pytest.mark.parametrize(
    ("path", "query_string", "missing_parameter"),
    [
        ("/query", {}, "type"),
        (
            "/query",
            {"type": "historical", "date": "2026-07-24"},
            "table",
        ),
        (
            "/query",
            {"type": "historical", "table": "days"},
            "date",
        ),
        ("/query", {"type": "days_in_month"}, "date"),
        ("/query", {"type": "months_in_year"}, "date"),
        ("/query", {"type": "real_time"}, "h"),
        ("/csv", {}, "table"),
    ],
)
def test_public_data_endpoints_reject_missing_parameters(
    client,
    path,
    query_string,
    missing_parameter,
):
    response = client.get(path, query_string=query_string)

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": f"missing parameter: {missing_parameter}",
    }


def test_real_time_query_preserves_valid_hour_range(client):
    response = client.get(
        "/query",
        query_string={"type": "real_time", "h": "2"},
    )

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == [
        [2, "12:01", 1.1, 0.6, 0.3],
        [1, "12:00", 1.0, 0.5, 0.2],
    ]


@pytest.mark.parametrize(
    "hours",
    ["", "0", "-1", "25", "999999", "1.5", "abc", "1 OR 1=1"],
)
def test_real_time_query_rejects_invalid_or_excessive_hours(client, hours):
    response = client.get(
        "/query",
        query_string={"type": "real_time", "h": hours},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "invalid hours",
    }


def test_internal_query_value_error_remains_a_logged_server_error(
    client,
    caplog,
):
    server.config.config_data["prices"]["price_per_grid_kwh"] = "not-a-number"

    with caplog.at_level(logging.ERROR):
        response = client.get(
            "/query",
            query_string={
                "type": "historical",
                "table": "days",
                "date": "2026-07-24",
            },
        )

    assert response.status_code == 500
    assert response.get_json() == {
        "state": "error",
        "message": "internal server error",
    }
    assert "Error while handling HTTP request" in caplog.text


def test_internal_csv_failure_returns_a_json_server_error(client):
    connection = sqlite3.connect("data/db.sqlite")
    connection.execute("DROP TABLE days")
    connection.commit()
    connection.close()

    response = client.get(
        "/csv",
        query_string={"table": "days", "date": "2026"},
    )

    assert response.status_code == 500
    assert response.get_json() == {
        "state": "error",
        "message": "internal server error",
    }


def test_query_rejects_unsupported_request_type(client):
    response = client.get(
        "/query",
        query_string={"type": "drop_everything"},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "state": "error",
        "message": "unsupported query type",
    }
