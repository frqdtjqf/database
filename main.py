from backend.lego_db.lego_models import LegoPart, Weapon
from backend.lego_db.write_lego_data import build_tables, write_model_list_to_db
from backend.lego_db.read_lego_data import read_models_from_table
from backend.sql_api import DataBaseWrapper
from backend.lego_db.db_converter.convert_rules import TABLES

LegoParts = [
    LegoPart(id="3001", color="Red", description="Brick 2x4"),
]

Weapons = [
    Weapon(id="W001", name="Sword", description="A simple sword", parts=frozenset([LegoParts[0]])),
]

db = DataBaseWrapper("./data/database.db")
db.delete_table(TABLES[0])
db.delete_table(TABLES[3])

build_tables(db, TABLES)

write_model_list_to_db(db, LegoParts, TABLES[0])
write_model_list_to_db(db, Weapons, TABLES[3])

data = read_models_from_table(db, TABLES[0])
print(data)

data_weapons = read_models_from_table(db, TABLES[3])
print(data_weapons)