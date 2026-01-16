from flask import Flask, render_template, request, redirect, url_for
from backend.lego_db import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure
from frontend.api_managers import LegoPartWebManager, WeaponWebManager, WeaponSlotWebManager, TemplateMinifigureWebManager, ActualMinifigureWebManager, WebTable, BaseWebManager
from backend.lego_db import LegoDBInterface, PRIMARY_KEY_NAME, WEAPON_PART_TABLE
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

ENTITY_NAMES = {
    "lego_parts": "Lego Parts",
    "weapons": "Weapons",
    "weapon_slots": "Weapon Slots",
    "template_minifigures": "Template Minifigures",
    "actual_minifigures": "Actual Minifigures"
}


db_inter = LegoDBInterface(db)
db_inter.create_all_tables()

app = Flask(__name__)

@app.context_processor
def inject_entities():
    return dict(
        entity_routes=ENTITY_ROUTES,
        entity_names=ENTITY_NAMES
    )

@app.route("/")
def home():
    return render_template("home.html")

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
        form_data = request.form.to_dict(flat=False)
        for f in model_fields:
            if f.name not in form_data:
                if f.metadata.get("related_field", False):
                    # default to empty container
                    form_data[f.name] = f.default_factory() if callable(f.default_factory) else None
                else:
                    form_data[f.name] = None

        # Create model dynamically
        new_model = web_manager.create_model(form_data)
        repo_manager.add_model(new_model)

        return redirect(url_for(ENTITY_ROUTES[entity]))


    # GET: Formular rendern
    return render_template("add_form.html", model_fields=model_fields, entity=entity)

@app.post("/<entity>/delete")
def delete(entity):
    id_values = request.args.to_dict()
    obj_id = id_values["id"]
    manager_class = WEB_MANAGERS[entity]

    web_manager: BaseWebManager = manager_class(db)
    repo_manager = web_manager.repo_mng

    obj = repo_manager.get_model_by_primary_key(obj_id)
    repo_manager.delete_model(obj)

    return redirect(url_for(ENTITY_ROUTES[entity]))

# --- Helper ---
def render_generic(web_mng: BaseWebManager):
    web_table = web_mng.get_web_table()
    return render_template("generic.html", title=web_table.name, columns=web_table.columns, rows=web_table.rows, entity=web_table.entity)

if __name__ == "__main__":
    app.run(debug=True)