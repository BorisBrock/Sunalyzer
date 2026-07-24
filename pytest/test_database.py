from database import Database


def test_execute_accepts_query_parameters(tmp_path):
    db = Database(tmp_path / "test.sqlite")
    db.execute("CREATE TABLE readings (date TEXT, value REAL)")
    db.execute(
        "INSERT INTO readings VALUES (?, ?)",
        ("2026-07-24", 12.5),
    )

    rows = db.execute(
        "SELECT date, value FROM readings WHERE date = ?",
        ("2026-07-24",),
    )

    assert rows == [("2026-07-24", 12.5)]
