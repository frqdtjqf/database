# backend/lego_db/relation_registry.py

from backend.lego_db.db_converter.registry.tables import TEMPLATE_MINIFIGURE_TABLE, LEGO_PART_TABLE, WEAPON_SLOT_TABLE, WEAPON_TABLE
from backend.sql_api import Attribute, Table

# column names
PART_NAME = "part_id"
TEMPLATE_NAME = "template_id"
WEAPON_NAME = "weapon_id"
WEAPON_SLOT_NAME = "weapon_slot_name"


# joint tables to define a N:M mapping

# Template -> Parts
TEMPLATE_MINIFIGURE_PART_TABLE = Table(
    name="template_minifigure_part",
    attributes=[
        Attribute(name=TEMPLATE_NAME, type="TEXT", primary_key=True, foreign_key=(TEMPLATE_MINIFIGURE_TABLE.name, "id")),
        Attribute(name=PART_NAME, type="TEXT", primary_key=True, foreign_key=(LEGO_PART_TABLE.name, "id"))
    ]
)

# Template -> Weapon Slot
TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE = Table(
    name="template_minifigure_weapon_slot",
    attributes=[
        Attribute(name=TEMPLATE_NAME, type="TEXT", primary_key=True, foreign_key=(TEMPLATE_MINIFIGURE_TABLE.name, "id")),
        Attribute(name=WEAPON_SLOT_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_SLOT_TABLE.name, "id"))
    ]
)

# Weapon Slot -> Weapon
WEAPON_SLOT_WEAPON_TABLE = Table(
    name="weapon_slot_weapon",
    attributes=[
        Attribute(name=WEAPON_SLOT_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_SLOT_TABLE.name, "id")),
        Attribute(name=WEAPON_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_TABLE.name, "id"))
    ]
)

# Weapon -> Part
WEAPON_PART_TABLE = Table(
    name="weapon_part_table",
    attributes=[
        Attribute(name=WEAPON_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_TABLE.name, "id")),
        Attribute(name=PART_NAME, type="TEXT", primary_key=True, foreign_key=(LEGO_PART_TABLE.name, "id"))
    ]
)

# relations collection
RELATIONS = {
    "template_parts": {
        "parent_table": TEMPLATE_MINIFIGURE_TABLE,
        "child_table": LEGO_PART_TABLE,
        "joint_table": TEMPLATE_MINIFIGURE_PART_TABLE,
        "parent_column": TEMPLATE_NAME,
        "child_column": PART_NAME
    },
    "template_weapon_slots": {
        "parent_table": TEMPLATE_MINIFIGURE_TABLE,
        "child_table": WEAPON_SLOT_TABLE,
        "joint_table": TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE,
        "parent_column": TEMPLATE_NAME,
        "child_column": WEAPON_SLOT_NAME
    },
    "weapon_slot_weapons": {
        "parent_table": WEAPON_SLOT_TABLE,
        "child_table": WEAPON_TABLE,
        "joint_table": WEAPON_SLOT_WEAPON_TABLE,
        "parent_column": WEAPON_SLOT_NAME,
        "child_column": WEAPON_NAME
    },
    "weapon_parts": {
        "parent_table": WEAPON_TABLE,
        "child_table": LEGO_PART_TABLE,
        "joint_table": WEAPON_PART_TABLE,
        "parent_column": WEAPON_NAME,
        "child_column": PART_NAME
    }
}
