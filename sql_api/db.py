import sqlite3
from sql_api.models import *

DB_NAME = "database.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table(table: Table):

    if not table.attributes:
        raise ValueError("Table must have at least one attribute")

    columns = []
    normal_attributes = []

    primary_key_found = False
    for attr in table.attributes:
        if attr.primary_key:
            if primary_key_found:
                raise ValueError("Multiple primary keys defined")
            columns.append(f"{attr.name} {attr.type} PRIMARY KEY")  # PK goes first
            primary_key_found = True
        else:
            normal_attributes.append(f"{attr.name} {attr.type}")

    columns.extend(normal_attributes)

    columns_sql = ",\n".join(columns)

    sql = f"CREATE TABLE IF NOT EXISTS {table.name} (\n{columns_sql}\n);"

    with connect() as db:
        db.execute(sql)
        db.commit()

def delete_table(table: Table):
    with connect() as db:
        db.execute(f"DROP TABLE IF EXISTS {table.name}")
        db.commit()

def insert_record(table: Table, record: Record):
    columns = []
    values = []

    for e in record.elements:
        columns.append(e.attribute.name)
        values.append(e.value)


    columns_sql = ", ".join(columns)
    placeholders_sql = ", ".join([f":{e.attribute.name}" for e in record.elements])
    sql = f"INSERT INTO {table.name} ({columns_sql}) VALUES ({placeholders_sql})"
    with connect() as db:
        db.execute(sql, values)
        db.commit()

def get_users():
    with connect() as db:
        return db.execute("SELECT * FROM benutzer").fetchall()
