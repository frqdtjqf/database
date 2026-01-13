# backend/lego_db/relation_registry.py

from backend.lego_db.db_converter.registry.tables import *
from backend.sql_api import Attribute, Table


# joint tables to define a N:M mapping

# Template -> Parts
TEMPLATE_MINIFIGURE_PART_TABLE = Table(
    name="template_minifigure_part",
    attributes=[
        Attribute(name=TEMPLATE_NAME, type="TEXT", primary_key=True, foreign_key=(TEMPLATE_MINIFIGURE_TABLE.name, PRIMARY_KEY_NAME)),
        Attribute(name=PART_NAME, type="TEXT", primary_key=True, foreign_key=(LEGO_PART_TABLE.name, PRIMARY_KEY_NAME))
    ]
)

# Template -> Weapon Slot
TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE = Table(
    name="template_minifigure_weapon_slot",
    attributes=[
        Attribute(name=TEMPLATE_NAME, type="TEXT", primary_key=True, foreign_key=(TEMPLATE_MINIFIGURE_TABLE.name, PRIMARY_KEY_NAME)),
        Attribute(name=WEAPON_SLOT_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_SLOT_TABLE.name, PRIMARY_KEY_NAME))
    ]
)

# Weapon Slot -> Weapon
WEAPON_SLOT_WEAPON_TABLE = Table(
    name="weapon_slot_weapon",
    attributes=[
        Attribute(name=WEAPON_SLOT_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_SLOT_TABLE.name, PRIMARY_KEY_NAME)),
        Attribute(name=WEAPON_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_TABLE.name, PRIMARY_KEY_NAME))
    ]
)

# Weapon -> Part
WEAPON_PART_TABLE = Table(
    name="weapon_part_table",
    attributes=[
        Attribute(name=WEAPON_NAME, type="TEXT", primary_key=True, foreign_key=(WEAPON_TABLE.name, PRIMARY_KEY_NAME)),
        Attribute(name=PART_NAME, type="TEXT", primary_key=True, foreign_key=(LEGO_PART_TABLE.name, PRIMARY_KEY_NAME))
    ]
)

# relation table names
TEMPLATE_PARTS_JOINT = "template_parts"
TEMPLATE_WEAPON_SLOTS_JOINT = "template_weapon_slots"
WEAPON_SLOT_WEAPONS_JOINT = "weapon_slot_weapons"
WEAPON_PARTS_JOINT = "weapon_parts"

# relations collection
RELATIONS = {
    TEMPLATE_PARTS_JOINT: {
        "parent_table": TEMPLATE_MINIFIGURE_TABLE,
        "child_table": LEGO_PART_TABLE,
        "joint_table": TEMPLATE_MINIFIGURE_PART_TABLE,
        "parent_column": TEMPLATE_NAME,
        "child_column": PART_NAME
    },
    TEMPLATE_WEAPON_SLOTS_JOINT: {
        "parent_table": TEMPLATE_MINIFIGURE_TABLE,
        "child_table": WEAPON_SLOT_TABLE,
        "joint_table": TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE,
        "parent_column": TEMPLATE_NAME,
        "child_column": WEAPON_SLOT_NAME
    },
    WEAPON_SLOT_WEAPONS_JOINT: {
        "parent_table": WEAPON_SLOT_TABLE,
        "child_table": WEAPON_TABLE,
        "joint_table": WEAPON_SLOT_WEAPON_TABLE,
        "parent_column": WEAPON_SLOT_NAME,
        "child_column": WEAPON_NAME
    },
    WEAPON_PARTS_JOINT: {
        "parent_table": WEAPON_TABLE,
        "child_table": LEGO_PART_TABLE,
        "joint_table": WEAPON_PART_TABLE,
        "parent_column": WEAPON_NAME,
        "child_column": PART_NAME
    }
}
