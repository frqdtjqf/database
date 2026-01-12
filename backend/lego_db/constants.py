from backend.sql_api import Attribute, Table
from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon

# Define attribute schemas for each table to avoid hardcoding
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
    Attribute(name="description", type="TEXT")
]

ACTUAL_MINIFIGURE_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="template_id", type="TEXT"),
    Attribute(name="box_number", type="INTEGER"),
    Attribute(name="position_in_box", type="INTEGER"),
    Attribute(name="condition", type="TEXT")
]

WEAPON_ATTRIBUTES = [
    Attribute(name="id", type="TEXT", primary_key=True),
    Attribute(name="name", type="TEXT"),
    Attribute(name="description", type="TEXT")
]

# all tables for the Lego database
TABLES = [
    Table(name="LegoParts", attributes=LEGO_PART_ATTRIBUTES),
    Table(name="TemplateMinifigures", attributes=TEMPLATE_MINIFIGURE_ATTRIBUTES),
    Table(name="ActualMinifigures", attributes=ACTUAL_MINIFIGURE_ATTRIBUTES),
    Table(name="Weapons", attributes=WEAPON_ATTRIBUTES)
]

MODEL_REGISTRY = {
    "LegoParts": LegoPart,
    "TemplateMinifigures": TemplateMinifigure,
    "ActualMinifigures": ActualMinifigure,
    "Weapons": Weapon
}