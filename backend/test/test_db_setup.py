# tests/test_db_setup.py
from backend.sql_api import DataBaseWrapper

from backend.lego_db.db_converter.registry.relations import *
from backend.lego_db.db_converter.registry.tables import *
from backend.sql_api import Record, Element
from backend.lego_db.db_converter import *
from backend.lego_db.lego_models import *
ALL_JOINT = [
        TEMPLATE_MINIFIGURE_PART_TABLE,
        TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE,
        WEAPON_SLOT_WEAPON_TABLE,
        WEAPON_PART_TABLE,
    ]

def build(db):
    # 1. tables
    for table in TABLES_ALL:
        db.create_table(table)

    # 2. joint tables
    for table in ALL_JOINT:
        db.create_table(table)


def parts(db):
    from backend.lego_db.db_converter import LegoPartRepoManager
    from backend.lego_db.lego_models import LegoPart

    part_repo = LegoPartRepoManager(db)

    head = LegoPart(id="head_01", color="yellow")
    body = LegoPart(id="body_01", color="red")

    part_repo.add_model(head)
    part_repo.add_model(body)

def weapon(db):
    from backend.lego_db.db_converter import WeaponRepoManager
    from backend.lego_db.lego_models import Weapon

    weapon_repo = WeaponRepoManager(db)
    body = LegoPart(id="body_01", color="red")

    sword = Weapon(id="sword_01", name="Sword", parts=frozenset({body}), description="HEHEHEH")
    weapon_repo.add_model(sword)

def slot(db):

    weapon_slot_repo = WeaponSlotRepoManager(db)

    slot = WeaponSlot(id="slot_01")
    weapon_slot_repo.add_model(slot)

def relation(db):
    # weapon_slot -> weapon
    db.insert_record(
        WEAPON_SLOT_WEAPON_TABLE,
        Record([
            Element(WEAPON_SLOT_WEAPON_TABLE.attributes[0], "slot_01"),
            Element(WEAPON_SLOT_WEAPON_TABLE.attributes[1], "sword_01"),
        ])
    )

def template(db):

    template_repo = TemplateMinifigureRepoManager(db)

    template = TemplateMinifigure(
        id="temp_01",
        name="Knight",
        year=1998,
        sets=frozenset({"set_01"}),
    )

    template_repo.add_model(template)

    db.insert_record(
        TEMPLATE_MINIFIGURE_PART_TABLE,
        Record([
            Element(TEMPLATE_MINIFIGURE_PART_TABLE.attributes[0], "temp_01"),
            Element(TEMPLATE_MINIFIGURE_PART_TABLE.attributes[1], "head_01"),
        ])
    )
    return template_repo

def reload_stuff(template_repo):
    loaded_templates = template_repo.get_models()
    return loaded_templates

def remove_tables(db):
    for table in ALL_JOINT:
        db.delete_table(table)
    for table in TABLES_ALL:
        db.delete_table(table)

def testing():
    TEST_DB = "test_database.db"

    db = DataBaseWrapper(TEST_DB)
    remove_tables(db)

    build(db)
    parts(db)
    weapon(db)
    slot(db)
    relation(db)
    temp = template(db)
    temp = TemplateMinifigureRepoManager(db)
    loaded = reload_stuff(temp)
    ls = reload_stuff(WeaponSlotRepoManager(db))
    lt = reload_stuff(WeaponRepoManager(db))

    print(loaded)
    print(ls)
    print(lt)







