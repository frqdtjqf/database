from backend.lego_db.db_converter import ActualMinifigureRepoManager, TemplateMinifigureRepoManager, WeaponRepoManager, WeaponSlotRepoManager, LegoPartRepoManager, ColorRepoManager
from backend.lego_db import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure, Color
from frontend.api_managers.base_web_managers import BaseWebManager, DataBaseWrapper

class ColorWebManager(BaseWebManager):
    columns = ["ID", "Bricklink Color ID", "Rebrickable Color ID", "Lego Color ID", "RGB", "Name"]
    rows = []
    t_name = "Colors"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = ColorRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models: list[Color] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            row = {
                c[0]: m.id,
                c[1]: m.bricklink_color_id if m.bricklink_color_id else None,
                c[2]: m.rebrickable_color_id if m.rebrickable_color_id else None,
                c[3]: m.lego_color_id if m.lego_color_id else None,
                c[4]: m.rgb_value if m.rgb_value else None,
                c[5]: m.name if m.name else None,
            }
            rows.append(row)
        return rows

class LegoPartWebManager(BaseWebManager):
    columns = ["ID", "BrickLink Part ID", "Color", "Lego Element ID", "Lego Design ID", "Description"]
    rows = []
    t_name = "Lego Parts"

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = LegoPartRepoManager(db)
        self.rows = self.get_rows()
        self.entity = self.repo_mng.table.name

        self.repos = {
            "colors": ColorRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models: list[LegoPart] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            row = {
                c[0]: m.id,
                c[1]: m.bricklink_part_id if m.bricklink_part_id else None,
                c[2]: m.bricklink_color.name if m.bricklink_color.name else None,
                c[3]: m.lego_element_id if m.lego_element_id else None,
                c[4]: m.lego_design_id if m.lego_design_id else None,
                c[5]: m.description if m.description else None
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
            "lego_parts": LegoPartRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models : list[Weapon] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            parts_str = ", ".join(f"{part.id} x {q}" for part, q in m.parts.items() if part is not None)
            row = {
                c[0]: m.id,
                c[1]: m.name if m.name else None,
                c[2]: parts_str if parts_str else None,
                c[3]: m.description if m.description else None,
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
            "weapons": WeaponRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models : list[WeaponSlot] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            weapons_str = ", ".join(f"{weapon.id} x {q}" for weapon, q in m.weapons.items() if weapon is not None)
            row = {
                c[0]: m.id,
                c[1]: weapons_str if weapons_str else None
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
            "weapon_slots": WeaponSlotRepoManager(db),
            "lego_parts": LegoPartRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models : list[TemplateMinifigure] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            sets_str = ", ".join(set_id for set_id in m.sets)
            parts_str = ", ".join(f"{part.id} x {q}" for part, q in m.parts.items() if part is not None)
            posw_str = ", ".join(slot.id for slot in m.possible_weapons)
            row = {
                c[0]: m.id,
                c[1]: m.bricklink_fig_id if m.bricklink_fig_id else None,
                c[2]: m.name if m.name else None,
                c[3]: m.year if m.year else None,
                c[4]: sets_str if sets_str else None,
                c[5]: parts_str if parts_str else None,
                c[6]: posw_str if posw_str else None,
                c[7]: m.description if m.description else None
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
            "template_minifigures": TemplateMinifigureRepoManager(db),
            "weapon_slots": WeaponSlotRepoManager(db)
        }

    def get_rows(self) -> list[dict[str, str]]:
        rows = []
        models : list[ActualMinifigure] = self.repo_mng.get_models()
        c = self.columns
        for m in models:
            row = {
                c[0]: m.id,
                c[1]: m.template.id if m.template else None,
                c[2]: m.box_number if m.box_number else None,
                c[3]: m.position_in_box if m.position_in_box else None,
                c[4]: m.weapon_slot.id if m.weapon_slot else None,
                c[5]: m.condition if m.condition else None,
            }
            rows.append(row)
        return rows