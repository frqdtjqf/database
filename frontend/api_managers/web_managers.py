from backend.lego_db.db_converter import ActualMinifigureRepoManager, TemplateMinifigureRepoManager, WeaponRepoManager, WeaponSlotRepoManager, LegoPartRepoManager
from backend.lego_db import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure
from frontend.api_managers.base_web_managers import BaseWebManager, DataBaseWrapper

class LegoPartWebManager(BaseWebManager):
    columns = ["ID", "BrickLink Part ID", "BrickLink Color ID", "Lego Element ID", "Lego Design ID", "Description"]
    rows = []
    t_name = "Lego Parts"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = LegoPartRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            row = {
                c[0]: m.id,
                c[1]: m.bricklink_part_id,
                c[2]: m.bricklink_color_id,
                c[3]: m.lego_element_id,
                c[4]: m.lego_design_id,
                c[5]: m.description
            }
            rows.append(row)
        return rows
    
class WeaponWebManager(BaseWebManager):
    columns = ["ID", "Name", "Parts", "Description"]
    rows = []
    t_name = "Weapons"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = WeaponRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

        self.repos = {
            "lego_part": LegoPartRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            parts_str = ", ".join(part.id for part in m.parts)
            row = {
                c[0]: m.id,
                c[1]: m.name,
                c[2]: parts_str,
                c[3]: m.description,
            }
            rows.append(row)
        return rows
    
class WeaponSlotWebManager(BaseWebManager):
    columns = ["ID", "Weapons"]
    rows = []
    t_name = "Weapon Slots"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = WeaponSlotRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

        self.repos = {
            "weapon": WeaponRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            weapons_str = ", ".join(weapon.id for weapon in m.weapons)
            row = {
                c[0]: m.id,
                c[1]: weapons_str
            }
            rows.append(row)
        return rows
    
class TemplateMinifigureWebManager(BaseWebManager):
    columns = ["ID", "BrickLink Figure ID", "Name", "Year", "Sets", "Parts", "Possible Weapon Slots", "Description"]
    rows = []
    t_name = "Minifigure Templates"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = TemplateMinifigureRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

        self.repos = {
            "weapon_slot": WeaponSlotRepoManager(db),
            "lego_part": LegoPartRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            sets_str = ", ".join(set_id for set_id in m.sets)
            parts_str = ", ".join(part.id for part in m.parts)
            posw_str = ", ".join(slot.id for slot in m.possible_weapons)
            row = {
                c[0]: m.id,
                c[1]: m.bricklink_fig_id,
                c[2]: m.name,
                c[3]: m.year,
                c[4]: sets_str,
                c[5]: parts_str,
                c[6]: posw_str,
                c[7]: m.description
            }
            rows.append(row)
        return rows
    
class ActualMinifigureWebManager(BaseWebManager):
    columns = ["ID", "Template ID", "Box Number", "Position Number", "Weapon Slot", "Condition"]
    rows = []
    t_name = "Actual Minifigures"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = ActualMinifigureRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

        self.repos = {
            "template": TemplateMinifigureRepoManager(db),
            "weapon_slot": WeaponSlotRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            row = {
                c[0]: m.id,
                c[1]: m.template.id,
                c[2]: m.box_number,
                c[3]: m.position_in_box,
                c[4]: m.weapon_slot.id,
                c[5]: m.condition,
            }
            rows.append(row)
        return rows