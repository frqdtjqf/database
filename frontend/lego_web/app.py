from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, abort
from frontend.api_managers import LegoPartWebManager, WeaponWebManager, WeaponSlotWebManager, TemplateMinifigureWebManager, ActualMinifigureWebManager, WebTable, BaseWebManager, ColorWebManager
from backend.lego_db import LegoDBInterface, PRIMARY_KEY_NAME, WEAPON_PART_TABLE
from backend.sql_api import DataBaseWrapper
from dataclasses import fields
import traceback
from backend.file_reader.get_info import import_csv

def create_app():

    db = DataBaseWrapper("database.db")
    WEB_MANAGERS = {
        "colors": ColorWebManager,
        "lego_parts": LegoPartWebManager,
        "weapons": WeaponWebManager,
        "weapon_slots": WeaponSlotWebManager,
        "template_minifigures": TemplateMinifigureWebManager,
        "actual_minifigures": ActualMinifigureWebManager,
    }

    ENTITY_ROUTES = {
        "colors": "render_colors",
        "lego_parts": "render_lego_parts",
        "weapons": "render_weapons",
        "weapon_slots": "render_weapon_slots",
        "template_minifigures": "render_template_minifigures",
        "actual_minifigures": "render_actual_minifigures",
    }

    ENTITY_NAMES = {
        "colors": "Colors",
        "lego_parts": "Lego Parts",
        "weapons": "Weapons",
        "weapon_slots": "Weapon Slots",
        "template_minifigures": "Template Minifigures",
        "actual_minifigures": "Actual Minifigures",
    }


    db_inter = LegoDBInterface(db)
    db_inter.create_all_tables()

    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    @app.context_processor
    def inject_entities():
        return dict(
            entity_routes=ENTITY_ROUTES,
            entity_names=ENTITY_NAMES,
            web_managers=WEB_MANAGERS
        )

    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/colors")
    def render_colors():
        mng = ColorWebManager(db)
        return render_generic(web_mng=mng)

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
                        form_data[f.name] = f.default_factory()
                    else:
                        form_data[f.name] = None

            # Create model dynamically
            try:
                new_model = web_manager.create_model(form_data)
                repo_manager.add_model(new_model)
                flash(f"Added {new_model.id}", "success")
                return redirect(url_for(ENTITY_ROUTES[entity]))
            except Exception as e:
                flash(str(e), "error")

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

        try:
            repo_manager.delete_model(obj)
        except Exception as e:
            flash(str(e), "error")

        return redirect(url_for(ENTITY_ROUTES[entity]))

    @app.route("/api/<entity>/ids")
    def get_ids(entity):
        mng_cls = WEB_MANAGERS.get(entity)
        mng : BaseWebManager = mng_cls(db)
        data = mng.get_model_ids()
        return jsonify(data)
    
    @app.route("/<entity>/upload_csv", methods=["POST"])
    def upload_csv(entity):
        if entity not in WEB_MANAGERS:
            abort(404)

        file = request.files.get("csv_file")
        if not file or not file.filename.endswith(".csv"):
            flash("Please upload a csv", "error")
            return redirect(url_for(ENTITY_ROUTES[entity]))

        try:
            rows = import_csv(file)
            print(rows)
            flash("CSV imported", "success")
        except Exception as e:
            traceback.print_exc()
            flash(str(e), "error")

        return redirect(url_for(ENTITY_ROUTES[entity]))

    # --- Helper ---
    def render_generic(web_mng: BaseWebManager):
        web_table = web_mng.get_web_table()
        return render_template("generic.html", title=web_table.name, columns=web_table.columns, rows=web_table.rows, entity=web_table.entity)
    
    return app
