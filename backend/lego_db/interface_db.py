from backend.sql_api import DataBaseWrapper
from backend.lego_db.db_converter import WeaponRepoManager, WeaponSlotRepoManager, TemplateMinifigureRepoManager, LegoPartRepoManager, ActualMinifigureRepoManager, BaseRepoManager
from backend.lego_db.lego_models import LegoPart, Weapon, WeaponSlot, TemplateMinifigure, ActualMinifigure, BasicModel
from backend.lego_db.db_converter.registry.relations import RELATIONS
from dataclasses import dataclass

class LegoDBInterface:

    def __init__(self, db: DataBaseWrapper):
        self.db = db

        self.managers : dict[str, BaseRepoManager] = {}
        self.managers = {
            "weapons": WeaponRepoManager(self.db),
            "weapon_slots": WeaponSlotRepoManager(self.db),
            "template_minifigures": TemplateMinifigureRepoManager(self.db),
            "lego_parts": LegoPartRepoManager(self.db),
            "actual_minifigures": ActualMinifigureRepoManager(self.db)
        }
    
    # --- GENERAL ---
    def create_all_tables(self):
        for relation in RELATIONS.values():
            self.db.create_relations_table(relation)
        for manager in self.managers.values():
            manager.create_tables()

    def delete_all_tables(self):
        for manager in self.managers.values():
            manager.delete_tables()

    def get_models(self, mng_name: str) -> list[BasicModel]:
        return self.managers[mng_name].get_models()
    
    def add_models(self, part: BasicModel, mng_name: str):
        self.managers[mng_name].add_model(part)

    def delete_model(self, part: BasicModel, mng_name: str):
        self.managers[mng_name].delete_model(part)
