# Define attribute schemas for each table
from backend.sql_api import Attribute

LEGO_PART_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="color", type="TEXT"),
    Attribute(name="description", type="TEXT")
]

TEMPLATE_MINIFIGURE_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="name", type="TEXT"),
    Attribute(name="year", type="INTEGER"),
    Attribute(name="sets", type="TEXT"),
    Attribute(name="description", type="TEXT"),
]

ACTUAL_MINIFIGURE_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="template_id", type="TEXT", foreign_key=("template_minifigure", "id")),
    Attribute(name="box_number", type="INTEGER"),
    Attribute(name="position_in_box", type="INTEGER"),
    Attribute(name="condition", type="TEXT")
]

WEAPON_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="name", type="TEXT"),
    Attribute(name="description", type="TEXT")
]

WEAPON_SLOT_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True)
]

# define each table
from backend.sql_api import Table

LEGO_PART_TABLE = Table(
    name="lego_part",
    attributes=LEGO_PART_ATTRIBUTES
)

TEMPLATE_MINIFIGURE_TABLE = Table(
    name="template_minifigure",
    attributes=TEMPLATE_MINIFIGURE_ATTRIBUTES
)

ACTUAL_MINIFIGURE_TABLE = Table(
    name="actual_minifigure",
    attributes=ACTUAL_MINIFIGURE_ATTRIBUTES
)

WEAPON_TABLE = Table(
    name="weapon",
    attributes=WEAPON_ATTRIBUTES
)

from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon
MODEL_REGISTRY = {
    LegoPart: LEGO_PART_ATTRIBUTES,
    TemplateMinifigure: TEMPLATE_MINIFIGURE_ATTRIBUTES,
    ActualMinifigure: ACTUAL_MINIFIGURE_ATTRIBUTES,
    Weapon: WEAPON_ATTRIBUTES
}

# joint tables to define a N:M mapping

# Template -> Parts
TEMPLATE_MINIFIGURE_PART_TABLE = Table(
    name="template_minifigure_part",
    attributes=[
        Attribute(name="template_id", type="TEXT", primary_key=True, foreign_key=("template_minifigure", "id")),
        Attribute(name="part_id", type="TEXT", primary_key=True, foreign_key=("lego_part", "id"))
    ]
)

# Template -> Weapon Slot
TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE = Table(
    name="template_minifigure_weapon_slot",
    attributes=[
        Attribute(name="template_id", type="TEXT", primary_key=True, foreign_key=("template_minifigure", "id")),
        Attribute(name="weapon_slot_id", type="TEXT", primary_key=True)
    ]
)

# Weapon Slot -> Weapon
WEAPON_SLOT_WEAPON_TABLE = Table(
    name="weapon_slot_weapon",
    attributes=[
        Attribute(name="weapon_slot_id", type="TEXT", primary_key=True, foreign_key=("weapon_slot", "id")),
        Attribute(name="weapon", type="TEXT", primary_key=True, foreign_key=("weapon", "id"))
    ]
)

# Weapon -> Part
WEAPON_PART_TABLE = Table(
    name="weapon_part_table",
    attributes=[
        Attribute(name="weapon_id", type="TEXT", primary_key=True, foreign_key=("weapon", "id")),
        Attribute(name="part_id", type="TEXT", primary_key=True, foreign_key=("lego_part", "id"))
    ]
)