import sqlite3
from .models import Table, Record, Element, Attribute

DB_NAME = "database.db"

class DataBaseWrapper:

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = f"./data/{db_name}"
        self._connect()

    def create_relations_table(self, relation: dict):
        joint_table = relation["joint_table"]
        self.create_table(joint_table, relation["parent_column"])

    def create_table(self, table: Table, parent_name: str = None):
        if not table.attributes:
            raise ValueError("Table must have at least one attribute")

        columns = []
        foreign_keys = []

        for attr in table.attributes:
            col_def = f"{attr.name} {attr.type}"
            columns.append(col_def)

            if attr.foreign_key:
                if attr.name == parent_name and parent_name is not None:
                    fk_action = "ON DELETE CASCADE"
                else:
                    fk_action = "ON DELETE RESTRICT"
                ref_table, ref_column = attr.foreign_key
                foreign_keys.append(f"FOREIGN KEY({attr.name}) REFERENCES {ref_table}({ref_column}) {fk_action}")

        pk_attrs = [attr.name for attr in table.attributes if attr.primary_key]
        if pk_attrs:
            columns.append(f"PRIMARY KEY ({', '.join(pk_attrs)})")

        columns_sql = ",\n".join(columns + foreign_keys)
        sql = f"CREATE TABLE IF NOT EXISTS {table.name} (\n{columns_sql}\n);"

        with self._connect() as db:
            db.execute(sql)
            db.commit()

    def delete_table(self, table: Table):
        sql = f"DROP TABLE IF EXISTS {table.name}"
        with self._connect() as db:
            db.execute("PRAGMA foreign_keys = OFF;")
            db.execute(sql)
            db.execute("PRAGMA foreign_keys = ON;")
            db.commit()

    def insert_record(self, table: Table, record: Record):
        columns = [e.attribute.name for e in record.elements]
        params = {e.attribute.name: e.value for e in record.elements}

        columns_sql = ", ".join(columns)
        placeholders_sql = ", ".join([f":{c}" for c in columns])
        print(table.name)
        sql = f"INSERT OR IGNORE INTO {table.name} ({columns_sql}) VALUES ({placeholders_sql})"
        print(sql)

        with self._connect() as db:
            db.execute(sql, params)
            db.commit()
        print("c")

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
                elements.append(Element(attribute=attr, value=value))
            records.append(Record(elements=elements))

        return records
    
    def get_query_records(self, table: Table, query_attribute: Attribute, query_value: any) -> list[Record]:
        """Return all Records, which have Element(attribute=query_attribute, value=query_value)"""
        if query_attribute.name not in [attr.name for attr in table.attributes]:
            raise ValueError(f"Table '{table.name}' has no attribute '{query_attribute.name}'")
        
        sql = f"SELECT * from {table.name} WHERE {query_attribute.name} = :val"
        params = {"val": query_value}

        with self._connect() as db:
            cursor = db.execute(sql, params)
            rows = cursor.fetchall()

        records = []
        for row in rows:
            elements = []
            for attr in table.attributes:
                value = row[attr.name]
                elements.append(Element(attribute=attr, value=value))
            records.append(Record(elements=elements))

        return records
    
    def _safe_identifier(self, name: str) -> str:
        if not name.isidentifier():
            raise ValueError(f"Invalid identifier: {name}")
        return name
    
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
