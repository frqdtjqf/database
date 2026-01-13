from flask import Flask, render_template
from backend.lego_db import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure
from frontend.api_managers import LegoPartWebManager, WeaponWebManager, WeaponSlotWebManager, TemplateMinifigureWebManager, ActualMinifigureWebManager, WebTable, BaseWebManager
from backend.lego_db import LegoDBInterface
from backend.sql_api import DataBaseWrapper

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

db = DataBaseWrapper("database.db")

db_inter = LegoDBInterface(db)
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
    mng = LegoPartWebManager(db)
    return render_generic(web_mng=mng)

@app.route("/weapons")
def render_weapons():
    mng = WeaponWebManager(db)
    return render_generic(web_mng=mng)


@app.route("/weapon_slots")
def render_weapon_slots():
    mng = WeaponSlotWebManager(db)
    return render_generic(web_mng=mng)


@app.route("/template_minifigures")
def render_template_minifigures():
    mng = TemplateMinifigureWebManager(db)
    return render_generic(web_mng=mng)


@app.route("/actual_minifigures")
def render_actual_minifigures():
    mng = ActualMinifigureWebManager(db)
    return render_generic(web_mng=mng)


# --- Helper ---
def render_generic(web_mng: BaseWebManager):
    web_table = web_mng.get_web_table()
    return render_template("generic.html", title=web_table.name, columns=web_table.columns, rows=web_table.rows)

if __name__ == "__main__":
    app.run(debug=True)