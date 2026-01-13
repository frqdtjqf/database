from backend.sql_api import DataBaseWrapper
from backend.lego_db.db_converter import WeaponRepoManager, WeaponSlotRepoManager, TemplateMinifigureRepoManager, LegoPartRepoManager, ActualMinifigureRepoManager
from backend.lego_db.lego_models import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure
from dataclasses import dataclass

@dataclass
class SuperManager:
    weapon_mgn: WeaponRepoManager
    weapon_slot_mgn: WeaponSlotRepoManager
    temp_min_mgn: TemplateMinifigureRepoManager
    lego_part_mgn: LegoPartRepoManager
    act_min_mgn: ActualMinifigureRepoManager

class LegoDBInterface:

    def __init__(self, data_base_name: str):
        self.db = DataBaseWrapper(data_base_name)

        self.super_mgn = SuperManager(
            weapon_mgn=WeaponRepoManager(self.db),
            weapon_slot_mgn=WeaponSlotRepoManager(self.db),
            temp_min_mgn=TemplateMinifigureRepoManager(self.db),
            lego_part_mgn=LegoPartRepoManager(self.db),
            act_min_mgn=ActualMinifigureRepoManager(self.db)
        )
    
    # --- GENERAL ---
    def create_all_tables(self):
        self.super_mgn.weapon_mgn.create_tables()
        self.super_mgn.weapon_slot_mgn.create_tables()
        self.super_mgn.temp_min_mgn.create_tables()
        self.super_mgn.lego_part_mgn.create_tables()
        self.super_mgn.act_min_mgn.create_tables()

    def delete_all_tables(self):
        self.super_mgn.weapon_mgn.delete_tables()
        self.super_mgn.weapon_slot_mgn.delete_tables()
        self.super_mgn.temp_min_mgn.delete_tables()
        self.super_mgn.lego_part_mgn.delete_tables()
        self.super_mgn.act_min_mgn.delete_tables()

    # --- Parts ---
    def get_parts(self) -> list[LegoPart]:
        return self.super_mgn.lego_part_mgn.get_models()
    
    def add_part(self, part: LegoPart):
        self.super_mgn.lego_part_mgn.add_model(part)

    def delete_part(self, part: LegoPart):
        self.super_mgn.lego_part_mgn.delete_model(part)

    # --- Templates ---
    def get_all_templates(self) -> list[TemplateMinifigure]:
        return self.super_mgn.temp_min_mgn.get_models()

    def add_template(self, template: TemplateMinifigure):
        self.super_mgn.temp_min_mgn.add_model(template)

    def delete_template(self, template: TemplateMinifigure):
        self.super_mgn.temp_min_mgn.delete_model(template)

    # --- Weapons ---
    def get_all_weapons(self) -> list[Weapon]:
        return self.super_mgn.weapon_mgn.get_models()

    def add_weapon(self, weapon: Weapon):
        self.super_mgn.weapon_mgn.add_model(weapon)

    def delete_weapon(self, weapon: Weapon):
        self.super_mgn.weapon_mgn.delete_model(weapon)

    # --- Weapon Slots ---
    def get_all_weapon_slots(self) -> list[WeaponSlot]:
        return self.super_mgn.weapon_slot_mgn.get_models()

    def add_weapon_slot(self, slot: WeaponSlot):
        self.super_mgn.weapon_slot_mgn.add_model(slot)

    def delete_weapon_slot(self, slot: WeaponSlot):
        self.super_mgn.weapon_slot_mgn.delete_model(slot)

    # --- Actual Minifigures ---
    def get_all_actual_minifigures(self) -> list[ActualMinifigure]:
        return self.super_mgn.act_min_mgn.get_models()

    def add_actual_minifigure(self, actual: ActualMinifigure):
        self.super_mgn.act_min_mgn.add_model(actual)

    def delete_actual_minifigure(self, actual: ActualMinifigure):
        self.super_mgn.act_min_mgn.delete_model(actual)
        
