import sqlite3
from sql_api.models import *

DB_NAME = "database.db"

class DataBaseWrapper:

    def __init__(self, db_name = DB_NAME):
        self.db_name = db_name

    def create_table(self, table: Table):

        if not table.attributes:
            raise ValueError("Table must have at least one attribute")

        columns = []
        normal_attributes = []

        primary_key_found = False
        for attr in table.attributes:
            if attr.primary_key:
                if primary_key_found:
                    raise ValueError("Multiple primary keys defined")
                columns.append(f"{attr.name} {attr.type} PRIMARY KEY")
                primary_key_found = True
            else:
                normal_attributes.append(f"{attr.name} {attr.type}")

        columns.extend(normal_attributes)

        columns_sql = ",\n".join(columns)

        sql = f"CREATE TABLE IF NOT EXISTS {table.name} (\n{columns_sql}\n);"

        with self._connect() as db:
            db.execute(sql)
            db.commit()

    def delete_table(self, table: Table):
        sql = f"DROP TABLE IF EXISTS {table.name}"
        with self._connect() as db:
            db.execute(sql)
            db.commit()

    def insert_record(self,table: Table, record: Record):
        columns = [e.attribute.name for e in record.elements]
        params = {e.attribute.name: e.value for e in record.elements}

        columns_sql = ", ".join(columns)
        placeholders_sql = ", ".join([f":{c}" for c in columns])
        sql = f"INSERT INTO {table.name} ({columns_sql}) VALUES ({placeholders_sql})"
        with self._connect() as db:
            db.execute(sql, params)
            db.commit()

    def delete_record(self, table: Table, record: Record):
        pk_element = record.get_primary_key_element()

        sql = f"DELETE FROM {table.name} WHERE {pk_element.attribute.name} = :{pk_element.attribute.name}"
        params = {pk_element.attribute.name: pk_element.value}
        with self._connect() as db:
            db.execute(sql, params)
            db.commit()

    def get_records(self, table: Table) -> list[Record]:
        sql = f"SELECT * FROM {table.name}"
        with self._connect() as db:
            cursor = db.execute(sql)
            rows = cursor.fetchall()

        records = []
        for row in rows:
            elements = []
            for attr in table.attributes:
                value = row[attr.name]
                element = Element(attribute=attr, value=value)
                elements.append(element)
            record = Record(elements=elements)
            records.append(record)

        return records
    
    def _safe_identifier(self, name: str) -> str:
        if not name.isidentifier():
            raise ValueError(f"Invalid identifier: {name}")
        return name
    
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
