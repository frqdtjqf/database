from flask import Flask, render_template
from backend.lego_db import *

# Example LegoParts
body = LegoPart(id="body_01", color="red")
legs = LegoPart(id="legs_01", color="blue")
helmet = LegoPart(id="helmet_01", color="yellow")

# Example Weapons
sword = Weapon(id="sword_01", name="Sword", parts=frozenset([body]))
shield = Weapon(id="shield_01", name="Shield", parts=frozenset([helmet]))

# WeaponSlot (contains a set of weapons)
slot1 = WeaponSlot(weapons=frozenset([sword, shield]))
slot2 = WeaponSlot(weapons=frozenset([shield]))  # another possible slot

# Template Minifigure
knight_template = TemplateMinifigure(
    id="knight_01",
    name="Red Knight",
    year=2020,
    sets=frozenset(["SetA", "SetB"]),
    parts=frozenset([body, legs, helmet]),
    possible_weapons=frozenset([slot1, slot2]),
    description="A brave red knight with armor and weapons."
)

# Actual Minifigure in inventory
actual_knight1 = ActualMinifigure(
    template=knight_template,
    box_number=1,
    position_in_box=1,
    weaponSlot=slot1,
    condition="new"
)

actual_knight2 = ActualMinifigure(
    template=knight_template,
    box_number=1,
    position_in_box=2,
    weaponSlot=slot2,
    condition="used"
)

app = Flask(__name__)

db_inter = LegoDBInterface("database.db")
db_inter.delete_all_tables()
db_inter.create_all_tables()


db_inter.add_part(body)
db_inter.add_part(legs)
db_inter.add_part(helmet)
db_inter.add_weapon(sword)
db_inter.add_weapon(shield)
db_inter.add_weapon_slot(slot1)
db_inter.add_weapon_slot(slot2)
db_inter.add_template(knight_template)
db_inter.add_actual_minifigure(actual_knight1)
db_inter.add_actual_minifigure(actual_knight2)

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/lego_parts")
def render_lego_parts():
    parts = db_inter.get_parts()
    return render_template("lego_parts.html", parts=parts)

@app.route("/weapons")
def render_weapons():
    weapons = db_inter.get_all_weapons()
    return render_template("weapons.html", weapons=weapons)

@app.route("/weapon_slots")
def render_weapon_slots():
    weapon_slots = db_inter.get_all_weapon_slots()
    return render_template("weapon_slots.html", weapon_slots=weapon_slots)

@app.route("/template_minifigures")
def render_template_minifigures():
    template_minifigures = db_inter.get_all_templates()
    return render_template("template_minifigures.html", templates=template_minifigures)

@app.route("/actual_minifigures")
def render_actual_minifigures():
    actual_minifigures = db_inter.get_all_actual_minifigures()
    return render_template("actual_minifigures.html", actuals=actual_minifigures)

if __name__ == "__main__":
    app.run(debug=True)