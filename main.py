from backend.lego_db import LegoDBInterface

db = LegoDBInterface("database.db").db

from backend.lego_db.db_converter.registry import RELATIONS, LEGO_PART_TABLE, TEMPLATE_MINIFIGURE_TABLE, WEAPON_TABLE, WEAPON_SLOT_TABLE, ACTUAL_MINIFIGURE_TABLE

def print_table(db, table):
    print(f"\n=== Table: {table.name} ===")
    records = db.get_records(table)
    if not records:
        print("No entries")
        return

    for r in records:
        row = {e.attribute.name: e.value for e in r.elements}
        print(row)

all_tables = [
    LEGO_PART_TABLE,
    TEMPLATE_MINIFIGURE_TABLE,
    WEAPON_TABLE,
    WEAPON_SLOT_TABLE,
    ACTUAL_MINIFIGURE_TABLE
]

# Add joint tables from RELATIONS
for rel in RELATIONS.values():
    all_tables.append(rel["joint_table"])

for table in all_tables:
    print_table(db, table)



