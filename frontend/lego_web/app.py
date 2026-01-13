from flask import Flask, render_template
from backend.lego_db import *

# Example LegoParts
body = LegoPart(bricklink_part_id="body_01", bricklink_color_id="1")
legs = LegoPart(bricklink_part_id="legs_01", bricklink_color_id="2")
helmet = LegoPart(bricklink_part_id="helmet_01", bricklink_color_id="1")

# Example Weapons
sword = Weapon(name="Sword", parts=frozenset([body]))
shield = Weapon(name="Shield", parts=frozenset([helmet]))

# WeaponSlot (contains a set of weapons)
slot1 = WeaponSlot(weapons=frozenset([sword, shield]))
slot2 = WeaponSlot(weapons=frozenset([shield]))  # another possible slot

# Template Minifigure
knight_template = TemplateMinifigure(
    bricklink_fig_id="knight_01",
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
    weapon_slot=slot1,
    condition="new"
)

actual_knight2 = ActualMinifigure(
    template=knight_template,
    box_number=1,
    position_in_box=2,
    weapon_slot=slot2,
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
    columns, rows = prepare_table_data(parts)
    return render_generic(table_name="Lego Parts", columns=columns, rows=rows)

@app.route("/weapons")
def render_weapons():
    weapons = db_inter.get_all_weapons()
    columns, rows = prepare_table_data(weapons)
    return render_generic(table_name="Weapons", columns=columns, rows=rows)


@app.route("/weapon_slots")
def render_weapon_slots():
    weapon_slots = db_inter.get_all_weapon_slots()
    columns, rows = prepare_table_data(weapon_slots)
    return render_generic(table_name="Weapon Slots", columns=columns, rows=rows)


@app.route("/template_minifigures")
def render_template_minifigures():
    templates = db_inter.get_all_templates()
    columns, rows = prepare_table_data(templates)
    return render_generic(table_name="Template Minifigures", columns=columns, rows=rows)


@app.route("/actual_minifigures")
def render_actual_minifigures():
    actuals = db_inter.get_all_actual_minifigures()
    columns, rows = prepare_table_data(actuals)
    return render_generic(table_name="Actual Minifigures", columns=columns, rows=rows)


# --- Helper ---
def render_generic(table_name: str, columns: list[str], rows: list[dict[str, str]]):
    return render_template("generic.html", title=table_name, columns=columns, rows=rows)

def prepare_table_data(elements: list[BasicModel]):
    if not elements:
        columns = []
        rows = []
    else:
        columns, _ = elements[0].get_column_row_data()
        rows = []
        for e in elements:
            _, rows_e = e.get_column_row_data()
            rows.append(rows_e)

    return columns, rows

if __name__ == "__main__":
    app.run(debug=True)