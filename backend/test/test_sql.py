import sqlite3
from sql_api.models import Table, Attribute
from sql_api.db import connect, create_table, delete_table

def test_create_table():
    # Define test table and attributes
    attrs = [
        Attribute("name", "TEXT"),
        Attribute("age", "INTEGER"),
        Attribute("id", "INTEGER", primary_key=True)
    ]
    table = Table("users_test", attrs)

    delete_table(table.name)  # Ensure clean state
    create_table(table)
    
    # Connect to DB and check table exists
    with connect() as db:

        # Check table exists
        cr = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table.name,))
        result = cr.fetchone()
        assert result is not None, "Table was not created"
        
        # Check columns
        cr =db.execute(f"PRAGMA table_info({table.name})")
        columns_info = cr.fetchall()
        columns_names_types = [(col[1], col[2]) for col in columns_info]
        
        # Expected columns
        expected_columns = [("id", "INTEGER"), ("name", "TEXT"), ("age", "INTEGER")]
        assert columns_names_types == expected_columns, f"Columns mismatch: {columns_names_types} != {expected_columns}"
    
    print("All tests passed!")

# Run the test
test_create_table()
