from backend.sql_api import DataBaseWrapper, Table
from backend.lego_db.lego_models import LegoPart, Weapon
from backend.test import test_db, testing

LegoParts = [
    LegoPart(id="3001", color="Red", description="Brick 2x4"),
]

Weapons = [
    Weapon(id="W001", name="Sword", description="A simple sword", parts=frozenset([LegoParts[0]])),
]

testing()
