from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon, WeaponSlot
from backend.sql_api import Record, Element
from backend.lego_db.db_converter.registry import LEGO_PART_TABLE, WEAPON_TABLE, WEAPON_SLOT_TABLE, TEMPLATE_MINIFIGURE_TABLE, ACTUAL_MINIFIGURE_TABLE, RELATIONS
from backend.lego_db.db_converter.generic_managers import ParentRepoManager, BaseRepoManager

# ==== BASIC ====
# basic Managers with max. 1:1 relations that dont require an extra Table
class LegoPartRepoManager(BaseRepoManager):
    table = LEGO_PART_TABLE
    
    def _model_from_record(self, record: Record) -> LegoPart:
        data = {e.attribute.name: e.value for e in record.elements}
        return LegoPart(**data)
    
class ActualMinifigureRepoManager(BaseRepoManager):
    table = ACTUAL_MINIFIGURE_TABLE

    def _model_from_record(self, record: Record) -> ActualMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}

        template_manager = TemplateMinifigureRepoManager(self.db)
        template = template_manager.get_model_by_primary_key(data["template_id"])

        data["template"] = template

        return ActualMinifigure(**data)

    def _record_from_model(self, model: ActualMinifigure) -> Record:
        elements = []
        for attr in self.table.attributes:
            if attr.name == "template_id":
                value = model.template.id
            else:
                value = getattr(model, attr.name)
            elements.append(Element(attribute=attr, value=value))
        return Record(elements=elements)
    
# ==== PARENT ====
# parent Managers with arbitrary relations N:M, that require an extra Table
class WeaponSlotRepoManager(ParentRepoManager):
    table = WEAPON_SLOT_TABLE
    
    def _model_from_record(self, record: Record) -> WeaponSlot:
        data = {e.attribute.name: e.value for e in record.elements}
        slot_id = data["id"]

        weapon_manager = WeaponRepoManager(self.db)
        weapons = self._load_related_models("weapon_slot_weapons", weapon_manager, slot_id)

        data["weapons"] = weapons
        return WeaponSlot(**data)
    
    def _persist_relations(self, model: WeaponSlot):
        weapon_manager = WeaponRepoManager(self.db)
        self._add_relations(model.weapons, weapon_manager, "weapon_slot_weapons", model.id)

class TemplateMinifigureRepoManager(ParentRepoManager):
    table = TEMPLATE_MINIFIGURE_TABLE

    def _model_from_record(self, record: Record) -> TemplateMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}
        template_id = data["id"]

        # 1) --- > TODO: load parts from TEMPLATE_MINIFIGURE_PART_TABLE
        part_manager = LegoPartRepoManager(self.db)
        parts = self._load_related_models("template_parts", part_manager, template_id)

        # 2) --- > TODO: load weaponSlots from TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE
        weapon_slot_manager = WeaponSlotRepoManager(self.db)
        possible_weapons = self._load_related_models("template_weapon_slots", weapon_slot_manager, template_id)

        data["parts"] = parts
        data["possible_weapons"] = possible_weapons

        return TemplateMinifigure(**data)
    
    def _record_from_model(self, model: TemplateMinifigure):
        elements = []
        for attr in self.table.attributes:
            value = getattr(model, attr.name)
            if attr.name == "sets":
                value = ",".join(sorted(value))  # serialize
            elements.append(Element(attr, value))
        return Record(elements=elements)
    
    def _persist_relations(self, model: TemplateMinifigure):
        part_manager = LegoPartRepoManager(self.db)
        self._add_relations(model.parts, part_manager, "template_parts", model.id)

        weapon_slot_manager = WeaponSlotRepoManager(self.db)
        self._add_relations(model.possible_weapons, weapon_slot_manager, "template_weapon_slots", model.id)

class WeaponRepoManager(ParentRepoManager):
    table = WEAPON_TABLE

    def _model_from_record(self, record: Record) -> Weapon:
        data = {e.attribute.name: e.value for e in record.elements}
        weapon_id = data["id"]

        # TODO: load parts from WEAPON_PART_TABLE
        part_manager = LegoPartRepoManager(self.db)
        parts = self._load_related_models("weapon_parts", part_manager, weapon_id)

        data["parts"] = parts

        return Weapon(**data)
    
    def _persist_relations(self, model: Weapon):
        part_manager = LegoPartRepoManager(self.db)
        self._add_relations(model.parts, part_manager, "weapon_parts", model.id)