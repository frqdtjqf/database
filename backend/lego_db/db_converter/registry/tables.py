# Define attribute schemas for each table
from backend.sql_api import Attribute

PRIMARY_KEY_NAME = "id"

# column names
PART_NAME = "part_id"
TEMPLATE_NAME = "template_id"
WEAPON_NAME = "weapon_id"
WEAPON_SLOT_NAME = "weapon_slot_id"

LEGO_PART_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
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
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name=TEMPLATE_NAME, type="TEXT", foreign_key=("template_minifigure", PRIMARY_KEY_NAME)),
    Attribute(name=WEAPON_SLOT_NAME, type="TEXT", foreign_key=("weapon_slot", PRIMARY_KEY_NAME)),
    Attribute(name="box_number", type="INTEGER"),
    Attribute(name="position_in_box", type="INTEGER"),
    Attribute(name="condition", type="TEXT")
]

WEAPON_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name="name", type="TEXT"),
    Attribute(name="description", type="TEXT")
]

WEAPON_SLOT_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True)
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

WEAPON_SLOT_TABLE = Table(
    name="weapon_slot",
    attributes=WEAPON_SLOT_ATTRIBUTES
)

TABLES_ALL = [
    LEGO_PART_TABLE,
    TEMPLATE_MINIFIGURE_TABLE,
    ACTUAL_MINIFIGURE_TABLE,
    WEAPON_SLOT_TABLE,
    WEAPON_TABLE
]