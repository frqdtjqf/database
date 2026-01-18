# Define attribute schemas for each table
from backend.sql_api import Attribute

PRIMARY_KEY_NAME = "id"

# column names
PART_NAME = "part_id"
TEMPLATE_NAME = "template_id"
WEAPON_NAME = "weapon_id"
WEAPON_SLOT_NAME = "weapon_slot_id"
COLOR_NAME = "bricklink_color_id"

COLOR_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name="bricklink_color_id", type="TEXT"),
    Attribute(name="rebrickable_color_id", type="TEXT"),
    Attribute(name="lego_color_id", type="TEXT"),
    Attribute(name="rgb_value", type="TEXT"),
    Attribute(name="name", type="TEXT")
]

LEGO_PART_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name="bricklink_part_id", type="TEXT"),
    Attribute(name=COLOR_NAME, type="TEXT", foreign_key=("colors", PRIMARY_KEY_NAME)),
    Attribute(name="lego_element_id", type="TEXT"),
    Attribute(name="lego_design_id", type="TEXT"),
    Attribute(name="description", type="TEXT")
]

TEMPLATE_MINIFIGURE_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name="color", type="TEXT", foreign_key=("colors", PRIMARY_KEY_NAME)),
    Attribute(name="name", type="TEXT"),
    Attribute(name="year", type="TEXT"),
    Attribute(name="sets", type="TEXT"),
    Attribute(name="description", type="TEXT"),
]

ACTUAL_MINIFIGURE_ATTRIBUTES = [
    Attribute(name=PRIMARY_KEY_NAME, type="TEXT", primary_key=True),
    Attribute(name=TEMPLATE_NAME, type="TEXT", foreign_key=("template_minifigures", PRIMARY_KEY_NAME)),
    Attribute(name=WEAPON_SLOT_NAME, type="TEXT", foreign_key=("weapon_slots", PRIMARY_KEY_NAME)),
    Attribute(name="box_number", type="TEXT"),
    Attribute(name="position_in_box", type="TEXT"),
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

COLOR_TABLE = Table(
    name="colors",
    attributes=COLOR_ATTRIBUTES,
    is_joint=False
)

LEGO_PART_TABLE = Table(
    name="lego_parts",
    attributes=LEGO_PART_ATTRIBUTES,
    is_joint=False
)

TEMPLATE_MINIFIGURE_TABLE = Table(
    name="template_minifigures",
    attributes=TEMPLATE_MINIFIGURE_ATTRIBUTES,
    is_joint=False
)

ACTUAL_MINIFIGURE_TABLE = Table(
    name="actual_minifigures",
    attributes=ACTUAL_MINIFIGURE_ATTRIBUTES,
    is_joint=False
)

WEAPON_TABLE = Table(
    name="weapons",
    attributes=WEAPON_ATTRIBUTES,
    is_joint=False
)

WEAPON_SLOT_TABLE = Table(
    name="weapon_slots",
    attributes=WEAPON_SLOT_ATTRIBUTES,
    is_joint=False
)

TABLES_ALL = [
    LEGO_PART_TABLE,
    TEMPLATE_MINIFIGURE_TABLE,
    ACTUAL_MINIFIGURE_TABLE,
    WEAPON_SLOT_TABLE,
    WEAPON_TABLE,
    COLOR_TABLE
]