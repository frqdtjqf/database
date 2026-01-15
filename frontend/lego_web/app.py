from flask import Flask, render_template, request, redirect, url_for
from backend.lego_db import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure
from frontend.api_managers import LegoPartWebManager, WeaponWebManager, WeaponSlotWebManager, TemplateMinifigureWebManager, ActualMinifigureWebManager, WebTable, BaseWebManager
from backend.lego_db import LegoDBInterface, PRIMARY_KEY_NAME
from backend.sql_api import DataBaseWrapper
from dataclasses import fields

db = DataBaseWrapper("database.db")
WEB_MANAGERS = {
    "lego_parts": LegoPartWebManager,
    "weapons": WeaponWebManager,
    "weapon_slots": WeaponSlotWebManager,
    "template_minifigures": TemplateMinifigureWebManager,
    "actual_minifigures": ActualMinifigureWebManager,
}

ENTITY_ROUTES = {
    "lego_parts": "render_lego_parts",
    "weapons": "render_weapons",
    "weapon_slots": "render_weapon_slots",
    "template_minifigures": "render_template_minifigures",
    "actual_minifigures": "render_actual_minifigures",
}

db_inter = LegoDBInterface(db)
db_inter.create_all_tables()

"""
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

web_manager = LegoPartWebManager(db)
form_data = {"bricklink_part_id": "3001testste", "bricklink_color_id": "5", "description": "red brick"}
new_model = web_manager.repo_mng.create_model(form_data)
web_manager.repo_mng.add_model(new_model)
"""

app = Flask(__name__)

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

@app.route("/add_form/<entity>", methods=["GET", "POST"])
def add_form(entity):
    if entity not in WEB_MANAGERS:
        return f"Unknown entity: {entity}", 404
    
    manager_class = WEB_MANAGERS[entity]
    web_manager: BaseWebManager = manager_class(db)
    repo_manager = web_manager.repo_mng

    model_cls = repo_manager.model_cls
    model_fields = fields(model_cls)

    if request.method == "POST":
        form_data = request.form.to_dict()

        # Convert numeric fields
        for f in model_fields:
            if f.type == float and f.name in form_data:
                form_data[f.name] = float(form_data[f.name])
            if f.type == int and f.name in form_data:
                form_data[f.name] = int(form_data[f.name])

        # Optionally ensure missing fields exist
        for f in model_fields:
            if f.name not in form_data:
                if f.metadata.get("related_field", False):
                    # default to empty container
                    form_data[f.name] = f.default_factory() if callable(f.default_factory) else None
                else:
                    form_data[f.name] = None

        # Create model dynamically
        new_model = web_manager.create_model_dynamic(form_data, web_manager.repo_mng.model_cls)
        repo_manager.add_model(new_model)

        return redirect(url_for(ENTITY_ROUTES[entity]))


    # GET: Formular rendern
    return render_template("add_form.html", model_fields=model_fields, entity=entity)

# --- Helper ---
def render_generic(web_mng: BaseWebManager):
    web_table = web_mng.get_web_table()
    return render_template("generic.html", title=web_table.name, columns=web_table.columns, rows=web_table.rows, entity=web_table.entity)

if __name__ == "__main__":
    app.run(debug=True)